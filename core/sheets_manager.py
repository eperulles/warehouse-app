"""
Módulo de integración con Google Sheets.

Maneja la conexión y operaciones con Google Sheets para el sistema de warehouse.
Adaptado del código original de Streamlit para Flet.
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import time
from typing import Tuple, Optional


SCOPE = ['https://www.googleapis.com/auth/spreadsheets']


class SheetsManager:
    """Gestor de Google Sheets para el sistema de warehouse."""
    
    def __init__(self, credentials_file: str = 'ProductoTerminado.json'):
        """
        Inicializa el gestor de Google Sheets.
        
        Args:
            credentials_file: Ruta al archivo JSON de credenciales de Google
        """
        self.credentials_file = credentials_file
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente de Google Sheets."""
        try:
            import os
            if not os.path.exists(self.credentials_file):
                print(f"⚠️ Archivo de credenciales no encontrado: {self.credentials_file}")
                print("   Google Sheets no estará disponible.")
                self.client = None
                return
                
            creds = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=SCOPE
            )
            self.client = gspread.authorize(creds)
            print("✅ Cliente de Google Sheets inicializado")
        except Exception as e:
            print(f"❌ Error inicializando Google Sheets: {e}")
            self.client = None
    
    def load_shipment_data(
        self, 
        sheet_id: str
    ) -> Tuple[Optional[pd.DataFrame], Optional[int], Optional[any]]:
        """
        Carga los datos del shipment desde Google Sheets.
        
        Args:
            sheet_id: ID de la hoja de Google Sheets
        
        Returns:
            Tuple (DataFrame con datos, número de fila del header, objeto sheet)
        """
        if not self.client:
            print("❌ Cliente no inicializado")
            return None, None, None
        
        try:
            start_time = time.time()
            
            spreadsheet = self.client.open_by_key(sheet_id)
            sheet = spreadsheet.get_worksheet(0)
            
            # Obtener todos los valores
            all_values = sheet.get_all_values()
            
            # Buscar fila del header
            header_row = None
            for idx, row in enumerate(all_values):
                if 'CAMION' in [cell.upper() for cell in row]:
                    header_row = idx
                    break
            
            if header_row is None:
                print("❌ No se encontró fila de header")
                return None, None, None
            
# Crear DataFrame
            headers = all_values[header_row]
            data = all_values[header_row + 1:]
            
            df = pd.DataFrame(data, columns=headers)
            
            # Limpiar datos vacíos
            df = df[df['CAMION'].str.strip() != '']
            
            load_time = time.time() - start_time
            print(f"✅ Datos cargados en {load_time:.1f}s - {len(df)} filas")
            
            return df, header_row, sheet
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return None, None, None
    
    def update_truck_status(
        self, 
        sheet: any, 
        truck_id: str, 
        status: str,
        header_row: int,
        status_column: int = 19
    ) -> bool:
        """
        Actualiza el estatus de un camión en Google Sheets.
        
        Args:
            sheet: Objeto de la hoja de Google Sheets
            truck_id: ID del camión a actualizar
            status: Nuevo estatus (ej: "Listo", "Entregado")
            header_row: Número de fila del header
            status_column: Número de columna del estatus (default: 19)
        
        Returns:
            True si se actualizó exitosamente
        """
        try:
            # Buscar la celda del camión
            truck_cells = sheet.findall(str(truck_id))
            
            for cell in truck_cells:
                if cell.row > header_row:
                    sheet.update_cell(cell.row, status_column, status)
                    print(f"✅ Camión {truck_id} actualizado a '{status}'")
                    return True
            
            print(f"⚠️ Camión {truck_id} no encontrado en la hoja")
            return False
            
        except Exception as e:
            print(f"❌ Error actualizando estatus: {e}")
            return False
    
    def extract_sheet_id(self, url: str) -> Optional[str]:
        """
        Extrae el ID de la hoja desde una URL de Google Sheets.
        
        Args:
            url: URL de Google Sheets
        
        Returns:
            ID de la hoja o None si no se puede extraer
        """
        import re
        
        patterns = [
            r'/spreadsheets/d/([a-zA-Z0-9-_]+)',
            r'id=([a-zA-Z0-9-_]+)',
            r'/d/([a-zA-Z0-9-_]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Si no coincide con ningún patrón pero es un ID largo, asumir que es el ID
        if len(url) > 30 and '/' not in url:
            return url
        
        return None
