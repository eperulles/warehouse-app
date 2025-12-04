"""
Aplicación SIMPLIFICADA - Sistema de gestión de almacén en Flet.
"""

import flet as ft
import os
import sys
from pathlib import Path

# Fix imports for Flet APK packaging
if hasattr(sys, '_MEIPASS'):
    sys.path.insert(0, sys._MEIPASS)
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock wsgiref for Android
try:
    import wsgiref
except ImportError:
    from unittest.mock import MagicMock
    import types
    wsgiref_mock = types.ModuleType('wsgiref')
    wsgiref_mock.simple_server = MagicMock()
    wsgiref_mock.util = MagicMock()
    wsgiref_mock.headers = MagicMock()
    sys.modules["wsgiref"] = wsgiref_mock
    sys.modules["wsgiref.simple_server"] = wsgiref_mock.simple_server
    sys.modules["wsgiref.util"] = wsgiref_mock.util
    sys.modules["wsgiref.headers"] = wsgiref_mock.headers

def main(page: ft.Page):
    page.title = "Warehouse Manager"
    page.padding = 20
    
    # Log area
    log = ft.ListView(expand=True, spacing=5, padding=10)
    
    def add_log(message: str):
        log.controls.append(ft.Text(message, size=12))
        page.update()
    
    def show_alert(title: str, message: str):
        def close_dlg(e):
            dlg.open = False
            page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_dlg)],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    # URL field
    url_field = ft.TextField(
        label="URL de Google Sheets",
        multiline=False,
        expand=True
    )
    
    def cargar_todo(e):
        add_log("🔘 Botón presionado")
        
        try:
            url = url_field.value
            add_log(f"📝 URL: {url[:50] if url else 'VACÍA'}")
            
            if not url:
                show_alert("Error", "❌ Por favor pega una URL")
                add_log("❌ URL vacía")
                return
            
            add_log("📡 Intentando cargar Google Sheets...")
            show_alert("Cargando", "🔄 Conectando a Google Sheets...")
            
            # Intentar importar sheets_manager
            try:
                from core.sheets_manager import SheetsManager
                add_log("✅ SheetsManager importado")
                
                sheets = SheetsManager()
                add_log(f"✅ SheetsManager creado. Cliente: {sheets.client is not None}")
                
                if not sheets.client:
                    show_alert("Sin Credenciales", "❌ ProductoTerminado.json no encontrado")
                    add_log("❌ Sin credenciales")
                    return
                
                sheet_id = sheets.extract_sheet_id(url)
                add_log(f"📋 Sheet ID: {sheet_id[:20] if sheet_id else 'INVÁLIDO'}")
                
                if not sheet_id:
                    show_alert("Error", "❌ URL inválida")
                    add_log("❌ URL inválida")
                    return
                
                add_log("🔄 Cargando datos...")
                df, header_row, sheet = sheets.load_shipment_data(sheet_id)
                
                if df is not None:
                    show_alert("Éxito", f"✅ {len(df)} camiones cargados")
                    add_log(f"✅ {len(df)} camiones cargados")
                else:
                    show_alert("Error", "❌ Error cargando datos")
                    add_log("❌ Error cargando datos")
                    
            except Exception as e:
                error_msg = str(e)
                show_alert("Error", f"❌ {error_msg}")
                add_log(f"❌ Error: {error_msg}")
                
        except Exception as e:
            error_msg = str(e)
            show_alert("Error Fatal", f"❌ {error_msg}")
            add_log(f"❌ Error fatal: {error_msg}")
    
    # Botón principal
    btn_cargar = ft.ElevatedButton(
        "CARGAR TODO",
        icon=ft.icons.DOWNLOAD,
        on_click=cargar_todo,
        expand=True
    )
    
    # Layout
    page.add(
        ft.Column([
            ft.Text("🗂️ Warehouse Manager", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([url_field]),
            ft.Row([btn_cargar]),
            ft.Divider(),
            ft.Text("📋 Log:", size=16),
            ft.Container(
                content=log,
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=5,
                padding=10,
                expand=True
            )
        ], expand=True)
    )
    
    add_log("✅ App iniciada")
    add_log("👉 Pega tu URL y presiona CARGAR TODO")

if __name__ == "__main__":
    ft.app(target=main)
