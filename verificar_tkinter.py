
#!/usr/bin/env python3
"""
Script para verificar e instalar tkinter en sistemas Linux
"""
import subprocess
import sys
import platform

def verificar_tkinter():
    """Verifica si tkinter está disponible"""
    try:
        import tkinter
        from tkinter import ttk
        print("✅ tkinter está disponible")
        return True
    except ImportError as e:
        print(f"❌ tkinter no disponible: {e}")
        return False

def instalar_tkinter_linux():
    """Instala tkinter en sistemas basados en Debian/Ubuntu"""
    sistema = platform.system().lower()
    
    if sistema == "linux":
        print("🔄 Intentando instalar tkinter para Linux...")
        
        # Detectar gestor de paquetes
        try:
            # Para sistemas basados en Debian/Ubuntu
            subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-tk', 'tk-dev'], check=True)
            print("✅ tkinter instalado exitosamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ No se pudo instalar tkinter automáticamente")
            
        # Para sistemas basados en RedHat/CentOS
        try:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'python3-tkinter'], check=True)
            print("✅ tkinter instalado exitosamente")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        # Para sistemas basados en Arch
        try:
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'tk'], check=True)
            print("✅ tkinter instalado exitosamente")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
    return False

def instrucciones_manuales():
    """Muestra instrucciones manuales para instalar tkinter"""
    sistema = platform.system().lower()
    
    print("\n📋 INSTRUCCIONES MANUALES PARA INSTALAR tkinter:")
    print("=" * 50)
    
    if sistema == "linux":
        print("""
Para sistemas basados en DEBIAN/UBUNTU:
    sudo apt update
    sudo apt install python3-tk tk-dev

Para sistemas basados en REDHAT/CENTOS/FEDORA:
    sudo yum install python3-tkinter
    # o en Fedora más reciente:
    sudo dnf install python3-tkinter

Para sistemas basados en ARCH/MANJARO:
    sudo pacman -S tk

Para sistemas basados en OPENSUSE:
    sudo zypper install python3-tk
        """)
    elif sistema == "windows":
        print("""
En Windows, tkinter normalmente viene incluido con Python.
Si no está disponible:
1. Reinstala Python desde python.org
2. Durante la instalación, marca la opción "Install tkinter and IDLE"
3. Asegúrate de marcar "Add Python to PATH"
        """)
    elif sistema == "darwin":  # macOS
        print("""
En macOS:
1. Si usas Python de python.org, tkinter viene incluido
2. Si usas Homebrew: brew install python-tk
3. Si usas MacPorts: sudo port install py39-tkinter (ajusta la versión)
        """)

def main():
    """Función principal"""
    print("🔍 Verificando tkinter...")
    
    if verificar_tkinter():
        print("🎉 tkinter está listo para usar!")
        return True
    else:
        print("\n❌ tkinter no está disponible")
        
        # Intentar instalación automática en Linux
        if platform.system().lower() == "linux":
            print("🔄 Intentando instalación automática...")
            if instalar_tkinter_linux():
                if verificar_tkinter():
                    print("🎉 tkinter instalado y verificado correctamente!")
                    return True
        
        # Mostrar instrucciones manuales
        instrucciones_manuales()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)