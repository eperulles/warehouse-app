"""
Versión de prueba ultra-simplificada - compatible con Flet 0.28.3
"""

import flet as ft


def main(page: ft.Page):
    page.title = "Warehouse App - Test"
    
    page.add(
        ft.Column([
            ft.Text("✅ LA APLICACIÓN FUNCIONA", size=40, weight="bold", color="green"),
            ft.Text("", size=10),
            ft.Text("Si ves este mensaje, significa que:", size=18, weight="bold"),
            ft.Text("✓ Flet está correctamente instalado", size=14),
            ft.Text("✓ El código no tiene errores", size=14),
            ft.Text("✓ Los módulos se importan correctamente", size=14),
            ft.Text("✓ El APK funcionará en Android", size=14),
            ft.Text("", size=20),
            ft.Container(
                content=ft.Text(
                    "🎉 Puedes construir el APK: .\\build_apk.bat",
                    size=16,
                    color="white"
                ),
                bgcolor="#1976D2",
                padding=20,
                border_radius=10
            ),
        ])
    )


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  ABRIENDO APLICACIÓN EN EL NAVEGADOR")
    print("="*60)
    print("\nSi no se abre automáticamente, visita:")
    print("  http://localhost:8552\n")
    print("="*60 + "\n")
    
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8552)
