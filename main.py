"""
Sistema Experto Híbrido para Identificación de Especies de Porcelanidae
"""
import tkinter as tk
import os
import sys
import traceback

# Configurar paths para importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'models'))
sys.path.insert(0, os.path.join(current_dir, 'ui'))
sys.path.insert(0, os.path.join(current_dir, 'utils'))
sys.path.insert(0, current_dir)

print("📁 Directorios de búsqueda configurados:")
for path in sys.path:
    if 'sistema_experto' in path:
        print(f"   📍 {path}")

try:
    from models.sistema_reglas import SistemaReglas
    from models.red_neuronal import RedNeuronalEspecies
    from ui.interfaz_grafica import InterfazSistemaExperto
    print("✅ Todos los módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("🔧 Verificando estructura de archivos...")
    
    # Verificar estructura
    estructura_esperada = {
        'models/': ['sistema_reglas.py', 'red_neuronal.py'],
        'ui/': ['interfaz_grafica.py'],
        'data/': ['clave_taxonomica.json']
    }
    
    for directorio, archivos in estructura_esperada.items():
        print(f"\n📁 {directorio}:")
        for archivo in archivos:
            ruta = os.path.join(directorio, archivo)
            if os.path.exists(ruta):
                print(f"   ✅ {archivo}")
            else:
                print(f"   ❌ {archivo} - NO ENCONTRADO")
    
    input("\nPresione Enter para salir...")
    sys.exit(1)

def inicializar_sistema():
    """
    Función que inicializa y ejecuta el sistema experto
    """
    print("🦀 Inicializando Sistema Experto de Porcelanidae...")
    print("=" * 60)
    
    try:
        # Inicializar sistema de reglas
        print("📋 Cargando sistema basado en reglas...")
        sistema_reglas = SistemaReglas()
        print(f"✅ Sistema de reglas cargado - {sistema_reglas.obtener_total_especies()} especies")
        
        # Inicializar red neuronal
        print("🧠 Inicializando red neuronal...")
        red_neuronal = RedNeuronalEspecies()
        
        # Buscar o entrenar modelo
        modelo_paths = [
            "modelo_entrenado.pkl",
            "models/modelo_entrenado.pkl",
            "data/modelo_entrenado.pkl"
        ]
        
        modelo_encontrado = None
        for path in modelo_paths:
            if os.path.exists(path):
                modelo_encontrado = path
                break
        
        if modelo_encontrado:
            try:
                red_neuronal.cargar_modelo(modelo_encontrado)
                print(f"✅ Modelo de red neuronal cargado - {red_neuronal.obtener_total_especies()} especies")
            except Exception as e:
                print(f"⚠️  No se pudo cargar el modelo: {e}")
                print("🔧 Entrenando nuevo modelo...")
                entrenar_red_neuronal(red_neuronal)
        else:
            print("🔧 Modelo no encontrado. Entrenando nuevo modelo...")
            entrenar_red_neuronal(red_neuronal)
        
        return sistema_reglas, red_neuronal
        
    except Exception as e:
        print(f"❌ Error crítico al inicializar el sistema: {e}")
        traceback.print_exc()
        return None, None

def entrenar_red_neuronal(red_neuronal):
    """Entrena la red neuronal"""
    try:
        print("📊 Generando datos de entrenamiento...")
        datos = red_neuronal.generar_datos_sinteticos(n_muestras_por_especie=50)
        X, y, caracteristicas = red_neuronal.preparar_datos(datos)
        
        print("🎯 Entrenando modelo...")
        metricas = red_neuronal.entrenar_modelo(X, y)
        
        # Guardar modelo en la ubicación más apropiada
        red_neuronal.guardar_modelo("models/modelo_entrenado.pkl")
        print(f"✅ Modelo entrenado - Precisión: {metricas['accuracy']:.2%}")
        print(f"📈 Especies entrenadas: {red_neuronal.obtener_total_especies()}")
        
    except Exception as e:
        print(f"⚠️  No se pudo entrenar el modelo: {e}")
        print("🔧 El modo red neuronal no estará disponible")

def main():
    """
    Función principal que ejecuta la aplicación
    """
    print("\n🚀 Iniciando Sistema Experto de Porcelanidae")
    print("⏳ Por favor espere...\n")
    
    # Mostrar estructura del proyecto
    print("📂 Estructura del proyecto:")
    for root, dirs, files in os.walk('.'):
        # Excluir directorios ocultos y __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}📁 {os.path.basename(root) or "sistema_experto_porcelanidae"}')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith(('.py', '.json', '.csv', '.pkl')):
                print(f'{subindent}📄 {file}')
        if level > 2:  # Limitar profundidad
            break
    
    sistema_reglas, red_neuronal = inicializar_sistema()
    
    if sistema_reglas is None:
        print("💥 No se pudo inicializar el sistema.")
        input("\nPresione Enter para salir...")
        return
    
    try:
        # Crear interfaz gráfica
        print("\n🎨 Inicializando interfaz gráfica...")
        root = tk.Tk()
        app = InterfazSistemaExperto(root, sistema_reglas, red_neuronal)
        
        print("\n🎉 ¡Sistema listo!")
        print("💡 Características disponibles:")
        print(f"   ✅ Sistema basado en reglas ({sistema_reglas.obtener_total_especies()} especies)")
        
        if hasattr(red_neuronal, 'modelo') and red_neuronal.modelo is not None:
            print(f"   ✅ Red neuronal ({red_neuronal.obtener_total_especies()} especies)")
        else:
            print("   ⚠️  Red neuronal (no disponible - use modo reglas)")
        
        print("   ✅ Interfaz gráfica intuitiva")
        print("   ✅ Historial de identificaciones")
        print("   ✅ Múltiples modos de operación")
        print("\n👆 La interfaz se ha abierto. ¡Comience a identificar especies!")
        
        # Configurar cierre seguro
        def al_cerrar():
            print("\n👋 Sesión finalizada - ¡Hasta pronto!")
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", al_cerrar)
        root.mainloop()
        
    except Exception as e:
        print(f"💥 Error en la interfaz gráfica: {e}")
        traceback.print_exc()
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()