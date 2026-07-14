# utils/manejador_imagenes.py
"""
Manejador de imágenes para el sistema experto
"""
import tkinter as tk
from tkinter import ttk
import os
import sys
from typing import Optional, Tuple

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.config_imagenes import ConfigImagenes

# Intentar importar PIL
try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False
    print("⚠️ Pillow no instalado. Las imágenes no se mostrarán correctamente.")
    print("   Instale con: pip install Pillow")

class ManejadorImagenes:
    """Clase para manejar la carga y visualización de imágenes"""
    
    # Tamaños predefinidos
    TAMANO_GRANDE = (400, 300)
    TAMANO_MEDIANO = (250, 200)
    TAMANO_PEQUEÑO = (150, 120)
    TAMANO_MINIATURA = (80, 60)
    
    def __init__(self, parent):
        """
        Inicializa el manejador de imágenes
        
        Args:
            parent: Widget padre para la imagen
        """
        self.parent = parent
        self.imagen_actual = None
        self.label_imagen = None
        self.tamano = self.TAMANO_MEDIANO
        
    def crear_frame_imagen(self, parent: ttk.Frame, tamano: Tuple[int, int] = None) -> ttk.Label:
        """
        Crea un frame para mostrar imágenes
        
        Args:
            parent: Widget padre
            tamano: Tupla (ancho, alto) para la imagen
            
        Returns:
            ttk.Label: Label donde se mostrará la imagen
        """
        if tamano is None:
            tamano = self.TAMANO_MEDIANO
        
        # Crear frame contenedor
        frame = ttk.LabelFrame(parent, text="📸 Especie", padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Crear label para la imagen
        self.label_imagen = ttk.Label(frame, 
                                     text="🖼️ No hay imagen disponible",
                                     font=('Segoe UI', 10),
                                     background='white')
        self.label_imagen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Guardar tamaño
        self.tamano = tamano
        
        # Configurar para que se expanda
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        
        return self.label_imagen
    
    def cargar_imagen(self, nombre_especie: str, 
                     tamano: Tuple[int, int] = None) -> bool:
        """
        Carga y muestra una imagen de la especie
        
        Args:
            nombre_especie: Nombre de la especie
            tamano: Tupla (ancho, alto) para redimensionar
            
        Returns:
            bool: True si se cargó la imagen, False si no
        """
        if tamano is None:
            tamano = self.tamano
        
        # Verificar que Pillow esté disponible
        if not PIL_DISPONIBLE:
            self.mostrar_mensaje_sin_imagen()
            return False
        
        # Obtener ruta de la imagen
        ruta_imagen = ConfigImagenes.obtener_ruta_imagen(nombre_especie)
        
        if not ruta_imagen:
            self.mostrar_mensaje_sin_imagen()
            return False
        
        try:
            # Cargar la imagen
            imagen = Image.open(ruta_imagen)
            
            # Redimensionar manteniendo proporción
            imagen = self.redimensionar_manteniendo_proporcion(imagen, tamano)
            
            # Convertir a PhotoImage
            photo = ImageTk.PhotoImage(imagen)
            
            # Mostrar en el label
            if self.label_imagen:
                self.label_imagen.config(image=photo, text="")
                self.label_imagen.image = photo  # Mantener referencia
                self.imagen_actual = photo
                return True
                
        except Exception as e:
            print(f"Error al cargar imagen para {nombre_especie}: {e}")
            self.mostrar_mensaje_sin_imagen()
            return False
        
        return False
    
    def redimensionar_manteniendo_proporcion(self, imagen, tamano: Tuple[int, int]):
        """
        Redimensiona una imagen manteniendo la proporción
        
        Args:
            imagen: Imagen a redimensionar
            tamano: Tupla (ancho, alto) máximo
            
        Returns:
            Image: Imagen redimensionada
        """
        ancho_max, alto_max = tamano
        
        # Obtener tamaño original
        ancho_orig, alto_orig = imagen.size
        
        # Calcular proporción
        proporcion = min(ancho_max / ancho_orig, alto_max / alto_orig)
        
        # Nuevo tamaño
        nuevo_ancho = int(ancho_orig * proporcion)
        nuevo_alto = int(alto_orig * proporcion)
        
        # Redimensionar usando el método correcto según la versión de Pillow
        try:
            # Para Pillow >= 9.1.0
            return imagen.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        except AttributeError:
            # Para Pillow < 9.1.0
            return imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
    
    def mostrar_mensaje_sin_imagen(self):
        """Muestra un mensaje cuando no hay imagen disponible"""
        if self.label_imagen:
            self.label_imagen.config(image='', text="🖼️ Sin imagen disponible")
            self.label_imagen.image = None
            self.imagen_actual = None
    
    def limpiar_imagen(self):
        """Limpia la imagen actual"""
        if self.label_imagen:
            self.label_imagen.config(image='', text="🖼️ No hay imagen disponible")
            self.label_imagen.image = None
            self.imagen_actual = None