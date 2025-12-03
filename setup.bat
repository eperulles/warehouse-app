@echo off
REM Script de instalación inicial para el proyecto

echo ========================================
echo  Instalación - Warehouse Flet App
echo ========================================
echo.

echo [1/3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [2/3] Instalando Flet...
pip install flet

echo.
echo [3/3] Instalando dependencias del proyecto...
pip install -r requirements.txt

echo.
echo ========================================
echo ✅ Instalación completada!
echo ========================================
echo.
echo Comandos disponibles:
echo   - Ejecutar aplicación:   flet run main.py
echo   - Construir APK:         build_apk.bat
echo   - Ver guía completa:     type BUILD.md
echo.

pause
