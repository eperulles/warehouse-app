"""
Aplicación principal del sistema de gestión de almacén en Flet.

Esta es una aplicación móvil/desktop para escaneo de pallets con asignación
mejorada de camiones físicos y visualización interactiva del layout.
"""

import flet as ft
import pandas as pd
import os
import sys
from pathlib import Path

# Fix imports for Flet APK packaging
if hasattr(sys, '_MEIPASS'):
    # Running as packaged app
    sys.path.insert(0, sys._MEIPASS)
else:
    # Running from source
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos core
from core.db_manager import DatabaseManager
from core.truck_assignment import (
    get_layout_trucks_from_locations,
    assign_packing_truck_to_layout,
    get_layout_truck_statistics
)
from core.pallet_ordering import (
    get_pallet_sequence_index,
    calculate_location_from_index,
    validate_pallet_can_scan
)
from core.sheets_manager import SheetsManager
from utils.svg_parser import parse_svg_xml, create_simple_layout_from_text


class WarehouseApp:
    """Aplicación principal de gestión de almacén."""
    
    def __init__(self, page: ft.Page):
        """
        Inicializa la aplicación.
        
        Args:
            page: Página principal de Flet
        """
        self.page = page
        self.page.title = "Sistema de Almacén"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        
        # Inicializar gestores
        self.db = DatabaseManager()
        self.sheets = SheetsManager()
        
        # Estado de la aplicación
        self.layout_locations = []
        self.layout_shapes = []
        self.layout_trucks = []
        self.shipment_df = None
        self.packing_df = None
        self.pallet_summary = None
        self.sheet = None
        self.header_row = None
        self.selected_truck = None
        self.current_layout_truck = None
        
        # Referencias a controles de UI
        self.main_content = ft.Column()
        self.status_bar = ft.Text("Listo", size=14)
        
        # Configurar página
        self.setup_page()
    
    def setup_page(self):
        """Configura la página inicial."""
        # Barra de estado superior
        status_container = ft.Container(
            content=self.status_bar,
            padding=10,
            bgcolor="#E3F2FD",
            border_radius=5
        )
        
        # Contenido principal
        self.main_content = ft.Column(
            controls=[
                ft.Text("🗺️ Sistema de Layout y Escaneo", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
        
        # Botones de navegación
        nav_buttons = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "📋 Configuración",
                    on_click=lambda _: self.show_config_view()
                ),
                ft.ElevatedButton(
                    "📦 Escaneo",
                    on_click=lambda _: self.show_scan_view(),
                    disabled=True  # Habilitado cuando hay datos cargados
                ),
                ft.ElevatedButton(
                    "🗺️ Layout",
                    on_click=lambda _: self.show_layout_view(),
                    disabled=True
                ),
                ft.ElevatedButton(
                    "🚚 Entregas",
                    on_click=lambda _: self.show_delivery_view(),
                    disabled=True
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        
        # Layout principal
        self.page.add(
            ft.Column(
                controls=[
                    status_container,
                    nav_buttons,
                    ft.Divider(),
                    self.main_content
                ],
                expand=True
            )
        )
        
        # Mostrar vista de configuración por defecto
        self.show_config_view()
    
    def update_status(self, message: str, color: str = None):
        """
        Actualiza la barra de estado.
        
        Args:
            message: Mensaje a mostrar
            color: Color de fondo opcional
        """
        self.status_bar.value = message
        if color:
            self.status_bar.color = color
        self.page.update()
    
    def show_config_view(self):
        """Muestra la vista de configuración."""
        self.update_status("📋 Configuración del sistema")
        
        # Campo para URL de Google Sheets
        sheet_url_field = ft.TextField(
            label="URL de Google Sheets",
            hint_text="Pega aquí la URL de tu Google Sheet",
            width=500
        )
        
        load_sheets_btn = ft.ElevatedButton(
            "Cargar Datos",
            on_click=lambda e: self.load_google_sheets(sheet_url_field.value)
        )
        
        # Selector de archivo SVG
        svg_file_picker = ft.FilePicker(
            on_result=lambda e: self.load_svg_file(e)
        )
        self.page.overlay.append(svg_file_picker)
        
        load_svg_btn = ft.ElevatedButton(
            "Cargar Layout SVG/XML",
            on_click=lambda _: svg_file_picker.pick_files(
                allowed_extensions=['svg', 'xml']
            )
        )
        
        # Campo de texto para layout manual
        layout_text_field = ft.TextField(
            label="O pega ubicaciones manualmente (C1-1, C1-2, ...)",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=500
        )
        
        load_text_btn = ft.ElevatedButton(
            "Cargar Layout desde Texto",
            on_click=lambda _: self.load_layout_from_text(layout_text_field.value)
        )
        
        # Selector de archivo Excel (Packing List)
        packing_file_picker = ft.FilePicker(
            on_result=lambda e: self.load_packing_list(e)
        )
        self.page.overlay.append(packing_file_picker)
        
        load_packing_btn = ft.ElevatedButton(
            "Cargar Packing List (Excel)",
            # icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: packing_file_picker.pick_files(
                allowed_extensions=['xlsx', 'xls']
            )
        )
        
        # Información del estado actual
        info_text = ft.Text("", size=12, color="#1976D2")
        
        # Actualizar información
        def update_info():
            info_parts = []
            if self.layout_locations:
                info_parts.append(f"📍 {len(self.layout_locations)} ubicaciones cargadas")
            if self.layout_trucks:
                trucks_str = ', '.join([f'C{t}' for t in self.layout_trucks])
                info_parts.append(f"🚛 Camiones en layout: {trucks_str}")
            if self.shipment_df is not None:
                info_parts.append(f"📋 {len(self.shipment_df)} camiones en shipment")
            if self.packing_df is not None:
                info_parts.append(f"📦 Packing list cargado")
            
            info_text.value = '\n'.join(info_parts) if info_parts else "⚠️ No hay datos cargados"
            self.page.update()
        
        # Actualizar info inicial
        update_info()
        
        # Construir vista
        self.main_content.controls = [
            ft.Text("📋 Configuración del Sistema", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Text("1. Cargar Datos de Google Sheets", size=16, weight=ft.FontWeight.BOLD),
            sheet_url_field,
            load_sheets_btn,
            ft.Divider(),
            
            ft.Text("2. Cargar Layout del Almacén", size=16, weight=ft.FontWeight.BOLD),
            load_svg_btn,
            ft.Text("O", text_align=ft.TextAlign.CENTER),
            layout_text_field,
            load_text_btn,
            ft.Divider(),
            
            ft.Text("3. Cargar Packing List", size=16, weight=ft.FontWeight.BOLD),
            load_packing_btn,
            ft.Divider(),
            
            ft.Container(
                content=info_text,
                padding=10,
                bgcolor="#E3F2FD",
                border_radius=5
            )
        ]
        
        self.page.update()
    
    def load_google_sheets(self, url: str):
        """Carga datos desde Google Sheets."""
        if not url:
            self.update_status("❌ Ingresa una URL", "red")
            return
        
        self.update_status("🔄 Cargando datos de Google Sheets...", ft.colors.ORANGE)
        
        try:
            sheet_id = self.sheets.extract_sheet_id(url)
            if not sheet_id:
                self.update_status("❌ URL inválida", ft.colors.RED)
                return
            
            df, header_row, sheet = self.sheets.load_shipment_data(sheet_id)
            
            if df is not None:
                self.shipment_df = df
                self.header_row = header_row
                self.sheet = sheet
                self.update_status(f"✅ Datos cargados: {len(df)} camiones", ft.colors.GREEN)
                self.show_config_view()  # Refresh para mostrar info actualizada
            else:
                self.update_status("❌ Error cargando datos", ft.colors.RED)
        
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", ft.colors.RED)
    
    def load_svg_file(self, e: ft.FilePickerResultEvent):
        """Carga un archivo SVG/XML."""
        if not e.files:
            return
        
        self.update_status("🔄 Cargando layout SVG...", ft.colors.ORANGE)
        
        try:
            file_path = e.files[0].path
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            locations, shapes = parse_svg_xml(xml_content)
            
            if locations:
                self.layout_locations = locations
                self.layout_shapes = shapes
                self.layout_trucks = get_layout_trucks_from_locations(locations)
                self.update_status(f"✅ Layout cargado: {len(locations)} ubicaciones", ft.colors.GREEN)
                self.show_config_view()  # Refresh
            else:
                self.update_status("❌ No se encontraron ubicaciones en el SVG", ft.colors.RED)
        
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", ft.colors.RED)
    
    def load_layout_from_text(self, text: str):
        """Carga layout desde texto."""
        if not text.strip():
            self.update_status("❌ Ingresa ubicaciones", ft.colors.RED)
            return
        
        self.update_status("🔄 Procesando layout...", ft.colors.ORANGE)
        
        try:
            locations, shapes = create_simple_layout_from_text(text)
            
            if locations:
                self.layout_locations = locations
                self.layout_shapes = shapes
                self.layout_trucks = get_layout_trucks_from_locations(locations)
                self.update_status(f"✅ Layout cargado: {len(locations)} ubicaciones", ft.colors.GREEN)
                self.show_config_view()  # Refresh
            else:
                self.update_status("❌ No se encontraron ubicaciones válidas", ft.colors.RED)
        
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", ft.colors.RED)
    
    def load_packing_list(self, e: ft.FilePickerResultEvent):
        """Carga el packing list desde Excel."""
        if not e.files:
            return
        
        self.update_status("🔄 Cargando packing list...", ft.colors.ORANGE)
        
        try:
            file_path = e.files[0].path
            
            # Leer Excel y procesar similar al código original
            df = pd.read_excel(file_path)
            
            # Crear summary de pallets
            pallet_data = []
            for _, row in df.iterrows():
                if pd.notna(row.get('Pallet number')):
                    pallet_data.append({
                        'Pallet number': row.get('Pallet number'),
                        'first_serial': row.get('Serial Number From', ''),
                        'last_serial': row.get('Serial Number To', ''),
                        'box_count': row.get('Box', 0)
                    })
            
            self.packing_df = df
            self.pallet_summary = pd.DataFrame(pallet_data)
            
            self.update_status(f"✅ Packing list cargado: {len(pallet_data)} pallets", ft.colors.GREEN)
            self.show_config_view()  # Refresh
        
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", ft.colors.RED)
    
    def show_scan_view(self):
        """Muestra la vista de escaneo (placeholder por ahora)."""
        self.update_status("📦 Vista de escaneo")
        self.main_content.controls = [
            ft.Text("📦 Vista de Escaneo", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("En construcción... Esta sección permitirá escanear pallets."),
        ]
        self.page.update()
    
    def show_layout_view(self):
        """Muestra la vista del layout (placeholder)."""
        self.update_status("🗺️ Vista del layout")
        self.main_content.controls = [
            ft.Text("🗺️ Vista del Layout", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("En construcción... Esta sección mostrará el layout interactivo."),
        ]
        self.page.update()
    
    def show_delivery_view(self):
        """Muestra la vista de entregas (placeholder)."""
        self.update_status("🚚 Vista de entregas")
        self.main_content.controls = [
            ft.Text("🚚 Vista de Entregas", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("En construcción... Esta sección permitirá dar de baja camiones."),
        ]
        self.page.update()


def main(page: ft.Page):
    """Función principal de la aplicación Flet."""
    app = WarehouseApp(page)


if __name__ == "__main__":
    # Ejecutar aplicación
    ft.app(target=main)
