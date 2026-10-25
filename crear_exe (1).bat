@echo off
title Crear ejecutable - Transporte Esquina Noroeste
cd /d "%~dp0"

set SCRIPT=EsquinaNoroesteCorregido.py
set NOMBRE=TransporteEsquinaNoroeste

if not exist "%SCRIPT%" (
    echo No se encontro %SCRIPT% en esta carpeta.
    echo Colocalo junto a este archivo .bat y vuelve a intentarlo.
    pause
    exit /b 1
)

python --version >nul 2>&1
if errorlevel 1 (
    echo Python no esta instalado o no esta en el PATH.
    echo Descargalo de https://www.python.org/downloads/ y marca "Add python.exe to PATH" al instalar.
    pause
    exit /b 1
)

echo Instalando PyInstaller...
python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo No se pudo instalar PyInstaller.
    pause
    exit /b 1
)

echo Creando el ejecutable...
python -m PyInstaller --onefile --windowed --clean --name "%NOMBRE%" "%SCRIPT%"
if errorlevel 1 (
    echo Ocurrio un error al crear el ejecutable.
    pause
    exit /b 1
)

echo.
echo Listo. Tu programa esta en la carpeta: dist\%NOMBRE%.exe
echo Puedes copiar ese .exe a cualquier computadora con Windows y funcionara sin Python.
pause
