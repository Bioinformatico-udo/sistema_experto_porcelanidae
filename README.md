🦀 Sistema Experto Híbrido para Identificación de Porcelanidae
Versión de Python Licencia Estado

Sistema Experto desarrollado como proyecto educativo para la Licenciatura en Informática Universidad de Oriente, Núcleo de Nueva Esparta - Venezuela

📋 Tabla de Contenidos
📖 Descripción del Proyecto
🎯 Objetivos Educativos
🏗️Arquitectura del Sistema
✨ Características principales
📊 Especies Soportadas
🛠️ Tecnologías Utilizadas
📦 Instalación y configuración
🚀 Guía de Uso
📁 Estructura del Proyecto
👨‍💻 Para Estudiantes (Guía de Aprendizaje)
🤝 Contribuciones
📄 Licencia
📞 Contacto
📖 Descripción del Proyecto
El Sistema Experto Híbrido para Identificación de Porcelanidae es una aplicación educativa que combina técnicas de Inteligencia Artificial y Sistemas Expertos para la identificación taxonómica de crustáceos de la familia Porcelanidae (cangrejos porcelana).

Este proyecto fue desarrollado como material didáctico para estudiantes de la Licenciatura en Informática de la Universidad de Oriente, Núcleo de Nueva Esparta , con el objetivo de demostrar la aplicación práctica de conceptos de:

Sistemas Basados ​​en Reglas (Clave Taxonómica)
Redes Neuronales Artificiales
Interfaces de Usuario (GUI)
Manejo de Datos e Imágenes
🎯 Objetivos Educativos
Demostrar la aplicación de sistemas expertos en el mundo real
Integrar diferentes técnicas de IA en una sola aplicación
Mostrar el ciclo de vida de un proyecto de software.
Enseñar buenas prácticas de programación en Python
Fomentar el interés por la Inteligencia Artificial y la Ciencia de Datos
🏗️Arquitectura del Sistema
gráfico TB subgrafo "Frontend" GUI[Interfaz Gráfica Tkinter] Pestañas[Sistema de Pestañas] Imágenes[Visualización de Imágenes] fin

subgraph "Motor de Inferencia"
    Rules[Sistema de Reglas]
    NN[Red Neuronal]
    Hybrid[Motor Híbrido]
end

subgraph "Base de Conocimiento"
    DB[(Base de Datos)]
    Fichas[Fichas Técnicas]
    Taxonomia[Clave Taxonómica]
    Imagenes[Carpeta de Imágenes]
end

GUI --> Rules
GUI --> NN
Rules --> Taxonomia
NN --> DB
Rules --> Fichas
NN --> Fichas
Hybrid --> Rules
Hybrid --> NN
Images --> Imagenes
Componentes Principales
Componente Descripción Tecnología
Sistema de Reglas Clave taxonómica dicotómica tradicional Python (Lógica de árbol) Red Neuronal Modelo de clasificación entrenado Scikit-learn (MLPClassifier) ​​Interfaz Gráfica Aplicación de escritorio Tkinter (GUI) Base de Datos Fichas técnicas de especies JSON Manejo de Imágenes Visualización de especies Pillow (PIL) ✨ Características Principales 🔍 Modo Clave Taxonómica (Reglas) Identificación mediante preguntas dicotómicas guiadas

Basado en características morfológicas tradicionales

Proceso educativo paso a paso

Ideal para estudiantes sin experiencia previa.

23 especies disponibles

🧠 Modo Red Neuronal (IA) Identificación mediante inteligencia artificial

predicción instantánea basada en medidas

Alta precisión con datos completos

Resultados con nivel de confianza

17 especies disponibles

📸 Visualización de Especies Imágenes de cada especie identificada

Fichas técnicas completas

Taxonomía, distribución y conservación.

Miniaturas en historial y favoritos

📊 Gestión de Resultados Historial completo de identificaciones

Sistema de favoritos

Exportación de resultados

📊 Especies Soportadas Género Petrolisthes (8 especies) Petrolisthes armatus - Cangrejo porcelana armado

Petrolisthes tridentatus - Cangrejo porcelana tridentado

Petrolisthes tonsorius - Cangrejo porcelana tonsor

Petrolisthes jugosus - Cangrejo porcelana rugoso

Petrolisthes politus - Cangrejo porcelana pulido

Petrolisthes lewisi - Cangrejo porcelana de Lewis

Petrolisthes galathinus - Cangrejo porcelana galatea

Petrolisthes marginatus - Cangrejo porcelana marginado

Género Pachycheles (4 especies) Pachycheles serratus - Cangrejo porcelana serrado

Pachycheles monilifer - Cangrejo porcelana monilífero

Pachycheles riseii - Cangrejo porcelana de Rise

Pachycheles ackleianus - Cangrejo porcelana de Ackley

Género Megalobrachium (4 especies) Megalobrachium soriatum - Cangrejo porcelana soriano

Megalobrachium mortenseni - Cangrejo porcelana de Mortensen

Megalobrachium poeyi - Cangrejo porcelana de Poey

Megalobrachium roseum - Cangrejo porcelana rosado

Otros Géneros (7 especies) Neopisosoma negligente - Cangrejo porcelana olvidado

Neopisosoma angustifrons - Cangrejo porcelana de frente angosta

Neopisosoma orientale - Cangrejo porcelana oriental

Clastotoechus nodosus - Cangrejo porcelana nodoso

Minyocerus angustus - Cangrejo porcelana angosto

Pisidia brasiliensis - Cangrejo porcelana de Brasil

Porcellana sayana - Cangrejo porcelana de Say

🛠️ Tecnologías Utilizadas
Lenguajes y Frameworks Python 3.13 - Lenguaje principal

Tkinter - Interfaz gráfica nativa

Scikit-learn - Redes neuronales y ML

Almohada - Procesamiento de imágenes

Bibliotecas y herramientas Python

Dependencias principales
numpy>=1.21.0 # Operaciones numéricas scikit-learn>=1.0.0 # Machine Learning pandas>=1.3.0 # Manipulación de datos matplotlib>=3.4.0 # Visualización Pillow>=9.0.0 # Procesamiento de imágenes Conceptos Aplicados IA Simbólica: Sistemas basados ​​en reglas

IA Subsimbólica: Redes neuronales

Sistemas Expertos: Motor de inferencia

Interacción Humano-Computador: Diseño de GUI

Ingeniería de Software: Estructura modular

📦 Instalación y configuración
Requisitos Anteriores Python 3.8 o superior

Conexión a Internet (para instalación de dependencias)

Instalación Paso a Paso

Clonar el Repositorio bash git clone https://github.com/tu-usuario/sistema-experto-porcelanidae.git cd sistema-experto-porcelanidae
Crear un Entorno Virtual (Recomendado) bash
En Windows
python -m venv venv venv\Scripts\activate

En Linux/Mac
python -m venv venv source venv/bin/activate 3. Instalar Dependencias bash pip install -r requisitos.txt 4. Verificar la Instalación bash

Verificar que todas las dependencias están instaladas
python -c "import tkinter, sklearn, PIL, numpy, pandas; print('✅ Todas las dependencias instaladas correctamente')" 5. Ejecutar la aplicación bash python main.py Configuración de Imágenes (Opcional) Para mostrar imágenes de las especies:

Crear una carpeta llamada imagenes_especies/

Agregar imágenes con formato: genero_especie.jpg

Ejecutar python verificar_imagenes.py para verificar

🚀 Guía de Uso
Inicio Rápido Seleccionar Modo: Elige entre "Clave Taxonómica" o "Red Neuronal"

Identificar: Sigue las instrucciones según el modo seleccionado

Ver Resultados: Revisa la especie identificada, imagen y ficha técnica

Gestionar: Guarda en favoritos o exporta resultados

Modo Clave Taxonómica texto

Haz clic en "Iniciar Identificación"
Responde Sí/No a cada pregunta
El sistema navega por el árbol de decisiones.
¡Identificación completada! Modo Rojo Texto neuronal
Complete el formulario con medidas
Haz clic en "Predecir Especie"
Revisa la predicción y confianza.
📁 Estructura del Proyecto
text sistema_experto_porcelanidae/ ├── data/ │ ├── clave_taxonomica.json # Base de conocimientos taxonómicos │ ├── fichas_tecnicas.json # Fichas técnicas de especies │ ├── dataset_especies.csv # Datos para entrenamiento │ └── dataset_manual.csv # Datos manuales ├── models/ │ ├── sistema_reglas.py # Sistema basado en reglas │ ├── red_neuronal.py # Red neuronal artificial │ └── modelo_entrenado.pkl # Modelo pre-entrenado ├── interfaz de usuario/ │ └── interfaz_grafica.py # Interfaz de usuario ├── utils/ │ ├── config_imagenes.py # Configuración de imágenes │ ├── fichas_tecnicas.py # Gestor de fichas técnicas │ ├── manejador_imagenes.py # Manejador de imágenes │ ├── preprocesamiento.py # Preprocesamiento de datos │ └── visualizacion.py # Visualización de datos ├── imagenes_especies/ # Carpeta de imágenes (opcional) ├── main.py # Punto de entrada ├── setup.py # Script de instalación ├── requisitos.txt # Dependencias └── README.md#Documentación

👨‍💻 Para Estudiantes (Guía de Aprendizaje)
Conceptos Clave a Aprender

Sistemas Basados ​​en Reglas Python
Ejemplo de regla en el sistema
{ "pregunta_1": { "texto": "¿El artejo basal de la antena es corto?", "si": "pregunta_2", "no": "pregunta_17" } } 2. Redes Neuronales con Scikit-learn python

Creación del modelo
modelo = MLPClassifier( hidden_layer_sizes=(100, 50), activation='relu', max_iter=1000, random_state=42 ) 3. Interfaz de Usuario con Tkinter python

Creación de ventana
root = tk.Tk() root.title("Sistema Experto Porcelanidae") root.geometry("1400x850") 4. Manejo de Datos Lectura/escritura de JSON

Procesamiento de imágenes con Pillow

Manipulación de datos con Pandas

Ejercicios Sugeridos Agregar una nueva especie:

Añadir ficha técnica en fichas_tecnicas.json

Actualizar la clave taxonómica

Mejorar la interfaz:

Agregar nuevos colores o temas

Crear nuevas pestañas de funcionalidad

Optimizar la red neuronal:

Probar diferentes arquitecturas

Mejorar el preprocesamiento

Exportar resultados:

Implementar exportación a PDF o Excel

Generar informes estadisticos

🤝 Contribuciones
Las contribuciones son bienvenidas para mejorar este proyecto educativo. Por favor:

Fork el repositorio

Crea una rama (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

Áreas de Mejora Sugeridas Agregar más especies

Mejorar el modelo de red neuronal

Implementar identificación por imágenes

Crear versión web

Agregar más fichas técnicas

Mejorar la documentación

Agregar pruebas unitarias

📄 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

Texto Licencia MIT

Copyright (c) 2024 José Morillo - Universidad de Oriente

Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y los archivos de documentación asociados (el "Software"), para utilizar el Software sin restricción alguna...

📞 Contacto
Autor José Morillo

📧 Correo electrónico: bioinformatico.udo@gmail.com

🔗 Portafolio: https://bioinformatico-udo.github.io/portafilio-digital/

🎓 Universidad de Oriente, Núcleo de Nueva Esparta

Enlaces del Proyecto 📂 Repositorio: https://github.com/tu-usuario/sistema-experto-porcelanidae

🐛 Reportar errores: problemas

📚 Documentación: Wiki del Proyecto

🙏 Agradecimientos A la Universidad de Oriente, Núcleo de Nueva Esparta por el apoyo académico

A los profesores y estudiantes de la Licenciatura en Informática

A la comunidad de código abierto por las herramientas utilizadas.

A los taxónomos que contribuyeron con la base de conocimientos.

📝 Notas Finales Este proyecto es 100% educativo y está diseñado para demostrar la aplicación práctica de conceptos de Inteligencia Artificial y Sistemas Expertos en un contexto real.

Recursos adicionales para estudiantes 📖 Documentación de Python

📖 Guía del usuario de Scikit-learn

📖 Documentación de Tkinter

📖 Documentación de la almohada

🦀 ¡Feliz aprendizaje y buen código!

"El conocimiento es la base de toda inteligencia, sea natural o artificial."

⭐ Si este proyecto te ha sido útil, ¡no olvides darle una estrella en GitHub!
