"""
Módulo de visualización para el sistema experto de Porcelanidae
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
import matplotlib
matplotlib.use('TkAgg')  # Para compatibilidad con Tkinter

class VisualizadorDatos:
    """
    Clase para visualización de datos morfológicos y resultados del sistema
    """
    
    def __init__(self, estilo: str = 'seaborn'):
        """
        Inicializa el visualizador con estilo
        
        Args:
            estilo (str): Estilo de matplotlib a usar
        """
        plt.style.use(estilo)
        self.colores_especies = plt.cm.Set3(np.linspace(0, 1, 20))
        self.figsize = (12, 8)
    
    def crear_dashboard_especies(self, datos: pd.DataFrame, ruta_guardado: str = None):
        """
        Crea un dashboard completo de análisis de especies
        
        Args:
            datos (pd.DataFrame): DataFrame con los datos de especies
            ruta_guardado (str): Ruta para guardar el dashboard
        """
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Dashboard de Análisis de Especies de Porcelanidae', fontsize=16, fontweight='bold')
        
        # 1. Distribución de especies
        self._graficar_distribucion_especies(datos, axes[0, 0])
        
        # 2. Características numéricas por especie
        self._graficar_boxplot_caracteristicas(datos, axes[0, 1])
        
        # 3. Matriz de correlación
        self._graficar_matriz_correlacion(datos, axes[0, 2])
        
        # 4. Patrones de granulación
        self._graficar_patron_granulacion(datos, axes[1, 0])
        
        # 5. Distribución de placas del telson
        self._graficar_distribucion_telson(datos, axes[1, 1])
        
        # 6. Relación longitud-setas
        self._graficar_relacion_longitud_setas(datos, axes[1, 2])
        
        plt.tight_layout()
        
        if ruta_guardado:
            plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
            print(f"Dashboard guardado en: {ruta_guardado}")
        
        return fig
    
    def _graficar_distribucion_especies(self, datos: pd.DataFrame, ax: plt.Axes):
        """
        Grafica la distribución de especies en el dataset
        
        Args:
            datos (pd.DataFrame): DataFrame con datos
            ax (plt.Axes): Ejes para graficar
        """
        conteo_especies = datos['especie'].value_counts()
        
        bars = ax.bar(conteo_especies.index, conteo_especies.values, 
                     color=self.colores_especies[:len(conteo_especies)])
        ax.set_title('Distribución de Especies', fontweight='bold')
        ax.set_xlabel('Especies')
        ax.set_ylabel('Número de Ejemplares')
        ax.tick_params(axis='x', rotation=45)
        
        # Añadir valores en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        ax.grid(axis='y', alpha=0.3)
    
    def _graficar_boxplot_caracteristicas(self, datos: pd.DataFrame, ax: plt.Axes):
        """
        Grafica boxplots de características numéricas por especie
        
        Args:
            datos (pd.DataFrame): DataFrame con datos
            ax (plt.Axes): Ejes para graficar
        """
        caracteristicas_numericas = ['longitud_caparazon', 'n_dientes_margen_flexor', 'n_placas_telson']
        
        datos_melted = datos.melt(id_vars=['especie'], 
                                 value_vars=caracteristicas_numericas,
                                 var_name='caracteristica', 
                                 value_name='valor')
        
        sns.boxplot(data=datos_melted, x='especie', y='valor', hue='caracteristica', ax=ax)
        ax.set_title('Distribución de Características por Especie', fontweight='bold')
        ax.set_xlabel('Especies')
        ax.set_ylabel('Valor')
        ax.tick_params(axis='x', rotation=45)
        ax.legend(title='Característica')
    
    def _graficar_matriz_correlacion(self, datos: pd.DataFrame, ax: plt.Axes):
        """
        Grafica matriz de correlación entre características numéricas
        
        Args:
            datos (pd.DataFrame): DataFrame con datos
            ax (plt.Axes): Ejes para graficar
        """
        # Seleccionar solo columnas numéricas
        columnas_numericas = datos.select_dtypes(include=[np.number]).columns
        matriz_correlacion = datos[columnas_numericas].corr()
        
        # Crear máscara para el triángulo superior
        mascara = np.triu(np.ones_like(matriz_correlacion, dtype=bool))
        
        # Graficar heatmap
        sns.heatmap(matriz_correlacion, mask=mascara, annot=True, cmap='coolwarm', 
                   center=0, ax=ax, fmt='.2f', cbar_kws={'shrink': 0.8})
        ax.set_title('Matriz de Correlación', fontweight='bold')
    
    def _graficar_patron_granulacion(self, datos: pd.DataFrame, ax: plt.Axes):
        """
        Grafica distribución de patrones de granulación por especie
        
        Args:
            datos (pd.DataFrame): DataFrame con datos
            ax (plt.Axes): Ejes para graficar
        """
        # Mapear valores numéricos a etiquetas
        mapeo_granulacion = {0: 'Ausente', 1: 'Finas', 2: 'Gruesas', 3: 'Mixtas'}
        datos['granulacion_etiqueta'] = datos['patron_granulacion_quelipodos'].map(mapeo_granulacion)
        
        tabla_cruzada = pd.crosstab(datos['especie'], datos['granulacion_etiqueta'])
        tabla_cruzada.plot(kind='bar', stacked=True, ax=ax, 
                          color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
        
        ax.set_title('Patrones de Granulación por Especie', fontweight='bold')
        ax.set_xlabel('Especies')
        ax.set_ylabel('Número de Ejemplares')
        ax.tick_params(axis='x', rotation=45)
        ax.legend(title='Patrón de Granulación', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    def _graficar_distribucion_telson(self, datos: pd.DataFrame, ax: plt.Axes):
        """
        Grafica distribución de número de placas del telson
        
        Args:
            datos (pd.DataFrame): DataFrame con datos
            ax (plt.Axes): Ejes para graficar
        """
        conteo_telson = datos['n_placas_telson'].value_counts().sort_index()
        
        wedges, texts, autotexts = ax.pie(conteo_telson.values, labels=conteo_telson.index, 
                                         autopct='%1.1f%%', startangle=90,
                                         colors=['#ff9999', '#66b3ff'])
        
        ax.set_title('Distribución de Placas del Telson', fontweight='bold')
        
        # Mejorar estética
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    
    def _graficar_relacion_longitud_setas(self, datos: pd.DataFrame, ax: plt.Axes):
        """
        Grafica relación entre longitud del caparazón y presencia de setas
        
        Args:
            datos (pd.DataFrame): DataFrame con datos
            ax (plt.Axes): Ejes para graficar
        """
        # Convertir setas a etiqueta
        datos['setas_etiqueta'] = datos['setas_margen_frontal'].map({0: 'Sin Setas', 1: 'Con Setas'})
        
        sns.scatterplot(data=datos, x='longitud_caparazon', y='n_dientes_margen_flexor',
                       hue='setas_etiqueta', style='especie', ax=ax, s=100, alpha=0.7)
        
        ax.set_title('Relación: Longitud vs Dientes y Setas', fontweight='bold')
        ax.set_xlabel('Longitud del Caparazón (mm)')
        ax.set_ylabel('Número de Dientes en Margen Flexor')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
    
    def graficar_importancia_caracteristicas(self, importancia: pd.DataFrame, ax: plt.Axes = None):
        """
        Grafica la importancia de las características
        
        Args:
            importancia (pd.DataFrame): DataFrame con importancia de características
            ax (plt.Axes): Ejes opcionales para graficar
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
        
        # Ordenar por importancia
        importancia_ordenada = importancia.sort_values('score_importancia', ascending=True)
        
        # Graficar barras horizontales
        bars = ax.barh(importancia_ordenada['caracteristica'], 
                      importancia_ordenada['score_importancia'],
                      color=plt.cm.viridis(np.linspace(0, 1, len(importancia_ordenada))))
        
        ax.set_title('Importancia de Características Morfológicas', fontweight='bold')
        ax.set_xlabel('Score de Importancia')
        ax.grid(axis='x', alpha=0.3)
        
        # Añadir valores en las barras
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2., 
                   f'{width:.2f}', ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        return ax.figure if ax is None else None
    
    def graficar_resultado_clasificacion(self, y_real: np.ndarray, y_pred: np.ndarray, 
                                       nombres_especies: List[str], ax: plt.Axes = None):
        """
        Grafica matriz de confusión para resultados de clasificación
        
        Args:
            y_real (np.ndarray): Etiquetas reales
            y_pred (np.ndarray): Etiquetas predichas
            nombres_especies (List[str]): Nombres de las especies
            ax (plt.Axes): Ejes opcionales para graficar
        """
        from sklearn.metrics import confusion_matrix
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
        
        cm = confusion_matrix(y_real, y_pred)
        
        # Graficar matriz de confusión
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax.set_title('Matriz de Confusión', fontweight='bold')
        
        # Añadir etiquetas
        tick_marks = np.arange(len(nombres_especies))
        ax.set_xticks(tick_marks)
        ax.set_yticks(tick_marks)
        ax.set_xticklabels(nombres_especies, rotation=45, ha='right')
        ax.set_yticklabels(nombres_especies)
        
        # Añadir valores en las celdas
        thresh = cm.max() / 2.
        for i, j in np.ndindex(cm.shape):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black")
        
        ax.set_ylabel('Etiqueta Real')
        ax.set_xlabel('Etiqueta Predicha')
        plt.colorbar(im, ax=ax)
        
        return ax.figure if ax is None else None
    
    def graficar_curva_aprendizaje(self, historial_entrenamiento: Dict[str, List[float]], 
                                 ax: plt.Axes = None):
        """
        Grafica curvas de aprendizaje del modelo
        
        Args:
            historial_entrenamiento (Dict[str, List[float]]): Historial de métricas
            ax (plt.Axes): Ejes opcionales para graficar
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
        
        for metrica, valores in historial_entrenamiento.items():
            ax.plot(valores, label=metrica, linewidth=2)
        
        ax.set_title('Curvas de Aprendizaje del Modelo', fontweight='bold')
        ax.set_xlabel('Épocas')
        ax.set_ylabel('Valor de la Métrica')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return ax.figure if ax is None else None
    
    def crear_visualizacion_interactiva(self, datos: pd.DataFrame, caracteristicas: List[str]):
        """
        Crea una visualización interactiva (placeholder para implementación futura)
        
        Args:
            datos (pd.DataFrame): DataFrame con datos
            caracteristicas (List[str]): Lista de características a visualizar
        """
        print("Visualización interactiva - Esta funcionalidad puede extenderse con Plotly")
        print(f"Características disponibles: {caracteristicas}")
        
        # Aquí se podría integrar Plotly para visualizaciones interactivas
        fig = self.crear_dashboard_especies(datos)
        return fig
    
    def guardar_visualizacion(self, figura: plt.Figure, ruta: str, formato: str = 'png'):
        """
        Guarda una visualización en archivo
        
        Args:
            figura (plt.Figure): Figura a guardar
            ruta (str): Ruta donde guardar
            formato (str): Formato de archivo
        """
        figura.savefig(ruta, format=formato, dpi=300, bbox_inches='tight')
        print(f"Visualización guardada en: {ruta}")
