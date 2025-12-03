# Guía de Construcción del APK para Android

Esta guía te explica paso a paso cómo convertir la aplicación Flet en un APK de Android.

## Requisitos Previos

### 1. Python 3.8 o superior
Verifica tu versión:
```bash
python --version
```

Ya tienes Python 3.13.9 instalado ✅

###  2. Instalar Flet
```bash
pip install flet
```

### 3. Instalar Dependencias del Proyecto
Navega a la carpeta del proyecto y ejecuta:
```bash
cd warehouse_flet_app
pip install -r requirements.txt
```

## Pasos para Construir el APK

### Método 1: Construcción Automática con Flet Build

**Paso 1: Probar la aplicación localmente**

Antes de construir el APK, prueba que la aplicación funcione:

```bash
cd warehouse_flet_app
flet run main.py
```

Esto abrirá la aplicación en una ventana. Verifica que todo funcione correctamente.

**Paso 2: Construir el APK**

Ejecuta el siguiente comando en la carpeta `warehouse_flet_app`:

```bash
flet build apk
```

**Opciones adicionales (opcional):**
```bash
flet build apk --build-number 1 --build-version 1.0.0 --verbose
```

- `--build-number`: Número de compilación (incrementar en cada nueva versión)
- `--build-version`: Versión visible para usuarios (ej: 1.0.0, 1.1.0)
- `--verbose`: Muestra más detalles durante la construcción

**Paso 3: Ubicación del APK**

El APK se generará en:
```
warehouse_flet_app/build/apk/app-release.apk
```

### Método 2: Usando el Script Incluido

También puedes usar el script `build_apk.bat` incluido:

```bash
cd warehouse_flet_app
build_apk.bat
```

Esto ejecutará automáticamente `flet build apk` y mostrará la ubicación del APK generado.

## Instalar el APK en tu Dispositivo Android

### Opción A: Transferencia por USB (ADB)

**Requisitos:**
- Habilitar "Modo Desarrollador" en tu Android
- Habilitar "Depuración USB"
- Instalar ADB (Android Debug Bridge)

**Pasos:**
1. Conecta tu dispositivo Android por USB
2. Ejecuta:
   ```bash
   adb devices
   ```
   Verifica que tu dispositivo aparezca en la lista

3 Instala el APK:
   ```bash
   adb install build/apk/app-release.apk
   ```

### Opción B: Transferencia Manual

1. Copia el archivo `app-release.apk` a tu dispositivo Android
   - Puedes usar cable USB y copiarlo a la carpeta Downloads
   - O enviarlo por correo/WhatsApp/Google Drive

2. En tu dispositivo Android:
   - Abre el gestor de archivos
   - Navega a Downloads (o donde lo hayas guardado)
   - Toca el archivo `app-release.apk`
   - Si aparece advertencia de "Fuentes desconocidas", ve a Configuración y habilita la instalación desde esa fuente
   - Confirma la instalación

3. La aplicación aparecerá en el cajón de aplicaciones

## Solución de Problemas Comunes

### Error: "flet: command not found"
**Solución:** Instala Flet:
```bash
pip install flet
```

### Error durante la construcción relacionado con Java/Android SDK
**Problema:** Flet build necesita herramientas de Android

**Solución 1 (Recomendada):** Usar Flet Cloud Build
Flet puede construir el APK en la nube sin necesidad de instalar Android SDK:
```bash
flet build apk --use-flet-build-server
```

**Solución 2:** Instalar Android SDK localmente
1. Descarga Android Studio desde: https://developer.android.com/studio
2. Instala Android SDK a través de Android Studio
3. Agrega Android SDK al PATH del sistema

### El APK se construye pero no se instala en el dispositivo
**Solución:**
- Verifica que hayas habilitado "Instalar apps desconocidas" en Android
- Asegúrate de que el archivo APK no esté corrupto (debería tener varios MB de tamaño)

### La aplicación se cierra inmediatamente al abrirla
**Solución:**
- Verifica que el archivo `ProductoTerminado.json` (credenciales de Google) esté en la carpeta correcta
- Usa `flet build apk --verbose` para ver logs detallados
- Prueba primero con `flet run main.py` en tu computadora para detectar errores

## Archivos Necesarios

Para que el APK funcione correctamente, asegúrate de que estos archivos estén en la carpeta del proyecto:

### Obligatorios:
- ✅ `main.py` - Aplicación principal
- ✅ `requirements.txt` - Dependencias
- ✅ Carpeta `core/` con módulos
- ✅ Carpeta `utils/` con utilidades

### Opcionales pero Recomendados:
- `ProductoTerminado.json` - Credenciales de Google Sheets
- Carpeta `assets/` con logo.png (ícono de la app)

## Personalizar el Ícono y Nombre de la App

### Cambiar Ícono
1. Coloca tu ícono como `assets/logo.png` (recomendado 512x512 px)
2. Construye con:
   ```bash
   flet build apk --icon assets/logo.png
   ```

### Cambiar Nombre
Edita `main.py` y cambia:
```python
self.page.title = "Tu Nombre de App"
```

## Actualizar la Aplicación

Cuando hagas cambios:
1. Incrementa `--build-number` en cada nueva versión
2. Reconstruye el APK:
   ```bash
   flet build apk --build-number 2
   ```
3. Desinstala la versión anterior del dispositivo
4. Instala la nueva versión

## Optimizaciones para el APK

### Reducir Tamaño del APK
El APK puede ser grande debido a las dependencias. Para reducir:
1. Remove dependencias no utilizadas de `requirements.txt`
2. Usa compresión al construir:
   ```bash
   flet build apk --optimize
   ```

### Firmar el APK (Para Google Play Store)
Si quieres publicar en Google Play, necesitas firmar el APK:
```bash
flet build apk --android-signing-key-store my-release-key.jks
```

## Contacto y Soporte

Si encuentras problemas:
1. Revisa los logs: `flet build apk --verbose`
2. Consulta la documentación oficial de Flet: https://flet.dev/docs/guides/python/packaging-app-for-distribution
3. Verifica que todas las dependencias estén instaladas correctamente

---

¡Listo! Con estos pasos deberías poder generar e instalar tu APK de Android. 🎉
