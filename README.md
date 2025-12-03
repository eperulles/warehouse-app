# Sistema de Gestión de Almacén - Flet App

Aplicación móvil para escaneo de pallets y gestión de layout de almacén, con asignación mejorada de camiones físicos.

## 🚀 Inicio Rápido

### 1. Instalación

Ejecuta el script de instalación:
```bash
setup.bat
```

O instala manualmente:
```bash
pip install flet
pip install -r requirements.txt
```

### 2. Ejecutar en Modo Desarrollo

```bash
flet run main.py
```

### 3. Construir APK para Android

```bash
build_apk.bat
```

O manualmente:
```bash
flet build apk
```

**El APK se generará en:** `build/apk/app-release.apk`

## 📚 Documentación Completa

Para instrucciones detalladas de construcción del APK, ver [BUILD.md](BUILD.md)

## ✨ Características Principales

- **✅ Asignación Inteligente de Camiones**: Solo asigna a camiones completamente vacíos en el layout
- **✅ Orden Secuencial de Pallets**: Mantiene el orden correcto (pallet 1 → ubicación 1 slot 1, pallet 5 → ubicación 3 slot 1)
- **✅ Límite de 57 Ubicaciones**: Validación estricta del límite por camión
- **✅ Bloqueo Automático**: Previene escaneo de nuevos camiones cuando el layout está lleno
- **✅ Integración Google Sheets**: Sincronización con datos de shipment
- **✅ Carga de Layouts**: Soporta archivos SVG/XML o entrada manual de texto
- **✅ Base de Datos Persistente**: SQLite para almacenar todos los escaneos

## 📁 Estructura del Proyecto

```
warehouse_flet_app/
├── main.py                      # Aplicación principal
├── requirements.txt             # Dependencias Python
├── setup.bat                    # Script de instalación
├── build_apk.bat               # Script para construir APK
├── BUILD.md                     # Guía detallada de construcción
├── core/                        # Módulos principales
│   ├── truck_assignment.py      # Lógica de asignación
│   ├── pallet_ordering.py       # Ordenamiento de pallets
│   ├── db_manager.py            # Gestión de BD
│   └── sheets_manager.py        # Google Sheets
├── utils/                       # Utilidades
│   └── svg_parser.py            # Parser de SVG
└── assets/                      # Recursos (opcional)
    └── logo.png                 # Ícono de la app
```

## 🔧 Configuración

### Credenciales de Google Sheets

Para usar la integración con Google Sheets, coloca tu archivo de credenciales:
```
ProductoTerminado.json
```

En la raíz del proyecto (mismo nivel que `main.py`).

### Layout del Almacén

Carga tu layout de una de estas formas:
1. Archivo SVG/XML con ubicaciones etiquetadas como "C1-1", "C1-2", etc.
2. Texto manual con formato: "C1-1, C1-2, C1-3, C2-1, C2-2..."

## 📱 Instalación en Android

Una vez construido el APK:

**Método 1 - ADB:**
```bash
adb install build/apk/app-release.apk
```

**Método 2 - Manual:**
1. Copia `app-release.apk` a tu dispositivo
2. Abre desde el gestor de archivos
3. Permite instalación de fuentes desconocidas
4. Instala

## 🐛 Solución de Problemas

### La app no construye el APK
Prueba usando Flet Cloud Build:
```bash
flet build apk --use-flet-build-server
```

### Error de importación en Python
Reinstala las dependencias:
```bash
pip install -r requirements.txt --force-reinstall
```

### El APK se cierra al abrirlo
1. Verifica que `ProductoTerminado.json` esté presente
2. Prueba primero `flet run main.py` para detectar errores
3. Revisa los logs con `flet build apk --verbose`

## 📄 Licencia

Este proyecto es de uso interno para gestión de almacén.

## 📞 Soporte

Para asistencia técnica, consulta [BUILD.md](BUILD.md) o la documentación oficial de Flet en https://flet.dev
