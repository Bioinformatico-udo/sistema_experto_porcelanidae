# verificar_imagenes.py (ubicado en la raíz del proyecto)
"""
Script para verificar qué imágenes están disponibles
"""
import os
import sys

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils.config_imagenes import ConfigImagenes

def verificar_imagenes():
    """Verifica el estado de todas las imágenes"""
    print("=" * 70)
    print("📸 VERIFICACIÓN DE IMÁGENES DE ESPECIES")
    print("=" * 70)
    
    # Verificar carpeta de imágenes
    if not os.path.exists(ConfigImagenes.RUTA_IMAGENES):
        print(f"\n❌ La carpeta '{ConfigImagenes.RUTA_IMAGENES}' no existe")
        print(f"💡 Crear la carpeta y agregar las imágenes")
        print(f"\n📝 Crear carpeta:")
        print(f"   mkdir {ConfigImagenes.RUTA_IMAGENES}")
        return
    
    # Verificar imágenes existentes
    print(f"\n📁 Carpeta de imágenes: {ConfigImagenes.RUTA_IMAGENES}")
    print("-" * 70)
    
    estado = ConfigImagenes.verificar_imagenes_existentes()
    
    total = len(estado)
    disponibles = sum(1 for v in estado.values() if v)
    faltantes = total - disponibles
    
    print(f"\n📊 Resumen:")
    print(f"   ✅ Imágenes disponibles: {disponibles}/{total}")
    print(f"   ❌ Imágenes faltantes: {faltantes}/{total}")
    print(f"   📊 Porcentaje: {disponibles/total*100:.1f}%")
    
    # Mostrar especies con y sin imagen
    if faltantes > 0:
        print("\n❌ Especies SIN imagen:")
        for especie, existe in estado.items():
            if not existe:
                nombre_formateado = especie.replace('_', ' ').title()
                print(f"   • {nombre_formateado}")
    
    print("\n✅ Especies CON imagen:")
    for especie, existe in estado.items():
        if existe:
            nombre_formateado = especie.replace('_', ' ').title()
            print(f"   • {nombre_formateado}")
    
    # Mostrar estructura de archivos
    print("\n📁 Archivos en la carpeta de imágenes:")
    archivos = os.listdir(ConfigImagenes.RUTA_IMAGENES)
    if archivos:
        for archivo in sorted(archivos):
            tamaño = os.path.getsize(os.path.join(ConfigImagenes.RUTA_IMAGENES, archivo))
            tamaño_kb = tamaño / 1024
            print(f"   • {archivo} ({tamaño_kb:.1f} KB)")
    else:
        print("   ⚠️ No hay archivos en la carpeta")
    
    print("\n" + "=" * 70)
    print("💡 Recomendaciones:")
    if faltantes > 0:
        print(f"   • Agregue las {faltantes} imágenes faltantes en la carpeta '{ConfigImagenes.RUTA_IMAGENES}'")
        print("   • Use el formato: genero_especie.jpg (ej: petrolisthes_armatus.jpg)")
    if disponibles == 0:
        print("   • No hay imágenes disponibles. El sistema mostrará placeholders.")
    print("=" * 70)

def crear_archivo_placeholder():
    """Crea un archivo de imagen placeholder si no existe"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Crear carpeta si no existe
        if not os.path.exists(ConfigImagenes.RUTA_IMAGENES):
            os.makedirs(ConfigImagenes.RUTA_IMAGENES)
        
        # Crear imagen placeholder
        img = Image.new('RGB', (400, 300), color=(200, 200, 200))
        draw = ImageDraw.Draw(img)
        
        # Dibujar texto
        draw.text((50, 130), "Sin imagen", fill=(100, 100, 100))
        draw.text((50, 160), "disponible", fill=(100, 100, 100))
        
        # Guardar
        ruta_placeholder = os.path.join(ConfigImagenes.RUTA_IMAGENES, ConfigImagenes.IMAGEN_DEFECTO)
        img.save(ruta_placeholder)
        print(f"✅ Imagen placeholder creada: {ruta_placeholder}")
        
    except ImportError:
        print("⚠️ Pillow no instalado. No se puede crear imagen placeholder.")
        print("   Instale con: pip install Pillow")
    except Exception as e:
        print(f"❌ Error creando placeholder: {e}")

if __name__ == "__main__":
    # Verificar si existe la carpeta de imágenes
    if not os.path.exists(ConfigImagenes.RUTA_IMAGENES):
        print(f"📁 Creando carpeta: {ConfigImagenes.RUTA_IMAGENES}")
        os.makedirs(ConfigImagenes.RUTA_IMAGENES)
        print("✅ Carpeta creada")
    
    # Crear placeholder si no existe
    ruta_placeholder = os.path.join(ConfigImagenes.RUTA_IMAGENES, ConfigImagenes.IMAGEN_DEFECTO)
    if not os.path.exists(ruta_placeholder):
        print("📸 Creando imagen placeholder...")
        crear_archivo_placeholder()
    
    verificar_imagenes()