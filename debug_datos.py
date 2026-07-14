#!/usr/bin/env python3
"""
Script de depuración para datos
"""
import pandas as pd
import numpy as np

def crear_datos_manual():
    """Crea datos manualmente para debugging"""
    datos = []
    
    # Crear datos de ejemplo manualmente
    for i in range(50):
        datos.append({
            'longitud_caparazon': np.random.normal(12.0, 2.0),
            'setas_margen_frontal': np.random.choice([0, 1]),
            'n_dientes_margen_flexor': np.random.choice([0, 2, 3, 4]),
            'patron_granulacion_quelipodos': np.random.choice([0, 1, 2, 3]),
            'tipo_quilla_abdominal': np.random.choice(['recta', 'curvada', 'discontinua']),
            'n_placas_telson': np.random.choice([5, 7]),
            'especie': np.random.choice(['Petrolisthes_armatus', 'Petrolisthes_galathinus'])
        })
    
    df = pd.DataFrame(datos)
    df.to_csv('data/dataset_manual.csv', index=False)
    print("✅ Datos manuales creados en data/dataset_manual.csv")
    return df

if __name__ == "__main__":
    df = crear_datos_manual()
    print(df.head())
    print(f"Columnas: {list(df.columns)}")
