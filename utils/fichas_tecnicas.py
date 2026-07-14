# utils/fichas_tecnicas.py
"""
Módulo para gestionar las fichas técnicas de las especies
"""
import json
import os
from typing import Dict, Optional, Any

class FichasTecnicas:
    """Clase para manejar las fichas técnicas de las especies"""
    
    # Ruta del archivo de fichas técnicas
    RUTA_FICHAS = "data/fichas_tecnicas.json"
    
    def __init__(self):
        """Inicializa el gestor de fichas técnicas"""
        self.fichas = {}
        self.cargar_fichas()
    
    def cargar_fichas(self) -> bool:
        """
        Carga las fichas técnicas desde el archivo JSON
        
        Returns:
            bool: True si se cargaron correctamente, False si no
        """
        try:
            # Obtener la ruta absoluta
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir)
            ruta_completa = os.path.join(base_dir, self.RUTA_FICHAS)
            
            if os.path.exists(ruta_completa):
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    self.fichas = json.load(f)
                print(f"✅ Fichas técnicas cargadas: {len(self.fichas)} especies")
                return True
            else:
                print(f"⚠️ Archivo de fichas no encontrado: {ruta_completa}")
                return False
                
        except Exception as e:
            print(f"❌ Error al cargar fichas técnicas: {e}")
            return False
    
    def obtener_ficha(self, nombre_especie: str) -> Optional[Dict]:
        """
        Obtiene la ficha técnica de una especie
        
        Args:
            nombre_especie (str): Nombre de la especie en formato 'Genero_especie'
            
        Returns:
            Dict: Ficha técnica de la especie o None si no existe
        """
        return self.fichas.get(nombre_especie)
    
    def obtener_taxonomia(self, nombre_especie: str) -> Optional[Dict]:
        """Obtiene la información taxonómica de una especie"""
        ficha = self.obtener_ficha(nombre_especie)
        return ficha.get('taxonomia') if ficha else None
    
    def obtener_distribucion(self, nombre_especie: str) -> Optional[Dict]:
        """Obtiene la información de distribución de una especie"""
        ficha = self.obtener_ficha(nombre_especie)
        return ficha.get('distribucion') if ficha else None
    
    def obtener_conservacion(self, nombre_especie: str) -> Optional[Dict]:
        """Obtiene la información de conservación de una especie"""
        ficha = self.obtener_ficha(nombre_especie)
        return ficha.get('conservacion') if ficha else None
    
    def obtener_nombre_comun(self, nombre_especie: str) -> str:
        """Obtiene el nombre común de una especie"""
        ficha = self.obtener_ficha(nombre_especie)
        return ficha.get('nombre_comun', nombre_especie.replace('_', ' ').title()) if ficha else nombre_especie.replace('_', ' ').title()
    
    def tiene_ficha(self, nombre_especie: str) -> bool:
        """Verifica si existe ficha para una especie"""
        return nombre_especie in self.fichas
    
    def listar_especies_con_ficha(self) -> list:
        """Lista todas las especies que tienen ficha técnica"""
        return list(self.fichas.keys())
    
    def agregar_ficha(self, nombre_especie: str, ficha: Dict) -> bool:
        """
        Agrega o actualiza una ficha técnica
        
        Args:
            nombre_especie (str): Nombre de la especie
            ficha (Dict): Datos de la ficha
            
        Returns:
            bool: True si se agregó correctamente
        """
        try:
            self.fichas[nombre_especie] = ficha
            return self.guardar_fichas()
        except Exception as e:
            print(f"❌ Error al agregar ficha: {e}")
            return False
    
    def guardar_fichas(self) -> bool:
        """
        Guarda las fichas técnicas en el archivo JSON
        
        Returns:
            bool: True si se guardaron correctamente
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir)
            ruta_completa = os.path.join(base_dir, self.RUTA_FICHAS)
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
            
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                json.dump(self.fichas, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"❌ Error al guardar fichas: {e}")
            return False