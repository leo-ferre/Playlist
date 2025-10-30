"""
Sistema de Gerenciamento de Playlist de Músicas
Programa de linha de comando para adicionar, listar, buscar, editar e remover músicas.
"""

from pathlib import Path


def carregar_dados(nome_arquivo="playlist.txt"):
    """
    Carrega os dados da playlist a partir de um arquivo de texto.
    Retorna uma lista de dicionários com as músicas.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    try:
        # Tenta abrir o arquivo em modo de leitura
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            playlist = []
            # Lê cada linha do arquivo
            for linha in arquivo:
                # Remove espaços em branco e divide pelos separadores
                dados = linha.strip().split(';')
                # Cria um dicionário com os dados da música
                if len(dados) == 5:  # Valida que tem os 5 campos
                    musica = {
                        'titulo': dados[0],
                        'artista': dados[1],
                        'album': dados[2],
                        'genero': dados[3],
                        'ano': dados[4]
                    }
                    playlist.append(musica)
            return playlist
    except FileNotFoundError:
        # Se o arquivo não existir, inicia com playlist vazia
        print("Arquivo não encontrado. Iniciando com playlist vazia.")
        return []


def salvar_dados(playlist, nome_arquivo="playlist.txt"):
    """
    Salva a playlist em um arquivo de texto.
    Formato: Titulo;Artista;Album;Genero;Ano
    """
    # Garante pasta de destino
    Path(nome_arquivo).parent.mkdir(parents=True, exist_ok=True)
    # Abre o arquivo em modo de escrita
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        # Itera sobre cada música na playlist
        for musica in playlist:
            # Formata a linha no formato especificado
            linha = f"{musica['titulo']};{musica['artista']};{musica['album']};{musica['genero']};{musica['ano']}\n"
            arquivo.write(linha)
    print("Playlist salva com sucesso!")


def exibir_menu():
    """
    Exibe o menu principal do programa.
    """
    print("\n--- MENU PLAYLIST ---")
    print("1. Adicionar Música")
    print("2. Listar Músicas")
    print("3. Buscar Música (por Título)")
    print("4. Editar Música")
    print("5. Remover Música")
    print("6. Gerar Relatório (Filtrar por Campo)")
    print("7. Sair")


def adicionar_musica(playlist):
    """
    Adiciona uma nova música à playlist.
    Título e Artista são campos obrigatórios.
    """
    print("\n--- Adicionar Nova Música ---")

    # Solicita os dados da música ao usuário
    titulo = input("Título: ").strip()
    artista = input("Artista: ").strip()

    # Valida que título e artista não estão vazios
    if not titulo or not artista:
        print("Título e Artista são campos obrigatórios!")
        return

    album = input("Álbum: ").strip()
    genero = input("Gênero: ").strip()
    ano = input("Ano: ").strip()

    # Cria o dicionário da nova música
    nova_musica = {
        'titulo': titulo,
        'artista': artista,
        'album': album,
        'genero': genero,
        'ano': ano
    }

    # Adiciona à playlist
    playlist.append(nova_musica)
    print("Música adicionada com sucesso!")


def listar_musicas(playlist):
    """
    Lista todas as músicas da playlist.
    """
    print("\n--- Lista de Músicas ---")

    # Verifica se a playlist está vazia
    if not playlist:
        print("Nenhuma música na playlist.")
        return

    # Itera sobre cada música e exibe formatada
    for i, musica in enumerate(playlist, 1):
        print(f"{i}. Título: {musica['titulo']} | Artista: {musica['artista']} | "
              f"Álbum: {musica['album']} | Gênero: {musica['genero']} | Ano: {musica['ano']}")


def buscar_musica(playlist):
    """
    Busca músicas por título (busca parcial, case-insensitive).
    """
    print("\n--- Buscar Música ---")

    termo_busca = input("Digite o título da música: ").strip()
    musicas_encontradas = []

    # Procura por correspondências parciais no título
    for musica in playlist:
        if termo_busca.lower() in musica['titulo'].lower():
            musicas_encontradas.append(musica)

    # Exibe os resultados
    if not musicas_encontradas:
        print("Música não encontrada.")
    else:
        print(f"\n{len(musicas_encontradas)} música(s) encontrada(s):")
        for musica in musicas_encontradas:
            print(f"Título: {musica['titulo']} | Artista: {musica['artista']} | "
                  f"Álbum: {musica['album']} | Gênero: {musica['genero']} | Ano: {musica['ano']}")


def editar_musica(playlist):
    """
    Edita os dados de uma música existente.
    Busca pela música pelo título e permite editar todos os campos.
    """
    print("\n--- Editar Música ---")

    titulo_busca = input("Digite o título da música a ser editada: ").strip()
    musica_encontrada = None

    # Procura pela música (correspondência exata ou primeira encontrada)
    for musica in playlist:
        if titulo_busca.lower() == musica['titulo'].lower():
            musica_encontrada = musica
            break

    if not musica_encontrada:
        print("Música não encontrada.")
        return

    # Exibe os dados atuais
    print("\nDados atuais:")
    print(f"Título: {musica_encontrada['titulo']} | Artista: {musica_encontrada['artista']} | "
          f"Álbum: {musica_encontrada['album']} | Gênero: {musica_encontrada['genero']} | "
          f"Ano: {musica_encontrada['ano']}")

    print("\nDigite os novos dados:")
    novo_titulo = input("Novo Título: ").strip()
    novo_artista = input("Novo Artista: ").strip()

    # Valida que título e artista não estão vazios
    if not novo_titulo or not novo_artista:
        print("Título e Artista são campos obrigatórios!")
        return

    novo_album = input("Novo Álbum: ").strip()
    novo_genero = input("Novo Gênero: ").strip()
    novo_ano = input("Novo Ano: ").strip()

    # Atualiza o dicionário da música
    musica_encontrada['titulo'] = novo_titulo
    musica_encontrada['artista'] = novo_artista
    musica_encontrada['album'] = novo_album
    musica_encontrada['genero'] = novo_genero
    musica_encontrada['ano'] = novo_ano

    print("Música atualizada com sucesso!")


def remover_musica(playlist):
    """
    Remove uma música da playlist após confirmação do usuário.
    """
    print("\n--- Remover Música ---")

    titulo_busca = input("Digite o título da música a ser removida: ").strip()
    musica_encontrada = None

    # Procura pela música (correspondência exata)
    for musica in playlist:
        if titulo_busca.lower() == musica['titulo'].lower():
            musica_encontrada = musica
            break

    if not musica_encontrada:
        print("Música não encontrada.")
        return

    # Exibe os dados da música
    print("\nMúsica encontrada:")
    print(f"Título: {musica_encontrada['titulo']} | Artista: {musica_encontrada['artista']} | "
          f"Álbum: {musica_encontrada['album']} | Gênero: {musica_encontrada['genero']} | "
          f"Ano: {musica_encontrada['ano']}")

    # Pede confirmação
    confirmacao = input("\nTem certeza que deseja remover esta música? (S/N): ").strip()

    if confirmacao.upper() == 'S':
        playlist.remove(musica_encontrada)
        print("Música removida com sucesso.")
    elif confirmacao.upper() == 'N':
        print("Remoção cancelada.")
    else:
        print("Opção inválida. Remoção cancelada.")


def gerar_relatorio(playlist):
    """
    Gera um relatório de músicas filtradas por diferentes critérios.
    Permite filtrar por: Título, Artista, Álbum, Gênero ou Ano.
    """
    print("\n--- Gerar Relatório ---")
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
            print("Opção inválida. Escolha de 1 a 5.")
            return

        # Solicita o valor para filtrar
        valor_busca = input(f"Digite o {nome_campo} para filtrar: ").strip()
        musicas_encontradas = []

        # Filtra músicas pelo campo escolhido (correspondência exata, case-insensitive)
        for musica in playlist:
            if valor_busca.lower() == musica[campo].lower():
                musicas_encontradas.append(musica)

        # Exibe o relatório
        if not musicas_encontradas:
            print(f"Nenhuma música encontrada para {nome_campo}: {valor_busca}")
        else:
            print(f"\n--- Relatório: {nome_campo} = {valor_busca} ---")
            print(f"Total de {len(musicas_encontradas)} música(s) encontrada(s):\n")
            for i, musica in enumerate(musicas_encontradas, 1):
                print(f"{i}. Título: {musica['titulo']} | Artista: {musica['artista']} | "
                      f"Álbum: {musica['album']} | Gênero: {musica['genero']} | Ano: {musica['ano']}")
            print("-------------------------------------------")

    except ValueError:
        print("Opção inválida. Digite um número.")


def main():
    """
    Função principal do programa.
    Gerencia o loop do menu e as interações com o usuário.
    """
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
                print("Saindo...")
                break
            else:
                print("Opção inválida. Escolha de 1 a 7.")

        except ValueError:
            # Tratamento de erro para entrada inválida
            print("Opção inválida. Digite um número.")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()
