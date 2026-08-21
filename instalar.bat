@echo off
chcp 65001 >nul
title Transcritum - Instalador

echo ===========================================================
echo                     T R A N S C R I T U M
echo                        VERUM SCIENTIA
echo ===========================================================
echo.
echo Preparando o ambiente do Transcritum...
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    py -m venv venv

    if errorlevel 1 (
        echo.
        echo [ERRO] Nao foi possivel criar o ambiente virtual.
        echo Verifique se o Python 3.12 esta instalado.
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Ativando ambiente virtual...
call "venv\Scripts\activate.bat"

echo.
echo Atualizando o pip...
python -m pip install --upgrade pip

echo.
echo Instalando as dependencias do Transcritum...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um problema durante a instalacao das dependencias.
    echo.
    pause
    exit /b 1
)

echo.
echo ===========================================================
echo                  INSTALACAO CONCLUIDA
echo ===========================================================
echo.
echo O Transcritum esta pronto para uso.
echo.
echo Para iniciar o programa, use o arquivo:
echo transcritum.bat
echo.
pause