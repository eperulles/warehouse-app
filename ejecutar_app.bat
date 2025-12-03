@echo off
echo ========================================
echo   Ejecutando Aplicación Warehouse
echo ========================================
echo.
echo La ventana de la aplicación se abrirá en unos segundos...
echo.

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ERROR: No se encontró main.py
    echo Ejecuta este script desde la carpeta warehouse_flet_app
    pause
    exit /b 1
)

echo Iniciando aplicación Flet...
echo.

flet run main.py

if errorlevel 1 (
    echo.
    echo ERROR: La aplicación no pudo iniciarse
    echo.
    echo Verifica que Flet esté instalado:
    echo   pip install flet
    echo.
    pause
)
