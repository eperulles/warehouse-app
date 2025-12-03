"""
Versión TEST MÍNIMA para verificar build APK
"""

import flet as ft


def main(page: ft.Page):
    page.title = "Warehouse Test"
    page.add(
        ft.Text("App funcionando ✅", size=30)
    )


if __name__ == "__main__":
    ft.app(target=main)
