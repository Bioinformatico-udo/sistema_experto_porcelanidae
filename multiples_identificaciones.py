
#!/usr/bin/env python3
"""
Ejemplo de uso del sistema con múltiples identificaciones
"""
import tkinter as tk
from models.sistema_reglas import SistemaReglas
from models.red_neuronal import RedNeuronalEspecies
from ui.interfaz_grafica import InterfazSistemaExperto

def main():
    """Función principal con sistema mejorado"""
    print("🚀 Iniciando Sistema Experto Mejorado...")
    print("✅ Ahora puede realizar múltiples identificaciones por sesión")
    print("✅ Use 'Nueva Identificación' para reiniciar")
    print("✅ Use 'Limpiar Historial' para borrar resultados\n")
    
    try:
        # Inicializar componentes
        sistema_reglas = SistemaReglas()
        red_neuronal = RedNeuronalEspecies()
        
        # Cargar modelo si existe
        modelo_path = "models/modelo_entrenado.pkl"
        try:
            red_neuronal.cargar_modelo(modelo_path)
            print("✅ Modelo de red neuronal cargado")
        except:
            print("⚠️  Modelo de red neuronal no disponible - usando solo modo reglas")
        
        # Crear interfaz
        root = tk.Tk()
        app = InterfazSistemaExperto(root, sistema_reglas, red_neuronal)
        
        print("🎯 Sistema listo para múltiples identificaciones")
        print("💡 Características mejoradas:")
        print("   • Múltiples identificaciones por sesión")
        print("   • Historial persistente")
        print("   • Botones de control mejorados")
        print("   • Cancelación de identificaciones en curso")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()