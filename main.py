"""
App Warehouse - Versión Funcional
"""
import flet as ft

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
            add_log(f"📝 URL recibida")
            
            if not url:
                show_alert("Error", "Por favor pega una URL")
                add_log("❌ URL vacía")
                return
            
            add_log("📦 Importando módulos...")
            
            # Importar SOLO cuando se necesite
            try:
                import sys
                import os
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                
                from core.sheets_manager import SheetsManager
                add_log("✅ SheetsManager importado")
            except Exception as import_err:
                show_alert("Error de Importación", f"No se pudo importar: {str(import_err)}")
                add_log(f"❌ Error importando: {str(import_err)}")
                return
            
            add_log("🔧 Creando SheetsManager...")
            sheets = SheetsManager()
            add_log(f"✅ SheetsManager creado")
            
            if not sheets.client:
                show_alert("Sin Credenciales", "ProductoTerminado.json no encontrado")
                add_log("❌ Sin credenciales")
                return
            
            add_log("🔍 Extrayendo Sheet ID...")
            sheet_id = sheets.extract_sheet_id(url)
            
            if not sheet_id:
                show_alert("Error", "URL inválida")
                add_log("❌ URL inválida")
                return
            
            add_log(f"✅ Sheet ID: {sheet_id[:20]}...")
            add_log("📡 Cargando datos de Google Sheets...")
            
            df, header_row, sheet = sheets.load_shipment_data(sheet_id)
            
            if df is not None:
                show_alert("Éxito", f"✅ {len(df)} camiones cargados")
                add_log(f"✅ {len(df)} camiones cargados correctamente")
            else:
                show_alert("Error", "Error cargando datos")
                add_log("❌ Error cargando datos")
                
        except Exception as e:
            error_msg = str(e)
            show_alert("Error", f"❌ {error_msg}")
            add_log(f"❌ Error: {error_msg}")
    
    # Botón principal
    btn_cargar = ft.ElevatedButton(
        "📥 CARGAR TODO",
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
                border=ft.border.all(1, "grey"),
                border_radius=5,
                padding=10,
                expand=True
            )
        ], expand=True)
    )
    
    add_log("✅ App iniciada correctamente")
    add_log("👉 Pega tu URL de Google Sheets y presiona CARGAR TODO")

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
