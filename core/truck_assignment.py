"""
Módulo de asignación mejorada de camiones físicos del layout.

Este módulo implementa la lógica para asignar camiones del packing list
a camiones físicos del layout, con las siguientes reglas:
1. Solo asignar a camiones del layout completamente vacíos
2. Bloquear cuando no hay camiones vacíos disponibles
3. Mantener mapeo consistente packing_truck_id -> layout_truck_id
"""

import re
import sqlite3
from typing import List, Dict, Tuple, Optional


def get_layout_trucks_from_locations(layout_locations: List[str]) -> List[int]:
    """
    Extrae los IDs únicos de camiones del layout desde las ubicaciones.
    
    Args:
        layout_locations: Lista de ubicaciones ej: ['C1-1', 'C1-2', 'C2-1', 'C3-1']
    
    Returns:
        Lista ordenada de IDs de camiones ej: [1, 2, 3]
    """
    camiones = set()
    for location in layout_locations:
        match = re.match(r'C(\d+)-\d+', location)
        if match:
            camiones.add(int(match.group(1)))
    
    return sorted(camiones)


def get_occupied_layout_trucks(db_path: str = 'scans.db') -> Dict[int, int]:
    """
    Obtiene la cantidad de pallets por camión del layout.
    
    Args:
        db_path: Ruta a la base de datos SQLite
    
    Returns:
        Dict con {layout_truck_id: pallet_count}
        Ejemplo: {1: 5, 2: 0, 3: 12} significa C1 tiene 5 pallets, C2 vacío, C3 tiene 12
    """
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT layout_truck_id, COUNT(*) 
            FROM pallet_scans 
            WHERE layout_truck_id IS NOT NULL 
            GROUP BY layout_truck_id
        ''')
        
        occupied = {}
        for row in cursor.fetchall():
            # Extraer número del layout_truck_id (ej: "C1" -> 1)
            match = re.match(r'C(\d+)', row[0])
            if match:
                truck_id = int(match.group(1))
                occupied[truck_id] = row[1]
        
        conn.close()
        return occupied
        
    except Exception as e:
        print(f"Error obteniendo camiones ocupados: {e}")
        return {}


def get_empty_layout_trucks(layout_trucks: List[int], db_path: str = 'scans.db') -> List[int]:
    """
    Retorna solo los camiones del layout que están completamente vacíos.
    
    CRÍTICO: Un camión se considera vacío SOLO si no tiene ningún pallet.
    Aunque tenga espacio disponible, si tiene 1 pallet, NO está vacío.
    
    Args:
        layout_trucks: Lista de IDs de camiones en el layout
        db_path: Ruta a la base de datos
    
    Returns:
        Lista ordenada de IDs de camiones completamente vacíos
    """
    occupied = get_occupied_layout_trucks(db_path)
    
    empty_trucks = []
    for truck_id in layout_trucks:
        if truck_id not in occupied or occupied[truck_id] == 0:
            empty_trucks.append(truck_id)
    
    return sorted(empty_trucks)


def get_packing_truck_assignment(packing_truck_id: str, db_path: str = 'scans.db') -> Optional[str]:
    """
    Obtiene el camión del layout asignado a un camión del packing list.
    
    Args:
        packing_truck_id: ID del camión en el packing list
        db_path: Ruta a la base de datos
    
    Returns:
        ID del layout truck asignado (ej: "C1") o None si no tiene asignación
    """
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT layout_truck_id 
            FROM pallet_scans 
            WHERE packing_truck_id = ? AND layout_truck_id IS NOT NULL
            LIMIT 1
        ''', (str(packing_truck_id),))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
        
    except Exception as e:
        print(f"Error obteniendo asignación de camión: {e}")
        return None


def assign_packing_truck_to_layout(
    packing_truck_id: str, 
    layout_trucks: List[int],
    db_path: str = 'scans.db'
) -> Tuple[bool, str, Optional[str]]:
    """
    Asigna un camión del packing list al primer camión vacío del layout.
    
    Lógica:
    1. Si el packing_truck_id ya tiene un camión asignado -> retornar ese
    2. Si no, buscar el PRIMER camión completamente vacío en el layout
    3. Si no hay camiones vacíos -> BLOQUEAR (retornar False)
    
    Args:
        packing_truck_id: ID del camión en el packing list
        layout_trucks: Lista de IDs disponibles en el layout
        db_path: Ruta a la base de datos
    
    Returns:
        Tuple (success, message, layout_truck_id)
        - success: True si se puede asignar, False si no
        - message: Mensaje descriptivo
        - layout_truck_id: ID del camión asignado (ej: "C1") o None
    """
    # 1. Verificar si ya tiene asignación
    existing_assignment = get_packing_truck_assignment(packing_truck_id, db_path)
    if existing_assignment:
        return True, f"✅ Camión ya asignado a {existing_assignment}", existing_assignment
    
    # 2. Buscar camiones completamente vacíos
    empty_trucks = get_empty_layout_trucks(layout_trucks, db_path)
    
    if len(empty_trucks) == 0:
        return False, "❌ No hay camiones disponibles. Entrega un camión para liberar espacio.", None
    
    # 3. Asignar al primer camión vacío
    layout_truck_id = f"C{empty_trucks[0]}"
    return True, f"✅ Asignado a {layout_truck_id}", layout_truck_id


def get_layout_truck_statistics(layout_trucks: List[int], db_path: str = 'scans.db') -> Dict:
    """
    Obtiene estadísticas de ocupación de todos los camiones del layout.
    
    Args:
        layout_trucks: Lista de IDs de camiones en el layout
        db_path: Ruta a la base de datos
    
    Returns:
        Dict con estadísticas por camión:
        {
            'C1': {'pallets': 10, 'locations_used': 5, 'is_empty': False, 'is_full': False},
            'C2': {'pallets': 0, 'locations_used': 0, 'is_empty': True, 'is_full': False},
            ...
        }
    """
    occupied = get_occupied_layout_trucks(db_path)
    
    stats = {}
    for truck_id in layout_trucks:
        pallet_count = occupied.get(truck_id, 0)
        # Cada ubicación tiene 2 pallets, entonces locations_used = ceil(pallets / 2)
        locations_used = (pallet_count + 1) // 2
        
        stats[f'C{truck_id}'] = {
            'pallets': pallet_count,
            'locations_used': locations_used,
            'is_empty': pallet_count == 0,
            'is_full': locations_used >= 57  # Límite de 57 ubicaciones
        }
    
    return stats
