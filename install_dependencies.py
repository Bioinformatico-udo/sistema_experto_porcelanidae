#!/usr/bin/env python3
"""
Script de instalación corregido para el Sistema Experto de Porcelanidae
"""
import subprocess
import sys
import os
import platform
from pathlib import Path

class InstaladorCorregido:
    """Instalador corregido que maneja tkinter apropiadamente"""
    
    def __init__(self):
        self.sistema_operativo = platform.system().lower()
        self.requirements_file = "requirements_corregido.txt"
        
    def crear_requirements_corregido(self):
        """Crea un archivo requirements sin tkinter"""
        try:
            with open("requirements.txt", "r") as f_orig:
                lineas = f_orig.readlines()
            
            with open(self.requirements_file, "w") as f_corr:
                for linea in lineas:
                    if "tkinter" not in linea.lower():
                        f_corr.write(linea)
            
            print(f"✅ Archivo {self.requirements_file} creado (sin tkinter)")
            return True
        except Exception as e:
            print(f"❌ Error creando requirements corregido: {e}")
            return False
    
    def instalar_dependencias_pip(self):
        """Instala dependencias via pip"""
        print("🚀 Instalando dependencias Python...")
        
        try:
            comando = [
                sys.executable, "-m", "pip", "install", 
                "-r", self.requirements_file,
                "--user"
            ]
            
            proceso = subprocess.run(comando, check=True, capture_output=True, text=True)
            print("✅ Dependencias Python instaladas correctamente")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            print(f"Salida de error: {e.stderr}")
            return False
    
    def verificar_todas_dependencias(self):
        """Verifica todas las dependencias críticas"""
        dependencias_verificar = {
            "pandas": "pandas",
            "numpy": "numpy", 
            "scikit-learn": "sklearn",
            "matplotlib": "matplotlib",
            "seaborn": "seaborn",
            "imbalanced-learn": "imblearn",
            "Pillow": "PIL",
            "joblib": "joblib"
        }
        
        print("\n🔍 Verificando dependencias instaladas...")
        todas_ok = True
        
        for nombre, import_name in dependencias_verificar.items():
            try:
                if import_name == "PIL":
                    import PIL
                elif import_name == "sklearn":
                    import sklearn
                else:
                    __import__(import_name)
                print(f"✅ {nombre} - OK")
            except ImportError as e:
                print(f"❌ {nombre} - FALTANTE: {e}")
                todas_ok = False
        
        # Verificar tkinter por separado
        try:
            import tkinter
            from tkinter import ttk
            print("✅ tkinter - OK")
        except ImportError as e:
            print(f"❌ tkinter - FALTANTE: {e}")
            print("💡 Ejecute: python verificar_tkinter.py para solucionar")
            todas_ok = False
        
        return todas_ok
    
    def ejecutar(self):
        """Ejecuta el proceso completo de instalación"""
        print("=" * 60)
        print("🦀 INSTALADOR CORREGIDO - SISTEMA EXPERTO PORCELANIDAE")
        print("=" * 60)
        
        # Crear requirements corregido
        if not self.crear_requirements_corregido():
            return False
        
        # Instalar dependencias pip
        if not self.instalar_dependencias_pip():
            return False
        
        # Verificar tkinter
        print("\n🔍 Verificando tkinter...")
        try:
            import tkinter
            print("✅ tkinter está disponible")
        except ImportError:
            print("❌ tkinter no disponible")
            print("🔄 Ejecutando solucionador de tkinter...")
            subprocess.run([sys.executable, "verificar_tkinter.py"])
        
        # Verificar todas las dependencias
        if not self.verificar_todas_dependencias():
            print("\n⚠️  Algunas dependencias pueden requerir atención manual")
        else:
            print("\n🎉 ¡Todas las dependencias están instaladas!")
        
        # Limpiar archivo temporal
        try:
            os.remove(self.requirements_file)
            print(f"✅ Archivo temporal {self.requirements_file} eliminado")
        except:
            pass
        
        return True

def main():
    instalador = InstaladorCorregido()
    success = instalador.ejecutar()
    
    if success:
        print("\n" + "=" * 60)
        print("✨ ¡El sistema está listo para usar!")
        print("Ejecute: python main.py")
        print("=" * 60)
    else:
        print("\n💥 La instalación encontró problemas.")
        print("💡 Soluciones:")
        print("1. Ejecute: python verificar_tkinter.py")
        print("2. Instale dependencias manualmente: pip install pandas numpy scikit-learn matplotlib seaborn imbalanced-learn Pillow")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)