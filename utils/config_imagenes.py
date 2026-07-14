# utils/config_imagenes.py
"""
Configuración para la gestión de imágenes de especies
"""
import os
from typing import Optional, Dict

class ConfigImagenes:
    """Configuración para la gestión de imágenes de especies"""
    
    # Ruta base donde se almacenan las imágenes (relativa a la raíz del proyecto)
    RUTA_IMAGENES = "imagenes_especies"
    
    # Mapeo de nombres de especies a nombres de archivos de imagen
    MAPEO_IMAGENES = {
        # Petrolisthes
        "Petrolisthes_tridentatus": "petrolisthes_tridentatus.jpg",
        "Petrolisthes_tonsorius": "petrolisthes_tonsorius.jpg",
        "Petrolisthes_jugosus": "petrolisthes_jugosus.jpg",
        "Petrolisthes_politus": "petrolisthes_politus.jpg",
        "Petrolisthes_lewisi": "petrolisthes_lewisi.jpg",
        "Petrolisthes_armatus": "petrolisthes_armatus.jpg",
        "Petrolisthes_galathinus": "petrolisthes_galathinus.jpg",
        "Petrolisthes_marginatus": "petrolisthes_marginatus.jpg",
        
        # Pachycheles
        "Pachycheles_serratus": "pachycheles_serratus.jpg",
        "Pachycheles_monilifer": "pachycheles_monilifer.jpg",
        "Pachycheles_riseii": "pachycheles_riseii.jpg",
        "Pachycheles_ackleianus": "pachycheles_ackleianus.jpg",
        
        # Megalobrachium
        "Megalobrachium_soriatum": "megalobrachium_soriatum.jpg",
        "Megalobrachium_mortenseni": "megalobrachium_mortenseni.jpg",
        "Megalobrachium_poeyi": "megalobrachium_poeyi.jpg",
        "Megalobrachium_roseum": "megalobrachium_roseum.jpg",
        
        # Neopisosoma
        "Neopisosoma_neglectum": "neopisosoma_neglectum.jpg",
        "Neopisosoma_angustifrons": "neopisosoma_angustifrons.jpg",
        "Neopisosoma_orientale": "neopisosoma_orientale.jpg",
        
        # Otros
        "Clastotoechus_nodosus": "clastotoechus_nodosus.jpg",
        "Minyocerus_angustus": "minyocerus_angustus.jpg",
        "Pisidia_brasiliensis": "pisidia_brasiliensis.jpg",
        "Porcellana_sayana": "porcellana_sayana.jpg"
    }
    
    # Imagen por defecto cuando no se encuentra la especie
    IMAGEN_DEFECTO = "especie_default.jpg"
    
    @classmethod
    def obtener_ruta_imagen(cls, nombre_especie: str) -> Optional[str]:
        """
        Obtiene la ruta completa de la imagen para una especie
        
        Args:
            nombre_especie (str): Nombre de la especie en formato 'Genero_especie'
            
        Returns:
            str: Ruta completa de la imagen o None si no existe
        """
        # Obtener el directorio base del proyecto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        
        # Buscar el nombre del archivo
        nombre_archivo = cls.MAPEO_IMAGENES.get(nombre_especie)
        
        if not nombre_archivo:
            # Si no está mapeada, usar el nombre de la especie como archivo
            nombre_archivo = f"{nombre_especie.lower()}.jpg"
        
        # Construir ruta completa
        ruta_completa = os.path.join(base_dir, cls.RUTA_IMAGENES, nombre_archivo)
        
        # Verificar si existe
        if os.path.exists(ruta_completa):
            return ruta_completa
        
        # Si no existe, buscar con otras extensiones
        extensiones = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        nombre_base = nombre_archivo.rsplit('.', 1)[0]
        for ext in extensiones:
            ruta_test = os.path.join(base_dir, cls.RUTA_IMAGENES, nombre_base + ext)
            if os.path.exists(ruta_test):
                return ruta_test
        
        # Si no se encuentra, buscar imagen por defecto
        ruta_defecto = os.path.join(base_dir, cls.RUTA_IMAGENES, cls.IMAGEN_DEFECTO)
        if os.path.exists(ruta_defecto):
            return ruta_defecto
        
        return None
    
    @classmethod
    def verificar_imagenes_existentes(cls) -> Dict[str, bool]:
        """
        Verifica qué imágenes existen en el sistema
        
        Returns:
            dict: Diccionario con especies y su estado de imagen
        """
        resultado = {}
        for especie in cls.MAPEO_IMAGENES:
            ruta = cls.obtener_ruta_imagen(especie)
            resultado[especie] = ruta is not None
        return resultado
    
    @classmethod
    def obtener_especies_con_imagen(cls) -> list:
        """
        Obtiene la lista de especies que tienen imagen disponible
        
        Returns:
            list: Lista de especies con imagen
        """
        return [especie for especie, existe in cls.verificar_imagenes_existentes().items() if existe]