from pathlib import Path

def carregar_dados(nome_arquivo="playlist.txt"):
    # Carrega os dados da playlist a partir de um arquivo de texto.
    # Retorna uma lista de dicionários com as músicas.
    # Se o arquivo não existir, retorna uma lista vazia.
    try:
        # Tenta abrir o arquivo em modo de leitura
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            # LISTA vazia para armazenar as músicas
            playlist = []

            # Lê cada linha do arquivo e adiciona à LISTA
            for linha in arquivo:
                # Remove espaços em branco e divide pelos separadores
                dados = linha.strip().split(';')

                # Cria um dicionário com os dados da música e adiciona à LISTA
                if len(dados) == 5:  # Valida que tem os 5 campos
                    musica = {
                        'titulo': dados[0],
                        'artista': dados[1],
                        'album': dados[2],
                        'genero': dados[3],
                        'ano': dados[4]
                    }
                    # Usa append() para adicionar à LISTA
                    playlist.append(musica)

            print(f">> {len(playlist)} música(s) carregada(s) na lista")
            return playlist

    except FileNotFoundError:
        # Se o arquivo não existir, inicia com LISTA vazia
        print(">> Arquivo não encontrado. Iniciando com lista vazia.")
        return []  # Retorna LISTA vazia


def salvar_dados(playlist, nome_arquivo="playlist.txt"):
    # Salva a playlist em um arquivo de texto.
    # Formato: Titulo;Artista;Album;Genero;Ano
    # Garante pasta de destino
    Path(nome_arquivo).parent.mkdir(parents=True, exist_ok=True)

    # Abre o arquivo em modo de escrita
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        # Itera sobre cada elemento da LISTA (cada música)
        for musica in playlist:
            # Formata a linha no formato especificado
            linha = f"{musica['titulo']};{musica['artista']};{musica['album']};{musica['genero']};{musica['ano']}\n"
            arquivo.write(linha)

    # Usa len() para obter tamanho da LISTA
    print(f">> Playlist salva com sucesso! ({len(playlist)} música(s) na lista)")


def exibir_menu():
    # Exibe o menu principal do programa.
    print("\n" + "="*50)
    print("         MENU PLAYLIST - Estrutura: LISTA")
    print("="*50)
    print("1. Adicionar Música")
    print("2. Listar Músicas")
    print("3. Buscar Música")
    print("4. Editar Música")
    print("5. Remover Música")
    print("6. Gerar Relatório")
    print("7. Salvar e Sair")
    print("="*50)


def adicionar_musica(playlist):
    # Adiciona uma nova música à playlist.
    # Título e Artista são campos obrigatórios.
    print("\n" + "="*50)
    print("         ADICIONAR NOVA MÚSICA")
    print("="*50)

    # Solicita os dados da música ao usuário
    titulo = input("Título: ").strip()
    artista = input("Artista: ").strip()

    # Valida que título e artista não estão vazios
    if not titulo or not artista:
        print(">> Erro: Título e Artista são campos obrigatórios!")
        return

    album = input("Álbum (opcional): ").strip() or "Desconhecido"
    genero = input("Gênero (opcional): ").strip() or "Desconhecido"
    ano = input("Ano (opcional): ").strip() or "----"

    # Cria o dicionário da nova música
    nova_musica = {
        'titulo': titulo,
        'artista': artista,
        'album': album,
        'genero': genero,
        'ano': ano
    }

    # OPERAÇÃO: append() - adiciona ao final da lista
    playlist.append(nova_musica)

    print(f"\n>> Música adicionada com sucesso!")
    print(f">> Total de músicas na lista: {len(playlist)}")


def listar_musicas(playlist):
    # Lista todas as músicas da playlist.
    print("\n" + "="*50)
    print("         LISTA DE MÚSICAS")
    print("="*50)

    # OPERAÇÃO: len() - verifica tamanho da LISTA
    if len(playlist) == 0:
        print(">> Nenhuma música na lista.")
        return

    print(f"Total: {len(playlist)} música(s) na lista\n")

    # OPERAÇÃO: enumerate() - itera com índice automaticamente
    for i, musica in enumerate(playlist, 1):
        print(f"{i}. {musica['titulo']}")
        print(f"   Artista: {musica['artista']}")
        print(f"   Álbum: {musica['album']}")
        print(f"   Gênero: {musica['genero']}")
        print(f"   Ano: {musica['ano']}")
        print("-" * 50)


def buscar_musica(playlist):
    # Busca músicas por título
    print("\n" + "="*50)
    print("         BUSCAR MÚSICA")
    print("="*50)

    termo_busca = input("Digite o título da música: ").strip()

    # Filtra músicas que contêm o termo no título
    musicas_encontradas = [
        musica for musica in playlist
        if termo_busca.lower() in musica['titulo'].lower()
    ]

    # Exibe os resultados
    if not musicas_encontradas:
        print(f">> Nenhuma música encontrada com '{termo_busca}'")
    else:
        print(f"\n>> {len(musicas_encontradas)} música(s) encontrada(s) na lista:\n")
        for i, musica in enumerate(musicas_encontradas, 1):
            print(f"{i}. {musica['titulo']}")
            print(f"   {musica['artista']} | {musica['album']}")
            print(f"   {musica['genero']} | {musica['ano']}")
            print("-" * 50)


def editar_musica(playlist):
    # Edita os dados de uma música existente.
    # Busca pela música pelo título e permite editar todos os campos.
    print("\n" + "="*50)
    print("         EDITAR MÚSICA")
    print("="*50)

    titulo_busca = input("Digite o título da música a ser editada: ").strip()
    musica_encontrada = None
    indice = -1

    # enumerate para obter índice e elemento
    for i, musica in enumerate(playlist):
        if titulo_busca.lower() == musica['titulo'].lower():
            musica_encontrada = musica
            indice = i
            break

    if not musica_encontrada:
        print(f">> Música '{titulo_busca}' não encontrada na lista.")
        return

    # Exibe os dados atuais
    print(f"\n>> Dados atuais (posição {indice} na lista):")
    print(f"   Título: {musica_encontrada['titulo']}")
    print(f"   Artista: {musica_encontrada['artista']}")
    print(f"   Álbum: {musica_encontrada['album']}")
    print(f"   Gênero: {musica_encontrada['genero']}")
    print(f"   Ano: {musica_encontrada['ano']}")

    print("\n>> Digite os novos dados (deixe vazio para manter):")
    novo_titulo = input(f"Novo Título [{musica_encontrada['titulo']}]: ").strip()
    novo_artista = input(f"Novo Artista [{musica_encontrada['artista']}]: ").strip()
    novo_album = input(f"Novo Álbum [{musica_encontrada['album']}]: ").strip()
    novo_genero = input(f"Novo Gênero [{musica_encontrada['genero']}]: ").strip()
    novo_ano = input(f"Novo Ano [{musica_encontrada['ano']}]: ").strip()

    # Atualiza elemento na lista
    playlist[indice]['titulo'] = novo_titulo if novo_titulo else musica_encontrada['titulo']
    playlist[indice]['artista'] = novo_artista if novo_artista else musica_encontrada['artista']
    playlist[indice]['album'] = novo_album if novo_album else musica_encontrada['album']
    playlist[indice]['genero'] = novo_genero if novo_genero else musica_encontrada['genero']
    playlist[indice]['ano'] = novo_ano if novo_ano else musica_encontrada['ano']

    print(f"\n>> Música na posição {indice} atualizada com sucesso na lista!")


def remover_musica(playlist):
    # Remove uma música da playlist após confirmação do usuário.
    print("\n" + "="*50)
    print("         REMOVER MÚSICA")
    print("="*50)

    titulo_busca = input("Digite o título da música a ser removida: ").strip()
    musica_encontrada = None
    indice = -1

    # Procura pela música (correspondência exata)
    for i, musica in enumerate(playlist):
        if titulo_busca.lower() == musica['titulo'].lower():
            musica_encontrada = musica
            indice = i
            break

    if not musica_encontrada:
        print(f">> Música '{titulo_busca}' não encontrada na lista.")
        return

    # Exibe os dados da música
    print(f"\n>> Música encontrada (posição {indice} na lista):")
    print(f"   Título: {musica_encontrada['titulo']}")
    print(f"   Artista: {musica_encontrada['artista']}")
    print(f"   Álbum: {musica_encontrada['album']}")
    print(f"   Gênero: {musica_encontrada['genero']}")
    print(f"   Ano: {musica_encontrada['ano']}")

    # Pede confirmação
    confirmacao = input("\n>> Tem certeza que deseja remover esta música? (S/N): ").strip()

    if confirmacao.upper() == 'S':
        # OPERAÇÃO: remove() - remove elemento da lista
        playlist.remove(musica_encontrada)
        print(f"\n>> Música removida com sucesso da lista!")
        print(f">> Total de músicas restantes: {len(playlist)}")
    else:
        print(">> Remoção cancelada.")


def gerar_relatorio(playlist):
    # Gera um relatório de músicas filtradas por diferentes critérios.
    # Permite filtrar por: Título, Artista, Álbum, Gênero ou Ano.
    print("\n" + "="*50)
    print("         GERAR RELATÓRIO - Filtrar Lista")
    print("="*50)
    print("Escolha o campo para filtrar:")
    print("1. Título")
    print("2. Artista")
    print("3. Álbum")
    print("4. Gênero")
    print("5. Ano")

    try:
        opcao_filtro = int(input("\nEscolha uma opção (1-5): ").strip())

        # Define qual campo será usado para o filtro
        if opcao_filtro == 1:
            campo = 'titulo'
            nome_campo = 'Título'
        elif opcao_filtro == 2:
            campo = 'artista'
            nome_campo = 'Artista'
        elif opcao_filtro == 3:
            campo = 'album'
            nome_campo = 'Álbum'
        elif opcao_filtro == 4:
            campo = 'genero'
            nome_campo = 'Gênero'
        elif opcao_filtro == 5:
            campo = 'ano'
            nome_campo = 'Ano'
        else:
            print(">> Opção inválida. Escolha de 1 a 5.")
            return

        # Solicita o valor para filtrar
        valor_busca = input(f"Digite o {nome_campo} para filtrar: ").strip()

        # LIST COMPREHENSION: Filtra músicas pelo campo escolhido
        musicas_encontradas = [
            musica for musica in playlist
            if valor_busca.lower() == musica[campo].lower()
        ]

        # Exibe o relatório
        if not musicas_encontradas:
            print(f"\n>> Nenhuma música encontrada para {nome_campo}: {valor_busca}")
        else:
            print(f"\n" + "="*50)
            print(f"         RELATÓRIO: {nome_campo} = {valor_busca}")
            print("="*50)
            print(f"Total: {len(musicas_encontradas)} música(s) na lista filtrada\n")

            for i, musica in enumerate(musicas_encontradas, 1):
                print(f"{i}. {musica['titulo']}")
                print(f"   {musica['artista']} | {musica['album']}")
                print(f"   {musica['genero']} | {musica['ano']}")
                print("-" * 50)

    except ValueError:
        print(">> Opção inválida. Digite um número.")



def main():
    # Função principal do programa.
    # Gerencia o loop do menu e as interações com o usuário.
    # Resolve caminho da playlist dentro de data/ independentemente do diretório atual
    project_root = Path(__file__).resolve().parent.parent
    nome_arquivo = str(project_root / 'data' / 'playlist.txt')

    # Carrega os dados do arquivo
    playlist = carregar_dados(nome_arquivo)

    # Loop principal do programa
    while True:
        exibir_menu()

        try:
            # Solicita a opção do usuário
            opcao = int(input("\nEscolha uma opção: "))

            # Executa a ação correspondente à opção escolhida
            if opcao == 1:
                adicionar_musica(playlist)
            elif opcao == 2:
                listar_musicas(playlist)
            elif opcao == 3:
                buscar_musica(playlist)
            elif opcao == 4:
                editar_musica(playlist)
            elif opcao == 5:
                remover_musica(playlist)
            elif opcao == 6:
                gerar_relatorio(playlist)
            elif opcao == 7:
                # Salva os dados e sai do programa
                salvar_dados(playlist, nome_arquivo)
                print("\n>> Saindo do sistema...")
                print(">> Dados salvos com sucesso!")
                break
            else:
                print(">> Opção inválida. Escolha de 1 a 7.")

        except ValueError:
            # Tratamento de erro para entrada inválida
            print(">> Opção inválida. Digite um número.")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()
