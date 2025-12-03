# 🚀 GUÍA RÁPIDA: Cómo Construir tu APK

**Sigue estos 3 simples pasos para convertir la aplicación a APK de Android:**

---

## ✅ PASO 1: Abrir PowerShell en la Carpeta del Proyecto

1. Abre el Explorador de Archivos de Windows
2. Navega a: `c:\Users\Administrator\Desktop\codigosappflet\codigos app flet\warehouse_flet_app`
3. En la barra de direcciones, escribe `powershell` y presiona Enter

![PowerShell se abrirá en esa carpeta]

---

## ✅ PASO 2: Instalar Dependencias

Copia y pega este comando en PowerShell:

```powershell
.\setup.bat
```

Presiona Enter y espera. Verás algo como:
```
========================================
 Instalación - Warehouse Flet App
========================================

[1/3] Verificando Python...
Python 3.13.9

[2/3] Instalando Flet...
...

[3/3] Instalando dependencias...
...

✅ Instalación completada!
```

**Presiona cualquier tecla para continuar cuando termine.**

---

## ✅ PASO 3: Construir el APK

Ahora ejecuta este comando:

```powershell
.\build_apk.bat
```

Verás el progreso:
```
========================================
 Construcción de APK - Warehouse App
========================================

[1/4] Verificando instalación de Flet...
[2/4] Instalando dependencias...
[3/4] Construyendo APK...
Esto puede tomar varios minutos...
```

**⏳ IMPORTANTE:** La construcción puede tomar entre 5-15 minutos. Sé paciente.

### Si Aparece un Error de Android SDK:

No te preocupes, usa este comando alternativo:

```powershell
flet build apk --use-flet-build-server
```

Esto construirá el APK en la nube (no necesita Android SDK en tu computadora).

---

## ✅ RESULTADO: Tu APK está Listo!

Cuando termine, verás:
```
========================================
✅ APK construido exitosamente!
========================================

El APK se encuentra en:
  build\apk\app-release.apk
```

**La ruta completa es:**
```
c:\Users\Administrator\Desktop\codigosappflet\codigos app flet\warehouse_flet_app\build\apk\app-release.apk
```

---

## 📱 INSTALAR EN TU CELULAR ANDROID

### Método 1: Transferencia Manual (Más Fácil)

1. **Copia el APK:**
   - Navega a la carpeta `warehouse_flet_app\build\apk\`
   - Copia el archivo `app-release.apk`

2. **Pasa el APK a tu celular:**
   - Conecta tu celular por USB y cópialo a la carpeta Downloads
   - O envíalo por WhatsApp a ti mismo
   - O súbelo a Google Drive y descárgalo

3. **Instala en el celular:**
   - Abre el archivo `app-release.apk` desde el gestor de archivos
   - Si aparece "Instalar apps desconocidas", toca "Configuración" y habilita la opción
   - Toca "Instalar"
   - ¡Listo! La app aparecerá en tu cajón de aplicaciones

### Método 2: Por ADB (Avanzado)

Si tienes ADB instalado:

```bash
adb install build\apk\app-release.apk
```

---

## 🎯 PROBAR ANTES DE CONSTRUIR EL APK

Si quieres probar la aplicación en tu computadora primero:

```powershell
flet run main.py
```

Esto abrirá la aplicación en una ventana para que la pruebes.

---

## ❓ PROBLEMAS COMUNES

### "flet: command not found"
**Solución:** Ejecuta `.\setup.bat` primero

### El APK se construye pero no se instala
**Solución:** En Android, ve a Configuración → Seguridad → Habilitar "Instalar apps de fuentes desconocidas"

### Error durante construcción
**Solución:** Usa el servidor de Flet en la nube:
```powershell
flet build apk --use-flet-build-server
```

---

## 📞 ¿NECESITAS MÁS AYUDA?

- Lee `BUILD.md` para instrucciones detalladas
- Lee `README.md` para características y uso
- Lee `walkthrough.md` para detalles técnicos completos

---

**¡Eso es todo! Con estos 3 pasos tendrás tu APK listo para instalar. 🎉**
