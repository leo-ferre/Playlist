@echo off
chcp 65001 > nul
title Gerenciador de Playlist - Windows
cls

echo.
echo ====================================================================
echo.
echo        GERENCIADOR DE PLAYLIST - LAUNCHER WINDOWS
echo.
echo ====================================================================
echo.

REM ====================================================================
REM Verifica se Python esta instalado
REM ====================================================================
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    cls
    echo.
    echo ====================================================================
    echo                         ERRO: PYTHON NAO ENCONTRADO
    echo ====================================================================
    echo.
    echo O Python nao esta instalado ou nao esta no PATH do sistema.
    echo.
    echo Para corrigir:
    echo.
    echo 1. Baixe o Python em: https://www.python.org/downloads/
    echo 2. Durante a instalacao, MARQUE estas opcoes:
    echo    [X] Add Python to PATH
    echo    [X] Install tcl/tk and IDLE
    echo 3. Reinicie o computador apos a instalacao
    echo 4. Execute este arquivo novamente
    echo.
    echo ====================================================================
    echo.
    pause
    exit /b 1
)
echo    OK - Python encontrado
python --version

REM ====================================================================
REM Verifica se tkinter esta disponivel (necessario para GUI)
REM ====================================================================
echo.
echo [2/4] Verificando tkinter (interface grafica)...
python -c "import tkinter; tkinter.Tk().withdraw()" >nul 2>&1
if %errorlevel% neq 0 (
    echo    AVISO - tkinter nao esta instalado ou nao funciona
    echo.
    echo    A Interface Grafica (opcao 1) nao funcionara.
    echo    Para corrigir, reinstale o Python marcando:
    echo    [X] Install tcl/tk and IDLE
    echo.
    echo    Voce ainda pode usar:
    echo    - Opcao 2: Linha de Comando (CLI)
    echo.
    echo    Pressione qualquer tecla para continuar (ou Ctrl+C para sair)...
    pause >nul
) else (
    echo    OK - tkinter disponivel
)

REM ====================================================================
REM Verifica se as dependencias estao instaladas
REM ====================================================================
echo.
echo [3/4] Verificando dependencias (Pillow e requests)...
python -c "import PIL, requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo    Dependencias nao encontradas. Instalando automaticamente...
    echo.
    echo    Aguarde, isso pode levar alguns minutos...
    echo.

    REM Atualiza pip
    python -m pip install --upgrade pip --quiet >nul 2>&1

    REM Instala dependencias
    python -m pip install Pillow requests --quiet

    if %errorlevel% neq 0 (
        echo.
        echo    ERRO ao instalar dependencias!
        echo.
        echo    Tente instalar manualmente:
        echo    python -m pip install Pillow requests
        echo.
        pause
        exit /b 1
    )

    echo    OK - Dependencias instaladas com sucesso!
) else (
    echo    OK - Dependencias ja instaladas
)

REM ====================================================================
REM Cria estrutura de pastas se nao existir
REM ====================================================================
echo.
echo [4/4] Verificando estrutura de pastas...
if not exist "data" mkdir data
if not exist "data\album_covers" mkdir data\album_covers
if not exist "docs" mkdir docs
if not exist "src" (
    echo    ERRO: Pasta src nao encontrada!
    echo    Certifique-se de executar este arquivo na raiz do projeto.
    pause
    exit /b 1
)
echo    OK - Estrutura de pastas pronta

echo.
echo ====================================================================
echo                    TUDO PRONTO! INICIANDO...
echo ====================================================================
echo.
timeout /t 2 /nobreak >nul

REM ====================================================================
REM Executa o programa
REM ====================================================================
cls
python playlist.py

REM ====================================================================
REM Verifica se houve erro
REM ====================================================================
if %errorlevel% neq 0 (
    echo.
    echo ====================================================================
    echo                            ERRO
    echo ====================================================================
    echo.
    echo Ocorreu um erro ao executar o programa.
    echo.
    echo Se o problema persistir:
    echo 1. Verifique se todas as dependencias estao instaladas
    echo 2. Tente executar: python playlist.py
    echo 3. Leia o arquivo README.md para mais informacoes
    echo.
    echo ====================================================================
    echo.
    pause
)

