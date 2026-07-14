"""
Sistema experto basado en reglas para identificación de especies de Porcelanidae
"""
import json
import os
from typing import Dict, List, Optional

class SistemaReglas:
    """
    Sistema experto basado en reglas para identificación taxonómica
    """
    
    def __init__(self, ruta_json: str = None):
        if ruta_json is None:
            self.ruta_json = self._encontrar_archivo_clave()
        else:
            self.ruta_json = ruta_json
            
        self.clave = self._cargar_clave_taxonomica()
        self.historial = []
        print(f"📋 Sistema de reglas inicializado con archivo: {self.ruta_json}")
    
    def _encontrar_archivo_clave(self):
        """Busca el archivo clave_taxonomica.json en múltiples ubicaciones"""
        ubicaciones = [
            "data/clave_taxonomica.json",  # Estructura esperada
            "../data/clave_taxonomica.json",  # Desde models/
            "clave_taxonomica.json",  # Directorio actual
            "../clave_taxonomica.json",  # Directorio padre
        ]
        
        for ubicacion in ubicaciones:
            if os.path.exists(ubicacion):
                print(f"✅ Clave taxonómica encontrada en: {ubicacion}")
                return ubicacion
        
        # Si no se encuentra, crear una básica en data/
        print("⚠️  No se encontró clave_taxonomica.json, creando una básica...")
        return "data/clave_taxonomica.json"
    
    def _cargar_clave_taxonomica(self) -> Dict:
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                data = json.load(archivo)
                print(f"✅ Clave taxonómica cargada correctamente")
                return data
        except FileNotFoundError:
            print(f"❌ No se pudo cargar {self.ruta_json}, creando clave básica...")
            return self._crear_clave_basica()
        except json.JSONDecodeError as e:
            print(f"❌ Error en formato JSON: {e}")
            return self._crear_clave_basica()
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return self._crear_clave_basica()
    
    def _crear_clave_basica(self) -> Dict:
        """Crea una clave taxonómica básica si no existe el archivo"""
        clave_basica = {
            "clave_porcelanidae": {
                "pregunta_1": {
                    "texto": "Artejo basal de la antena corto, no alcanza el margen anterior del caparazón",
                    "si": "pregunta_2", 
                    "no": "pregunta_17"
                },
                "pregunta_2": {
                    "texto": "Porciones posteriores de la pared del caparazón ausentes",
                    "si": "pregunta_3",
                    "no": "genero_petrolisthes"
                },
                "pregunta_3": {
                    "texto": "Caparazón con paredes laterales incompletas",
                    "si": "pregunta_4",
                    "no": "pregunta_6"
                },
                "pregunta_4": {
                    "texto": "Quelípedos con la superficie dorsal cubierta por gránulos y/o tubérculos",
                    "si": "pregunta_5",
                    "no": "Neopisosoma_cf_neglectum"
                },
                "pregunta_5": {
                    "texto": "Quelípedos con gránulos y tubérculos cónicos; setas escasas",
                    "si": "Neopisosoma_angustifrons", 
                    "no": "Neopisosoma_orientale"
                },
                "pregunta_6": {
                    "texto": "Quelípedos aplanados, subiguales. Frente trilobulada. Telson con 5 piezas",
                    "si": "Clastotoechus_nodosus",
                    "no": "genero_pachycheles"
                },
                "genero_pachycheles": {
                    "pregunta_7": {
                        "texto": "Telson compuesto por siete piezas",
                        "si": "Pachycheles_serratus",
                        "no": "pregunta_8"
                    },
                    "pregunta_8": {
                        "texto": "Frente con la porción media más avanzada que los ángulos orbitales",
                        "si": "Pachycheles_monilifer", 
                        "no": "pregunta_9"
                    },
                    "pregunta_9": {
                        "texto": "Carpo de los quelípedos lisos, sin gránulos. Frente sinuosa",
                        "si": "Pachycheles_riseii",
                        "no": "Pachycheles_ackleianus"
                    }
                },
                "genero_petrolisthes": {
                    "pregunta_10": {
                        "texto": "Carpo de los quelípedos entero",
                        "si": "pregunta_11",
                        "no": "pregunta_12"
                    },
                    "pregunta_11": {
                        "texto": "Frente con un diente lobuliforme en ángulos orbitales internos",
                        "si": "Petrolisthes_tridentatus",
                        "no": "Petrolisthes_tonsorius"
                    },
                    "pregunta_12": {
                        "texto": "Telson constituido por cinco piezas", 
                        "si": "Petrolisthes_jugosus",
                        "no": "pregunta_13"
                    },
                    "pregunta_13": {
                        "texto": "Espina epibranquial ausente",
                        "si": "pregunta_14",
                        "no": "pregunta_15"
                    },
                    "pregunta_14": {
                        "texto": "Margen flexor del carpo con tres dientes subiguales",
                        "si": "Petrolisthes_politus",
                        "no": "Petrolisthes_lewisi"
                    },
                    "pregunta_15": {
                        "texto": "Margen flexor del carpo con tres dientes separados",
                        "si": "Petrolisthes_armatus",
                        "no": "pregunta_16"
                    },
                    "pregunta_16": {
                        "texto": "Caparazón áspero, con estrías pilíferas transversas prominentes",
                        "si": "Petrolisthes_galathinus",
                        "no": "Petrolisthes_marginatus"
                    }
                },
                "pregunta_17": {
                    "texto": "Artejos móviles de la antena muy pequeños, flagelo rudimentario",
                    "si": "Minyocerus_angustus",
                    "no": "pregunta_18"
                },
                "pregunta_18": {
                    "texto": "Caparazón tan largo como ancho. Frente inclinada, redondeada triangular", 
                    "si": "genero_megalobrachium",
                    "no": "pregunta_22"
                },
                "genero_megalobrachium": {
                    "pregunta_19": {
                        "texto": "Telson constituido por cinco placas",
                        "si": "Megalobrachium_soriatum",
                        "no": "pregunta_20"
                    },
                    "pregunta_20": {
                        "texto": "Caparazón y quelípedos fuertemente erosionados",
                        "si": "Megalobrachium_mortenseni",
                        "no": "pregunta_21"
                    },
                    "pregunta_21": {
                        "texto": "Caparazón y quelípedos con setas abundantes",
                        "si": "Megalobrachium_poeyi",
                        "no": "Megalobrachium_roseum"
                    }
                },
                "pregunta_22": {
                    "texto": "Márgenes laterales del caparazón con espínulas posteriores",
                    "si": "Pisidia_brasiliensis",
                    "no": "Porcellana_sayana"
                }
            }
        }
        
        # Guardar la clave básica
        try:
            # Asegurar que el directorio existe
            directorio = os.path.dirname(self.ruta_json)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)
            
            with open(self.ruta_json, 'w', encoding='utf-8') as f:
                json.dump(clave_basica, f, indent=4, ensure_ascii=False)
            print(f"✅ Clave taxonómica básica creada en: {self.ruta_json}")
        except Exception as e:
            print(f"⚠️  No se pudo guardar la clave básica: {e}")
        
        return clave_basica
    
    def obtener_pregunta(self, nodo: str) -> Optional[Dict]:
        """Obtiene los datos de una pregunta por su nodo"""
        return self.clave["clave_porcelanidae"].get(nodo)
    
    def obtener_siguiente_nodo(self, nodo_actual: str, respuesta: bool) -> str:
        """Obtiene el siguiente nodo basado en la respuesta"""
        pregunta = self.obtener_pregunta(nodo_actual)
        if not pregunta:
            return None
        return pregunta['si'] if respuesta else pregunta['no']
    
    def es_especie_final(self, nodo: str) -> bool:
        """Determina si un nodo representa una especie final"""
        especies_finales = [
            'Neopisosoma_cf_neglectum', 'Neopisosoma_angustifrons', 'Neopisosoma_orientale',
            'Clastotoechus_nodosus', 'Pachycheles_serratus', 'Pachycheles_monilifer',
            'Pachycheles_riseii', 'Pachycheles_ackleianus', 'Petrolisthes_tridentatus',
            'Petrolisthes_tonsorius', 'Petrolisthes_jugosus', 'Petrolisthes_politus',
            'Petrolisthes_lewisi', 'Petrolisthes_armatus', 'Petrolisthes_galathinus',
            'Petrolisthes_marginatus', 'Minyocerus_angustus', 'Megalobrachium_soriatum',
            'Megalobrachium_mortenseni', 'Megalobrachium_poeyi', 'Megalobrachium_roseum',
            'Pisidia_brasiliensis', 'Porcellana_sayana'
        ]
        return nodo in especies_finales
    
    def formatear_especie(self, nombre_especie: str) -> str:
        """Formatea el nombre de la especie para mostrar"""
        nombre_formateado = nombre_especie.replace('_', ' ').title()
        return nombre_formateado
    
    def obtener_total_especies(self) -> int:
        """Retorna el número total de especies identificables"""
        return 23
    
    def obtener_historial(self) -> List:
        """Retorna el historial de preguntas y respuestas"""
        return self.historial

if __name__ == "__main__":
    # Prueba del sistema
    sistema = SistemaReglas()
    print(f"🦀 Sistema de reglas cargado - {sistema.obtener_total_especies()} especies")
    
    # Probar una pregunta
    pregunta = sistema.obtener_pregunta("pregunta_1")
    if pregunta:
        print(f"📝 Primera pregunta: {pregunta['texto']}")