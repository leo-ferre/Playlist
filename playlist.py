#!/usr/bin/env python3
"""
NOMES
Leonardo Ferreira
Heloi Vecchi Sgarbi
Kaua Schiavolin Monteiro

Launcher multiplataforma para o Sistema de Gerenciamento de Playlist
"""

import os
import sys
import subprocess
from pathlib import Path

def limpar_tela():
    """Limpa a tela do terminal de forma segura"""
    try:
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # macOS/Linux
            # Verifica se TERM está definida antes de tentar limpar
            if os.environ.get('TERM'):
                os.system('clear')
            else:
                # Fallback: imprime linhas em branco se TERM não estiver definida
                print('\n' * 50)
    except Exception:
        # Se qualquer erro ocorrer, usa fallback seguro
        print('\n' * 50)


def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    try:
        import PIL
        import requests
        return True
    except ImportError:
        return False


def instalar_dependencias():
    """Instala todas as dependências necessárias automaticamente"""
    print()
    print("=" * 70)
    print()
    print("    INSTALADOR AUTOMÁTICO".center(70))
    print()
    print("=" * 70)
    print()

    # Detecta sistema operacional
    sistema = sys.platform
    if sistema == 'win32':
        sistema_nome = "Windows"
    elif sistema == 'darwin':
        sistema_nome = "macOS"
    else:
        sistema_nome = "Linux"

    print(f">> Sistema detectado: {sistema_nome}")
    print()

    # Verifica se Python está instalado corretamente
    print(f">> Python {sys.version.split()[0]} encontrado")
    print()

    print(">> Instalando dependências necessárias...")
    print("   - Pillow (manipulação de imagens)")
    print("   - requests (chamadas à API)")
    print()

    try:
        # Atualiza pip
        print("[1/2] Atualizando pip...")
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', '--quiet'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("      >> pip atualizado")

        # Instala dependências
        print("[2/2] Instalando Pillow e requests...")
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', 'Pillow', 'requests', '--quiet'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("      >> Dependências instaladas")

        print()
        print("=" * 70)
        print()
        print("    INSTALAÇÃO CONCLUÍDA COM SUCESSO!".center(70))
        print()
        print("=" * 70)
        print()

        return True

    except subprocess.CalledProcessError as e:
        print()
        print(">> Erro durante a instalação!")
        print()
        print(">> Tente instalar manualmente:")
        print(f"   {sys.executable} -m pip install Pillow requests")
        print()
        return False
    except Exception as e:
        print(f">> Erro inesperado: {e}")
        return False


def configurar_estrutura():
    """Cria a estrutura de pastas e arquivos necessários"""
    project_root = Path(__file__).resolve().parent

    # Cria pastas
    (project_root / 'data' / 'album_covers').mkdir(parents=True, exist_ok=True)
    (project_root / 'docs').mkdir(parents=True, exist_ok=True)

    # Cria arquivo de playlist vazio se não existir
    playlist_file = project_root / 'data' / 'playlist.txt'
    if not playlist_file.exists():
        playlist_file.touch()

    return project_root


def mostrar_cabecalho():
    """Exibe o cabeçalho do sistema"""
    print("=" * 60)
    print()
    print("SISTEMA DE GERENCIAMENTO DE PLAYLIST".center(60))
    print()
    print("=" * 60)
    print()


def mostrar_menu():
    """Exibe o menu principal"""
    print("-" * 60)
    print("OPÇÕES DISPONÍVEIS".center(60))
    print("-" * 60)
    print()
    print("  1. Interface Gráfica")
    print("  2. Linha de Comando (CLI)")
    print("  3. Ver Documentação")
    print("  4. Sair")
    print()
    print("-" * 60)
    print()


def abrir_documentacao(doc_path):
    """Abre a documentação de acordo com o sistema operacional"""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(str(doc_path))
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', str(doc_path)], check=False)
        else:  # Linux
            subprocess.run(['xdg-open', str(doc_path)], check=False)
        print(">> Documentação aberta!")
    except Exception as e:
        print(f">> Não foi possível abrir automaticamente.")
        print(f">> Documentação disponível em: {doc_path}")


def verificar_tkinter():
    """Verifica se tkinter está disponível"""
    try:
        import tkinter
        # Tenta criar uma janela de teste para garantir que funciona
        try:
            root = tkinter.Tk()
            root.withdraw()  # Esconde a janela
            root.destroy()   # Destrói a janela de teste
        except Exception:
            # tkinter importou mas não funciona (pode acontecer em alguns ambientes)
            return False
        return True
    except (ImportError, ModuleNotFoundError):
        return False


def executar_gui(project_root):
    """Executa a interface gráfica"""
    print()
    print(">> Iniciando Interface Gráfica...")
    print()

    if not verificar_tkinter():
        print(">> Erro: tkinter não está instalado!")
        print()
        print(">> Para instalar:")
        if os.name == 'nt':
            print("   - Reinstale o Python marcando 'tcl/tk and IDLE' na instalação")
            print("   - Ou baixe de: https://www.python.org/downloads/")
        elif sys.platform == 'darwin':
            print("   - macOS (Homebrew): brew install python-tk")
        else:
            print("   - Ubuntu/Debian: sudo apt-get install python3-tk")
            print("   - Fedora: sudo dnf install python3-tkinter")
        print()
        input("Pressione Enter para voltar ao menu...")
        return

    gui_path = project_root / 'src' / 'main_gui.py'
    try:
        subprocess.run([sys.executable, str(gui_path)], check=True)
    except subprocess.CalledProcessError:
        print(">> Erro ao executar a interface gráfica")
        input("Pressione Enter para voltar ao menu...")
    except KeyboardInterrupt:
        print("\n>> Interface gráfica fechada pelo usuário")


def executar_cli(project_root):
    """Executa a interface de linha de comando"""
    print()
    print(">> Iniciando Modo Linha de Comando...")
    print()

    cli_path = project_root / 'src' / 'main.py'
    try:
        subprocess.run([sys.executable, str(cli_path)], check=True)
    except subprocess.CalledProcessError:
        print(">> Erro ao executar a CLI")
        input("Pressione Enter para voltar ao menu...")
    except KeyboardInterrupt:
        print("\n>> CLI fechada pelo usuário")


def main():
    """Função principal do launcher"""

    # Verifica e instala dependências na primeira execução
    if not verificar_dependencias():
        limpar_tela()
        print()
        print("=" * 70)
        print()
        print("BEM-VINDO AO GERENCIADOR DE PLAYLIST!".center(70))
        print()
        print("=" * 70)
        print()
        print(">> Primeira execução detectada!")
        print("   Vou instalar as dependências necessárias automaticamente.")
        print()

        resposta = input("Deseja continuar com a instalação? (S/n): ").strip().lower()

        if resposta == 'n':
            print()
            print(">> Instalação cancelada.")
            print()
            return

        if not instalar_dependencias():
            print()
            input("Pressione Enter para sair...")
            return

        print(">> Tudo pronto! Reiniciando o programa...")
        print()
        input("Pressione Enter para continuar...")

    # Configura estrutura de pastas
    project_root = configurar_estrutura()

    # Loop principal do menu
    while True:
        limpar_tela()
        mostrar_cabecalho()
        mostrar_menu()

        try:
            opcao = input(">> Escolha uma opção (1-4): ").strip()

            if opcao == '1':
                executar_gui(project_root)
            elif opcao == '2':
                executar_cli(project_root)
            elif opcao == '3':
                doc_path = project_root / 'docs' / 'README.md'
                abrir_documentacao(doc_path)
                input("\nPressione Enter para voltar ao menu...")
            elif opcao == '4':
                print()
                print(">> Até logo!")
                print()
                break
            else:
                print()
                print(">> Opção inválida!")
                print()
                input("Pressione Enter para tentar novamente...")

        except KeyboardInterrupt:
            print("\n\n>> Até logo!")
            break
        except Exception as e:
            print(f"\n>> Erro inesperado: {e}")
            input("Pressione Enter para continuar...")


if __name__ == '__main__':
    main()

