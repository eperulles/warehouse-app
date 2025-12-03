"""
Parser de archivos SVG/XML para extraer ubicaciones del layout.

Adaptado del código original de Streamlit para trabajar con Flet.
"""

import xml.etree.ElementTree as ET
import re
from typing import List, Tuple, Dict


def parse_svg_xml(xml_content: str) -> Tuple[List[str], List[Dict]]:
    """
    Parsea un archivo SVG/XML y extrae las ubicaciones y formas.
    
    Args:
        xml_content: Contenido del archivo SVG/XML como string
    
    Returns:
        Tuple (locations, shapes_data)
        - locations: Lista de ubicaciones encontradas (ej: ['C1-1', 'C1-2', ...])
        - shapes_data: Lista de dicts con información de las formas
    """
    try:
        # Remover namespace si existe para facilitar parsing
        xml_content = re.sub(r'xmlns="[^"]+"', '', xml_content)
        xml_content = re.sub(r'xmlns:[\w]+="[^"]+"', '', xml_content)
        
        root = ET.fromstring(xml_content)
        
        locations = []
        shapes_data = []
        
        # Buscar todos los elementos con IDs que sigan el patrón CX-Y
        for element in root.iter():
            element_id = element.get('id', '')
            
            # Verificar si el ID sigue el patrón C+número-número
            if re.match(r'^C\d+-\d+$', element_id):
                locations.append(element_id)
                
                # Extraer información de la forma
                shape_info = {'ubicacion': element_id}
                
                # Detectar tipo de forma
                tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
                
                if tag == 'rect':
                    shape_info['type'] = 'rect'
                    shape_info['x'] = float(element.get('x', 0))
                    shape_info['y'] = float(element.get('y', 0))
                    shape_info['width'] = float(element.get('width', 50))
                    shape_info['height'] = float(element.get('height', 30))
                    shape_info['fill'] = element.get('fill', '#cccccc')
                    shape_info['stroke'] = element.get('stroke', '#666666')
                
                elif tag == 'polygon':
                    shape_info['type'] = 'polygon'
                    points_str = element.get('points', '')
                    shape_info['points'] = points_str.split()
                    shape_info['fill'] = element.get('fill', '#cccccc')
                    shape_info['stroke'] = element.get('stroke', '#666666')
                
                elif tag == 'circle':
                    shape_info['type'] = 'circle'
                    shape_info['cx'] = float(element.get('cx', 0))
                    shape_info['cy'] = float(element.get('cy', 0))
                    shape_info['r'] = float(element.get('r', 20))
                    shape_info['fill'] = element.get('fill', '#cccccc')
                    shape_info['stroke'] = element.get('stroke', '#666666')
                
                elif tag == 'text':
                    shape_info['type'] = 'text'
                    shape_info['x'] = float(element.get('x', 0))
                    shape_info['y'] = float(element.get('y', 0))
                    shape_info['content'] = element.text or element_id
                
                else:
                    # Forma desconocida, intentar extraer coordenadas básicas
                    shape_info['type'] = 'unknown'
                    shape_info['x'] = float(element.get('x', 0))
                    shape_info['y'] = float(element.get('y', 0))
                
                shapes_data.append(shape_info)
        
        # Ordenar ubicaciones
        locations.sort(key=lambda x: (int(x.split('-')[0][1:]), int(x.split('-')[1])))
        
        print(f"✅ SVG parseado: {len(locations)} ubicaciones, {len(shapes_data)} formas")
        
        return locations, shapes_data
        
    except Exception as e:
        print(f"❌ Error parseando SVG: {e}")
        return [], []


def create_simple_layout_from_text(layout_text: str) -> Tuple[List[str], List[Dict]]:
    """
    Crea un layout simple desde texto.
    
    Args:
        layout_text: Texto con ubicaciones separadas por comas, tabs o saltos de línea
                     Ejemplo: "C1-1, C1-2, C1-3\nC2-1, C2-2"
    
    Returns:
        Tuple (locations, shapes_data) similar a parse_svg_xml
    """
    try:
        locations = []
        lines = layout_text.strip().split('\n')
        
        for line in lines:
            # Separar por tabs, comas o múltiples espacios
            cells = re.split(r'\t|,|\s{2,}', line.strip())
            for cell in cells:
                cell = cell.strip()
                if cell and re.match(r'^C\d+-\d+$', cell):
                    locations.append(cell)
        
        # Crear formas simples en una cuadrícula
        shapes_data = []
        for i, ubicacion in enumerate(locations):
            shapes_data.append({
                'type': 'rect',
                'ubicacion': ubicacion,
                'x': (i % 10) * 60,
                'y': (i // 10) * 40,
                'width': 50,
                'height': 30,
                'fill': '#cccccc',
                'stroke': '#666666'
            })
            
            # Agregar etiqueta de texto
            shapes_data.append({
                'type': 'text',
                'ubicacion': ubicacion,
                'x': (i % 10) * 60 + 25,
                'y': (i // 10) * 40 + 15,
                'content': ubicacion
            })
        
        print(f"✅ Layout de texto creado: {len(locations)} ubicaciones")
        
        return locations, shapes_data
        
    except Exception as e:
        print(f"❌ Error creando layout desde texto: {e}")
        return [], []
