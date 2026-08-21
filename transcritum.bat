@echo off
chcp 65001 >nul
title Transcritum - Verum Scientia

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo ===========================================================
    echo                     T R A N S C R I T U M
    echo                        VERUM SCIENTIA
    echo ===========================================================
    echo.
    echo O Transcritum ainda nao foi instalado neste computador.
    echo.
    echo Execute primeiro o arquivo:
    echo instalar.bat
    echo.
    pause
    exit /b 1
)

call "venv\Scripts\activate.bat"

python transcritum.py

if errorlevel 1 (
    echo.
    echo [ERRO] O Transcritum foi encerrado devido a um problema.
    echo.
    pause
)