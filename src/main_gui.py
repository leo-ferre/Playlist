import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import os
from pathlib import Path
import unicodedata
import threading

# Importa as funções do programa original
from main import carregar_dados, salvar_dados
from api_music import buscar_informacoes_musica


class PlaylistGUI:
    """Classe principal da interface gráfica"""

    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Playlist")
        self.root.geometry("780x700")
        self.root.configure(bg='#1a1a2e')

        # Caminhos base do projeto
        self._project_root = Path(__file__).resolve().parent.parent
        self._data_dir = self._project_root / 'data'
        self._images_dir = self._data_dir / 'album_covers'

        # Variáveis
        self.nome_arquivo = str(self._data_dir / "playlist.txt")
        self.pasta_imagens = str(self._images_dir)  # Pasta para armazenar capas de álbuns
        self.playlist = carregar_dados(self.nome_arquivo)
        self.imagens_cache = {}  # Cache de imagens carregadas

        # Cria pasta para imagens se não existir
        Path(self.pasta_imagens).mkdir(parents=True, exist_ok=True)

        # Configura estilo
        self.configurar_estilo()

        # Cria interface
        self.criar_interface()

        # Carrega músicas
        self.atualizar_lista()

    def _configurar_trace_busca(self):
        """Configura o trace da busca de forma compatível com diferentes versões do tkinter"""
        try:
            # Tcl 9+ (Python 3.14+) - usa trace_add
            self.search_var.trace_add('write', lambda var, index, mode: self.filtrar_musicas())
        except (AttributeError, Exception):
            try:
                # Tcl 8.x (versões antigas) - usa trace
                self.search_var.trace('w', lambda var, index, mode: self.filtrar_musicas())
            except Exception as e:
                print(f"⚠️ Aviso: Não foi possível configurar busca em tempo real: {e}")
                # Busca funcionará apenas com Enter se houver erro

    def configurar_estilo(self):
        """Configura o estilo visual da aplicação"""
        style = ttk.Style()
        style.theme_use('clam')

        # Cores personalizadas
        self.cores = {
            'bg_principal': '#1a1a2e',
            'bg_secundario': '#16213e',
            'bg_card': '#0f3460',
            'texto': '#e94560',
            'texto_claro': '#ffffff',
            'botao': '#e94560',
            'botao_hover': '#c23a4f',
            'texto_botoes': '#000000',  # Cor do texto dos botões (alto contraste)
        }

        # Estilo dos botões
        style.configure('Accent.TButton',
                       background=self.cores['botao'],
                       foreground=self.cores['texto_claro'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'))

        # Estilo do Frame
        style.configure('Card.TFrame',
                       background=self.cores['bg_card'],
                       relief='flat')

    def criar_interface(self):
        """Cria toda a interface gráfica"""

        # ===== CABEÇALHO =====
        header_frame = tk.Frame(self.root, bg=self.cores['bg_secundario'], height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)

        titulo = tk.Label(header_frame,
                         text="GERENCIADOR DE PLAYLIST",
                         font=('Arial', 24, 'bold'),
                         bg=self.cores['bg_secundario'],
                         fg=self.cores['texto'])
        titulo.pack(pady=20)

        # ===== CONTAINER PRINCIPAL =====
        main_container = tk.Frame(self.root, bg=self.cores['bg_principal'])
        main_container.pack(fill='both', expand=True, padx=5, pady=5)

        # ===== PAINEL ESQUERDO (Lista de Músicas) =====
        left_panel = tk.Frame(main_container, bg=self.cores['bg_secundario'], width=520)
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        left_panel.pack_propagate(False)

        # Título do painel
        tk.Label(left_panel,
                text="📚 BIBLIOTECA DE MÚSICAS",
                font=('Arial', 14, 'bold'),
                bg=self.cores['bg_secundario'],
                fg=self.cores['texto_claro']).pack(pady=10)

        # Barra de pesquisa
        search_frame = tk.Frame(left_panel, bg=self.cores['bg_secundario'])
        search_frame.pack(fill='x', padx=5, pady=5)

        tk.Label(search_frame,
                text="🔍 Buscar:",
                bg=self.cores['bg_secundario'],
                fg=self.cores['texto_claro']).pack(side='left', padx=5)

        self.search_var = tk.StringVar()
        # Compatibilidade com diferentes versões do tkinter/Tcl
        self._configurar_trace_busca()

        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=('Arial', 11),
                               bg=self.cores['bg_card'],
                               fg=self.cores['texto_claro'],
                               insertbackground=self.cores['texto_claro'])
        search_entry.pack(side='left', fill='x', expand=True, padx=5)

        # Canvas com scrollbar para lista de músicas
        canvas_frame = tk.Frame(left_panel, bg=self.cores['bg_secundario'])
        canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(canvas_frame,
                               bg=self.cores['bg_secundario'],
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=self.cores['bg_secundario'])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind para scroll com mouse (multiplataforma)
        self._bind_mousewheel()

        # ===== PAINEL DIREITO (Ações) =====
        right_panel = tk.Frame(main_container, bg=self.cores['bg_secundario'], width=240)
        right_panel.pack(side='right', fill='y', padx=(5, 0))
        right_panel.pack_propagate(False)

        # Título do painel
        tk.Label(right_panel,
                text="⚙️ AÇÕES",
                font=('Arial', 14, 'bold'),
                bg=self.cores['bg_secundario'],
                fg=self.cores['texto_claro']).pack(pady=15)

        # Botões de ação
        botoes = [
            ("➕ Adicionar Música", self.adicionar_musica),
            ("📊 Gerar Relatório", self.gerar_relatorio),
            ("💾 Salvar Playlist", self.salvar_playlist),
            ("🔄 Recarregar Dados", self.recarregar_dados),
        ]

        for texto, comando in botoes:
            btn = tk.Button(right_panel,
                          text=texto,
                          command=comando,
                          bg=self.cores['botao'],
                          fg=self.cores['texto_botoes'],
                          font=('Arial', 11, 'bold'),
                          relief='flat',
                          cursor='hand2',
                          activebackground=self.cores['botao_hover'],
                          activeforeground=self.cores['texto_botoes'])
            btn.pack(pady=8, padx=10, fill='x')

            # Efeito hover
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.cores['botao_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.cores['botao']))

        # Estatísticas
        stats_frame = tk.Frame(right_panel, bg=self.cores['bg_card'], relief='ridge', bd=2)
        stats_frame.pack(pady=15, padx=10, fill='x')

        tk.Label(stats_frame,
                text="📈 ESTATÍSTICAS",
                font=('Arial', 12, 'bold'),
                bg=self.cores['bg_card'],
                fg=self.cores['texto']).pack(pady=10)

        self.stats_label = tk.Label(stats_frame,
                                    text="",
                                    font=('Arial', 10),
                                    bg=self.cores['bg_card'],
                                    fg=self.cores['texto_claro'],
                                    justify='left')
        self.stats_label.pack(pady=10, padx=10)

        self.atualizar_estatisticas()

    def _bind_mousewheel(self):
        """Configura o scroll do mouse/trackpad de forma multiplataforma"""
        import platform
        self.sistema = platform.system()

        # Bind para entrar/sair da área do canvas
        self.canvas.bind('<Enter>', self._on_enter)
        self.canvas.bind('<Leave>', self._on_leave)
        self.scrollable_frame.bind('<Enter>', self._on_enter)
        self.scrollable_frame.bind('<Leave>', self._on_leave)

    def _on_enter(self, event):
        """Ativa scroll quando mouse entra na área"""
        # macOS (funciona com mouse e trackpad)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_leave(self, event):
        """Desativa scroll quando mouse sai da área"""
        # macOS
        self.canvas.unbind_all("<MouseWheel>")
        # Linux
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        """Handler para scroll com mouse/trackpad (multiplataforma)"""
        # Linux - usa Button-4 e Button-5
        if hasattr(event, 'num'):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
                return
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
                return

        # macOS e Windows - usa event.delta
        # No macOS com trackpad, delta pode ser qualquer valor (não apenas 120/-120)
        if hasattr(event, 'delta'):
            if self.sistema == 'Darwin':  # macOS
                # No macOS, delta pode ser valores pequenos (trackpad) ou grandes (mouse)
                # Normaliza para funcionar bem com ambos
                delta = event.delta
                if delta > 0:
                    self.canvas.yview_scroll(-1, "units")
                elif delta < 0:
                    self.canvas.yview_scroll(1, "units")
            else:  # Windows
                # No Windows, delta é geralmente 120 ou -120
                self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def carregar_imagem_album(self, musica):
        """Carrega a imagem do álbum ou retorna imagem padrão"""
        # Nome do arquivo de imagem baseado no álbum
        nome_limpo = "".join(c for c in musica['album'] if c.isalnum() or c in (' ', '-', '_')).strip()
        nome_imagem = f"{nome_limpo.replace(' ', '_').lower()}.png"
        caminho_imagem = os.path.join(self.pasta_imagens, nome_imagem)

        # Verifica se já está no cache
        if caminho_imagem in self.imagens_cache:
            return self.imagens_cache[caminho_imagem]

        try:
            # Tenta carregar a imagem do álbum
            if os.path.exists(caminho_imagem):
                img = Image.open(caminho_imagem)
            else:
                # Cria imagem padrão se não existir
                img = self.criar_imagem_padrao(musica)

            # Redimensiona para 80x80
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            # Adiciona ao cache
            self.imagens_cache[caminho_imagem] = photo
            return photo

        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            return self.criar_imagem_padrao_tk(musica)

    def criar_imagem_padrao(self, musica):
        """Cria uma imagem padrão com cor baseada no gênero"""
        cores_genero = {
            'rock': '#E74C3C',
            'pop': '#3498DB',
            'jazz': '#9B59B6',
            'classical': '#1ABC9C',
            'hip hop': '#F39C12',
            'electronic': '#2ECC71',
        }

        genero = musica.get('genero', '').lower()
        cor = cores_genero.get(genero, '#34495E')

        img = Image.new('RGB', (80, 80), color=cor)
        return img

    def criar_imagem_padrao_tk(self, musica):
        """Cria uma imagem padrão TK"""
        img = self.criar_imagem_padrao(musica)
        photo = ImageTk.PhotoImage(img)
        return photo

    def criar_card_musica(self, musica, index):
        """Cria um card visual para cada música"""
        # Frame do card
        card = tk.Frame(self.scrollable_frame,
                       bg=self.cores['bg_card'],
                       relief='raised',
                       bd=2)
        card.pack(fill='x', padx=3, pady=3)

        # Frame para imagem
        img_frame = tk.Frame(card, bg=self.cores['bg_card'])
        img_frame.pack(side='left', padx=5, pady=5)

        # Carrega e exibe imagem do álbum
        foto = self.carregar_imagem_album(musica)
        img_label = tk.Label(img_frame, image=foto, bg=self.cores['bg_card'])
        img_label.image = foto  # Mantém referência
        img_label.pack()

        # Frame para informações
        info_frame = tk.Frame(card, bg=self.cores['bg_card'], width=240)
        info_frame.pack(side='left', fill='y', padx=5, pady=5)
        info_frame.pack_propagate(False)

        # Título
        tk.Label(info_frame,
                text=f"♪ {musica['titulo']}",
                font=('Arial', 12, 'bold'),
                bg=self.cores['bg_card'],
                fg=self.cores['texto'],
                anchor='w').pack(fill='x')

        # Artista
        tk.Label(info_frame,
                text=f"👤 {musica['artista']}",
                font=('Arial', 10),
                bg=self.cores['bg_card'],
                fg=self.cores['texto_claro'],
                anchor='w').pack(fill='x')

        # Álbum e Ano
        tk.Label(info_frame,
                text=f"💿 {musica['album']} • {musica['ano']}",
                font=('Arial', 9),
                bg=self.cores['bg_card'],
                fg='#aaaaaa',
                anchor='w').pack(fill='x')

        # Gênero
        tk.Label(info_frame,
                text=f"🎸 {musica['genero']}",
                font=('Arial', 9),
                bg=self.cores['bg_card'],
                fg='#aaaaaa',
                anchor='w').pack(fill='x')

        # Frame para botões de ação
        btn_frame = tk.Frame(card, bg=self.cores['bg_card'])
        btn_frame.pack(side='right', padx=5, pady=5)

        # Botão Editar
        btn_editar = tk.Button(btn_frame,
                              text="✏️ Editar",
                              command=lambda m=musica: self.editar_musica(m),
                              bg='#4CAF50',
                              fg=self.cores['texto_botoes'],
                              font=('Arial', 9, 'bold'),
                              relief='flat',
                              cursor='hand2',
                              padx=10,
                              pady=5,
                              activeforeground=self.cores['texto_botoes'])
        btn_editar.pack(pady=2, fill='x')

        # Botão Remover
        btn_remover = tk.Button(btn_frame,
                               text="🗑️ Remover",
                               command=lambda m=musica: self.remover_musica(m),
                               bg='#f44336',
                               fg=self.cores['texto_botoes'],
                               font=('Arial', 9, 'bold'),
                               relief='flat',
                               cursor='hand2',
                               padx=10,
                               pady=5,
                               activeforeground=self.cores['texto_botoes'])
        btn_remover.pack(pady=2, fill='x')

        # Botão Trocar Imagem
        btn_imagem = tk.Button(btn_frame,
                              text="🖼️ Imagem",
                              command=lambda m=musica: self.trocar_imagem(m),
                              bg='#2196F3',
                              fg=self.cores['texto_botoes'],
                              font=('Arial', 9, 'bold'),
                              relief='flat',
                              cursor='hand2',
                              padx=10,
                              pady=5,
                              activeforeground=self.cores['texto_botoes'])
        btn_imagem.pack(pady=2, fill='x')

    def atualizar_lista(self):
        """Atualiza a lista de músicas na interface"""
        # Limpa frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Cria cards para cada música
        if not self.playlist:
            tk.Label(self.scrollable_frame,
                    text="Nenhuma música na playlist.\nClique em 'Adicionar Música' para começar!",
                    font=('Arial', 12),
                    bg=self.cores['bg_secundario'],
                    fg=self.cores['texto_claro']).pack(pady=50)
        else:
            for i, musica in enumerate(self.playlist):
                self.criar_card_musica(musica, i)

        self.atualizar_estatisticas()

    def filtrar_musicas(self):
        """Filtra músicas baseado no termo de busca"""
        termo = self.search_var.get().lower()

        # Limpa frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Filtra e exibe
        musicas_filtradas = [m for m in self.playlist
                            if termo in m['titulo'].lower()
                            or termo in m['artista'].lower()
                            or termo in m['album'].lower()
                            or termo in m['genero'].lower()]

        if not musicas_filtradas:
            tk.Label(self.scrollable_frame,
                    text="Nenhuma música encontrada com este termo.",
                    font=('Arial', 12),
                    bg=self.cores['bg_secundario'],
                    fg=self.cores['texto_claro']).pack(pady=50)
        else:
            for i, musica in enumerate(musicas_filtradas):
                self.criar_card_musica(musica, i)

    def adicionar_musica(self):
        """Abre janela para adicionar nova música com busca automática de informações"""
        janela = tk.Toplevel(self.root)
        janela.title("➕ Adicionar Nova Música")
        janela.geometry("600x550")
        janela.configure(bg=self.cores['bg_principal'])
        janela.transient(self.root)
        janela.grab_set()

        # Título
        tk.Label(janela,
                text="➕ ADICIONAR NOVA MÚSICA",
                font=('Arial', 14, 'bold'),
                bg=self.cores['bg_principal'],
                fg=self.cores['texto']).pack(pady=15)

        # Frame para campos básicos (Título e Artista)
        busca_frame = tk.Frame(janela, bg=self.cores['bg_principal'])
        busca_frame.pack(padx=30, pady=10, fill='x')

        # Campo Título
        tk.Label(busca_frame,
                text="Título *",
                bg=self.cores['bg_principal'],
                fg=self.cores['texto_claro'],
                font=('Arial', 10, 'bold')).pack(anchor='w')

        titulo_entry = tk.Entry(busca_frame,
                               font=('Arial', 11),
                               bg=self.cores['bg_card'],
                               fg=self.cores['texto_claro'],
                               insertbackground=self.cores['texto_claro'])
        titulo_entry.pack(fill='x', pady=(0, 10))

        # Campo Artista
        tk.Label(busca_frame,
                text="Artista *",
                bg=self.cores['bg_principal'],
                fg=self.cores['texto_claro'],
                font=('Arial', 10, 'bold')).pack(anchor='w')

        artista_entry = tk.Entry(busca_frame,
                                font=('Arial', 11),
                                bg=self.cores['bg_card'],
                                fg=self.cores['texto_claro'],
                                insertbackground=self.cores['texto_claro'])
        artista_entry.pack(fill='x', pady=(0, 10))

        # Botão para buscar informações automaticamente
        def buscar_info_auto():
            titulo = titulo_entry.get().strip()
            artista = artista_entry.get().strip()

            if not titulo or not artista:
                messagebox.showwarning("Atenção", "Digite o título e artista primeiro!")
                return

            # Mostra loading
            btn_buscar.config(text="🔍 Buscando...", state='disabled')
            janela.update()

            # Busca informações
            info = buscar_informacoes_musica(titulo, artista)

            if info:
                # Preenche os campos automaticamente
                album_entry.delete(0, tk.END)
                album_entry.insert(0, info['album'])

                genero_entry.delete(0, tk.END)
                genero_entry.insert(0, info['genero'])

                ano_entry.delete(0, tk.END)
                ano_entry.insert(0, info['ano'])

                messagebox.showinfo("Sucesso", "Informações encontradas e preenchidas automaticamente!\n\n"
                                  f"📀 Álbum: {info['album']}\n"
                                  f"🎸 Gênero: {info['genero']}\n"
                                  f"📅 Ano: {info['ano']}\n"
                                  f"🖼️ Capa: {'✅ Baixada' if info.get('capa_path') else '❌ Não encontrada'}")
            else:
                messagebox.showinfo("Aviso", "Não foi possível encontrar informações automáticas.\n"
                                  "Preencha os campos manualmente.")

            btn_buscar.config(text="🔍 Buscar Informações Automáticas", state='normal')

        btn_buscar = tk.Button(busca_frame,
                              text="🔍 Buscar Informações Automáticas",
                              command=buscar_info_auto,
                              bg='#4CAF50',
                              fg=self.cores['texto_botoes'],
                              font=('Arial', 10, 'bold'),
                              relief='flat',
                              cursor='hand2',
                              activeforeground=self.cores['texto_botoes'])
        btn_buscar.pack(pady=10, fill='x')

        # Separador
        ttk.Separator(janela, orient='horizontal').pack(fill='x', padx=30, pady=10)

        # Frame para campos adicionais
        campos_frame = tk.Frame(janela, bg=self.cores['bg_principal'])
        campos_frame.pack(padx=30, pady=10, fill='both', expand=True)

        # Campo Álbum
        tk.Label(campos_frame,
                text="Álbum",
                bg=self.cores['bg_principal'],
                fg=self.cores['texto_claro'],
                font=('Arial', 10, 'bold')).pack(anchor='w')

        album_entry = tk.Entry(campos_frame,
                              font=('Arial', 11),
                              bg=self.cores['bg_card'],
                              fg=self.cores['texto_claro'],
                              insertbackground=self.cores['texto_claro'])
        album_entry.pack(fill='x', pady=(0, 10))

        # Campo Gênero
        tk.Label(campos_frame,
                text="Gênero",
                bg=self.cores['bg_principal'],
                fg=self.cores['texto_claro'],
                font=('Arial', 10, 'bold')).pack(anchor='w')

        genero_entry = tk.Entry(campos_frame,
                               font=('Arial', 11),
                               bg=self.cores['bg_card'],
                               fg=self.cores['texto_claro'],
                               insertbackground=self.cores['texto_claro'])
        genero_entry.pack(fill='x', pady=(0, 10))

        # Campo Ano
        tk.Label(campos_frame,
                text="Ano",
                bg=self.cores['bg_principal'],
                fg=self.cores['texto_claro'],
                font=('Arial', 10, 'bold')).pack(anchor='w')

        ano_entry = tk.Entry(campos_frame,
                            font=('Arial', 11),
                            bg=self.cores['bg_card'],
                            fg=self.cores['texto_claro'],
                            insertbackground=self.cores['texto_claro'])
        ano_entry.pack(fill='x', pady=(0, 10))

        # Função para salvar
        def salvar():
            titulo = titulo_entry.get().strip()
            artista = artista_entry.get().strip()

            if not titulo or not artista:
                messagebox.showwarning("Campos Obrigatórios",
                                      "Título e Artista são obrigatórios!")
                return

            nova_musica = {
                'titulo': titulo,
                'artista': artista,
                'album': album_entry.get().strip() or "Desconhecido",
                'genero': genero_entry.get().strip() or "Desconhecido",
                'ano': ano_entry.get().strip() or "----"
            }

            self.playlist.append(nova_musica)

            # Limpa cache de imagens para forçar recarregamento
            self.imagens_cache.clear()

            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Música adicionada com sucesso!")
            janela.destroy()

        # Botões finais
        btn_frame = tk.Frame(janela, bg=self.cores['bg_principal'])
        btn_frame.pack(pady=15)

        tk.Button(btn_frame,
                 text="💾 Adicionar à Playlist",
                 command=salvar,
                 bg=self.cores['botao'],
                 fg=self.cores['texto_botoes'],
                 font=('Arial', 12, 'bold'),
                 relief='flat',
                 cursor='hand2',
                 activebackground=self.cores['botao_hover'],
                 activeforeground=self.cores['texto_botoes'],
                 width=18).pack(side='left', padx=5)

        tk.Button(btn_frame,
                 text="❌ Cancelar",
                 command=janela.destroy,
                 bg='#B0B0B0',
                 fg=self.cores['texto_botoes'],
                 font=('Arial', 12, 'bold'),
                 relief='flat',
                 cursor='hand2',
                 activeforeground=self.cores['texto_botoes'],
                 width=12).pack(side='left', padx=5)

    def editar_musica(self, musica):
        """Abre janela para editar música existente"""
        janela = tk.Toplevel(self.root)
        janela.title("✏️ Editar Música")
        janela.geometry("500x400")
        janela.configure(bg=self.cores['bg_principal'])
        janela.transient(self.root)
        janela.grab_set()

        # Título
        tk.Label(janela,
                text="✏️ EDITAR MÚSICA",
                font=('Arial', 14, 'bold'),
                bg=self.cores['bg_principal'],
                fg=self.cores['texto']).pack(pady=15)

        # Frame para campos
        campos_frame = tk.Frame(janela, bg=self.cores['bg_principal'])
        campos_frame.pack(padx=30, pady=10, fill='both', expand=True)

        # Campos de entrada (preenchidos com dados atuais)
        campos = ['titulo', 'artista', 'album', 'genero', 'ano']
        labels = ['Título *', 'Artista *', 'Álbum', 'Gênero', 'Ano']
        entries = {}

        for campo, label in zip(campos, labels):
            frame = tk.Frame(campos_frame, bg=self.cores['bg_principal'])
            frame.pack(fill='x', pady=5)

            tk.Label(frame,
                    text=label,
                    bg=self.cores['bg_principal'],
                    fg=self.cores['texto_claro'],
                    font=('Arial', 10, 'bold')).pack(anchor='w')

            entry = tk.Entry(frame,
                           font=('Arial', 11),
                           bg=self.cores['bg_card'],
                           fg=self.cores['texto_claro'],
                           insertbackground=self.cores['texto_claro'])
            entry.insert(0, musica[campo])
            entry.pack(fill='x')
            entries[campo] = entry

        # Função para salvar
        def salvar():
            titulo = entries['titulo'].get().strip()
            artista = entries['artista'].get().strip()

            if not titulo or not artista:
                messagebox.showwarning("Campos Obrigatórios",
                                      "Título e Artista são obrigatórios!")
                return

            musica['titulo'] = titulo
            musica['artista'] = artista
            musica['album'] = entries['album'].get().strip() or "Desconhecido"
            musica['genero'] = entries['genero'].get().strip() or "Desconhecido"
            musica['ano'] = entries['ano'].get().strip() or "----"

            # Limpa cache de imagens
            self.imagens_cache.clear()

            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Música atualizada com sucesso!")
            janela.destroy()

        # Botões
        btn_frame = tk.Frame(janela, bg=self.cores['bg_principal'])
        btn_frame.pack(pady=15)

        tk.Button(btn_frame,
                 text="💾 Salvar",
                 command=salvar,
                 bg=self.cores['botao'],
                 fg=self.cores['texto_botoes'],
                 font=('Arial', 12, 'bold'),
                 relief='flat',
                 cursor='hand2',
                 activebackground=self.cores['botao_hover'],
                 activeforeground=self.cores['texto_botoes'],
                 width=12).pack(side='left', padx=5)

        tk.Button(btn_frame,
                 text="❌ Cancelar",
                 command=janela.destroy,
                 bg='#B0B0B0',
                 fg=self.cores['texto_botoes'],
                 font=('Arial', 12, 'bold'),
                 relief='flat',
                 cursor='hand2',
                 activeforeground=self.cores['texto_botoes'],
                 width=12).pack(side='left', padx=5)

    def remover_musica(self, musica):
        """Remove música após confirmação"""
        resposta = messagebox.askyesno(
            "Confirmar Remoção",
            f"Tem certeza que deseja remover:\n\n{musica['titulo']} - {musica['artista']}?"
        )

        if resposta:
            self.playlist.remove(musica)
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Música removida com sucesso!")

    def trocar_imagem(self, musica):
        """Permite selecionar uma imagem para o álbum"""
        arquivo = filedialog.askopenfilename(
            title="Selecione a imagem do álbum",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if arquivo:
            try:
                # Copia imagem para pasta de capas
                nome_limpo = "".join(c for c in musica['album'] if c.isalnum() or c in (' ', '-', '_')).strip()
                nome_destino = f"{nome_limpo.replace(' ', '_').lower()}.png"
                caminho_destino = os.path.join(self.pasta_imagens, nome_destino)

                # Abre, redimensiona e salva
                img = Image.open(arquivo)
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                img.save(caminho_destino, 'PNG')

                # Limpa cache e atualiza
                if caminho_destino in self.imagens_cache:
                    del self.imagens_cache[caminho_destino]

                self.imagens_cache.clear()
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Imagem do álbum atualizada!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar imagem:\n{str(e)}")

    def gerar_relatorio(self):
        """Abre janela com opções de relatório"""
        janela = tk.Toplevel(self.root)
        janela.title("📊 Gerar Relatório")
        janela.geometry("600x500")
        janela.configure(bg=self.cores['bg_principal'])
        janela.transient(self.root)
        janela.grab_set()

        # Título
        tk.Label(janela,
                text="📊 GERAR RELATÓRIO",
                font=('Arial', 14, 'bold'),
                bg=self.cores['bg_principal'],
                fg=self.cores['texto']).pack(pady=15)

        # Frame para opções
        opcoes_frame = tk.Frame(janela, bg=self.cores['bg_principal'])
        opcoes_frame.pack(padx=30, pady=10)

        tk.Label(opcoes_frame,
                text="Escolha o campo para filtrar:",
                bg=self.cores['bg_principal'],
                fg=self.cores['texto_claro'],
                font=('Arial', 11)).pack(pady=10)

        campo_var = tk.StringVar(value='genero')

        opcoes = [
            ('Título', 'titulo'),
            ('Artista', 'artista'),
            ('Álbum', 'album'),
            ('Gênero', 'genero'),
            ('Ano', 'ano')
        ]

        for texto, valor in opcoes:
            tk.Radiobutton(opcoes_frame,
                          text=texto,
                          variable=campo_var,
                          value=valor,
                          bg=self.cores['bg_principal'],
                          fg=self.cores['texto_claro'],
                          selectcolor=self.cores['bg_card'],
                          font=('Arial', 10)).pack(anchor='w', padx=20)

        # Campo de entrada
        tk.Label(opcoes_frame,
                text="Digite o valor para filtrar:",
                bg=self.cores['bg_principal'],
                fg=self.cores['texto_claro'],
                font=('Arial', 11)).pack(pady=(15, 5))

        valor_entry = tk.Entry(opcoes_frame,
                              font=('Arial', 11),
                              bg=self.cores['bg_card'],
                              fg=self.cores['texto_claro'],
                              insertbackground=self.cores['texto_claro'],
                              width=40)
        valor_entry.pack()
        valor_entry.focus_set()

        # Área de resultados
        resultado_frame = tk.Frame(janela, bg=self.cores['bg_principal'])
        resultado_frame.pack(padx=20, pady=15, fill='both', expand=True)

        resultado_text = scrolledtext.ScrolledText(resultado_frame,
                                                   font=('Courier', 9),
                                                   bg=self.cores['bg_card'],
                                                   fg=self.cores['texto_claro'],
                                                   wrap=tk.WORD,
                                                   height=15)
        resultado_text.pack(fill='both', expand=True)

        def _norm(s: str) -> str:
            s = s or ""
            s = unicodedata.normalize('NFKD', s)
            s = s.encode('ASCII', 'ignore').decode('ASCII')
            return s.casefold().strip()

        # Função para gerar
        def gerar(event=None):
            campo = campo_var.get()
            valor = valor_entry.get().strip()

            if not valor:
                messagebox.showwarning("Atenção", "Digite um valor para filtrar!")
                return

            val_n = _norm(valor)

            # Filtra músicas (correspondência parcial, case/acento-insensitive)
            musicas_filtradas = [m for m in self.playlist
                                 if val_n in _norm(m.get(campo, ''))]

            # Exibe resultado
            resultado_text.delete(1.0, tk.END)

            if not musicas_filtradas:
                resultado_text.insert(tk.END, f"Nenhuma música encontrada para {campo}: {valor}")
            else:
                nomes_campos = {
                    'titulo': 'TÍTULO',
                    'artista': 'ARTISTA',
                    'album': 'ÁLBUM',
                    'genero': 'GÊNERO',
                    'ano': 'ANO'
                }
                resultado_text.insert(tk.END, f"=== Relatório: {nomes_campos.get(campo, campo.upper())} = {valor} ===\n\n")
                resultado_text.insert(tk.END, f"Total: {len(musicas_filtradas)} música(s)\n\n")

                for i, musica in enumerate(musicas_filtradas, 1):
                    resultado_text.insert(tk.END, f"{i}. {musica['titulo']}\n")
                    resultado_text.insert(tk.END, f"   Artista: {musica['artista']}\n")
                    resultado_text.insert(tk.END, f"   Álbum: {musica['album']} ({musica['ano']})\n")
                    resultado_text.insert(tk.END, f"   Gênero: {musica['genero']}\n\n")

        # Bind Enter para gerar rapidamente
        valor_entry.bind('<Return>', gerar)

        # Botão gerar
        tk.Button(janela,
                 text="📊 Gerar Relatório",
                 command=gerar,
                 bg=self.cores['botao'],
                 fg=self.cores['texto_botoes'],
                 font=('Arial', 12, 'bold'),
                 relief='flat',
                 cursor='hand2',
                 activebackground=self.cores['botao_hover'],
                 activeforeground=self.cores['texto_botoes']).pack(pady=10)

    def salvar_playlist(self):
        """Salva a playlist no arquivo"""
        salvar_dados(self.playlist, self.nome_arquivo)
        messagebox.showinfo("Sucesso", "Playlist salva com sucesso!")

    def recarregar_dados(self):
        """Recarrega os dados do arquivo e busca informações faltantes via API"""
        # Recarrega dados do arquivo
        self.playlist = carregar_dados(self.nome_arquivo)

        # Verifica músicas com dados incompletos (apenas baseado em título e artista)
        musicas_incompletas = []
        for musica in self.playlist:
            # Verifica se tem título e artista (requisitos mínimos)
            if not musica.get('titulo') or not musica.get('artista'):
                continue  # Pula músicas sem título ou artista

            # Considera incompleta se não tiver álbum, ano ou gênero definido
            # Busca SEMPRE para esses campos, mesmo que estejam preenchidos incorretamente
            if (musica.get('album') in [None, '', 'Desconhecido', '----'] or
                musica.get('ano') in [None, '', '----'] or
                musica.get('genero') in [None, '', 'Desconhecido']):
                musicas_incompletas.append(musica)

        if musicas_incompletas:
            # Pergunta se deseja buscar dados
            resposta = messagebox.askyesno(
                "Dados Incompletos Encontrados",
                f"Encontrei {len(musicas_incompletas)} música(s) com dados incompletos.\n\n"
                "A busca será feita usando apenas:\n"
                "  • Título da música\n"
                "  • Nome do artista\n\n"
                "Deseja buscar informações na internet para completar os dados?"
            )

            if resposta:
                self.buscar_dados_faltantes(musicas_incompletas)
                self.imagens_cache.clear()
                self.atualizar_lista()
                return  # Não mostra a mensagem "Dados recarregados" pois já foi mostrada
        else:
            # Nenhuma música incompleta
            messagebox.showinfo(
                "Dados Completos",
                "✅ Todas as músicas já possuem dados completos!\n\n"
                "Para recarregar dados mesmo assim, você pode:\n"
                "1. Editar uma música e limpar os campos que deseja atualizar\n"
                "2. Clicar em 'Recarregar Dados' novamente"
            )

        self.imagens_cache.clear()
        self.atualizar_lista()

    def buscar_dados_faltantes(self, musicas_incompletas):
        """Busca dados faltantes via API e confirma com o usuário"""
        import threading

        # Cria janela de progresso
        janela_progresso = tk.Toplevel(self.root)
        janela_progresso.title("Buscando Informações")
        janela_progresso.geometry("400x150")
        janela_progresso.configure(bg=self.cores['bg_secundario'])
        janela_progresso.transient(self.root)
        janela_progresso.grab_set()

        # Centraliza janela
        janela_progresso.update_idletasks()
        x = (janela_progresso.winfo_screenwidth() // 2) - (400 // 2)
        y = (janela_progresso.winfo_screenheight() // 2) - (150 // 2)
        janela_progresso.geometry(f"400x150+{x}+{y}")

        tk.Label(janela_progresso,
                text="🔍 Buscando informações na API...",
                font=('Arial', 12, 'bold'),
                bg=self.cores['bg_secundario'],
                fg=self.cores['texto_claro']).pack(pady=20)

        label_progresso = tk.Label(janela_progresso,
                                   text="Aguarde...",
                                   font=('Arial', 10),
                                   bg=self.cores['bg_secundario'],
                                   fg=self.cores['texto_claro'])
        label_progresso.pack(pady=10)

        def buscar_async():
            atualizadas = 0
            nao_encontradas = []

            for i, musica in enumerate(musicas_incompletas):
                # Atualiza label de progresso
                label_progresso.config(
                    text=f"Buscando {i+1} de {len(musicas_incompletas)}...\n{musica['titulo']} - {musica['artista']}"
                )
                janela_progresso.update()

                # Busca informações usando APENAS título e artista
                # Isso garante que mesmo com álbum/ano/gênero errados, encontrará dados corretos
                info = buscar_informacoes_musica(musica['titulo'], musica['artista'])

                if info:
                    # Mostra janela de confirmação
                    janela_progresso.withdraw()

                    if self.confirmar_atualizacao_dados(musica, info):
                        # Atualiza dados da música
                        musica['album'] = info['album']
                        musica['genero'] = info['genero']
                        musica['ano'] = info['ano']
                        atualizadas += 1

                    janela_progresso.deiconify()
                else:
                    # Música não encontrada
                    nao_encontradas.append(f"• {musica['titulo']} - {musica['artista']}")

            janela_progresso.destroy()

            # Salva alterações
            if atualizadas > 0:
                salvar_dados(self.playlist, self.nome_arquivo)

            # Monta mensagem de resultado
            mensagem = ""
            if atualizadas > 0:
                mensagem += f"✅ {atualizadas} música(s) atualizada(s) com sucesso!\n"

            if nao_encontradas:
                mensagem += f"\n⚠️ {len(nao_encontradas)} música(s) não encontrada(s) na API:\n\n"
                # Limita a 10 músicas para não ficar muito grande
                mensagem += "\n".join(nao_encontradas[:10])
                if len(nao_encontradas) > 10:
                    mensagem += f"\n... e mais {len(nao_encontradas) - 10} música(s)"
                mensagem += "\n\n💡 Dica: Verifique se o nome e artista estão corretos."

            if not mensagem:
                mensagem = "Nenhuma música foi atualizada."

            titulo_janela = "Atualização Concluída" if atualizadas > 0 else "Busca Concluída"
            messagebox.showinfo(titulo_janela, mensagem)

        # Executa busca em thread separada para não travar a interface
        thread = threading.Thread(target=buscar_async)
        thread.daemon = True
        thread.start()

    def confirmar_atualizacao_dados(self, musica_antiga, info_nova):
        """Mostra janela de confirmação comparando dados antigos e novos"""
        janela = tk.Toplevel(self.root)
        janela.title("Confirmar Atualização")
        janela.geometry("600x500")
        janela.configure(bg=self.cores['bg_secundario'])
        janela.transient(self.root)
        janela.grab_set()

        # Centraliza janela
        janela.update_idletasks()
        x = (janela.winfo_screenwidth() // 2) - (600 // 2)
        y = (janela.winfo_screenheight() // 2) - (500 // 2)
        janela.geometry(f"600x500+{x}+{y}")

        # Título
        tk.Label(janela,
                text="📊 Informações Encontradas",
                font=('Arial', 16, 'bold'),
                bg=self.cores['bg_secundario'],
                fg=self.cores['texto']).pack(pady=15)

        # Frame principal com scroll
        canvas = tk.Canvas(janela, bg=self.cores['bg_secundario'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(janela, orient='vertical', command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=self.cores['bg_secundario'])

        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame_scroll, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True, padx=10)
        scrollbar.pack(side='right', fill='y')

        # Frame de comparação
        frame_info = tk.Frame(frame_scroll, bg=self.cores['bg_card'], relief='ridge', bd=2)
        frame_info.pack(pady=10, padx=10, fill='both')

        # Música
        tk.Label(frame_info,
                text=f"🎵 {musica_antiga['titulo']}",
                font=('Arial', 14, 'bold'),
                bg=self.cores['bg_card'],
                fg=self.cores['texto']).pack(pady=10)

        tk.Label(frame_info,
                text=f"👤 {musica_antiga['artista']}",
                font=('Arial', 12),
                bg=self.cores['bg_card'],
                fg=self.cores['texto_claro']).pack(pady=5)

        # Dados atuais vs novos
        comparacao = [
            ("Álbum", musica_antiga.get('album', '----'), info_nova['album']),
            ("Gênero", musica_antiga.get('genero', '----'), info_nova['genero']),
            ("Ano", musica_antiga.get('ano', '----'), info_nova['ano'])
        ]

        for campo, antigo, novo in comparacao:
            frame_campo = tk.Frame(frame_info, bg=self.cores['bg_card'])
            frame_campo.pack(fill='x', padx=20, pady=8)

            tk.Label(frame_campo,
                    text=f"{campo}:",
                    font=('Arial', 11, 'bold'),
                    bg=self.cores['bg_card'],
                    fg=self.cores['texto_claro'],
                    width=10,
                    anchor='w').pack(side='left')

            # Valor antigo
            tk.Label(frame_campo,
                    text=str(antigo) if antigo else '----',
                    font=('Arial', 10),
                    bg=self.cores['bg_card'],
                    fg='#888888',
                    width=20,
                    anchor='w').pack(side='left', padx=5)

            tk.Label(frame_campo,
                    text="→",
                    font=('Arial', 12, 'bold'),
                    bg=self.cores['bg_card'],
                    fg=self.cores['texto']).pack(side='left', padx=5)

            # Valor novo
            tk.Label(frame_campo,
                    text=str(novo),
                    font=('Arial', 10, 'bold'),
                    bg=self.cores['bg_card'],
                    fg='#4CAF50',
                    width=20,
                    anchor='w').pack(side='left', padx=5)

        # Mostra prévia da capa se disponível
        if info_nova.get('capa_path'):
            try:
                img = Image.open(info_nova['capa_path'])
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                tk.Label(frame_info,
                        text="🖼️ Capa do Álbum:",
                        font=('Arial', 11, 'bold'),
                        bg=self.cores['bg_card'],
                        fg=self.cores['texto_claro']).pack(pady=10)

                img_label = tk.Label(frame_info, image=photo, bg=self.cores['bg_card'])
                img_label.image = photo  # Mantém referência
                img_label.pack(pady=10)
            except Exception as e:
                print(f"Erro ao carregar prévia da imagem: {e}")

        # Frame de botões
        frame_botoes = tk.Frame(janela, bg=self.cores['bg_secundario'])
        frame_botoes.pack(pady=20)

        resultado = {'confirmado': False}

        def confirmar():
            resultado['confirmado'] = True
            janela.destroy()

        def cancelar():
            resultado['confirmado'] = False
            janela.destroy()

        btn_confirmar = tk.Button(frame_botoes,
                                  text="✅ Usar Estes Dados",
                                  command=confirmar,
                                  bg='#4CAF50',
                                  fg='#000000',
                                  font=('Arial', 12, 'bold'),
                                  relief='flat',
                                  cursor='hand2',
                                  width=18)
        btn_confirmar.pack(side='left', padx=10)

        btn_cancelar = tk.Button(frame_botoes,
                                text="❌ Manter Original",
                                command=cancelar,
                                bg='#f44336',
                                fg='#000000',
                                font=('Arial', 12, 'bold'),
                                relief='flat',
                                cursor='hand2',
                                width=18)
        btn_cancelar.pack(side='left', padx=10)

        # Aguarda janela fechar
        janela.wait_window()

        return resultado['confirmado']

    def atualizar_estatisticas(self):
        """Atualiza as estatísticas exibidas"""
        total = len(self.playlist)
        generos = len(set(m['genero'] for m in self.playlist)) if self.playlist else 0
        artistas = len(set(m['artista'] for m in self.playlist)) if self.playlist else 0

        texto = f"Total de Músicas: {total}\n"
        texto += f"Artistas Únicos: {artistas}\n"
        texto += f"Gêneros Únicos: {generos}"

        self.stats_label.config(text=texto)


def main():
    """Função principal para executar a GUI"""
    root = tk.Tk()
    app = PlaylistGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
