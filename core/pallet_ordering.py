"""
Módulo de ordenamiento secuencial de pallets.

Implementa la lógica para calcular ubicaciones basadas en el índice secuencial
del pallet dentro de su camión, respetando el límite de 57 ubicaciones.

LÓGICA CRÍTICA:
- Pallet índice 1 → Ubicación 1, Slot 1
- Pallet índice 2 → Ubicación 1, Slot 2
- Pallet índice 3 → Ubicación 2, Slot 1
- Pallet índice 4 → Ubicación 2, Slot 2
- Pallet índice 5 → Ubicación 3, Slot 1
...
- Pallet índice 10 → Ubicación 5, Slot 2
"""

import re
import pandas as pd
from typing import Tuple, Optional


def extract_pallet_number(pallet_code: str) -> Optional[int]:
    """
    Extrae el número de pallet de un código escaneado.
    
    Soporta varios formatos:
    - "PALLET003" -> 3
    - "PLT-045" -> 45
    - "P_012" -> 12
    - "456" -> 456
    
    Args:
        pallet_code: Código del pallet escaneado
    
    Returns:
        Número del pallet o None si no se puede extraer
    """
    try:
        # Buscar  números al final del código
        match = re.search(r'(\d{2,3})$', pallet_code)
        if match:
            return int(match.group(1))
        
        # Buscar números después de "PALLET", "PLT", "P", etc.
        match = re.search(r'(?:PALLET|PLT|P)[_-]?(\d{2,3})', pallet_code, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Si el código es completamente numérico
        if pallet_code.isdigit():
            return int(pallet_code)
        
        # Intentar extraer cualquier secuencia de 2-3 dígitos
        match = re.search(r'(\d{2,3})', pallet_code)
        if match:
            return int(match.group(1))
        
        return None
    except:
        return None


def get_pallet_sequence_index(pallet_number: str, truck_pallets_df: pd.DataFrame) -> Optional[int]:
    """
    Obtiene el índice secuencial de un pallet dentro de su camión.
    
    IMPORTANTE: El índice empieza en 1 (no en 0).
    
    Ejemplo:
    Si el camión tiene pallets [101, 102, 103, 104, 105]:
    - Pallet 101 -> índice 1 (primer pallet)
    - Pallet 102 -> índice 2 (segundo pallet)
    - Pallet 105 -> índice 5 (quinto pallet)
    
    Args:
        pallet_number: Número del pallet a buscar
        truck_pallets_df: DataFrame con los pallets del camión
    
    Returns:
        Índice secuencial (1-based) o None si no se encuentra
    """
    try:
        # Convertir todo a string para comparación
        pallet_str = str(pallet_number)
        
        # Ordenar pallets por número
        sorted_pallets = truck_pallets_df.sort_values('Pallet number')
        
        # Buscar el índice (1-based)
        for idx, row in enumerate(sorted_pallets.itertuples(), start=1):
            if str(row.__getattribute__('Pallet number')) == pallet_str:
                return idx
        
        return None
    except Exception as e:
        print(f"Error obteniendo índice secuencial: {e}")
        return None


def calculate_location_from_index(
    pallet_index: int, 
    layout_truck_id: str
) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    """
    Calcula la ubicación y slot basándose en el índice secuencial del pallet.
    
    Fórmulas:
    - ubicacion_num = ((pallet_index - 1) // 2) + 1
    - slot = ((pallet_index - 1) % 2) + 1
    - ubicacion = f"C{layout_truck_id}-{ubicacion_num}"
    
    Ejemplos:
    - Índice 1: ubicacion_num=1, slot=1 -> "C1-1", slot 1
    - Índice 2: ubicacion_num=1, slot=2 -> "C1-1", slot 2
    - Índice 3: ubicacion_num=2, slot=1 -> "C1-2", slot 1
    - Índice 5: ubicacion_num=3, slot=1 -> "C1-3", slot 1
    - Índice 10: ubicacion_num=5, slot=2 -> "C1-5", slot 2
    
    VALIDACIÓN: Si ubicacion_num > 57, retorna None (límite alcanzado).
    
    Args:
        pallet_index: Índice secuencial del pallet (1-based)
        layout_truck_id: ID del camión del layout (ej: "C1", "C2")
    
    Returns:
        Tuple (ubicacion, slot, error_message)
        - ubicacion: String como "C1-5" o None si excede límite
        - slot: 1 o 2, o None si há error
        - error_message: Mensaje de error o None si es exitoso
    """
    try:
        # Calcular número de ubicación (cada ubicación tiene 2 pallets)
        ubicacion_num = ((pallet_index - 1) // 2) + 1
        
        # Validar límite de 57 ubicaciones
        if ubicacion_num > 57:
            return None, None, f"❌ Límite de 57 ubicaciones alcanzado. Pallet índice {pallet_index} requiere ubicación {ubicacion_num}."
        
        # Calcular slot (1 o 2)
        slot = ((pallet_index - 1) % 2) + 1
        
        # Construir ubicación
        # Extraer el número del camión si viene como "C1", "C2", etc.
        truck_num = layout_truck_id.replace('C', '') if layout_truck_id.startswith('C') else layout_truck_id
        ubicacion = f"C{truck_num}-{ubicacion_num}"
        
        return ubicacion, slot, None
        
    except Exception as e:
        return None, None, f"Error calculando ubicación: {e}"


def validate_pallet_can_scan(
    pallet_index: int,
    layout_truck_id: str,
    layout_locations: list
) -> Tuple[bool, str]:
    """
    Valida si un pallet puede ser escaneado.
    
    Validaciones:
    1. El índice del pallet no debe exceder el límite de 57 ubicaciones
    2. (Opcional) La ubicación calculada debe existir en el layout
    
    Args:
        pallet_index: Índice secuencial del pallet
        layout_truck_id: ID del camión del layout
        layout_locations: Lista de ubicaciones disponibles en el layout
    
    Returns:
        Tuple (can_scan, message)
    """
    ubicacion, slot, error = calculate_location_from_index(pallet_index, layout_truck_id)
    
    if error:
        return False, error
    
    # Opcional: Verificar si la ubicación existe en el layout
    # (Puede ser desactivado si no se requiere)
    if layout_locations and ubicacion not in layout_locations:
        return False, f"⚠️ La ubicación {ubicacion} no existe en el layout cargado."
    
    return True, f"✅ Pallet puede escanearse en {ubicacion} slot {slot}"


def get_next_expected_pallet(
    scanned_pallets: list,
    all_pallets_df: pd.DataFrame
) -> Optional[dict]:
    """
    OPCIONAL: Obtiene el siguiente pallet esperado en el orden secuencial.
    
    Útil si se quiere validar que se escanean en orden.
    
    Args:
        scanned_pallets: Lista de pallets ya escaneados
        all_pallets_df: DataFrame con todos los pallets del camión
    
    Returns:
        Dict con información del siguiente pallet esperado o None
    """
    try:
        sorted_pallets = all_pallets_df.sort_values('Pallet number')
        
        for idx, row in sorted_pallets.iterrows():
            pallet_num = str(row['Pallet number'])
            if pallet_num not in scanned_pallets:
                return {
                    'pallet_number': pallet_num,
                    'index': len([p for p in sorted_pallets['Pallet number'] if str(p) <= pallet_num]),
                    'first_serial': row['first_serial'],
                    'last_serial': row['last_serial']
                }
        
        return None
    except Exception as e:
        print(f"Error obteniendo siguiente pallet: {e}")
        return None
