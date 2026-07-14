"""
Módulo de interfaz gráfica mejorada para el sistema experto de identificación de especies
VERSIÓN COMPLETA - Responsiva, con pestañas, imágenes y fichas técnicas
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
from typing import Dict, Any, List
import time
from datetime import datetime
import os
import sys
import webbrowser  # Para abrir enlaces en el navegador

# Configurar paths para importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from utils.manejador_imagenes import ManejadorImagenes
    from utils.config_imagenes import ConfigImagenes
    from utils.fichas_tecnicas import FichasTecnicas
except ImportError as e:
    print(f"⚠️ Error importando módulos: {e}")
    # Crear clases dummy si no están disponibles
    class ManejadorImagenes:
        def __init__(self, parent):
            self.parent = parent
            self.label_imagen = None
        def cargar_imagen(self, nombre_especie, tamano=None):
            return False
        def limpiar_imagen(self):
            pass
    
    class ConfigImagenes:
        RUTA_IMAGENES = "imagenes_especies"
        IMAGEN_DEFECTO = "especie_default.jpg"
    
    class FichasTecnicas:
        def __init__(self):
            self.fichas = {}
        def cargar_fichas(self):
            return False
        def obtener_ficha(self, nombre_especie):
            return None
        def obtener_nombre_comun(self, nombre_especie):
            return nombre_especie.replace('_', ' ').title()
        def tiene_ficha(self, nombre_especie):
            return False

class InterfazSistemaExperto:
    """
    Interfaz gráfica mejorada con pestañas, soporte para imágenes y fichas técnicas
    """
    
    # Colores del tema
    COLORES = {
        'fondo': '#f0f4f8',
        'primario': '#2c3e50',
        'secundario': '#3498db',
        'exito': '#27ae60',
        'peligro': '#e74c3c',
        'advertencia': '#f39c12',
        'info': '#2980b9',
        'gris_claro': '#ecf0f1',
        'gris_medio': '#bdc3c7',
        'blanco': '#ffffff',
        'sombra': '#d5dbe0'
    }
    
    def __init__(self, root: tk.Tk, sistema_reglas, red_neuronal):
        """
        Inicializa la interfaz gráfica
        
        Args:
            root (tk.Tk): Ventana principal
            sistema_reglas: Instancia del sistema basado en reglas
            red_neuronal: Instancia de la red neuronal
        """
        self.root = root
        self.sistema_reglas = sistema_reglas
        self.red_neuronal = red_neuronal
        
        # Estado de la aplicación
        self.modo_actual = "reglas"
        self.pregunta_actual = None
        self.subpregunta_actual = None
        self.historial_preguntas = []
        self.identificacion_activa = False
        self.resultados = []
        self.favoritos = []
        self.mostrar_bienvenida = True
        self.especie_actual = None
        
        # Variables para scroll
        self.canvas = None
        self.scrollbar = None
        self.frame_scrollable = None
        self.scroll_habilitado = False
        self.ancho_canvas = 0  # Para mantener el ancho consistente
        
        # Variables para animaciones
        self.animacion_activa = False
        
        # URL del portafolio
        self.url_portafolio = "https://bioinformatico-udo.github.io/portafilio-digital/"
        
        # Inicializar atributos de UI
        self.frame_proceso = None
        self.frame_resultados_reglas = None
        self.frame_resultados_rn = None
        self.boton_iniciar_reglas = None
        self.boton_cancelar_reglas = None
        self.frame_bienvenida = None
        self.frame_contenido_principal = None
        self.notebook = None
        
        # Variables para formulario RN
        self.entry_longitud = None
        self.combo_setas = None
        self.combo_dientes = None
        self.combo_granulacion = None
        self.combo_placas = None
        self.combo_quilla = None
        
        # Manejador de imágenes y fichas
        self.manejador_imagenes = None
        self.fichas = FichasTecnicas()
        
        # Verificar disponibilidad de imágenes
        self.imagenes_disponibles = self.verificar_imagenes()
        
        self.configurar_interfaz()
        self.crear_interfaz_con_scroll()
        self.crear_barra_estado_mejorada()
        self.mostrar_panel_bienvenida()
        
        # Iniciar actualización de hora
        self.actualizar_reloj()
        
        # Configurar eventos de redimensionamiento
        self.root.bind('<Configure>', self.on_resize)
        
        # Ajustar la ventana al contenido después de la inicialización
        self.root.after(100, self.ajustar_ventana)
        
        # Configurar el ancho del canvas después de que la ventana se muestre
        self.root.after(200, self.actualizar_ancho_canvas)
    
    def actualizar_ancho_canvas(self):
        """Actualiza el ancho del canvas para mantener consistencia"""
        if self.canvas:
            self.ancho_canvas = self.canvas.winfo_width()
            # Forzar actualización del scroll region
            self.actualizar_scroll()
    
    def ajustar_ventana(self):
        """Ajusta el tamaño de la ventana al contenido"""
        self.root.update_idletasks()
        # Obtener el tamaño mínimo recomendado
        self.root.geometry("")  # Esto permite que la ventana se ajuste al contenido
        # Establecer un tamaño mínimo
        self.root.minsize(900, 650)
        # Centrar la ventana
        self.root.eval('tk::PlaceWindow . center')
    
    def verificar_imagenes(self) -> dict:
        """Verifica qué imágenes están disponibles"""
        try:
            return ConfigImagenes.verificar_imagenes_existentes()
        except:
            return {}
    
    def configurar_interfaz(self):
        """Configura la ventana principal con diseño moderno"""
        self.root.title("🦀 Sistema Experto Porcelanidae v2.0 - Con Imágenes y Fichas")
        self.root.configure(bg=self.COLORES['fondo'])
        self.root.minsize(900, 650)
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Configurar icono (si existe)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def on_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        if event.widget == self.root:
            self.actualizar_ancho_canvas()
            self.actualizar_scroll()
    
    def configurar_estilos(self):
        """Configura los estilos con diseño moderno"""
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Colores base
        bg = self.COLORES['fondo']
        primary = self.COLORES['primario']
        secondary = self.COLORES['secundario']
        
        # Configurar estilos personalizados
        estilo.configure('Titulo.TLabel', 
                        font=('Segoe UI', 18, 'bold'), 
                        background=bg,
                        foreground=primary)
        
        estilo.configure('Subtitulo.TLabel',
                        font=('Segoe UI', 12),
                        background=bg,
                        foreground='#34495e')
        
        estilo.configure('Pregunta.TLabel',
                        font=('Segoe UI', 11),
                        background=bg,
                        foreground=primary,
                        wraplength=800)
        
        estilo.configure('Exito.TLabel',
                        font=('Segoe UI', 12, 'bold'),
                        foreground=self.COLORES['exito'])
        
        # ESTILOS PARA NOMBRES CIENTÍFICOS EN CURSIVA
        estilo.configure('Cientifico.TLabel',
                        font=('Georgia', 12, 'italic'),
                        background=bg,
                        foreground=primary)
        
        estilo.configure('CientificoGrande.TLabel',
                        font=('Georgia', 16, 'bold italic'),
                        background=bg,
                        foreground=primary)
        
        estilo.configure('CientificoResultado.TLabel',
                        font=('Georgia', 14, 'bold italic'),
                        background='#e8f6f3',
                        foreground=primary,
                        padding=20)
        
        estilo.configure('CientificoLista.TLabel',
                        font=('Georgia', 10, 'italic'),
                        background=bg,
                        foreground=primary)
        
        # Estilo para fichas técnicas
        estilo.configure('Ficha.TLabel',
                        font=('Segoe UI', 9),
                        background=bg,
                        foreground='#34495e',
                        wraplength=600)
        
        estilo.configure('FichaTitulo.TLabel',
                        font=('Segoe UI', 10, 'bold'),
                        background=bg,
                        foreground=primary)
        
        # Estilo para pestañas
        estilo.configure('TNotebook', background=bg, borderwidth=0)
        estilo.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[10, 5])
        estilo.map('TNotebook.Tab', background=[('selected', '#3498db'), ('active', '#2980b9')],
                   foreground=[('selected', 'white'), ('active', 'white')])
        
        # Estilos para botones con efectos
        estilo.configure('BotonPrincipal.TButton',
                        font=('Segoe UI', 10, 'bold'),
                        padding=(20, 10),
                        background=secondary,
                        foreground='white',
                        relief='flat')
        
        estilo.map('BotonPrincipal.TButton',
                  background=[('active', '#2980b9'), ('pressed', '#1a6fa0')],
                  relief=[('pressed', 'sunken')])
        
        estilo.configure('BotonSecundario.TButton',
                        font=('Segoe UI', 9),
                        padding=(15, 8),
                        background=self.COLORES['gris_claro'],
                        foreground=primary,
                        relief='flat')
        
        estilo.map('BotonSecundario.TButton',
                  background=[('active', '#d5dbe0'), ('pressed', '#bdc3c7')])
        
        estilo.configure('BotonPeligro.TButton',
                        font=('Segoe UI', 9, 'bold'),
                        padding=(15, 8),
                        background=self.COLORES['peligro'],
                        foreground='white',
                        relief='flat')
        
        estilo.map('BotonPeligro.TButton',
                  background=[('active', '#c0392b')])
        
        # Estilos para frames
        estilo.configure('Marco.TLabelframe',
                        background=bg,
                        borderwidth=2,
                        relief='solid',
                        bordercolor=self.COLORES['gris_medio'])
        
        estilo.configure('Marco.TLabelframe.Label',
                        background=bg,
                        font=('Segoe UI', 11, 'bold'),
                        foreground=primary)
        
        # Estilo para tarjetas
        estilo.configure('Card.TFrame',
                        background='white',
                        relief='raised',
                        borderwidth=1)
        
        # Estilo para progressbar
        estilo.configure("Custom.Horizontal.TProgressbar",
                        thickness=20,
                        troughcolor=self.COLORES['gris_claro'],
                        background=secondary)
    
    def crear_interfaz_con_scroll(self):
        """Crea la interfaz completa con scroll vertical"""
        # Frame principal
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Canvas principal
        self.canvas = tk.Canvas(self.frame_principal, bg=self.COLORES['fondo'], 
                               highlightthickness=0)
        
        # Scrollbar vertical
        self.scrollbar = ttk.Scrollbar(self.frame_principal, orient="vertical", 
                                      command=self.canvas.yview)
        
        # Frame scrollable
        self.frame_scrollable = ttk.Frame(self.canvas)
        
        # Configurar canvas
        self.canvas.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configurar el frame scrollable
        self.frame_scrollable.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Eventos de scroll con el mouse
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.frame_scrollable.bind("<MouseWheel>", self._on_mousewheel)
        
        # Configurar el grid del frame scrollable con columnas de igual ancho
        self.frame_scrollable.columnconfigure(0, weight=1)
        self.frame_scrollable.columnconfigure(1, weight=0)
        self.frame_scrollable.rowconfigure(1, weight=1)
        
        # Crear componentes
        self.crear_header()
        self.crear_contenido_principal()
        self.crear_footer()
        
        # Actualizar scroll
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scroll_habilitado = True
        
        # Obtener el ancho inicial del canvas
        self.actualizar_ancho_canvas()
    
    def _on_mousewheel(self, event):
        """Maneja el evento de scroll del mouse"""
        if self.scroll_habilitado and self.canvas:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def crear_header(self):
        """Crea el encabezado con diseño moderno y responsivo"""
        frame_header = ttk.Frame(self.frame_scrollable)
        frame_header.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        frame_header.columnconfigure(0, weight=1)
        frame_header.columnconfigure(1, weight=0)
        
        # Título y logo
        frame_titulo = ttk.Frame(frame_header)
        frame_titulo.grid(row=0, column=0, sticky=tk.W)
        
        titulo = ttk.Label(frame_titulo, 
                          text="🦀 Sistema Experto de Porcelanidae",
                          style='Titulo.TLabel')
        titulo.grid(row=0, column=0, sticky=tk.W)
        
        # Versión
        version = ttk.Label(frame_titulo,
                           text="v2.0 | Identificación Taxonómica Híbrida con Imágenes y Fichas",
                           style='Subtitulo.TLabel',
                           foreground=self.COLORES['gris_medio'])
        version.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
        
        # Reloj
        self.label_reloj = ttk.Label(frame_header,
                                     font=('Segoe UI', 10),
                                     foreground=self.COLORES['gris_medio'])
        self.label_reloj.grid(row=0, column=1, sticky=tk.E, padx=(20, 0))
        
        # Selector de modo
        frame_modo = ttk.Frame(frame_header)
        frame_modo.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(15, 0))
        
        ttk.Label(frame_modo, text="🎯 Modo de identificación:", 
                 style='Subtitulo.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        self.modo_var = tk.StringVar(value="reglas")
        
        # Botones estilo toggle - responsivos
        frame_toggle = ttk.Frame(frame_modo)
        frame_toggle.grid(row=0, column=1, padx=(15, 0), sticky=tk.W)
        
        # Botón Modo Reglas
        self.btn_modo_reglas = ttk.Button(frame_toggle,
                                         text="🔍 Clave Taxonómica",
                                         command=lambda: self.cambiar_modo_animado("reglas"),
                                         style='BotonPrincipal.TButton')
        self.btn_modo_reglas.grid(row=0, column=0, padx=(0, 5))
        
        # Botón Modo Red Neuronal
        self.btn_modo_rn = ttk.Button(frame_toggle,
                                     text="🧠 Red Neuronal",
                                     command=lambda: self.cambiar_modo_animado("red_neuronal"),
                                     style='BotonSecundario.TButton')
        self.btn_modo_rn.grid(row=0, column=1)
        
        # Botón para ocultar/mostrar bienvenida
        self.btn_toggle_bienvenida = ttk.Button(frame_toggle,
                                               text="📖 Ocultar Bienvenida",
                                               command=self.toggle_bienvenida,
                                               style='BotonSecundario.TButton')
        self.btn_toggle_bienvenida.grid(row=0, column=2, padx=(15, 0))
        
        # Botón Acerca de
        self.btn_acerca_de = ttk.Button(frame_toggle,
                                       text="ℹ️ Acerca de",
                                       command=self.mostrar_acerca_de,
                                       style='BotonSecundario.TButton')
        self.btn_acerca_de.grid(row=0, column=3, padx=(15, 0))
        
        # Indicador de imágenes
        if hasattr(self, 'imagenes_disponibles') and self.imagenes_disponibles:
            total = len(self.imagenes_disponibles)
            disponibles = sum(1 for v in self.imagenes_disponibles.values() if v)
            label_imagenes = ttk.Label(frame_toggle,
                                      text=f"📸 {disponibles}/{total} imágenes",
                                      font=('Segoe UI', 9),
                                      foreground=self.COLORES['gris_medio'])
            label_imagenes.grid(row=0, column=4, padx=(15, 0))
        
        # Actualizar estilo inicial
        self.actualizar_botones_modo()
    
    def toggle_bienvenida(self):
        """Alterna la visibilidad del panel de bienvenida"""
        self.mostrar_bienvenida = not self.mostrar_bienvenida
        
        # Actualizar texto del botón
        if self.mostrar_bienvenida:
            self.btn_toggle_bienvenida.config(text="📖 Ocultar Bienvenida")
        else:
            self.btn_toggle_bienvenida.config(text="📖 Mostrar Bienvenida")
        
        # Actualizar visibilidad
        self.actualizar_visibilidad_bienvenida()
    
    def actualizar_visibilidad_bienvenida(self):
        """Actualiza la visibilidad del panel de bienvenida"""
        if hasattr(self, 'frame_bienvenida') and self.frame_bienvenida:
            if self.mostrar_bienvenida:
                self.frame_bienvenida.grid()
            else:
                self.frame_bienvenida.grid_remove()
            
            # Actualizar scroll
            self.actualizar_scroll()
    
    def actualizar_botones_modo(self):
        """Actualiza el estilo de los botones de modo"""
        if self.modo_actual == "reglas":
            self.btn_modo_reglas.config(style='BotonPrincipal.TButton')
            self.btn_modo_rn.config(style='BotonSecundario.TButton')
        else:
            self.btn_modo_reglas.config(style='BotonSecundario.TButton')
            self.btn_modo_rn.config(style='BotonPrincipal.TButton')
    
    def cambiar_modo_animado(self, modo):
        """Cambia de modo con animación suave"""
        if modo == self.modo_actual:
            return
        
        self.modo_actual = modo
        self.modo_var.set(modo)
        self.actualizar_botones_modo()
        
        # Mostrar transición
        self.mostrar_transicion()
        
        # Cambiar contenido después de la animación
        self.root.after(300, self.cambiar_modo)
    
    def mostrar_transicion(self):
        """Muestra una animación de transición"""
        if hasattr(self, 'frame_contenido_principal') and self.frame_contenido_principal:
            for widget in self.frame_contenido_principal.winfo_children():
                try:
                    widget.destroy()
                except:
                    pass
            
            ttk.Label(self.frame_contenido_principal,
                     text="⏳ Cambiando de modo...",
                     style='Titulo.TLabel',
                     foreground=self.COLORES['secundario']).pack(pady=50)
            
            self.root.update_idletasks()
    
    def cambiar_modo(self):
        """Cambia entre los modos de identificación"""
        if not hasattr(self, 'frame_contenido_principal') or not self.frame_contenido_principal:
            return
        
        if not self.frame_contenido_principal.winfo_exists():
            return
        
        # Limpiar contenido anterior
        for widget in self.frame_contenido_principal.winfo_children():
            try:
                widget.destroy()
            except:
                pass
        
        if self.modo_actual == "reglas":
            self.mostrar_modo_reglas()
        else:
            self.mostrar_modo_red_neuronal()
        
        self.actualizar_estado(f"Modo {self.modo_actual.replace('_', ' ').title()} activo")
        self.actualizar_scroll()
    
    def crear_contenido_principal(self):
        """Crea el contenedor principal del contenido"""
        # Panel de bienvenida (visible inicialmente)
        self.frame_bienvenida = ttk.Frame(self.frame_scrollable)
        self.frame_bienvenida.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        self.frame_bienvenida.columnconfigure(0, weight=1)
        self.frame_bienvenida.rowconfigure(0, weight=1)
        
        # Contenido principal (donde van los modos)
        self.frame_contenido_principal = ttk.Frame(self.frame_scrollable)
        self.frame_contenido_principal.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        self.frame_contenido_principal.columnconfigure(0, weight=1)
        self.frame_contenido_principal.rowconfigure(0, weight=1)
        
        # Configurar el grid del frame scrollable
        self.frame_scrollable.rowconfigure(2, weight=1)
        self.frame_scrollable.columnconfigure(0, weight=1)
    
    def crear_footer(self):
        """Crea el pie de página con controles responsivos"""
        frame_footer = ttk.Frame(self.frame_scrollable)
        frame_footer.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        frame_footer.columnconfigure(0, weight=1)
        frame_footer.columnconfigure(1, weight=1)
        
        # Botones de control
        frame_botones = ttk.Frame(frame_footer)
        frame_botones.grid(row=0, column=0, sticky=tk.W)
        
        botones = [
            ("🆕 Nueva Identificación", self.nueva_identificacion, 'BotonPrincipal.TButton'),
            ("📊 Historial", self.mostrar_historial_completo, 'BotonSecundario.TButton'),
            ("⭐ Favoritos", self.mostrar_favoritos, 'BotonSecundario.TButton'),
            ("💾 Exportar", self.exportar_resultados, 'BotonSecundario.TButton')
        ]
        
        for i, (texto, comando, estilo) in enumerate(botones):
            btn = ttk.Button(frame_botones, text=texto, command=comando, style=estilo)
            btn.grid(row=0, column=i, padx=(0, 5))
        
        # Indicadores de estado
        frame_indicadores = ttk.Frame(frame_footer)
        frame_indicadores.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
        
        # Estado
        self.label_estado = ttk.Label(frame_indicadores,
                                     text="🟢 Sistema listo",
                                     style='Subtitulo.TLabel',
                                     foreground='#7f8c8d')
        self.label_estado.grid(row=0, column=0, sticky=tk.E)
        
        # Contador de identificaciones
        self.label_contador = ttk.Label(frame_indicadores,
                                       text="📝 0 identificaciones",
                                       font=('Segoe UI', 9),
                                       foreground=self.COLORES['gris_medio'])
        self.label_contador.grid(row=1, column=0, sticky=tk.E, pady=(2, 0))
        
        # Indicador de scroll
        ttk.Label(frame_footer, 
                 text="📜 Scroll vertical disponible",
                 font=('Segoe UI', 8),
                 foreground=self.COLORES['gris_medio']).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
    
    def crear_barra_estado_mejorada(self):
        """Crea una barra de estado mejorada en la parte inferior"""
        frame_estado = ttk.Frame(self.root)
        frame_estado.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Barra de progreso general
        self.progress_general = ttk.Progressbar(frame_estado,
                                               orient='horizontal',
                                               length=200,
                                               mode='determinate',
                                               style="Custom.Horizontal.TProgressbar")
        self.progress_general.pack(side=tk.RIGHT, padx=(10, 0))
        self.progress_general['value'] = 0
        
        # Etiqueta de progreso
        self.label_progreso = ttk.Label(frame_estado,
                                       text="Progreso: 0%",
                                       font=('Segoe UI', 9),
                                       foreground=self.COLORES['gris_medio'])
        self.label_progreso.pack(side=tk.RIGHT, padx=5)
        
        # Mensaje de estado persistente
        self.label_estado_persistente = ttk.Label(frame_estado,
                                                 text="Bienvenido al Sistema Experto de Porcelanidae",
                                                 font=('Segoe UI', 9),
                                                 foreground=self.COLORES['primario'])
        self.label_estado_persistente.pack(side=tk.LEFT)
    
    def actualizar_reloj(self):
        """Actualiza el reloj en tiempo real"""
        ahora = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, 'label_reloj'):
            self.label_reloj.config(text=f"🕐 {ahora}")
        self.root.after(1000, self.actualizar_reloj)
    
    def formatear_nombre_cientifico(self, nombre_especie: str) -> str:
        """
        Formatea el nombre científico según convenciones taxonómicas:
        - Género con primera letra mayúscula
        - Especie en minúscula
        - Formato: "Género especie"
        
        Args:
            nombre_especie (str): Nombre de la especie en formato 'genero_especie'
            
        Returns:
            str: Nombre formateado correctamente
        """
        try:
            # Reemplazar underscores por espacios
            nombre = nombre_especie.replace('_', ' ')
            
            # Dividir en palabras
            palabras = nombre.split()
            
            if len(palabras) >= 2:
                # Primera palabra (género) con mayúscula inicial
                genero = palabras[0].capitalize()
                
                # Segunda palabra (especie) en minúscula
                especie = palabras[1].lower()
                
                # Unir y devolver
                if len(palabras) > 2:
                    # Si hay más palabras (subespecies, etc.)
                    resto = ' '.join(palabras[2:]).lower()
                    return f"{genero} {especie} {resto}"
                else:
                    return f"{genero} {especie}"
            else:
                # Si solo hay una palabra, capitalizar
                return nombre.capitalize()
                
        except Exception as e:
            print(f"Error formateando nombre científico: {e}")
            return nombre_especie.replace('_', ' ').title()
    
    def mostrar_panel_bienvenida(self):
        """Muestra el panel de bienvenida separado"""
        if not hasattr(self, 'frame_bienvenida') or not self.frame_bienvenida:
            return
        
        if not self.frame_bienvenida.winfo_exists():
            return
        
        for widget in self.frame_bienvenida.winfo_children():
            try:
                widget.destroy()
            except:
                pass
        
        # Frame para la bienvenida
        frame_bienvenida_inner = ttk.Frame(self.frame_bienvenida, style='Card.TFrame')
        frame_bienvenida_inner.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        frame_bienvenida_inner.columnconfigure(0, weight=1)
        frame_bienvenida_inner.rowconfigure(0, weight=1)
        
        # Título del panel
        ttk.Label(frame_bienvenida_inner,
                 text="🎉 ¡Bienvenido!",
                 style='Titulo.TLabel').grid(row=0, column=0, pady=(10, 5))
        
        ttk.Label(frame_bienvenida_inner,
                 text="Sistema Experto Híbrido para Identificación de Porcelanidae",
                 style='Subtitulo.TLabel').grid(row=1, column=0, pady=(0, 15))
        
        # Contenido de la bienvenida en un ScrolledText
        texto_bienvenida = scrolledtext.ScrolledText(frame_bienvenida_inner,
                                                    wrap=tk.WORD,
                                                    width=100,
                                                    height=18,
                                                    font=('Segoe UI', 11),
                                                    bg='white',
                                                    relief='flat',
                                                    padx=20,
                                                    pady=20)
        texto_bienvenida.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=(0, 15))
        
        info_texto = """
🌟 SISTEMA EXPERTO HÍBRIDO PARA IDENTIFICACIÓN DE PORCELANIDAE

Este sistema combina dos metodologías complementarias para la identificación taxonómica de crustáceos de la familia Porcelanidae.


🔍 MODO CLAVE TAXONÓMICA (Reglas)
   • Identificación mediante preguntas dicotómicas guiadas
   • Basado en características morfológicas tradicionales
   • Proceso educativo paso a paso
   • Ideal para usuarios sin experiencia previa
   • 23 especies disponibles

🧠 MODO RED NEURONAL (IA)
   • Identificación mediante inteligencia artificial
   • Predicción instantánea basada en medidas
   • Alta precisión con datos completos
   • Resultados con nivel de confianza
   • 17 especies disponibles

📸 IMÁGENES Y FICHAS TÉCNICAS
   • Imagen de la especie en la pestaña de proceso
   • Ficha técnica completa en la pestaña de resultados
   • Taxonomía, distribución y conservación
   • Miniaturas en historial y favoritos

📊 ESTADÍSTICAS DEL SISTEMA
   • Total de especies identificables: 23
   • Preguntas en clave taxonómica: 12+
   • Precisión del modelo IA: >85%
   • Tiempo promedio de identificación: 30 segundos

Seleccione un modo de identificación en la parte superior para comenzar.
        """
        
        texto_bienvenida.insert(tk.INSERT, info_texto)
        texto_bienvenida.config(state=tk.DISABLED)
        
        # Botón de inicio rápido dentro del panel de bienvenida
        frame_botones_bienvenida = ttk.Frame(frame_bienvenida_inner)
        frame_botones_bienvenida.grid(row=3, column=0, pady=(0, 15))
        
        ttk.Button(frame_botones_bienvenida,
                  text="🚀 Iniciar Identificación por Reglas",
                  command=self.iniciar_identificacion_reglas,
                  style='BotonPrincipal.TButton').grid(row=0, column=0, padx=5)
        
        ttk.Button(frame_botones_bienvenida,
                  text="🧠 Probar Red Neuronal",
                  command=lambda: self.cambiar_modo_animado("red_neuronal"),
                  style='BotonSecundario.TButton').grid(row=0, column=1, padx=5)
        
        ttk.Button(frame_botones_bienvenida,
                  text="📖 Ver Guía Rápida",
                  command=self.mostrar_guia_rapida,
                  style='BotonSecundario.TButton').grid(row=0, column=2, padx=5)
        
        # Botón para ocultar el panel
        ttk.Button(frame_botones_bienvenida,
                  text="✖ Ocultar Panel de Bienvenida",
                  command=self.toggle_bienvenida,
                  style='BotonPeligro.TButton').grid(row=0, column=3, padx=5)
        
        # Configurar expansión
        frame_bienvenida_inner.rowconfigure(2, weight=1)
        self.frame_bienvenida.rowconfigure(0, weight=1)
        self.frame_bienvenida.columnconfigure(0, weight=1)
        
        # Mostrar un mensaje en el contenido principal
        self.mostrar_mensaje_inicial_en_principal()
        
        self.actualizar_scroll()
    
    def mostrar_mensaje_inicial_en_principal(self):
        """Muestra un mensaje inicial en el área principal"""
        if not hasattr(self, 'frame_contenido_principal') or not self.frame_contenido_principal:
            return
        
        if not self.frame_contenido_principal.winfo_exists():
            return
        
        for widget in self.frame_contenido_principal.winfo_children():
            try:
                widget.destroy()
            except:
                pass
        
        ttk.Label(self.frame_contenido_principal,
                 text="👈 Seleccione un modo de identificación en la parte superior\n\n"
                      "o explore el panel de bienvenida para más información.",
                 style='Subtitulo.TLabel',
                 foreground=self.COLORES['gris_medio'],
                 justify='center').pack(pady=50)
    
    def mostrar_guia_rapida(self):
        """Muestra una guía rápida de uso"""
        guia = """
📖 GUÍA RÁPIDA DE USO

🔍 MODO CLAVE TAXONÓMICA:
1. Haga clic en "Iniciar Identificación por Reglas"
2. Responda las preguntas con Sí o No
3. El sistema navegará por el árbol de decisiones
4. Al finalizar, verá la imagen en la pestaña Proceso y la ficha técnica en Resultados

🧠 MODO RED NEURONAL:
1. Complete todos los campos del formulario
2. Verifique que los datos sean correctos
3. Haga clic en "Predecir Especie"
4. El sistema mostrará la imagen en la pestaña Proceso y la ficha técnica en Resultados

📊 GESTIÓN DE RESULTADOS:
• Historial: Guarda todas sus identificaciones con imágenes
• Favoritos: Marque identificaciones importantes
• Exportar: Guarde resultados en archivo

📸 IMÁGENES Y FICHAS:
• Imagen de la especie en la pestaña Proceso de Identificación
• Ficha técnica completa en la pestaña Resultados
• Miniaturas disponibles en historial y favoritos
        """
        
        messagebox.showinfo("Guía Rápida de Uso", guia)
    
    def mostrar_acerca_de(self):
        """Muestra la ventana Acerca de con el enlace al portafolio"""
        ventana_acerca = tk.Toplevel(self.root)
        ventana_acerca.title("ℹ️ Acerca del Sistema Experto Porcelanidae")
        ventana_acerca.geometry("600x550")
        ventana_acerca.configure(bg=self.COLORES['fondo'])
        ventana_acerca.resizable(False, False)
        
        # Centrar ventana
        ventana_acerca.transient(self.root)
        ventana_acerca.grab_set()
        
        # Frame principal
        frame_principal = ttk.Frame(ventana_acerca, padding="30")
        frame_principal.pack(fill="both", expand=True)
        
        # Icono
        ttk.Label(frame_principal,
                 text="🦀",
                 font=('Segoe UI', 48)).pack(pady=(0, 10))
        
        # Título
        ttk.Label(frame_principal,
                 text="Sistema Experto de Porcelanidae",
                 style='Titulo.TLabel').pack(pady=5)
        
        # Versión
        ttk.Label(frame_principal,
                 text="Versión 2.0",
                 style='Subtitulo.TLabel',
                 foreground=self.COLORES['gris_medio']).pack(pady=2)
        
        # Separador
        ttk.Separator(frame_principal, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Descripción
        descripcion = """
        Sistema experto híbrido para la identificación taxonómica de 
        crustáceos de la familia Porcelanidae.
        
        Combina un sistema basado en reglas con redes neuronales 
        para ofrecer una identificación precisa y confiable.
        """
        
        ttk.Label(frame_principal,
                 text=descripcion,
                 font=('Segoe UI', 10),
                 background=self.COLORES['fondo'],
                 justify='center').pack(pady=5)
        
        # Separador
        ttk.Separator(frame_principal, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Información del autor
        ttk.Label(frame_principal,
                 text="👨‍💻 Desarrollado por:",
                 font=('Segoe UI', 10, 'bold'),
                 background=self.COLORES['fondo']).pack(pady=2)
        
        ttk.Label(frame_principal,
                 text="José Morillo",
                 font=('Segoe UI', 10),
                 background=self.COLORES['fondo']).pack(pady=2)
        
        # ======================== ENLACE AL PORTAFOLIO ========================
        frame_enlace = ttk.Frame(frame_principal)
        frame_enlace.pack(pady=15)
        
        # Label de icono
        ttk.Label(frame_enlace,
                 text="🔗 ",
                 font=('Segoe UI', 11),
                 background=self.COLORES['fondo']).pack(side=tk.LEFT)
        
        # Crear label como enlace usando tk.Label (no ttk.Label) para mejor control
        label_enlace = tk.Label(frame_enlace,
                               text="Portafolio Digital",
                               font=('Segoe UI', 11, 'underline'),
                               fg=self.COLORES['secundario'],
                               bg=self.COLORES['fondo'],
                               cursor='hand2')
        label_enlace.pack(side=tk.LEFT)
        
        # Eventos del enlace
        label_enlace.bind("<Button-1>", lambda e: self.abrir_portafolio())
        label_enlace.bind("<Enter>", lambda e: label_enlace.config(fg='#1a6fa0'))  # Color más oscuro al pasar el mouse
        label_enlace.bind("<Leave>", lambda e: label_enlace.config(fg=self.COLORES['secundario']))
        
        # URL debajo del enlace (como texto informativo)
        ttk.Label(frame_principal,
                 text=self.url_portafolio,
                 font=('Segoe UI', 8),
                 foreground=self.COLORES['gris_medio'],
                 background=self.COLORES['fondo']).pack(pady=(5, 0))
        
        # Mensaje de ayuda
        ttk.Label(frame_principal,
                 text="💡 Haz clic en el enlace para visitar mi portafolio",
                 font=('Segoe UI', 9),
                 foreground=self.COLORES['gris_medio'],
                 background=self.COLORES['fondo']).pack(pady=5)
        # ======================== FIN ENLACE ========================
        
        # Separador
        ttk.Separator(frame_principal, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Tecnologías utilizadas
        ttk.Label(frame_principal,
                 text="🛠️ Tecnologías utilizadas:",
                 font=('Segoe UI', 10, 'bold'),
                 background=self.COLORES['fondo']).pack(pady=2)
        
        ttk.Label(frame_principal,
                 text="Python 3.13 | Tkinter | Scikit-learn | Pillow",
                 font=('Segoe UI', 9),
                 foreground=self.COLORES['gris_medio'],
                 background=self.COLORES['fondo']).pack(pady=2)
        
        # Separador
        ttk.Separator(frame_principal, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Botón de cerrar
        ttk.Button(frame_principal,
                  text="Cerrar",
                  command=ventana_acerca.destroy,
                  style='BotonPrincipal.TButton').pack(pady=10)
        
        # Configurar grid
        ventana_acerca.columnconfigure(0, weight=1)
        ventana_acerca.rowconfigure(0, weight=1)
    
    def abrir_portafolio(self):
        """Abre el portafolio en el navegador predeterminado"""
        try:
            webbrowser.open(self.url_portafolio)
            messagebox.showinfo("Portafolio", 
                               f"🌐 Abriendo el portafolio en el navegador:\n\n{self.url_portafolio}")
        except Exception as e:
            messagebox.showerror("Error", 
                               f"No se pudo abrir el enlace:\n{str(e)}\n\n"
                               f"Puedes visitar manualmente:\n{self.url_portafolio}")
    
    def mostrar_modo_reglas(self):
        """Muestra la interfaz del modo reglas mejorada"""
        # Ocultar panel de bienvenida automáticamente al iniciar un modo
        if self.mostrar_bienvenida:
            self.mostrar_bienvenida = False
            self.btn_toggle_bienvenida.config(text="📖 Mostrar Bienvenida")
            self.actualizar_visibilidad_bienvenida()
        
        if not hasattr(self, 'frame_contenido_principal') or not self.frame_contenido_principal:
            return
        
        if not self.frame_contenido_principal.winfo_exists():
            return
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.frame_contenido_principal)
        self.notebook.pack(fill="both", expand=True)
        
        # ======================== PESTAÑA 1: PROCESO ========================
        pestaña_proceso = ttk.Frame(self.notebook)
        self.notebook.add(pestaña_proceso, text="🔍 Proceso de Identificación")
        pestaña_proceso.columnconfigure(0, weight=1)
        pestaña_proceso.rowconfigure(0, weight=1)
        pestaña_proceso.rowconfigure(1, weight=0)
        
        # Panel de proceso - aquí se mostrará la imagen
        self.frame_proceso = ttk.LabelFrame(pestaña_proceso, text="🔍 Proceso de Identificación", padding="20")
        self.frame_proceso.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.frame_proceso.columnconfigure(0, weight=1)
        self.frame_proceso.rowconfigure(0, weight=1)
        
        # Mensaje inicial
        label_inicial_proceso = ttk.Label(self.frame_proceso,
                                         text="🔄 Haga clic en 'Iniciar Identificación' para comenzar",
                                         style='Subtitulo.TLabel',
                                         foreground=self.COLORES['gris_medio'])
        label_inicial_proceso.grid(row=0, column=0, pady=20)
        
        # Panel de información
        frame_info = ttk.LabelFrame(pestaña_proceso, text="📋 Información del Modo Reglas", padding="15")
        frame_info.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_info.columnconfigure(0, weight=1)
        
        info_texto = f"""
🦀 CLAVE TAXONÓMICA DICOTÓMICA

• Especies identificables: {self.sistema_reglas.obtener_total_especies()}
• Basado en características morfológicas
• Proceso guiado paso a paso
• Preguntas dicotómicas (Sí/No)
• Imagen de la especie en esta pestaña al finalizar
        """
        
        label_info = ttk.Label(frame_info, text=info_texto, style='Pregunta.TLabel')
        label_info.grid(row=0, column=0, sticky=tk.W)
        
        # Botones de control
        frame_botones = ttk.Frame(frame_info)
        frame_botones.grid(row=1, column=0, sticky=tk.W, pady=(15, 0))
        
        self.boton_iniciar_reglas = ttk.Button(frame_botones,
                                             text="🚀 Iniciar Identificación",
                                             command=self.iniciar_identificacion_reglas,
                                             style='BotonPrincipal.TButton')
        self.boton_iniciar_reglas.grid(row=0, column=0, padx=(0, 10))
        
        self.boton_cancelar_reglas = ttk.Button(frame_botones,
                                              text="⏹️ Cancelar",
                                              command=self.cancelar_identificacion,
                                              state='disabled',
                                              style='BotonPeligro.TButton')
        self.boton_cancelar_reglas.grid(row=0, column=1)
        
        # ======================== PESTAÑA 2: RESULTADOS ========================
        pestaña_resultados = ttk.Frame(self.notebook)
        self.notebook.add(pestaña_resultados, text="📊 Resultados")
        pestaña_resultados.columnconfigure(0, weight=1)
        pestaña_resultados.rowconfigure(0, weight=1)
        
        # Panel de resultados - aquí se mostrará la ficha técnica
        self.frame_resultados_reglas = ttk.LabelFrame(pestaña_resultados, text="📊 Ficha Técnica", padding="15")
        self.frame_resultados_reglas.pack(fill="both", expand=True)
        self.frame_resultados_reglas.columnconfigure(0, weight=1)
        self.frame_resultados_reglas.rowconfigure(0, weight=1)
        
        # Mensaje inicial en resultados
        label_resultados = ttk.Label(self.frame_resultados_reglas,
                                    text="📋 La ficha técnica aparecerá aquí al finalizar la identificación.",
                                    style='Pregunta.TLabel',
                                    foreground=self.COLORES['gris_medio'])
        label_resultados.pack(pady=50)
        
        self.actualizar_scroll()
    
    def mostrar_modo_red_neuronal(self):
        """Muestra la interfaz del modo red neuronal"""
        # Ocultar panel de bienvenida automáticamente al iniciar un modo
        if self.mostrar_bienvenida:
            self.mostrar_bienvenida = False
            self.btn_toggle_bienvenida.config(text="📖 Mostrar Bienvenida")
            self.actualizar_visibilidad_bienvenida()
        
        if not hasattr(self, 'frame_contenido_principal') or not self.frame_contenido_principal:
            return
        
        if not self.frame_contenido_principal.winfo_exists():
            return
        
        # Verificar si la red neuronal está disponible
        if not hasattr(self.red_neuronal, 'modelo') or self.red_neuronal.modelo is None:
            self.mostrar_error_red_neuronal()
            return
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.frame_contenido_principal)
        self.notebook.pack(fill="both", expand=True)
        
        # ======================== PESTAÑA 1: FORMULARIO ========================
        pestaña_formulario = ttk.Frame(self.notebook)
        self.notebook.add(pestaña_formulario, text="📝 Formulario")
        pestaña_formulario.columnconfigure(0, weight=1)
        pestaña_formulario.rowconfigure(0, weight=0)
        pestaña_formulario.rowconfigure(1, weight=1)
        
        # Panel de información
        frame_info = ttk.LabelFrame(pestaña_formulario, text="🧠 Información del Modo Red Neuronal", padding="15")
        frame_info.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        frame_info.columnconfigure(0, weight=1)
        
        info_texto = f"""
Este modo utiliza una red neuronal artificial entrenada con {self.red_neuronal.obtener_total_especies()} especies.
Ingrese las características morfológicas del ejemplar para obtener una predicción.

🎯 Precisión del modelo: Alta (entrenado con datos sintéticos balanceados)
⚡ Velocidad de predicción: Instantánea
📸 Imagen en pestaña Proceso y Ficha técnica en Resultados
        """
        
        label_info = ttk.Label(frame_info, text=info_texto, style='Pregunta.TLabel')
        label_info.grid(row=0, column=0, sticky=tk.W)
        
        # Formulario de características
        frame_formulario = ttk.LabelFrame(pestaña_formulario, text="📝 Características del Ejemplar", padding="20")
        frame_formulario.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        frame_formulario.columnconfigure(0, weight=1)
        
        # Crear formulario
        self.crear_formulario_caracteristicas(frame_formulario)
        
        # ======================== PESTAÑA 2: PROCESO (con imagen) ========================
        pestaña_proceso_rn = ttk.Frame(self.notebook)
        self.notebook.add(pestaña_proceso_rn, text="🔍 Proceso")
        pestaña_proceso_rn.columnconfigure(0, weight=1)
        pestaña_proceso_rn.rowconfigure(0, weight=1)
        
        # Panel de proceso para RN
        self.frame_proceso = ttk.LabelFrame(pestaña_proceso_rn, text="🔍 Imagen de la Especie", padding="20")
        self.frame_proceso.pack(fill="both", expand=True)
        self.frame_proceso.columnconfigure(0, weight=1)
        self.frame_proceso.rowconfigure(0, weight=1)
        
        label_proceso_rn = ttk.Label(self.frame_proceso,
                                    text="📸 La imagen de la especie aparecerá aquí después de la predicción.",
                                    style='Pregunta.TLabel',
                                    foreground=self.COLORES['gris_medio'])
        label_proceso_rn.pack(pady=50)
        
        # ======================== PESTAÑA 3: RESULTADOS ========================
        pestaña_resultados_rn = ttk.Frame(self.notebook)
        self.notebook.add(pestaña_resultados_rn, text="📊 Resultados")
        pestaña_resultados_rn.columnconfigure(0, weight=1)
        pestaña_resultados_rn.rowconfigure(0, weight=1)
        
        # Panel de resultados para RN
        self.frame_resultados_rn = ttk.LabelFrame(pestaña_resultados_rn, text="📊 Ficha Técnica", padding="15")
        self.frame_resultados_rn.pack(fill="both", expand=True)
        self.frame_resultados_rn.columnconfigure(0, weight=1)
        self.frame_resultados_rn.rowconfigure(0, weight=1)
        
        label_resultados_rn = ttk.Label(self.frame_resultados_rn,
                                       text="📋 La ficha técnica aparecerá aquí después de la predicción.",
                                       style='Pregunta.TLabel',
                                       foreground=self.COLORES['gris_medio'])
        label_resultados_rn.pack(pady=50)
        
        self.actualizar_scroll()
    
    def mostrar_error_red_neuronal(self):
        """Muestra mensaje de error cuando la red neuronal no está disponible"""
        if not hasattr(self, 'frame_contenido_principal') or not self.frame_contenido_principal:
            return
        
        if not self.frame_contenido_principal.winfo_exists():
            return
        
        frame_error = ttk.Frame(self.frame_contenido_principal)
        frame_error.pack(fill="both", expand=True)
        frame_error.columnconfigure(0, weight=1)
        
        mensaje_error = """
⚠️ Modo Red Neuronal No Disponible

El modelo de red neuronal no está cargado o no está disponible en este momento.

🔧 Soluciones:
• Use el modo Clave Taxonómica (completamente funcional)
• Verifique que el archivo models/modelo_entrenado.pkl exista
• Reinicie la aplicación

El modo Clave Taxonómica puede identificar todas las 23 especies disponibles.
        """
        
        texto_error = scrolledtext.ScrolledText(frame_error,
                                               wrap=tk.WORD,
                                               width=100,
                                               height=15,
                                               font=('Segoe UI', 11),
                                               bg='#fff5f5',
                                               fg='#c0392b',
                                               relief='flat')
        texto_error.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        texto_error.insert(tk.INSERT, mensaje_error)
        texto_error.config(state=tk.DISABLED)
        
        frame_error.rowconfigure(0, weight=1)
        frame_error.columnconfigure(0, weight=1)
        
        self.actualizar_scroll()
    
    def crear_formulario_caracteristicas(self, parent):
        """Crea el formulario de características para la red neuronal"""
        # Frame para los campos del formulario
        frame_campos = ttk.Frame(parent)
        frame_campos.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        frame_campos.columnconfigure(0, weight=0)
        frame_campos.columnconfigure(1, weight=0)
        frame_campos.columnconfigure(2, weight=1)
        
        # longitud_caparazon
        ttk.Label(frame_campos, text="Longitud del caparazón (mm):", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.entry_longitud = ttk.Entry(frame_campos, width=15, font=('Segoe UI', 10))
        self.entry_longitud.grid(row=0, column=1, padx=(10, 20), pady=8, sticky=tk.W)
        ttk.Label(frame_campos, text="Ej: 12.5", font=('Segoe UI', 9), 
                 foreground=self.COLORES['gris_medio']).grid(row=0, column=2, sticky=tk.W)
        
        # setas_margen_frontal
        ttk.Label(frame_campos, text="Setas en margen frontal:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.combo_setas = ttk.Combobox(frame_campos, values=["No", "Sí"], width=13, 
                                       state="readonly", font=('Segoe UI', 10))
        self.combo_setas.grid(row=1, column=1, padx=(10, 20), pady=8, sticky=tk.W)
        
        # n_dientes_margen_flexor
        ttk.Label(frame_campos, text="N° dientes margen flexor:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.combo_dientes = ttk.Combobox(frame_campos, values=["0", "1", "2", "3", "4"], width=13, 
                                         state="readonly", font=('Segoe UI', 10))
        self.combo_dientes.grid(row=2, column=1, padx=(10, 20), pady=8, sticky=tk.W)
        
        # patron_granulacion_quelipodos
        ttk.Label(frame_campos, text="Patrón de granulación:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.combo_granulacion = ttk.Combobox(frame_campos, 
                                             values=["Ausente", "Finas", "Gruesas", "Mixtas"], 
                                             width=13, state="readonly", font=('Segoe UI', 10))
        self.combo_granulacion.grid(row=3, column=1, padx=(10, 20), pady=8, sticky=tk.W)
        
        # n_placas_telson
        ttk.Label(frame_campos, text="N° placas telson:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=8)
        self.combo_placas = ttk.Combobox(frame_campos, values=["5", "7"], width=13, 
                                        state="readonly", font=('Segoe UI', 10))
        self.combo_placas.grid(row=4, column=1, padx=(10, 20), pady=8, sticky=tk.W)
        
        # tipo_quilla_abdominal
        ttk.Label(frame_campos, text="Tipo de quilla abdominal:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=8)
        self.combo_quilla = ttk.Combobox(frame_campos, 
                                        values=["Recta", "Curvada", "Discontinua"], 
                                        width=13, state="readonly", font=('Segoe UI', 10))
        self.combo_quilla.grid(row=5, column=1, padx=(10, 20), pady=8, sticky=tk.W)
        
        # Botones del formulario
        frame_botones_form = ttk.Frame(parent)
        frame_botones_form.grid(row=1, column=0, pady=20)
        
        ttk.Button(frame_botones_form, text="🧠 Predecir Especie", 
                  command=self.predecir_red_neuronal,
                  style='BotonPrincipal.TButton').grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(frame_botones_form, text="🔄 Limpiar Formulario",
                  command=self.limpiar_formulario,
                  style='BotonSecundario.TButton').grid(row=0, column=1)
        
        # Botón para mostrar bienvenida nuevamente
        ttk.Button(frame_botones_form, text="📖 Mostrar Bienvenida",
                  command=self.mostrar_bienvenida_nuevamente,
                  style='BotonSecundario.TButton').grid(row=0, column=2, padx=(10, 0))
    
    def mostrar_bienvenida_nuevamente(self):
        """Muestra el panel de bienvenida nuevamente"""
        self.mostrar_bienvenida = True
        self.btn_toggle_bienvenida.config(text="📖 Ocultar Bienvenida")
        self.actualizar_visibilidad_bienvenida()
        self.mostrar_panel_bienvenida()
        self.actualizar_estado("Panel de bienvenida mostrado")
    
    def iniciar_identificacion_reglas(self):
        """Inicia el proceso de identificación por reglas"""
        try:
            print("🚀 Iniciando identificación por reglas...")
            
            # Verificar que el sistema esté listo
            if not hasattr(self, 'sistema_reglas') or self.sistema_reglas is None:
                messagebox.showerror("Error", "El sistema de reglas no está disponible")
                return
            
            # Verificar que el frame_proceso existe
            if not hasattr(self, 'frame_proceso') or not self.frame_proceso:
                print("⚠️ Frame proceso no inicializado")
                messagebox.showerror("Error", "El sistema no está completamente inicializado")
                return
            
            # Limpiar panel de proceso
            if self.frame_proceso.winfo_exists():
                for widget in self.frame_proceso.winfo_children():
                    try:
                        widget.destroy()
                    except:
                        pass
            
            # Limpiar resultados anteriores
            if hasattr(self, 'frame_resultados_reglas') and self.frame_resultados_reglas:
                if self.frame_resultados_reglas.winfo_exists():
                    for widget in self.frame_resultados_reglas.winfo_children():
                        try:
                            widget.destroy()
                        except:
                            pass
                    # Volver a poner el mensaje inicial
                    label_resultados = ttk.Label(self.frame_resultados_reglas,
                                                text="📋 La ficha técnica aparecerá aquí al finalizar la identificación.",
                                                style='Pregunta.TLabel',
                                                foreground=self.COLORES['gris_medio'])
                    label_resultados.pack(pady=50)
            
            # Reiniciar estado
            self.reiniciar_estado_identificacion()
            self.pregunta_actual = "pregunta_1"
            self.subpregunta_actual = None
            self.identificacion_activa = True
            
            # Cambiar a la pestaña de proceso
            if self.notebook:
                try:
                    self.notebook.select(0)
                except:
                    pass
            
            # Actualizar botones
            if (hasattr(self, 'boton_iniciar_reglas') and 
                self.boton_iniciar_reglas and 
                self.boton_iniciar_reglas.winfo_exists()):
                self.boton_iniciar_reglas.config(state='disabled')
            
            if (hasattr(self, 'boton_cancelar_reglas') and 
                self.boton_cancelar_reglas and 
                self.boton_cancelar_reglas.winfo_exists()):
                self.boton_cancelar_reglas.config(state='normal')
            
            # Actualizar estado
            self.actualizar_estado("Identificación por reglas iniciada")
            
            # Mostrar primera pregunta
            self.mostrar_pregunta_actual()
            
            print("✅ Identificación por reglas iniciada correctamente")
            
        except Exception as e:
            print(f"❌ Error al iniciar identificación: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo iniciar la identificación: {str(e)}")
            # Asegurarse de reactivar botones en caso de error
            if (hasattr(self, 'boton_iniciar_reglas') and 
                self.boton_iniciar_reglas and 
                self.boton_iniciar_reglas.winfo_exists()):
                self.boton_iniciar_reglas.config(state='normal')
            
            if (hasattr(self, 'boton_cancelar_reglas') and 
                self.boton_cancelar_reglas and 
                self.boton_cancelar_reglas.winfo_exists()):
                self.boton_cancelar_reglas.config(state='disabled')
    
    def mostrar_pregunta_actual(self):
        """Muestra la pregunta actual en la interfaz"""
        if not self.identificacion_activa:
            return
        
        # Verificar que el frame_proceso existe
        if not hasattr(self, 'frame_proceso') or not self.frame_proceso:
            print("⚠️ Frame proceso no disponible")
            return
        
        if not self.frame_proceso.winfo_exists():
            print("⚠️ Frame proceso no existe")
            return
        
        # Limpiar panel de proceso
        for widget in self.frame_proceso.winfo_children():
            try:
                widget.destroy()
            except:
                pass
        
        if self.pregunta_actual is None:
            self.mostrar_resultado("Error: No hay pregunta actual")
            return
        
        # Obtener pregunta
        pregunta_data = self.sistema_reglas.obtener_pregunta(self.pregunta_actual)
        
        if not pregunta_data:
            self.mostrar_resultado("Error: No se pudo cargar la pregunta")
            return
        
        # VERIFICAR SI ES UN GÉNERO (contiene subpreguntas)
        if self._es_genero(pregunta_data):
            if self.subpregunta_actual is None:
                # Es la primera vez que entramos al género, obtener primera subpregunta
                subpreguntas = self._obtener_subpreguntas(pregunta_data)
                if subpreguntas:
                    self.subpregunta_actual = subpreguntas[0]
                    # Recargar con la subpregunta
                    self.mostrar_pregunta_actual()
                    return
                else:
                    self.mostrar_resultado("Error: No se encontraron subpreguntas en el género")
                    return
            
            # Obtener datos de la subpregunta actual
            subpregunta_data = pregunta_data.get(self.subpregunta_actual)
            if not subpregunta_data or 'texto' not in subpregunta_data:
                self.mostrar_resultado("Error: Subpregunta inválida")
                return
            
            texto_pregunta = subpregunta_data['texto']
            es_subpregunta = True
            
        else:
            # Es una pregunta normal
            if 'texto' not in pregunta_data:
                self.mostrar_resultado("Error: Pregunta sin texto")
                return
            
            texto_pregunta = pregunta_data['texto']
            es_subpregunta = False
        
        # Mostrar número de pregunta
        num_pregunta = len(self.historial_preguntas) + 1
        label_numero = ttk.Label(self.frame_proceso,
                                text=f"📋 Pregunta {num_pregunta}",
                                style='Subtitulo.TLabel')
        label_numero.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        # Mostrar contexto si es subpregunta
        if es_subpregunta:
            genero = self._obtener_nombre_genero(self.pregunta_actual)
            label_contexto = ttk.Label(self.frame_proceso,
                                      text=f"Género: {genero}",
                                      style='Pregunta.TLabel',
                                      foreground=self.COLORES['gris_medio'])
            label_contexto.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # Mostrar pregunta
        frame_pregunta = ttk.Frame(self.frame_proceso)
        frame_pregunta.grid(row=2 if es_subpregunta else 1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        frame_pregunta.columnconfigure(0, weight=1)
        
        label_pregunta = ttk.Label(frame_pregunta,
                                  text=texto_pregunta,
                                  style='Pregunta.TLabel',
                                  background='#e8f4f8',
                                  padding=15,
                                  borderwidth=1,
                                  relief='solid')
        label_pregunta.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Botones de respuesta
        frame_botones = ttk.Frame(self.frame_proceso)
        frame_botones.grid(row=3 if es_subpregunta else 2, column=0, sticky=tk.W, pady=10)
        
        # Pasar los datos correctos según si es subpregunta o no
        if es_subpregunta:
            datos_pregunta = subpregunta_data
        else:
            datos_pregunta = pregunta_data
        
        ttk.Button(frame_botones, text="✅ Sí", 
                  command=lambda: self.procesar_respuesta(True, datos_pregunta, es_subpregunta),
                  style='BotonPrincipal.TButton',
                  width=8).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(frame_botones, text="❌ No", 
                  command=lambda: self.procesar_respuesta(False, datos_pregunta, es_subpregunta),
                  style='BotonPrincipal.TButton',
                  width=8).grid(row=0, column=1)
        
        # Mostrar progreso
        self.mostrar_barra_progreso()
        
        # Actualizar scroll
        self.actualizar_scroll()
    
    def _es_genero(self, pregunta_data: Dict) -> bool:
        """Determina si los datos de pregunta representan un género"""
        if not isinstance(pregunta_data, dict):
            return False
        
        # Un género tiene subpreguntas (claves que empiezan con 'pregunta_')
        return any(key.startswith('pregunta_') for key in pregunta_data.keys())
    
    def _obtener_subpreguntas(self, genero_data: Dict) -> List[str]:
        """Obtiene las subpreguntas de un género en orden"""
        subpreguntas = [key for key in genero_data.keys() if key.startswith('pregunta_')]
        # Ordenar por número
        subpreguntas.sort(key=lambda x: int(x.split('_')[1]) if x.split('_')[1].isdigit() else 0)
        return subpreguntas
    
    def _obtener_nombre_genero(self, nodo_genero: str) -> str:
        """Obtiene el nombre legible del género"""
        nombres = {
            'genero_petrolisthes': 'Petrolisthes',
            'genero_pachycheles': 'Pachycheles', 
            'genero_megalobrachium': 'Megalobrachium'
        }
        return nombres.get(nodo_genero, nodo_genero.replace('genero_', '').title())
    
    def obtener_total_preguntas(self):
        """Estima el total de preguntas para la barra de progreso"""
        return min(len(self.historial_preguntas) + 5, 10)
    
    def mostrar_barra_progreso(self):
        """Muestra la barra de progreso"""
        if not hasattr(self, 'frame_proceso') or not self.frame_proceso:
            return
        
        if not self.frame_proceso.winfo_exists():
            return
        
        frame_progreso = ttk.Frame(self.frame_proceso)
        frame_progreso.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=20)
        
        progreso = len(self.historial_preguntas) / self.obtener_total_preguntas()
        
        ttk.Label(frame_progreso, text="Progreso:", 
                 style='Subtitulo.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        # Barra de progreso
        self.barra_progreso = ttk.Progressbar(frame_progreso, 
                                            orient='horizontal',
                                            length=400,
                                            mode='determinate',
                                            style="Custom.Horizontal.TProgressbar")
        self.barra_progreso.grid(row=0, column=1, padx=(10, 10), sticky=(tk.W, tk.E))
        self.barra_progreso['value'] = progreso * 100
        
        ttk.Label(frame_progreso, text=f"{int(progreso * 100)}%",
                 style='Subtitulo.TLabel').grid(row=0, column=2)
        
        frame_progreso.columnconfigure(1, weight=1)
    
    def procesar_respuesta(self, respuesta: bool, pregunta_data: dict, es_subpregunta: bool = False):
        """Procesa la respuesta del usuario"""
        if not self.identificacion_activa:
            return
        
        # Guardar en historial
        texto_pregunta = pregunta_data.get('texto', 'Pregunta sin texto')
        self.historial_preguntas.append({
            'pregunta': texto_pregunta,
            'respuesta': 'Sí' if respuesta else 'No',
            'timestamp': time.strftime("%H:%M:%S")
        })
        
        # Determinar siguiente paso
        siguiente = pregunta_data['si'] if respuesta else pregunta_data['no']
        
        # Verificar si es una especie final
        if self.sistema_reglas.es_especie_final(siguiente):
            self.mostrar_resultado_final(siguiente)
        else:
            # Manejar transiciones entre géneros y subpreguntas
            if es_subpregunta:
                # Estamos en una subpregunta de un género
                if siguiente.startswith('pregunta_'):
                    # Siguiente subpregunta del mismo género
                    self.subpregunta_actual = siguiente
                else:
                    # Salimos del género, siguiente es un nuevo nodo
                    self.pregunta_actual = siguiente
                    self.subpregunta_actual = None
            else:
                # Pregunta normal
                self.pregunta_actual = siguiente
                self.subpregunta_actual = None
            
            self.mostrar_pregunta_actual()
    
    def mostrar_resultado_final(self, especie: str):
        """
        Muestra el resultado final:
        - IMAGEN en la pestaña de Proceso
        - FICHA TÉCNICA en la pestaña de Resultados
        """
        if not self.identificacion_activa:
            return
        
        self.especie_actual = especie
        
        # Formatear nombre CIENTÍFICAMENTE CORRECTO
        nombre_formateado = self.formatear_nombre_cientifico(especie)
        nombre_comun = self.fichas.obtener_nombre_comun(especie) if self.fichas.tiene_ficha(especie) else ""
        
        # ======================== PESTAÑA DE PROCESO: MOSTRAR IMAGEN ========================
        if hasattr(self, 'frame_proceso') and self.frame_proceso:
            if self.frame_proceso.winfo_exists():
                # Limpiar panel de proceso
                for widget in self.frame_proceso.winfo_children():
                    try:
                        widget.destroy()
                    except:
                        pass
                
                # Título de éxito
                frame_titulo = ttk.Frame(self.frame_proceso)
                frame_titulo.pack(fill=tk.X, pady=10)
                
                ttk.Label(frame_titulo, text="🎉", font=('Segoe UI', 36)).pack(pady=5)
                ttk.Label(frame_titulo,
                         text="¡IDENTIFICACIÓN EXITOSA!",
                         style='Titulo.TLabel',
                         foreground=self.COLORES['exito']).pack(pady=5)
                
                # Nombre científico
                ttk.Label(frame_titulo,
                         text=nombre_formateado,
                         style='CientificoResultado.TLabel').pack(pady=5)
                
                if nombre_comun:
                    ttk.Label(frame_titulo,
                             text=f"📌 {nombre_comun}",
                             style='Subtitulo.TLabel').pack(pady=2)
                
                ttk.Label(frame_titulo,
                         text=f"Preguntas: {len(self.historial_preguntas)} | Hora: {time.strftime('%H:%M:%S')}",
                         font=('Segoe UI', 9),
                         foreground=self.COLORES['gris_medio']).pack(pady=2)
                
                ttk.Separator(self.frame_proceso, orient='horizontal').pack(fill=tk.X, pady=10)
                
                # ======================== IMAGEN ========================
                frame_imagen = ttk.LabelFrame(self.frame_proceso, text="📸 Imagen de la Especie", padding="10")
                frame_imagen.pack(fill=tk.X, pady=10, padx=5)
                
                # Contenedor para centrar la imagen
                frame_imagen_contenedor = ttk.Frame(frame_imagen)
                frame_imagen_contenedor.pack()
                
                # Intentar cargar la imagen
                try:
                    from PIL import Image, ImageTk
                    
                    # Obtener ruta de la imagen
                    ruta_imagen = ConfigImagenes.obtener_ruta_imagen(especie)
                    
                    if ruta_imagen:
                        # Cargar la imagen
                        img = Image.open(ruta_imagen)
                        
                        # Redimensionar manteniendo proporción
                        ancho_max, alto_max = 400, 350
                        ancho_orig, alto_orig = img.size
                        proporcion = min(ancho_max / ancho_orig, alto_max / alto_orig)
                        nuevo_ancho = int(ancho_orig * proporcion)
                        nuevo_alto = int(alto_orig * proporcion)
                        
                        try:
                            img_resized = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                        except AttributeError:
                            img_resized = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
                        
                        photo = ImageTk.PhotoImage(img_resized)
                        
                        # Label para la imagen
                        label_imagen = ttk.Label(frame_imagen_contenedor, image=photo, background=self.COLORES['fondo'])
                        label_imagen.image = photo
                        label_imagen.pack(pady=10)
                        
                    else:
                        ttk.Label(frame_imagen_contenedor, 
                                 text="📷\nImagen no disponible",
                                 font=('Segoe UI', 16),
                                 foreground=self.COLORES['gris_medio'],
                                 background=self.COLORES['fondo'],
                                 justify='center').pack(pady=30)
                        
                except Exception as e:
                    print(f"⚠️ Error al cargar imagen: {e}")
                    ttk.Label(frame_imagen_contenedor, 
                             text="📷\nImagen no disponible",
                             font=('Segoe UI', 16),
                             foreground=self.COLORES['gris_medio'],
                             background=self.COLORES['fondo'],
                             justify='center').pack(pady=30)
                
                # Botones de acción
                frame_acciones = ttk.Frame(self.frame_proceso)
                frame_acciones.pack(pady=15)
                
                ttk.Button(frame_acciones,
                          text="⭐ Agregar a Favoritos",
                          command=lambda: self.agregar_favorito(especie),
                          style='BotonSecundario.TButton').pack(side=tk.LEFT, padx=5)
                
                ttk.Button(frame_acciones,
                          text="📋 Ver Detalles del Proceso",
                          command=self.mostrar_detalles_proceso,
                          style='BotonSecundario.TButton').pack(side=tk.LEFT, padx=5)
        
        # ======================== PESTAÑA DE RESULTADOS: FICHA TÉCNICA ========================
        if hasattr(self, 'frame_resultados_reglas') and self.frame_resultados_reglas:
            if self.frame_resultados_reglas.winfo_exists():
                # Limpiar panel de resultados
                for widget in self.frame_resultados_reglas.winfo_children():
                    try:
                        widget.destroy()
                    except:
                        pass
                
                # Mostrar la ficha técnica
                self.mostrar_ficha_tecnica_en_resultados(self.frame_resultados_reglas, especie, nombre_formateado, nombre_comun)
        
        # Guardar resultado
        self.resultados.append({
            'especie': especie,
            'modo': 'reglas',
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'preguntas': len(self.historial_preguntas),
            'nombre_comun': nombre_comun
        })
        
        # Cambiar a la pestaña de resultados
        if self.notebook:
            try:
                self.notebook.select(1)
            except:
                pass
        
        # Finalizar identificación
        self.finalizar_identificacion()
        
        # Actualizar estado
        self.actualizar_estado(f"Identificación completada: {nombre_formateado}")
        
        # Actualizar scroll
        self.actualizar_scroll()
    
    def mostrar_ficha_tecnica_en_resultados(self, frame_destino, especie, nombre_formateado=None, nombre_comun=None):
        """
        Muestra la ficha técnica en el frame de resultados
        """
        if nombre_formateado is None:
            nombre_formateado = self.formatear_nombre_cientifico(especie)
        if nombre_comun is None:
            nombre_comun = self.fichas.obtener_nombre_comun(especie) if self.fichas.tiene_ficha(especie) else ""
        
        # Frame para la ficha técnica
        frame_ficha = ttk.Frame(frame_destino)
        frame_ficha.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(frame_ficha,
                 text=f"📋 Ficha Técnica - {nombre_formateado}",
                 style='Titulo.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        if nombre_comun:
            ttk.Label(frame_ficha,
                     text=f"Nombre común: {nombre_comun}",
                     style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Separator(frame_ficha, orient='horizontal').pack(fill=tk.X, pady=5)
        
        if self.fichas.tiene_ficha(especie):
            ficha = self.fichas.obtener_ficha(especie)
            
            # Usar ScrolledText para mostrar la ficha
            texto_ficha = scrolledtext.ScrolledText(frame_ficha,
                                                   wrap=tk.WORD,
                                                   width=80,
                                                   height=20,
                                                   font=('Segoe UI', 10),
                                                   bg='white',
                                                   relief='flat')
            texto_ficha.pack(fill=tk.BOTH, expand=True, pady=5)
            
            # Construir el texto de la ficha
            contenido = ""
            
            # Taxonomía
            if 'taxonomia' in ficha:
                tax = ficha['taxonomia']
                contenido += "🏷️ TAXONOMÍA\n"
                for key, value in tax.items():
                    contenido += f"  • {key.capitalize()}: {value}\n"
                contenido += "\n"
            
            # Distribución
            if 'distribucion' in ficha:
                dist = ficha['distribucion']
                contenido += "📍 DISTRIBUCIÓN\n"
                for key, value in dist.items():
                    if key == 'paises' and isinstance(value, list):
                        paises = ', '.join(value[:5])
                        if len(value) > 5:
                            paises += f" y {len(value)-5} más..."
                        contenido += f"  • Países: {paises}\n"
                    else:
                        contenido += f"  • {key.capitalize()}: {value}\n"
                contenido += "\n"
            
            # Descripción
            if 'descripcion' in ficha:
                contenido += "📝 DESCRIPCIÓN\n"
                contenido += f"  {ficha['descripcion']}\n\n"
            
            # Conservación
            if 'conservacion' in ficha:
                cons = ficha['conservacion']
                contenido += "🛡️ CONSERVACIÓN\n"
                for key, value in cons.items():
                    if key == 'amenazas' and isinstance(value, list):
                        contenido += f"  • {key.capitalize()}: {', '.join(value)}\n"
                    else:
                        contenido += f"  • {key.capitalize()}: {value}\n"
                contenido += "\n"
            
            # Características destacadas
            if 'caracteristicas_destacadas' in ficha and ficha['caracteristicas_destacadas']:
                contenido += "⭐ CARACTERÍSTICAS DESTACADAS\n"
                for carac in ficha['caracteristicas_destacadas']:
                    contenido += f"  • {carac}\n"
                contenido += "\n"
            
            # Datos adicionales
            contenido += "📊 DATOS ADICIONALES\n"
            for key in ['tamano', 'alimentacion', 'reproduccion']:
                if key in ficha:
                    contenido += f"  • {key.capitalize()}: {ficha[key]}\n"
            
            texto_ficha.insert(tk.INSERT, contenido)
            texto_ficha.config(state=tk.DISABLED)
        else:
            ttk.Label(frame_ficha,
                     text="⚠️ No hay ficha técnica disponible para esta especie.",
                     style='Pregunta.TLabel',
                     foreground=self.COLORES['advertencia']).pack(pady=20)
    
    def agregar_favorito(self, especie: str):
        """Agrega una especie a favoritos"""
        favorito = {
            'especie': especie,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'modo': self.modo_actual
        }
        
        # Verificar si ya existe
        for fav in self.favoritos:
            if fav['especie'] == especie:
                nombre_formateado = self.formatear_nombre_cientifico(especie)
                messagebox.showinfo("Favoritos", f"La especie {nombre_formateado} ya está en favoritos.")
                return
        
        self.favoritos.append(favorito)
        nombre_formateado = self.formatear_nombre_cientifico(especie)
        messagebox.showinfo("Favoritos", f"✅ {nombre_formateado} agregada a favoritos.")
        self.actualizar_estado(f"Agregado a favoritos: {nombre_formateado}")
    
    def mostrar_favoritos(self):
        """Muestra las identificaciones marcadas como favoritas con imágenes"""
        if not self.favoritos:
            messagebox.showinfo("Favoritos", "No hay identificaciones marcadas como favoritas.")
            return
        
        ventana_fav = tk.Toplevel(self.root)
        ventana_fav.title("⭐ Identificaciones Favoritas")
        ventana_fav.geometry("900x600")
        ventana_fav.configure(bg=self.COLORES['fondo'])
        
        frame_principal = ttk.Frame(ventana_fav, padding="20")
        frame_principal.pack(fill="both", expand=True)
        
        ttk.Label(frame_principal,
                 text="⭐ Identificaciones Favoritas",
                 style='Titulo.TLabel').pack(anchor=tk.W, pady=(0, 20))
        
        # Canvas para scroll
        canvas_fav = tk.Canvas(frame_principal, bg=self.COLORES['fondo'], highlightthickness=0)
        scrollbar_fav = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas_fav.yview)
        frame_fav_inner = ttk.Frame(canvas_fav)
        
        canvas_fav.create_window((0, 0), window=frame_fav_inner, anchor="nw")
        canvas_fav.configure(yscrollcommand=scrollbar_fav.set)
        
        frame_fav_inner.bind("<Configure>", lambda e: canvas_fav.configure(scrollregion=canvas_fav.bbox("all")))
        
        canvas_fav.pack(side="left", fill="both", expand=True)
        scrollbar_fav.pack(side="right", fill="y")
        
        # Mostrar cada favorito con imagen
        for i, fav in enumerate(self.favoritos):
            frame_item = ttk.Frame(frame_fav_inner, style='Card.TFrame')
            frame_item.pack(fill=tk.X, pady=5)
            
            # Frame para información
            frame_info = ttk.Frame(frame_item)
            frame_info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            
            especie_formateada = self.formatear_nombre_cientifico(fav['especie'])
            
            # NOMBRE CIENTÍFICO EN CURSIVA
            ttk.Label(frame_info,
                     text=f"🦀 {especie_formateada}",
                     style='Cientifico.TLabel').pack(anchor=tk.W)
            
            # Nombre común
            if self.fichas.tiene_ficha(fav['especie']):
                nombre_comun = self.fichas.obtener_nombre_comun(fav['especie'])
                ttk.Label(frame_info,
                         text=f"({nombre_comun})",
                         font=('Segoe UI', 9),
                         foreground=self.COLORES['gris_medio']).pack(anchor=tk.W, padx=(25, 0))
            
            ttk.Label(frame_info,
                     text=f"Agregado: {fav['timestamp']} | Modo: {fav['modo'].upper()}",
                     font=('Segoe UI', 9),
                     foreground=self.COLORES['gris_medio']).pack(anchor=tk.W, padx=(25, 0))
            
            # Mini imagen
            frame_img = ttk.Frame(frame_item)
            frame_img.pack(side=tk.RIGHT, padx=10, pady=10)
            
            try:
                from PIL import Image, ImageTk
                ruta_img = ConfigImagenes.obtener_ruta_imagen(fav['especie'])
                if ruta_img:
                    img = Image.open(ruta_img)
                    img.thumbnail((80, 80), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    label_img = ttk.Label(frame_img, image=photo)
                    label_img.image = photo
                    label_img.pack()
                else:
                    ttk.Label(frame_img, text="📷", font=('Segoe UI', 30)).pack()
            except Exception as e:
                ttk.Label(frame_img, text="📷", font=('Segoe UI', 30)).pack()
            
            # Línea separadora
            if i < len(self.favoritos) - 1:
                ttk.Separator(frame_fav_inner, orient='horizontal').pack(fill=tk.X, pady=5)
    
    def mostrar_detalles_proceso(self):
        """Muestra los detalles del proceso de identificación"""
        ventana_detalles = tk.Toplevel(self.root)
        ventana_detalles.title("Detalles del Proceso de Identificación")
        ventana_detalles.geometry("800x600")
        ventana_detalles.configure(bg=self.COLORES['fondo'])
        
        # Centrar ventana
        ventana_detalles.transient(self.root)
        ventana_detalles.grab_set()
        
        frame_principal = ttk.Frame(ventana_detalles, padding="20")
        frame_principal.pack(fill="both", expand=True)
        
        ttk.Label(frame_principal,
                 text="📊 Historial Detallado del Proceso",
                 style='Titulo.TLabel').pack(anchor=tk.W, pady=(0, 20))
        
        # Crear texto del historial
        texto_historial = "PROCESO DE IDENTIFICACIÓN POR REGLAS\n"
        texto_historial += "=" * 50 + "\n\n"
        
        for i, item in enumerate(self.historial_preguntas, 1):
            texto_historial += f"PREGUNTA {i}:\n"
            texto_historial += f"• Hora: {item['timestamp']}\n"
            texto_historial += f"• Pregunta: {item['pregunta']}\n"
            texto_historial += f"• Respuesta: {item['respuesta']}\n"
            texto_historial += "-" * 40 + "\n\n"
        
        # Mostrar resultado final
        if self.resultados:
            ultimo_resultado = self.resultados[-1]
            nombre_cientifico = self.formatear_nombre_cientifico(ultimo_resultado['especie'])
            texto_historial += f"RESULTADO FINAL:\n"
            texto_historial += f"• Especie: {nombre_cientifico}\n"
            if 'nombre_comun' in ultimo_resultado and ultimo_resultado['nombre_comun']:
                texto_historial += f"• Nombre común: {ultimo_resultado['nombre_comun']}\n"
            texto_historial += f"• Total de preguntas: {ultimo_resultado['preguntas']}\n"
            texto_historial += f"• Hora de finalización: {ultimo_resultado['timestamp']}\n"
        
        # Widget de texto con scroll
        texto_widget = scrolledtext.ScrolledText(frame_principal,
                                                wrap=tk.WORD,
                                                width=80,
                                                height=25,
                                                font=('Courier New', 10),
                                                bg='#fafafa')
        texto_widget.pack(fill="both", expand=True)
        texto_widget.insert(tk.INSERT, texto_historial)
        texto_widget.config(state=tk.DISABLED)
        
        # Botón de cerrar
        ttk.Button(frame_principal,
                  text="Cerrar",
                  command=ventana_detalles.destroy,
                  style='BotonPrincipal.TButton').pack(pady=20)
    
    def finalizar_identificacion(self):
        """Finaliza la identificación actual"""
        self.identificacion_activa = False
        self.subpregunta_actual = None
        
        # Reactivar botones
        if (hasattr(self, 'boton_iniciar_reglas') and 
            self.boton_iniciar_reglas and 
            self.boton_iniciar_reglas.winfo_exists()):
            self.boton_iniciar_reglas.config(state='normal')
        
        if (hasattr(self, 'boton_cancelar_reglas') and 
            self.boton_cancelar_reglas and 
            self.boton_cancelar_reglas.winfo_exists()):
            self.boton_cancelar_reglas.config(state='disabled')
    
    def cancelar_identificacion(self):
        """Cancela la identificación en curso"""
        print("⏹️ Cancelando identificación...")
        
        try:
            # Desactivar bandera de identificación
            self.identificacion_activa = False
            
            # Reiniciar estado
            self.reiniciar_estado_identificacion()
            
            # Reactivar botones
            if (hasattr(self, 'boton_iniciar_reglas') and 
                self.boton_iniciar_reglas and 
                self.boton_iniciar_reglas.winfo_exists()):
                self.boton_iniciar_reglas.config(state='normal')
            
            if (hasattr(self, 'boton_cancelar_reglas') and 
                self.boton_cancelar_reglas and 
                self.boton_cancelar_reglas.winfo_exists()):
                self.boton_cancelar_reglas.config(state='disabled')
            
            # Limpiar panel de proceso
            if (hasattr(self, 'frame_proceso') and 
                self.frame_proceso and 
                self.frame_proceso.winfo_exists()):
                
                for widget in self.frame_proceso.winfo_children():
                    try:
                        widget.destroy()
                    except:
                        pass
                
                # Mostrar mensaje de cancelación
                ttk.Label(self.frame_proceso,
                         text="⏹️ Identificación cancelada",
                         style='Subtitulo.TLabel',
                         foreground=self.COLORES['peligro']).pack(pady=20)
                
                ttk.Label(self.frame_proceso,
                         text="Haga clic en 'Iniciar Identificación' para comenzar una nueva identificación.",
                         style='Pregunta.TLabel',
                         foreground=self.COLORES['gris_medio']).pack(pady=10)
            
            # Actualizar estado
            self.actualizar_estado("Identificación cancelada por el usuario")
            
            print("✅ Identificación cancelada correctamente")
            
        except Exception as e:
            print(f"❌ Error en cancelar_identificacion: {e}")
    
    def reiniciar_estado_identificacion(self):
        """Reinicia completamente el estado de identificación"""
        print("🔄 Reiniciando estado de identificación...")
        
        # Reiniciar todas las variables de estado
        self.pregunta_actual = None
        self.subpregunta_actual = None
        self.historial_preguntas = []
        self.identificacion_activa = False
        
        print(f"✅ Estado reiniciado: pregunta_actual={self.pregunta_actual}, "
              f"subpregunta_actual={self.subpregunta_actual}, "
              f"historial={len(self.historial_preguntas)} preguntas, "
              f"activa={self.identificacion_activa}")
    
    def nueva_identificacion(self):
        """Prepara para una nueva identificación"""
        try:
            print("🔄 Iniciando nueva identificación...")
            
            # Reiniciar estado completamente
            self.reiniciar_estado_identificacion()
            
            # Actualizar estado
            self.actualizar_estado("Preparado para nueva identificación")
            
            # Recrear la interfaz según el modo actual
            self.cambiar_modo()
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo("Nueva Identificación", 
                               "✅ Sistema listo para una nueva identificación.\n\n"
                               "Puede comenzar el proceso de identificación nuevamente.")
            
            print("✅ Nueva identificación configurada correctamente")
            
        except Exception as e:
            print(f"❌ Error en nueva_identificacion: {e}")
            messagebox.showerror("Error", 
                               f"No se pudo preparar para nueva identificación:\n{str(e)}")
    
    def predecir_red_neuronal(self):
        """Realiza predicción usando la red neuronal CON IMAGEN Y FICHA"""
        try:
            # Recoger características
            caracteristicas = self.obtener_caracteristicas_formulario()
            
            if not caracteristicas:
                return
            
            # Realizar predicción
            especie, probabilidad = self.red_neuronal.predecir_especie(caracteristicas)
            
            # Formatear nombre CIENTÍFICAMENTE CORRECTO
            nombre_formateado = self.formatear_nombre_cientifico(especie)
            
            # Mostrar resultado
            self.mostrar_resultado_red_neuronal(especie, probabilidad, caracteristicas)
            
            # Guardar resultado
            self.resultados.append({
                'especie': especie,
                'modo': 'red_neuronal',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'probabilidad': probabilidad,
                'caracteristicas': caracteristicas,
                'nombre_comun': self.fichas.obtener_nombre_comun(especie) if self.fichas.tiene_ficha(especie) else ""
            })
            
            # Actualizar estado
            self.actualizar_estado(f"Predicción completada: {nombre_formateado} ({probabilidad:.2%})")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la predicción: {str(e)}")
    
    def obtener_caracteristicas_formulario(self) -> Dict[str, Any]:
        """Recoge y valida las características del formulario"""
        caracteristicas = {}
        
        try:
            # Validar longitud del caparazón
            if not self.entry_longitud.get().strip():
                messagebox.showerror("Error", "La longitud del caparazón es requerida")
                return None
            
            try:
                longitud = float(self.entry_longitud.get())
                if longitud <= 0 or longitud > 50:
                    messagebox.showerror("Error", "La longitud debe ser un valor positivo entre 0.1 y 50 mm")
                    return None
                caracteristicas['longitud_caparazon'] = longitud
            except ValueError:
                messagebox.showerror("Error", "La longitud debe ser un número válido")
                return None
            
            # setas_margen_frontal
            if self.combo_setas.get():
                caracteristicas['setas_margen_frontal'] = 1 if self.combo_setas.get() == "Sí" else 0
            else:
                messagebox.showerror("Error", "Seleccione si hay setas en el margen frontal")
                return None
            
            # n_dientes_margen_flexor
            if self.combo_dientes.get():
                caracteristicas['n_dientes_margen_flexor'] = int(self.combo_dientes.get())
            else:
                messagebox.showerror("Error", "Seleccione el número de dientes")
                return None
            
            # patron_granulacion_quelipodos
            if self.combo_granulacion.get():
                mapa_granulacion = {"Ausente": 0, "Finas": 1, "Gruesas": 2, "Mixtas": 3}
                caracteristicas['patron_granulacion_quelipodos'] = mapa_granulacion[self.combo_granulacion.get()]
            else:
                messagebox.showerror("Error", "Seleccione el patrón de granulación")
                return None
            
            # n_placas_telson
            if self.combo_placas.get():
                caracteristicas['n_placas_telson'] = int(self.combo_placas.get())
            else:
                messagebox.showerror("Error", "Seleccione el número de placas del telson")
                return None
            
            # tipo_quilla_abdominal
            if self.combo_quilla.get():
                caracteristicas['tipo_quilla_abdominal'] = self.combo_quilla.get().lower()
            else:
                messagebox.showerror("Error", "Seleccione el tipo de quilla abdominal")
                return None
            
            return caracteristicas
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
            return None
    
    def mostrar_resultado_red_neuronal(self, especie: str, probabilidad: float, caracteristicas: Dict[str, Any]):
        """
        Muestra el resultado de la red neuronal:
        - IMAGEN en la pestaña de Proceso
        - FICHA TÉCNICA en la pestaña de Resultados
        """
        # Verificar que el frame de proceso existe
        if hasattr(self, 'frame_proceso') and self.frame_proceso:
            if self.frame_proceso.winfo_exists():
                # Limpiar panel de proceso
                for widget in self.frame_proceso.winfo_children():
                    try:
                        widget.destroy()
                    except:
                        pass
                
                # Formatear nombre
                nombre_formateado = self.formatear_nombre_cientifico(especie)
                nombre_comun = self.fichas.obtener_nombre_comun(especie) if self.fichas.tiene_ficha(especie) else ""
                
                # Título
                frame_titulo_rn = ttk.Frame(self.frame_proceso)
                frame_titulo_rn.pack(fill=tk.X, pady=10)
                
                ttk.Label(frame_titulo_rn, text="🧠", font=('Segoe UI', 36)).pack(pady=5)
                ttk.Label(frame_titulo_rn,
                         text="¡PREDICCIÓN COMPLETADA!",
                         style='Titulo.TLabel',
                         foreground=self.COLORES['info']).pack(pady=5)
                
                ttk.Label(frame_titulo_rn,
                         text=nombre_formateado,
                         style='CientificoResultado.TLabel').pack(pady=5)
                
                if nombre_comun:
                    ttk.Label(frame_titulo_rn,
                             text=f"📌 {nombre_comun}",
                             style='Subtitulo.TLabel').pack(pady=2)
                
                # Barra de probabilidad
                frame_prob_rn = ttk.Frame(self.frame_proceso)
                frame_prob_rn.pack(fill=tk.X, pady=10, padx=20)
                
                ttk.Label(frame_prob_rn,
                         text="Confianza:",
                         style='Subtitulo.TLabel').pack(side=tk.LEFT)
                
                barra_prob_rn = ttk.Progressbar(frame_prob_rn,
                                               orient='horizontal',
                                               length=300,
                                               mode='determinate',
                                               style="Custom.Horizontal.TProgressbar")
                barra_prob_rn.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
                barra_prob_rn['value'] = probabilidad * 100
                
                ttk.Label(frame_prob_rn,
                         text=f"{probabilidad:.2%}",
                         style='Subtitulo.TLabel').pack(side=tk.LEFT)
                
                ttk.Separator(self.frame_proceso, orient='horizontal').pack(fill=tk.X, pady=10)
                
                # ======================== IMAGEN ========================
                frame_imagen_rn = ttk.LabelFrame(self.frame_proceso, text="📸 Imagen de la Especie", padding="10")
                frame_imagen_rn.pack(fill=tk.X, pady=10, padx=5)
                
                frame_imagen_contenedor_rn = ttk.Frame(frame_imagen_rn)
                frame_imagen_contenedor_rn.pack()
                
                try:
                    from PIL import Image, ImageTk
                    ruta_imagen_rn = ConfigImagenes.obtener_ruta_imagen(especie)
                    
                    if ruta_imagen_rn:
                        img = Image.open(ruta_imagen_rn)
                        ancho_max, alto_max = 350, 280
                        ancho_orig, alto_orig = img.size
                        proporcion = min(ancho_max / ancho_orig, alto_max / alto_orig)
                        nuevo_ancho = int(ancho_orig * proporcion)
                        nuevo_alto = int(alto_orig * proporcion)
                        
                        try:
                            img_resized = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                        except AttributeError:
                            img_resized = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
                        
                        photo = ImageTk.PhotoImage(img_resized)
                        label_imagen_rn = ttk.Label(frame_imagen_contenedor_rn, image=photo, background=self.COLORES['fondo'])
                        label_imagen_rn.image = photo
                        label_imagen_rn.pack(pady=10)
                    else:
                        ttk.Label(frame_imagen_contenedor_rn, 
                                 text="📷\nImagen no disponible",
                                 font=('Segoe UI', 16),
                                 foreground=self.COLORES['gris_medio'],
                                 background=self.COLORES['fondo'],
                                 justify='center').pack(pady=30)
                except Exception as e:
                    ttk.Label(frame_imagen_contenedor_rn, 
                             text="📷\nImagen no disponible",
                             font=('Segoe UI', 16),
                             foreground=self.COLORES['gris_medio'],
                             background=self.COLORES['fondo'],
                             justify='center').pack(pady=30)
                
                # Botones
                frame_acciones_rn = ttk.Frame(self.frame_proceso)
                frame_acciones_rn.pack(pady=15)
                
                ttk.Button(frame_acciones_rn,
                          text="⭐ Agregar a Favoritos",
                          command=lambda: self.agregar_favorito(especie),
                          style='BotonSecundario.TButton').pack(side=tk.LEFT, padx=5)
        
        # ======================== FICHA TÉCNICA EN RESULTADOS ========================
        if hasattr(self, 'frame_resultados_rn') and self.frame_resultados_rn:
            if self.frame_resultados_rn.winfo_exists():
                # Limpiar panel de resultados
                for widget in self.frame_resultados_rn.winfo_children():
                    try:
                        widget.destroy()
                    except:
                        pass
                
                # Mostrar la ficha técnica
                nombre_formateado = self.formatear_nombre_cientifico(especie)
                nombre_comun = self.fichas.obtener_nombre_comun(especie) if self.fichas.tiene_ficha(especie) else ""
                self.mostrar_ficha_tecnica_en_resultados(self.frame_resultados_rn, especie, nombre_formateado, nombre_comun)
        
        # Cambiar a la pestaña de resultados
        if self.notebook:
            try:
                self.notebook.select(2 if self.modo_actual == "red_neuronal" else 1)
            except:
                pass
        
        self.actualizar_scroll()
    
    def limpiar_formulario(self):
        """Limpia el formulario de red neuronal"""
        if hasattr(self, 'entry_longitud'):
            self.entry_longitud.delete(0, tk.END)
        if hasattr(self, 'combo_setas'):
            self.combo_setas.set('')
        if hasattr(self, 'combo_dientes'):
            self.combo_dientes.set('')
        if hasattr(self, 'combo_granulacion'):
            self.combo_granulacion.set('')
        if hasattr(self, 'combo_placas'):
            self.combo_placas.set('')
        if hasattr(self, 'combo_quilla'):
            self.combo_quilla.set('')
        
        self.actualizar_estado("Formulario limpiado")
        self.actualizar_scroll()
    
    def mostrar_historial_completo(self):
        """Muestra el historial completo de identificaciones CON IMÁGENES"""
        if not self.resultados:
            messagebox.showinfo("Historial", "No hay identificaciones realizadas en esta sesión.")
            return
        
        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title("📊 Historial Completo de Identificaciones")
        ventana_historial.geometry("1100x650")
        ventana_historial.configure(bg=self.COLORES['fondo'])
        
        frame_principal = ttk.Frame(ventana_historial, padding="20")
        frame_principal.pack(fill="both", expand=True)
        
        ttk.Label(frame_principal,
                 text="📈 Historial de Identificaciones",
                 style='Titulo.TLabel').pack(anchor=tk.W, pady=(0, 20))
        
        canvas_hist = tk.Canvas(frame_principal, bg=self.COLORES['fondo'], highlightthickness=0)
        scrollbar_hist = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas_hist.yview)
        frame_hist_inner = ttk.Frame(canvas_hist)
        
        canvas_hist.create_window((0, 0), window=frame_hist_inner, anchor="nw")
        canvas_hist.configure(yscrollcommand=scrollbar_hist.set)
        
        frame_hist_inner.bind("<Configure>", lambda e: canvas_hist.configure(scrollregion=canvas_hist.bbox("all")))
        
        canvas_hist.pack(side="left", fill="both", expand=True)
        scrollbar_hist.pack(side="right", fill="y")
        
        for i, resultado in enumerate(self.resultados):
            frame_item = ttk.Frame(frame_hist_inner, style='Card.TFrame')
            frame_item.pack(fill=tk.X, pady=5)
            
            frame_info = ttk.Frame(frame_item)
            frame_info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            
            especie_formateada = self.formatear_nombre_cientifico(resultado['especie'])
            
            ttk.Label(frame_info,
                     text=f"🦀 {especie_formateada}",
                     style='Cientifico.TLabel').pack(anchor=tk.W)
            
            if 'nombre_comun' in resultado and resultado['nombre_comun']:
                ttk.Label(frame_info,
                         text=f"({resultado['nombre_comun']})",
                         font=('Segoe UI', 9),
                         foreground=self.COLORES['gris_medio']).pack(anchor=tk.W, padx=(25, 0))
            
            ttk.Label(frame_info,
                     text=f"Fecha: {resultado['timestamp']} | Modo: {resultado['modo'].upper()}",
                     font=('Segoe UI', 9),
                     foreground=self.COLORES['gris_medio']).pack(anchor=tk.W, padx=(25, 0))
            
            if resultado['modo'] == 'red_neuronal' and 'probabilidad' in resultado:
                ttk.Label(frame_info,
                         text=f"Confianza: {resultado['probabilidad']:.2%}",
                         font=('Segoe UI', 9),
                         foreground=self.COLORES['info']).pack(anchor=tk.W, padx=(25, 0))
            
            if resultado['modo'] == 'reglas' and 'preguntas' in resultado:
                ttk.Label(frame_info,
                         text=f"Preguntas: {resultado['preguntas']}",
                         font=('Segoe UI', 9),
                         foreground=self.COLORES['gris_medio']).pack(anchor=tk.W, padx=(25, 0))
            
            frame_img = ttk.Frame(frame_item)
            frame_img.pack(side=tk.RIGHT, padx=10, pady=10)
            
            try:
                from PIL import Image, ImageTk
                ruta_img = ConfigImagenes.obtener_ruta_imagen(resultado['especie'])
                if ruta_img:
                    img = Image.open(ruta_img)
                    img.thumbnail((80, 80), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    label_img = ttk.Label(frame_img, image=photo)
                    label_img.image = photo
                    label_img.pack()
                else:
                    ttk.Label(frame_img, text="📷", font=('Segoe UI', 30)).pack()
            except Exception as e:
                ttk.Label(frame_img, text="📷", font=('Segoe UI', 30)).pack()
            
            if i < len(self.resultados) - 1:
                ttk.Separator(frame_hist_inner, orient='horizontal').pack(fill=tk.X, pady=5)
    
    def exportar_resultados(self):
        """Exporta los resultados a un archivo"""
        if not self.resultados:
            messagebox.showinfo("Exportar", "No hay resultados para exportar.")
            return
        
        messagebox.showinfo("Exportar", 
                           f"📊 Se exportarían {len(self.resultados)} identificaciones.\n\n"
                           "En una versión completa, los resultados se guardarían en un archivo CSV con:\n"
                           "• Especie identificada\n"
                           "• Nombre común\n"
                           "• Fecha y hora\n"
                           "• Modo de identificación\n"
                           "• Detalles del proceso\n"
                           "• Nivel de confianza (para RN)\n"
                           "• Ruta de la imagen asociada")
    
    def mostrar_ayuda(self):
        """Muestra la ventana de ayuda"""
        mensaje_ayuda = """
🦀 SISTEMA EXPERTO PORCELANIDAE - AYUDA COMPLETA

🔍 MODO CLAVE TAXONÓMICA:
• Sistema basado en reglas dicotómicas tradicionales
• Responda Sí/No a cada pregunta presentada
• El sistema navega por el árbol de decisiones
• Ideal cuando no tiene medidas exactas
• Proceso educativo y guiado paso a paso
• 23 especies disponibles para identificación
• Muestra imagen en pestaña Proceso y ficha en Resultados

🧠 MODO RED NEURONAL:
• Identificación mediante inteligencia artificial
• Requiere características cuantitativas precisas
• Proporcione medidas y características observables
• Resultado inmediato con probabilidad de acierto
• Más rápido pero requiere datos precisos
• 17 especies disponibles para predicción
• Muestra imagen en pestaña Proceso y ficha en Resultados

📸 IMÁGENES Y FICHAS TÉCNICAS:
• Imagen de la especie en la pestaña "Proceso de Identificación"
• Ficha técnica completa en la pestaña "Resultados"
• Miniaturas disponibles en historial y favoritos

📊 CARACTERÍSTICAS DEL SISTEMA:
• Sistema de reglas: 23 especies identificables
• Red neuronal: 17 especies disponibles
• Múltiples identificaciones por sesión
• Historial completo con imágenes
• Sistema de favoritos con imágenes
• Exportación de resultados

💡 CONSEJOS PRÁCTICOS:
• Observe cuidadosamente el ejemplar
• Use una lupa si es necesario para detalles finos
• Tenga a mano una regla para mediciones precisas
• En caso de duda, use el modo clave taxonómica
• Consulte la guía rápida para más detalles
        """
        
        messagebox.showinfo("Ayuda del Sistema", mensaje_ayuda)
    
    def actualizar_estado(self, mensaje: str):
        """Actualiza la barra de estado"""
        if hasattr(self, 'label_estado') and self.label_estado.winfo_exists():
            self.label_estado.config(text=f"🟢 {mensaje}")
        
        if hasattr(self, 'label_estado_persistente') and self.label_estado_persistente.winfo_exists():
            self.label_estado_persistente.config(text=mensaje)
        
        if hasattr(self, 'label_contador') and self.label_contador.winfo_exists():
            self.label_contador.config(text=f"📝 {len(self.resultados)} identificaciones")
        
        if hasattr(self, 'label_progreso') and self.label_progreso.winfo_exists():
            if self.resultados:
                progreso = min(len(self.resultados) * 10, 100)
                self.progress_general['value'] = progreso
                self.label_progreso.config(text=f"Progreso: {progreso}%")
            else:
                self.progress_general['value'] = 0
                self.label_progreso.config(text="Progreso: 0%")
    
    def actualizar_scroll(self):
        """Actualiza la región de scroll después de cambios en el contenido"""
        if self.scroll_habilitado and self.canvas:
            self.root.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def mostrar_resultado(self, mensaje: str):
        """Muestra un mensaje de resultado genérico"""
        messagebox.showinfo("Resultado", mensaje)