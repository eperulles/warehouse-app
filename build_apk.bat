@echo off
REM Script para construir el APK de la aplicación de almacén

echo ========================================
echo  Construcción de APK - Warehouse App
echo ========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ERROR: No se encontró main.py
    echo Asegúrate de ejecutar este script desde la carpeta warehouse_flet_app
    pause
    exit /b 1
)

echo [1/3] Verificando instalación de Flet...
python -c "import flet" 2>nul
if errorlevel 1 (
    echo ERROR: Flet no está instalado
    echo Instalando Flet...
    pip install flet
)

echo [2/3] Instalando dependencias...
pip install -r requirements.txt

echo [3/3] Construyendo APK...
echo Esto puede tomar varios minutos (5-15 min aprox)...
echo.

REM Intentar build simple primero
flet build apk

if errorlevel 1 (
    echo.
    echo ========================================
    echo ⚠️ Build local falló, intentando con Flet Cloud Build...
    echo ========================================
    echo.
    
    flet build apk --use-flet-build-server
    
    if errorlevel 1 (
        echo.
        echo ========================================
        echo ERROR: La construcción del APK falló
        echo ========================================
        echo.
        echo Intenta manualmente:
        echo   flet build apk
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo ✅ APK construido exitosamente!
echo ========================================
echo.
echo El APK se encuentra en:
echo   build\apk\app-release.apk
echo.
echo Tamaño aproximado: 30-50 MB
echo.
echo Para instalar en tu dispositivo Android:
echo   1. Copia el APK a tu dispositivo
echo   2. Abre el archivo desde el gestor de archivos
echo   3. Permite la instalación de fuentes desconocidas
echo.
echo O usa ADB:
echo   adb install build\apk\app-release.apk
echo.

pause
