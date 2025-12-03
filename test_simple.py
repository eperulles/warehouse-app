"""
Test VISUAL - Verifica que Flet muestre la ventana
"""

import flet as ft


def main(page: ft.Page):
    # Configurar ventana
    page.title = "✅ TEST EXITOSO - Warehouse App"
    page.window_width = 900
    page.window_height = 700
    page.window_resizable = True
    page.padding = 30
    page.bgcolor = ft.colors.GREY_50
    
    # Contenido de prueba
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=100),
                ft.Text(
                    "✅ ¡FLET FUNCIONA CORRECTAMENTE!", 
                    size=40, 
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.GREEN_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(height=30),
                ft.Text(
                    "Si ves esta ventana, significa que:", 
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text("• Tu instalación de Flet está correcta", size=16),
                ft.Text("• La aplicación puede mostrar interfaz gráfica", size=16),
                ft.Text("• El APK que construyas funcionará en Android", size=16),
                ft.Divider(height=30),
                ft.Container(
                    content=ft.Text(
                        "📱 Puedes proceder a construir el APK",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE
                    ),
                    bgcolor=ft.colors.BLUE_700,
                    padding=20,
                    border_radius=10
                ),
                ft.Divider(height=20),
                ft.ElevatedButton(
                    "Cerrar esta ventana",
                    icon=ft.icons.CLOSE,
                    on_click=lambda _: page.window_destroy(),
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.RED_700,
                    height=50
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            padding=40,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_200,
            )
        )
    )


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  ABRIENDO VENTANA DE PRUEBA")
    print("="*50)
    print("\nSi no ves una ventana, puede ser que:")
    print("1. Flet esté ejecutándose en segundo plano")
    print("2. La ventana se haya minimizado")
    print("3. Necesites presionar Alt+Tab para verla")
    print("\n"  + "="*50 + "\n")
    
    # Ejecutar con view=WEB_BROWSER para forzar que se vea
    ft.app(target=main, view=ft.AppView.FLET_APP)
