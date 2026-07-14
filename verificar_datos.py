
#!/usr/bin/env python3
"""
Script para verificar la generación de datos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.red_neuronal import RedNeuronalEspecies
import pandas as pd

def verificar_generacion_datos():
    """Verifica que los datos se generen correctamente"""
    print("🔍 Verificando generación de datos...")
    
    try:
        red_neuronal = RedNeuronalEspecies()
        
        # Generar datos de prueba
        datos = red_neuronal.generar_datos_sinteticos(n_muestras_por_especie=5)
        
        print(f"✅ Datos generados: {datos.shape[0]} registros, {datos.shape[1]} columnas")
        print(f"📊 Columnas: {list(datos.columns)}")
        print(f"🐠 Especies: {datos['especie'].unique()}")
        
        # Verificar valores nulos
        print(f"🔍 Valores nulos por columna:")
        for col in datos.columns:
            nulos = datos[col].isnull().sum()
            if nulos > 0:
                print(f"   ❌ {col}: {nulos} valores nulos")
            else:
                print(f"   ✅ {col}: Sin valores nulos")
        
        # Mostrar algunas muestras
        print(f"\n📋 Primeras 3 muestras:")
        print(datos.head(3))
        
        # Preparar datos
        X, y, caracteristicas = red_neuronal.preparar_datos(datos)
        print(f"✅ Datos preparados: X.shape={X.shape}, y.shape={y.shape}")
        print(f"📈 Características: {len(caracteristicas)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verificar_generacion_datos()
    sys.exit(0 if success else 1)