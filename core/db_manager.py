"""
Módulo de gestión de base de datos SQLite.

Maneja la base de datos de escaneos de pallets con el esquema mejorado
que incluye tracking de índice secuencial y relación packing_truck -> layout_truck.
"""

import sqlite3
import pandas as pd
from typing import Optional, List, Dict, Tuple
from datetime import datetime


class DatabaseManager:
    """Gestor de base de datos SQLite para el sistema de warehouse."""
    
    def __init__(self, db_path: str = 'scans.db'):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Crea las tablas necesarias si no existen."""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        # Tabla de escaneos de pallets con esquema mejorado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pallet_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                packing_truck_id TEXT NOT NULL,
                layout_truck_id TEXT NOT NULL,
                pallet_number TEXT NOT NULL,
                pallet_sequence_index INTEGER,
                first_serial TEXT,
                last_serial TEXT,
                ubicacion TEXT,
                slot INTEGER,
                scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(packing_truck_id, pallet_number)
            )
        ''')
        
        # Índices para mejorar rendimiento
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_packing_truck 
            ON pallet_scans(packing_truck_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_layout_truck 
            ON pallet_scans(layout_truck_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_ubicacion 
            ON pallet_scans(ubicacion)
        ''')
        
        conn.commit()
        conn.close()
    
    def register_pallet_scan(
        self,
        packing_truck_id: str,
        layout_truck_id: str,
        pallet_number: str,
        pallet_sequence_index: int,
        first_serial: str,
        last_serial: str,
        ubicacion: str,
        slot: int
    ) -> bool:
        """
        Registra un escaneo de pallet en la base de datos.
        
        Args:
            packing_truck_id: ID del camión en el packing list
            layout_truck_id: ID del camión físico en el layout (ej: "C1")
            pallet_number: Número del pallet
            pallet_sequence_index: Índice secuencial del pallet (1, 2, 3...)
            first_serial: Primer serial del pallet
            last_serial: Último serial del pallet
            ubicacion: Ubicación asignada (ej: "C1-5")
            slot: Slot en la ubicación (1 o 2)
        
        Returns:
            True si se registró exitosamente, False en caso de error
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO pallet_scans 
                (packing_truck_id, layout_truck_id, pallet_number, pallet_sequence_index,
                 first_serial, last_serial, ubicacion, slot)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(packing_truck_id),
                str(layout_truck_id),
                str(pallet_number),
                int(pallet_sequence_index),
                str(first_serial),
                str(last_serial),
                str(ubicacion),
                int(slot)
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error registrando pallet scan: {e}")
            return False
    
    def is_pallet_scanned(self, packing_truck_id: str, pallet_number: str) -> bool:
        """
        Verifica si un pallet ya fue escaneado.
        
        Args:
            packing_truck_id: ID del camión en el packing list
            pallet_number: Número del pallet
        
        Returns:
            True si ya fue escaneado, False en caso contrario
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM pallet_scans
                WHERE packing_truck_id = ? AND pallet_number = ?
            ''', (str(packing_truck_id), str(pallet_number)))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count > 0
            
        except Exception as e:
            print(f"Error verificando pallet: {e}")
            return False
    
    def get_pallet_location(
        self, 
        packing_truck_id: str, 
        pallet_number: str
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Obtiene la ubicación de un pallet escaneado.
        
        Args:
            packing_truck_id: ID del camión en el packing list
            pallet_number: Número del pallet
        
        Returns:
            Tuple (ubicacion, slot) o (None, None) si no se encuentra
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT ubicacion, slot FROM pallet_scans
                WHERE packing_truck_id = ? AND pallet_number = ?
            ''', (str(packing_truck_id), str(pallet_number)))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0], result[1]
            return None, None
            
        except Exception as e:
            print(f"Error obteniendo ubicación: {e}")
            return None, None
    
    def get_truck_scans(self, packing_truck_id: str) -> pd.DataFrame:
        """
        Obtiene todos los escaneos de un camión específico.
        
        Args:
            packing_truck_id: ID del camión en el packing list
        
        Returns:
            DataFrame con los escaneos del camión
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            
            df = pd.read_sql('''
                SELECT * FROM pallet_scans
                WHERE packing_truck_id = ?
                ORDER BY pallet_sequence_index
            ''', conn, params=(str(packing_truck_id),))
            
            conn.close()
            return df
            
        except Exception as e:
            print(f"Error obteniendo scans del camión: {e}")
            return pd.DataFrame()
    
    def get_location_assignments(self) -> Dict[str, List[Dict]]:
        """
        Obtiene todas las asignaciones de ubicaciones.
        
        Returns:
            Dict con formato:
            {
                'C1-1': [
                    {'packing_truck': '4', 'pallet': '101', 'slot': 1},
                    {'packing_truck': '4', 'pallet': '102', 'slot': 2}
                ],
                'C1-2': [...]
            }
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT ubicacion, packing_truck_id, pallet_number, slot
                FROM pallet_scans
                WHERE ubicacion IS NOT NULL
                ORDER BY ubicacion, slot
            ''')
            
            assignments = {}
            for row in cursor.fetchall():
                ubicacion = row[0]
                pallet_data = {
                    'packing_truck': row[1],
                    'pallet': row[2],
                    'slot': row[3]
                }
                
                if ubicacion not in assignments:
                    assignments[ubicacion] = []
                assignments[ubicacion].append(pallet_data)
            
            conn.close()
            return assignments
            
        except Exception as e:
            print(f"Error obteniendo asignaciones: {e}")
            return {}
    
    def deliver_truck(self, packing_truck_id: str) -> bool:
        """
        Elimina todos los registros de un camión (simula entrega/dar de baja).
        Esto libera todas las ubicaciones del layout ocupadas por este camión.
        
        Args:
            packing_truck_id: ID del camión del packing list a entregar
        
        Returns:
            True si se eliminó exitosamente, False en caso de error
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM pallet_scans
                WHERE packing_truck_id = ?
            ''', (str(packing_truck_id),))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            print(f"Entregado camión {packing_truck_id}: {deleted_count} registros eliminados")
            return True
            
        except Exception as e:
            print(f"Error entregando camión: {e}")
            return False
    
    def get_all_scanned_trucks(self) -> List[str]:
        """
        Obtiene lista de todos los camiones que tienen pallets escaneados.
        
        Returns:
            Lista de IDs de camiones del packing list
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT packing_truck_id
                FROM pallet_scans
                ORDER BY packing_truck_id
            ''')
            
            trucks = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return trucks
            
        except Exception as e:
            print(f"Error obteniendo camiones escaneados: {e}")
            return []
    
    def clear_all_data(self) -> bool:
        """
        PELIGRO: Elimina todos los datos de la base de datos.
        Usar solo para testing o reset completo.
        
        Returns:
            True si se eliminó exitosamente
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM pallet_scans')
            conn.commit()
            conn.close()
            
            print("⚠️ Base de datos limpiada completamente")
            return True
            
        except Exception as e:
            print(f"Error limpiando base de datos: {e}")
            return False
