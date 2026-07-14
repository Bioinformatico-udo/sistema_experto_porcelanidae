"""
Red neuronal para clasificación de especies de Porcelanidae
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import joblib
import os
import sys
from typing import Tuple, Dict, Any, Optional

# Añadir el directorio utils al path para posibles importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_path = os.path.join(current_dir, '..', 'utils')
if utils_path not in sys.path:
    sys.path.insert(0, utils_path)

class RedNeuronalEspecies:
    """
    Red neuronal para clasificación de especies basada en características morfológicas
    """
    
    def __init__(self):
        self.modelo = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.caracteristicas = None
        self.especies_disponibles = None
        print("🧠 Red neuronal inicializada")
    
    def _obtener_ruta_modelo(self, ruta_sugerida=None):
        """Determina la mejor ruta para guardar/cargar el modelo"""
        if ruta_sugerida and os.path.exists(os.path.dirname(ruta_sugerida) or os.path.dirname(ruta_sugerida) == ''):
            return ruta_sugerida
        
        rutas_posibles = [
            "models/modelo_entrenado.pkl",  # Estructura preferida
            "modelo_entrenado.pkl",         # Directorio raíz
            "../models/modelo_entrenado.pkl", # Desde otro directorio
            "data/modelo_entrenado.pkl"     # Alternativa en data
        ]
        
        for ruta in rutas_posibles:
            directorio = os.path.dirname(ruta) if os.path.dirname(ruta) else '.'
            if os.path.exists(directorio) or directorio == '.':
                return ruta
        
        return "models/modelo_entrenado.pkl"  # Default preferido
    
    def generar_datos_sinteticos(self, n_muestras_por_especie: int = 100) -> pd.DataFrame:
        """
        Genera dataset sintético basado en características morfológicas
        """
        print(f"📊 Generando {n_muestras_por_especie} muestras por especie...")
        
        especies = [
            'Petrolisthes_armatus', 'Petrolisthes_galathinus', 'Petrolisthes_marginatus',
            'Petrolisthes_politus', 'Petrolisthes_lewisi', 'Petrolisthes_jugosus',
            'Petrolisthes_tridentatus', 'Petrolisthes_tonsorius',
            'Pachycheles_serratus', 'Pachycheles_monilifer', 'Pachycheles_riseii',
            'Pachycheles_ackleianus', 'Neopisosoma_angustifrons', 'Neopisosoma_orientale',
            'Neopisosoma_cf_neglectum', 'Clastotoechus_nodosus', 'Minyocerus_angustus',
            'Megalobrachium_poeyi', 'Megalobrachium_roseum', 'Megalobrachium_soriatum',
            'Megalobrachium_mortenseni', 'Pisidia_brasiliensis', 'Porcellana_sayana'
        ]
        
        datos = []
        
        for especie in especies:
            for _ in range(n_muestras_por_especie):
                muestra = self._generar_muestra_especie(especie)
                muestra['especie'] = especie
                datos.append(muestra)
        
        df = pd.DataFrame(datos)
        print(f"✅ Dataset sintético generado: {len(df)} muestras, {len(especies)} especies")
        return df
    
    def _generar_muestra_especie(self, especie: str) -> Dict[str, Any]:
        """Genera una muestra sintética para una especie específica"""
        if especie.startswith('Petrolisthes'):
            return self._caracteristicas_petrolisthes(especie)
        elif especie.startswith('Pachycheles'):
            return self._caracteristicas_pachycheles(especie)
        elif especie.startswith('Neopisosoma'):
            return self._caracteristicas_neopisosoma(especie)
        elif especie.startswith('Megalobrachium'):
            return self._caracteristicas_megalobrachium(especie)
        else:
            return self._caracteristicas_generales(especie)
    
    def _caracteristicas_petrolisthes(self, especie: str) -> Dict[str, Any]:
        """Genera características para especies del género Petrolisthes"""
        base = {
            'longitud_caparazon': max(5.0, np.random.normal(15.0, 3.0)),
            'setas_margen_frontal': np.random.choice([0, 1], p=[0.7, 0.3]),
            'patron_granulacion_quelipodos': np.random.choice([0, 1, 2, 3], p=[0.1, 0.4, 0.3, 0.2]),
            'tipo_quilla_abdominal': np.random.choice(['recta', 'curvada', 'discontinua'], p=[0.6, 0.3, 0.1])
        }
        
        # Específico por especie
        if especie == 'Petrolisthes_armatus':
            base.update({'n_dientes_margen_flexor': 3, 'n_placas_telson': 7})
        elif especie == 'Petrolisthes_galathinus':
            base.update({'n_dientes_margen_flexor': 4, 'n_placas_telson': 7})
        elif especie == 'Petrolisthes_marginatus':
            base.update({'n_dientes_margen_flexor': 0, 'n_placas_telson': 7})
        elif especie == 'Petrolisthes_politus':
            base.update({'n_dientes_margen_flexor': 3, 'n_placas_telson': 7})
        elif especie == 'Petrolisthes_lewisi':
            base.update({'n_dientes_margen_flexor': 2, 'n_placas_telson': 7})
        elif especie == 'Petrolisthes_jugosus':
            base.update({'n_dientes_margen_flexor': 0, 'n_placas_telson': 5})
        elif especie == 'Petrolisthes_tridentatus':
            base.update({'n_dientes_margen_flexor': 0, 'n_placas_telson': 7})
        elif especie == 'Petrolisthes_tonsorius':
            base.update({'n_dientes_margen_flexor': 0, 'n_placas_telson': 7})
        
        return base
    
    def _caracteristicas_pachycheles(self, especie: str) -> Dict[str, Any]:
        """Genera características para especies del género Pachycheles"""
        base = {
            'longitud_caparazon': max(3.0, np.random.normal(8.0, 2.0)),
            'setas_margen_frontal': np.random.choice([0, 1], p=[0.5, 0.5]),
            'patron_granulacion_quelipodos': np.random.choice([0, 1, 2, 3], p=[0.2, 0.3, 0.3, 0.2]),
            'tipo_quilla_abdominal': np.random.choice(['recta', 'curvada', 'discontinua'], p=[0.3, 0.4, 0.3])
        }
        
        if especie == 'Pachycheles_serratus':
            base.update({'n_dientes_margen_flexor': 2, 'n_placas_telson': 7})
        elif especie == 'Pachycheles_monilifer':
            base.update({'n_dientes_margen_flexor': 3, 'n_placas_telson': 5})
        elif especie == 'Pachycheles_riseii':
            base.update({'n_dientes_margen_flexor': 1, 'n_placas_telson': 5})
        elif especie == 'Pachycheles_ackleianus':
            base.update({'n_dientes_margen_flexor': 2, 'n_placas_telson': 5})
        
        return base
    
    def _caracteristicas_neopisosoma(self, especie: str) -> Dict[str, Any]:
        """Genera características para especies del género Neopisosoma"""
        return {
            'longitud_caparazon': max(2.0, np.random.normal(6.0, 1.5)),
            'setas_margen_frontal': np.random.choice([0, 1], p=[0.6, 0.4]),
            'n_dientes_margen_flexor': np.random.choice([0, 1]),
            'patron_granulacion_quelipodos': np.random.choice([1, 2], p=[0.6, 0.4]),
            'tipo_quilla_abdominal': 'recta',
            'n_placas_telson': 5
        }
    
    def _caracteristicas_megalobrachium(self, especie: str) -> Dict[str, Any]:
        """Genera características para especies del género Megalobrachium"""
        base = {
            'longitud_caparazon': max(5.0, np.random.normal(9.0, 1.0)),
            'n_dientes_margen_flexor': np.random.choice([1, 2]),
            'patron_granulacion_quelipodos': np.random.choice([0, 1], p=[0.7, 0.3]),
            'n_placas_telson': 7
        }
        
        if especie == 'Megalobrachium_poeyi':
            base.update({'setas_margen_frontal': 1, 'tipo_quilla_abdominal': 'recta'})
        elif especie == 'Megalobrachium_roseum':
            base.update({'setas_margen_frontal': 0, 'tipo_quilla_abdominal': 'curvada'})
        elif especie == 'Megalobrachium_soriatum':
            base.update({'setas_margen_frontal': 0, 'tipo_quilla_abdominal': 'curvada', 'n_placas_telson': 5})
        elif especie == 'Megalobrachium_mortenseni':
            base.update({'setas_margen_frontal': 0, 'tipo_quilla_abdominal': 'recta'})
        
        return base
    
    def _caracteristicas_generales(self, especie: str) -> Dict[str, Any]:
        """Genera características para otras especies"""
        if especie == 'Clastotoechus_nodosus':
            return {
                'longitud_caparazon': max(5.0, np.random.normal(8.5, 1.0)),
                'setas_margen_frontal': np.random.choice([0, 1]),
                'n_dientes_margen_flexor': 1,
                'patron_granulacion_quelipodos': 1,
                'tipo_quilla_abdominal': 'recta',
                'n_placas_telson': 5
            }
        elif especie == 'Minyocerus_angustus':
            return {
                'longitud_caparazon': max(2.0, np.random.normal(4.5, 0.5)),
                'setas_margen_frontal': np.random.choice([0, 1]),
                'n_dientes_margen_flexor': 0,
                'patron_granulacion_quelipodos': np.random.choice([0, 1]),
                'tipo_quilla_abdominal': 'recta',
                'n_placas_telson': 7
            }
        elif especie == 'Pisidia_brasiliensis':
            return {
                'longitud_caparazon': max(8.0, np.random.normal(12.5, 1.5)),
                'setas_margen_frontal': np.random.choice([0, 1]),
                'n_dientes_margen_flexor': 2,
                'patron_granulacion_quelipodos': 1,
                'tipo_quilla_abdominal': 'recta',
                'n_placas_telson': 7
            }
        elif especie == 'Porcellana_sayana':
            return {
                'longitud_caparazon': max(8.0, np.random.normal(11.5, 1.5)),
                'setas_margen_frontal': np.random.choice([0, 1]),
                'n_dientes_margen_flexor': np.random.choice([2, 3]),
                'patron_granulacion_quelipodos': 1,
                'tipo_quilla_abdominal': 'recta',
                'n_placas_telson': 7
            }
        
        # Default para especies no especificadas
        return {
            'longitud_caparazon': max(5.0, np.random.normal(11.0, 2.0)),
            'setas_margen_frontal': np.random.choice([0, 1]),
            'n_dientes_margen_flexor': np.random.choice([1, 2, 3]),
            'patron_granulacion_quelipodos': np.random.choice([0, 1, 2]),
            'tipo_quilla_abdominal': np.random.choice(['recta', 'curvada']),
            'n_placas_telson': np.random.choice([5, 7])
        }
    
    def preparar_datos(self, datos: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, list]:
        """Prepara los datos para el entrenamiento"""
        print("🔧 Preparando datos para entrenamiento...")
        
        columnas_requeridas = [
            'longitud_caparazon', 'setas_margen_frontal', 'n_dientes_margen_flexor',
            'patron_granulacion_quelipodos', 'tipo_quilla_abdominal', 'n_placas_telson'
        ]
        
        # Asegurar que todas las columnas requeridas existen
        for col in columnas_requeridas:
            if col not in datos.columns:
                datos[col] = 0
                print(f"⚠️  Columna {col} no encontrada, se añadió con valores por defecto")
        
        # Codificar variables categóricas
        datos_encoded = pd.get_dummies(datos, columns=['tipo_quilla_abdominal'], prefix=['tipo_quilla_abdominal'])
        
        # Separar características y etiquetas
        columnas_caracteristicas = [col for col in datos_encoded.columns if col != 'especie']
        X = datos_encoded[columnas_caracteristicas]
        y = datos_encoded['especie']
        
        # Codificar etiquetas
        y_encoded = self.label_encoder.fit_transform(y)
        
        self.caracteristicas = X.columns.tolist()
        self.especies_disponibles = self.label_encoder.classes_.tolist()
        
        print(f"✅ Datos preparados: {X.shape[0]} muestras, {X.shape[1]} características")
        print(f"✅ Especies codificadas: {len(self.especies_disponibles)}")
        
        return X.values, y_encoded, self.caracteristicas
    
    def entrenar_modelo(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2) -> Dict[str, Any]:
        """Entrena el modelo de red neuronal con SMOTE"""
        print("🎯 Entrenando modelo con SMOTE...")
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Aplicar SMOTE para balancear clases
        smote = SMOTE(random_state=42)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        
        print(f"📈 Datos después de SMOTE: {X_train_balanced.shape[0]} muestras")
        
        # Estandarizar características
        X_train_scaled = self.scaler.fit_transform(X_train_balanced)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Crear y entrenar modelo
        self.modelo = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver='adam',
            max_iter=1000,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=50
        )
        
        print("⏳ Entrenando red neuronal...")
        self.modelo.fit(X_train_scaled, y_train_balanced)
        
        # Evaluar modelo
        y_pred = self.modelo.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        metricas = {
            'accuracy': accuracy,
            'reporte_clasificacion': classification_report(y_test, y_pred, target_names=self.label_encoder.classes_),
            'tamano_entrenamiento': len(X_train_balanced),
            'tamano_prueba': len(X_test),
            'n_caracteristicas': X.shape[1],
            'n_especies': len(self.especies_disponibles)
        }
        
        print(f"✅ Modelo entrenado - Precisión: {accuracy:.2%}")
        return metricas
    
    def predecir_especie(self, caracteristicas: Dict[str, Any]) -> Tuple[str, float]:
        """Predice la especie basada en características morfológicas"""
        if self.modelo is None:
            raise ValueError("❌ El modelo no ha sido entrenado")
        
        # Convertir a DataFrame
        df_caracteristicas = pd.DataFrame([caracteristicas])
        
        # Aplicar one-hot encoding si es necesario
        if 'tipo_quilla_abdominal' in df_caracteristicas.columns:
            df_encoded = pd.get_dummies(df_caracteristicas, columns=['tipo_quilla_abdominal'], prefix=['tipo_quilla_abdominal'])
        else:
            df_encoded = df_caracteristicas
        
        # Asegurar que todas las características estén presentes
        for col in self.caracteristicas:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        # Reordenar columnas
        df_encoded = df_encoded[self.caracteristicas]
        
        # Estandarizar y predecir
        X_scaled = self.scaler.transform(df_encoded.values)
        probabilidades = self.modelo.predict_proba(X_scaled)[0]
        
        indice_prediccion = np.argmax(probabilidades)
        especie_predicha = self.label_encoder.inverse_transform([indice_prediccion])[0]
        probabilidad = probabilidades[indice_prediccion]
        
        return especie_predicha, probabilidad
    
    def guardar_modelo(self, ruta: str = None):
        """Guarda el modelo entrenado"""
        if self.modelo is None:
            raise ValueError("❌ No hay modelo entrenado para guardar")
        
        if ruta is None:
            ruta = self._obtener_ruta_modelo()
        
        datos = {
            'modelo': self.modelo,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'caracteristicas': self.caracteristicas,
            'especies_disponibles': self.especies_disponibles
        }
        
        # Asegurar que el directorio existe
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
        
        joblib.dump(datos, ruta)
        print(f"💾 Modelo guardado en: {ruta}")
    
    def cargar_modelo(self, ruta: str = None):
        """Carga un modelo previamente entrenado"""
        if ruta is None:
            ruta = self._obtener_ruta_modelo()
        
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"❌ No se encontró el modelo en: {ruta}")
        
        datos = joblib.load(ruta)
        self.modelo = datos['modelo']
        self.scaler = datos['scaler']
        self.label_encoder = datos['label_encoder']
        self.caracteristicas = datos['caracteristicas']
        self.especies_disponibles = datos['especies_disponibles']
        
        print(f"📂 Modelo cargado desde: {ruta}")
        print(f"✅ {len(self.especies_disponibles)} especies disponibles")
    
    def obtener_total_especies(self) -> int:
        """Retorna el número total de especies disponibles"""
        return len(self.especies_disponibles) if self.especies_disponibles else 0
    
    def esta_entrenada(self) -> bool:
        """Verifica si el modelo está entrenado"""
        return self.modelo is not None

if __name__ == "__main__":
    # Prueba básica
    rn = RedNeuronalEspecies()
    print("🧠 Red neuronal probada correctamente")