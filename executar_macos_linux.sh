#!/usr/bin/env bash

# ==================================================================
# Gerenciador de Playlist - Launcher para macOS/Linux
# Com verificação e instalação automática de dependências
# ==================================================================

set -e

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "===================================================================="
echo ""
echo "        GERENCIADOR DE PLAYLIST - LAUNCHER macOS/Linux"
echo ""
echo "===================================================================="
echo ""

# ==================================================================
# [1/4] Verifica se Python está instalado
# ==================================================================
echo "[1/4] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}   ERRO - Python3 não encontrado!${NC}"
    echo ""
    echo "   Para instalar:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   • macOS (Homebrew): brew install python3"
    elif [[ -f /etc/debian_version ]]; then
        echo "   • Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    elif [[ -f /etc/redhat-release ]]; then
        echo "   • Fedora/RHEL: sudo dnf install python3 python3-pip"
    else
        echo "   • Use o gerenciador de pacotes do seu sistema"
    fi
    echo ""
    exit 1
fi
echo -e "${GREEN}   OK - Python encontrado${NC}"
python3 --version

# ==================================================================
# [2/4] Verifica se tkinter está disponível
# ==================================================================
echo ""
echo "[2/4] Verificando tkinter (interface gráfica)..."
if python3 -c "import tkinter; tkinter.Tk().withdraw()" &> /dev/null; then
    echo -e "${GREEN}   OK - tkinter disponível${NC}"
else
    echo -e "${YELLOW}   AVISO - tkinter não está instalado${NC}"
    echo ""
    echo "   A Interface Gráfica (opção 1) não funcionará."
    echo "   Para instalar:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   • macOS (Homebrew): brew install python-tk"
    elif [[ -f /etc/debian_version ]]; then
        echo "   • Ubuntu/Debian: sudo apt-get install python3-tk"
    elif [[ -f /etc/redhat-release ]]; then
        echo "   • Fedora/RHEL: sudo dnf install python3-tkinter"
    fi
    echo ""
    echo "   Você ainda pode usar a opção 2 (CLI)."
    echo ""
    read -p "   Pressione Enter para continuar..."
fi

# ==================================================================
# [3/4] Verifica e instala dependências
# ==================================================================
echo ""
echo "[3/4] Verificando dependências (Pillow e requests)..."
if python3 -c "import PIL, requests" &> /dev/null; then
    echo -e "${GREEN}   OK - Dependências já instaladas${NC}"
else
    echo -e "${YELLOW}   Dependências não encontradas. Instalando...${NC}"
    echo ""
    echo "   Aguarde, isso pode levar alguns minutos..."
    echo ""

    # Atualiza pip
    python3 -m pip install --upgrade pip --quiet &> /dev/null

    # Instala dependências
    if python3 -m pip install Pillow requests --quiet; then
        echo -e "${GREEN}   OK - Dependências instaladas com sucesso!${NC}"
    else
        echo -e "${RED}   ERRO ao instalar dependências!${NC}"
        echo ""
        echo "   Tente instalar manualmente:"
        echo "   python3 -m pip install Pillow requests"
        echo ""
        exit 1
    fi
fi

# ==================================================================
# [4/4] Verifica estrutura de pastas
# ==================================================================
echo ""
echo "[4/4] Verificando estrutura de pastas..."
mkdir -p data/album_covers
mkdir -p docs
if [ ! -d "src" ]; then
    echo -e "${RED}   ERRO: Pasta src/ não encontrada!${NC}"
    echo "   Certifique-se de executar este arquivo na raiz do projeto."
    exit 1
fi
echo -e "${GREEN}   OK - Estrutura de pastas pronta${NC}"

echo ""
echo "===================================================================="
echo "                    TUDO PRONTO! INICIANDO..."
echo "===================================================================="
echo ""
sleep 1

# ==================================================================
# Executa o programa
# ==================================================================
clear
python3 playlist.py

# ==================================================================
# Verifica se houve erro
# ==================================================================
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo ""
    echo "===================================================================="
    echo "                            ERRO"
    echo "===================================================================="
    echo ""
    echo "Ocorreu um erro ao executar o programa."
    echo ""
    echo "Se o problema persistir:"
    echo "1. Verifique se todas as dependências estão instaladas"
    echo "2. Tente executar: python3 playlist.py"
    echo "3. Leia o arquivo README.md para mais informações"
    echo ""
    echo "===================================================================="
    echo ""
    read -p "Pressione Enter para sair..."
fi

exit $exit_code

