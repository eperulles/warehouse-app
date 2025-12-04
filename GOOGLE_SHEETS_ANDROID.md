# Configuración de Google Sheets para Android

## El Problema
El APK genera automáticamente **NO incluye** el archivo `ProductoTerminado.json` por seguridad (tiene credenciales privadas).

## Solución Temporal
La app funciona SIN Google Sheets. Puedes:
1. Cargar el layout manualmente (txt o SVG)
2. Cargar el packing list desde Excel local

## Solución Permanente (Si necesitas Google Sheets)

### Opción 1: Incluir credenciales en el build
1. Sube `ProductoTerminado.json` a GitHub (en carpeta principal del proyecto)
2. Actualiza `.gitignore` para PERMITIR este archivo (quita la línea que lo excluye)
3. GitHub Actions generará APK con credenciales incluidas

⚠️ **CUIDADO**: Esto expone tus credenciales públicamente si el repo es público.

### Opción 2: Cargar dinámicamente (Más seguro)
Modificar la app para que el usuario pueda subir el archivo de credenciales desde el celular.

---

**Próximos pasos recomendados:**
- Si NO necesitas Google Sheets: App ya funciona, solo usa archivos locales
- Si SÍ necesitas Google Sheets: Implementa Opción 2 o acepta riesgo de Opción 1
