"""
Script de instalación para el Sistema Experto de Porcelanidae
"""
from setuptools import setup, find_packages
import os
import sys

# Verificar versión de Python
if sys.version_info < (3, 8):
    sys.exit("Se requiere Python 3.8 o superior")

# Leer la descripción del README (si existe)
long_description = "Sistema experto híbrido para identificación de especies de Porcelanidae"
try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except FileNotFoundError:
    print("⚠️  README.md no encontrado, usando descripción por defecto")

# Leer requirements
try:
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    print("⚠️  requirements.txt no encontrado, usando dependencias mínimas")
    requirements = [
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
    ]

setup(
    name="sistema_experto_porcelanidae",
    version="1.0.0",
    author="Equipo de Desarrollo - Sistema Experto",
    author_email="desarrollo@porcelanidae-expert.com",
    description="Sistema experto híbrido para identificación de especies de Porcelanidae",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/sistema-experto-porcelanidae",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        'data': ['*.json', '*.csv'],
        'models': ['*.pkl'],
    },
    entry_points={
        'console_scripts': [
            'porcelanidae-expert=main:main',
        ],
    },
    keywords="taxonomia crustaceos porcelanidae sistema-experto ia",
    project_urls={
        "Documentación": "https://github.com/tu-usuario/sistema-experto-porcelanidae/docs",
        "Código Fuente": "https://github.com/tu-usuario/sistema-experto-porcelanidae",
        "Reportar Errores": "https://github.com/tu-usuario/sistema-experto-porcelanidae/issues",
    },
)