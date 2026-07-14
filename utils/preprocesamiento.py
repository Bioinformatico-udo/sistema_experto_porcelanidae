
"""
Módulo de preprocesamiento de datos para el sistema experto de Porcelanidae
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
import joblib
from typing import Tuple, Dict, Any, List

class PreprocesadorDatos:
    """
    Clase para preprocesamiento de datos morfológicos de crustáceos
    """
    
    def __init__(self):
        """Inicializa el preprocesador con sus componentes"""
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.onehot_encoder = OneHotEncoder(sparse_output=False, drop='first')
        self.imputer = SimpleImputer(strategy='median')
        self.selector_caracteristicas = None
        self.columnas_numericas = None
        self.columnas_categoricas = None
        self.especies_mapeo = None
        
    def cargar_y_limpiar_datos(self, ruta_csv: str) -> pd.DataFrame:
        """
        Carga y limpia el dataset de especies
        
        Args:
            ruta_csv (str): Ruta al archivo CSV con los datos
            
        Returns:
            pd.DataFrame: DataFrame limpio y procesado
        """
        try:
            # Cargar datos
            datos = pd.read_csv(ruta_csv, encoding='utf-8')
            print(f"Datos cargados: {datos.shape[0]} registros, {datos.shape[1]} características")
            
            # Limpieza básica
            datos = self._aplicar_limpieza_basica(datos)
            
            # Validar características requeridas
            datos = self._validar_caracteristicas(datos)
            
            # Imputar valores faltantes
            datos = self._imputar_valores_faltantes(datos)
            
            # Detectar y manejar outliers
            datos = self._manejar_outliers(datos)
            
            print("Limpieza de datos completada exitosamente")
            return datos
            
        except Exception as e:
            raise Exception(f"Error en carga y limpieza de datos: {str(e)}")
    
    def _aplicar_limpieza_basica(self, datos: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica limpieza básica al dataset
        
        Args:
            datos (pd.DataFrame): DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame limpio
        """
        # Crear copia para no modificar el original
        datos_limpios = datos.copy()
        
        # Eliminar duplicados exactos
        duplicados = datos_limpios.duplicated().sum()
        if duplicados > 0:
            print(f"Eliminando {duplicados} registros duplicados")
            datos_limpios = datos_limpios.drop_duplicates()
        
        # Normalizar nombres de columnas
        datos_limpios.columns = [col.lower().strip() for col in datos_limpios.columns]
        
        # Eliminar columnas completamente vacías
        columnas_vacias = datos_limpios.columns[datos_limpios.isnull().all()].tolist()
        if columnas_vacias:
            print(f"Eliminando columnas vacías: {columnas_vacias}")
            datos_limpios = datos_limpios.drop(columns=columnas_vacias)
        
        return datos_limpios
    
    def _validar_caracteristicas(self, datos: pd.DataFrame) -> pd.DataFrame:
        """
        Valida y asegura la presencia de características requeridas
        
        Args:
            datos (pd.DataFrame): DataFrame a validar
            
        Returns:
            pd.DataFrame: DataFrame validado
        """
        caracteristicas_requeridas = [
            'longitud_caparazon', 'setas_margen_frontal', 'n_dientes_margen_flexor',
            'patron_granulacion_quelipodos', 'tipo_quilla_abdominal', 'n_placas_telson', 'especie'
        ]
        
        # Verificar características faltantes
        faltantes = [col for col in caracteristicas_requeridas if col not in datos.columns]
        if faltantes:
            print(f"Advertencia: Características faltantes: {faltantes}")
        
        return datos
    
    def _imputar_valores_faltantes(self, datos: pd.DataFrame) -> pd.DataFrame:
        """
        Imputa valores faltantes en el dataset
        
        Args:
            datos (pd.DataFrame): DataFrame con valores faltantes
            
        Returns:
            pd.DataFrame: DataFrame sin valores faltantes
        """
        datos_imputados = datos.copy()
        
        # Estrategias por tipo de columna
        for columna in datos_imputados.columns:
            if datos_imputados[columna].isnull().sum() > 0:
                n_faltantes = datos_imputados[columna].isnull().sum()
                print(f"Imputando {n_faltantes} valores faltantes en {columna}")
                
                if datos_imputados[columna].dtype in ['float64', 'int64']:
                    # Para numéricas: mediana
                    valor_imputacion = datos_imputados[columna].median()
                    datos_imputados[columna].fillna(valor_imputacion, inplace=True)
                else:
                    # Para categóricas: moda
                    valor_imputacion = datos_imputados[columna].mode()[0] if not datos_imputados[columna].mode().empty else "Desconocido"
                    datos_imputados[columna].fillna(valor_imputacion, inplace=True)
        
        return datos_imputados
    
    def _manejar_outliers(self, datos: pd.DataFrame) -> pd.DataFrame:
        """
        Detecta y maneja valores atípicos en características numéricas
        
        Args:
            datos (pd.DataFrame): DataFrame con posibles outliers
            
        Returns:
            pd.DataFrame: DataFrame con outliers manejados
        """
        datos_sin_outliers = datos.copy()
        columnas_numericas = datos_sin_outliers.select_dtypes(include=[np.number]).columns
        
        for columna in columnas_numericas:
            if columna != 'especie':  # No aplicar a la columna especie
                Q1 = datos_sin_outliers[columna].quantile(0.25)
                Q3 = datos_sin_outliers[columna].quantile(0.75)
                IQR = Q3 - Q1
                limite_inferior = Q1 - 1.5 * IQR
                limite_superior = Q3 + 1.5 * IQR
                
                outliers = datos_sin_outliers[(datos_sin_outliers[columna] < limite_inferior) | 
                                            (datos_sin_outliers[columna] > limite_superior)]
                
                if len(outliers) > 0:
                    print(f"Detectados {len(outliers)} outliers en {columna}")
                    # Reemplazar outliers con los límites
                    datos_sin_outliers[columna] = np.where(
                        datos_sin_outliers[columna] < limite_inferior, limite_inferior, datos_sin_outliers[columna]
                    )
                    datos_sin_outliers[columna] = np.where(
                        datos_sin_outliers[columna] > limite_superior, limite_superior, datos_sin_outliers[columna]
                    )
        
        return datos_sin_outliers
    
    def preparar_datos_entrenamiento(self, datos: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Prepara los datos para entrenamiento de modelos
        
        Args:
            datos (pd.DataFrame): DataFrame limpio
            
        Returns:
            Tuple: Arrays de características (X) y etiquetas (y), lista de nombres de características
        """
        # Separar características y etiqueta
        X = datos.drop('especie', axis=1)
        y = datos['especie']
        
        # Identificar tipos de columnas
        self.columnas_numericas = X.select_dtypes(include=[np.number]).columns.tolist()
        self.columnas_categoricas = X.select_dtypes(include=['object']).columns.tolist()
        
        print(f"Características numéricas: {self.columnas_numericas}")
        print(f"Características categóricas: {self.columnas_categoricas}")
        
        # Preprocesar características numéricas
        if self.columnas_numericas:
            X_numerico = self.scaler.fit_transform(X[self.columnas_numericas])
        else:
            X_numerico = np.array([]).reshape(len(X), 0)
        
        # Preprocesar características categóricas
        if self.columnas_categoricas:
            X_categorico = self.onehot_encoder.fit_transform(X[self.columnas_categoricas])
            nombres_categorias = self.onehot_encoder.get_feature_names_out(self.columnas_categoricas)
        else:
            X_categorico = np.array([]).reshape(len(X), 0)
            nombres_categorias = []
        
        # Combinar características
        if X_numerico.size > 0 and X_categorico.size > 0:
            X_combinado = np.hstack([X_numerico, X_categorico])
            nombres_caracteristicas = self.columnas_numericas + nombres_categorias.tolist()
        elif X_numerico.size > 0:
            X_combinado = X_numerico
            nombres_caracteristicas = self.columnas_numericas
        else:
            X_combinado = X_categorico
            nombres_caracteristicas = nombres_categorias.tolist()
        
        # Codificar etiquetas
        y_encoded = self.label_encoder.fit_transform(y)
        self.especies_mapeo = dict(zip(self.label_encoder.classes_, 
                                     self.label_encoder.transform(self.label_encoder.classes_)))
        
        print(f"Datos preparados: {X_combinado.shape}")
        print(f"Especies únicas: {len(self.especies_mapeo)}")
        
        return X_combinado, y_encoded, nombres_caracteristicas
    
    def seleccionar_caracteristicas(self, X: np.ndarray, y: np.ndarray, k: int = 10) -> np.ndarray:
        """
        Selecciona las k mejores características usando prueba F de ANOVA
        
        Args:
            X (np.ndarray): Array de características
            y (np.ndarray): Array de etiquetas
            k (int): Número de características a seleccionar
            
        Returns:
            np.ndarray: Características seleccionadas
        """
        self.selector_caracteristicas = SelectKBest(score_func=f_classif, k=min(k, X.shape[1]))
        X_seleccionado = self.selector_caracteristicas.fit_transform(X, y)
        
        print(f"Características seleccionadas: {X_seleccionado.shape[1]}")
        return X_seleccionado
    
    def preparar_nueva_muestra(self, caracteristicas: Dict[str, Any]) -> np.ndarray:
        """
        Prepara una nueva muestra para predicción
        
        Args:
            caracteristicas (Dict[str, Any]): Diccionario con características
            
        Returns:
            np.ndarray: Array preparado para el modelo
        """
        # Crear DataFrame con las características
        df_muestra = pd.DataFrame([caracteristicas])
        
        # Preprocesar características numéricas
        if self.columnas_numericas:
            X_numerico = self.scaler.transform(df_muestra[self.columnas_numericas])
        else:
            X_numerico = np.array([]).reshape(1, 0)
        
        # Preprocesar características categóricas
        if self.columnas_categoricas:
            X_categorico = self.onehot_encoder.transform(df_muestra[self.columnas_categoricas])
        else:
            X_categorico = np.array([]).reshape(1, 0)
        
        # Combinar características
        if X_numerico.size > 0 and X_categorico.size > 0:
            X_combinado = np.hstack([X_numerico, X_categorico])
        elif X_numerico.size > 0:
            X_combinado = X_numerico
        else:
            X_combinado = X_categorico
        
        # Aplicar selección de características si está disponible
        if self.selector_caracteristicas is not None:
            X_combinado = self.selector_caracteristicas.transform(X_combinado)
        
        return X_combinado
    
    def decodificar_especie(self, etiqueta_codificada: int) -> str:
        """
        Decodifica una etiqueta numérica a nombre de especie
        
        Args:
            etiqueta_codificada (int): Etiqueta codificada
            
        Returns:
            str: Nombre de la especie
        """
        return self.label_encoder.inverse_transform([etiqueta_codificada])[0]
    
    def obtener_importancia_caracteristicas(self, nombres_caracteristicas: List[str]) -> pd.DataFrame:
        """
        Obtiene la importancia de las características si se usó selección
        
        Args:
            nombres_caracteristicas (List[str]): Nombres de las características
            
        Returns:
            pd.DataFrame: DataFrame con importancia de características
        """
        if self.selector_caracteristicas is not None:
            scores = self.selector_caracteristicas.scores_
            importancia = pd.DataFrame({
                'caracteristica': nombres_caracteristicas,
                'score_importancia': scores
            }).sort_values('score_importancia', ascending=False)
            return importancia
        else:
            print("No se ha aplicado selección de características")
            return pd.DataFrame()
    
    def guardar_preprocesador(self, ruta: str):
        """
        Guarda el preprocesador entrenado
        
        Args:
            ruta (str): Ruta donde guardar el preprocesador
        """
        joblib.dump({
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'onehot_encoder': self.onehot_encoder,
            'imputer': self.imputer,
            'selector_caracteristicas': self.selector_caracteristicas,
            'columnas_numericas': self.columnas_numericas,
            'columnas_categoricas': self.columnas_categoricas,
            'especies_mapeo': self.especies_mapeo
        }, ruta)
    
    def cargar_preprocesador(self, ruta: str):
        """
        Carga un preprocesador entrenado
        
        Args:
            ruta (str): Ruta del preprocesador guardado
        """
        datos = joblib.load(ruta)
        self.scaler = datos['scaler']
        self.label_encoder = datos['label_encoder']
        self.onehot_encoder = datos['onehot_encoder']
        self.imputer = datos['imputer']
        self.selector_caracteristicas = datos['selector_caracteristicas']
        self.columnas_numericas = datos['columnas_numericas']
        self.columnas_categoricas = datos['columnas_categoricas']
        self.especies_mapeo = datos['especies_mapeo']