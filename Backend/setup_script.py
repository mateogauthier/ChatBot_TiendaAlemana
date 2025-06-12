#!/usr/bin/env python3
"""
Script de configuración para el chatbot de Tienda Alemana
Este script verifica e instala las dependencias necesarias
"""

import subprocess
import sys
import os
import shutil

def run_command(command):
    """Ejecuta un comando y maneja errores"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Verifica la versión de Python"""
    print("Verificando versión de Python...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 o superior es requerido")
        print("Por favor, actualiza tu versión de Python")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} encontrado")
    return True

def check_ollama():
    """Verifica si Ollama está instalado y funcionando"""
    print("Verificando Ollama...")
    
    # Verificar si ollama está en el PATH
    if not shutil.which("ollama"):
        print("❌ Ollama no está instalado o no está en el PATH")
        print("Por favor, instala Ollama desde: https://ollama.ai/")
        return False
    
    # Verificar si el servicio está corriendo
    success, output = run_command("ollama list")
    if not success:
        print("❌ El servicio de Ollama no está corriendo")
        print("Ejecuta: ollama serve")
        return False
    
    print("✅ Ollama está funcionando correctamente")
    return True

def install_requirements():
    """Instala las dependencias de Python"""
    print("Instalando dependencias de Python...")
    
    requirements = [
        "fastapi",
        "uvicorn",
        "langchain",
        "langchain-community",
        "chromadb",
        "pypdf",
        "pydantic",
        "ollama",
        "python-dotenv",
        "sentence-transformers"
    ]
    
    for requirement in requirements:
        print(f"Instalando {requirement.split('==')[0]}...")
        success, output = run_command(f"pip install {requirement}")
        if not success:
            print(f"❌ Error instalando {requirement}")
            print(output)
            return False
    
    print("✅ Todas las dependencias instaladas correctamente")
    return True

def setup_directories():
    """Crea los directorios necesarios"""
    print("Creando directorios...")
    
    directories = ["pdfs", "chroma_db"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Directorio '{directory}' creado")
        else:
            print(f"✅ Directorio '{directory}' ya existe")
    
    return True

def download_ollama_model(model_name="llama3.1"):
    """Descarga el modelo de Ollama si no está disponible"""
    print(f"Verificando modelo {model_name}...")
    
    success, output = run_command("ollama list")
    if model_name in output:
        print(f"✅ Modelo {model_name} ya está disponible")
        return True
    
    print(f"Descargando modelo {model_name}... (esto puede tomar varios minutos)")
    success, output = run_command(f"ollama pull {model_name}")
    
    if success:
        print(f"✅ Modelo {model_name} descargado correctamente")
        return True
    else:
        print(f"❌ Error descargando modelo {model_name}")
        print(output)
        return False

def create_env_template():
    """Crea un archivo .env.txt de ejemplo"""
    print("Creando archivo de configuración...")
    
    env_content = """# Configuracion del Chatbot Tienda Alemana
# Copia este archivo como .env y ajusta los valores segun necesites

# Modelo de Ollama a usar
OLLAMA_MODEL=llama3.1

# Puerto para la API
API_PORT=8000

# URL Ollama
OLLAMA_PORT=http://localhost:11434

# Configuracion de logging
LOG_LEVEL=INFO

# Directorio de PDFs
PDF_DIRECTORY=./pdfs

# Configuracion de ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db
"""
    
    with open(".env.txt", "w") as f:
        f.write(env_content)
    
    print("✅ Archivo .env.txt creado")
    return True

def main():
    """Función principal de configuración"""
    print("🤖 Configurando Chatbot de Tienda Alemana")
    print("=" * 50)
    
    steps = [
        ("Verificar Python", check_python_version),
        ("Verificar Ollama", check_ollama),
        ("Instalar dependencias", install_requirements),
        ("Crear directorios", setup_directories),
        ("Descargar modelo Ollama", download_ollama_model),
        ("Crear configuración", create_env_template)
    ]
    
    for step_name, step_function in steps:
        print(f"\n{step_name}...")
        if not step_function():
            print(f"❌ Error en: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 ¡Configuración completada exitosamente!")
    print("\nPróximos pasos:")
    print("1. Coloca los PDFs en la carpeta 'pdfs/'")
    print("2. Ejecuta: python main.py")
    print("3. La API estará disponible en http://localhost:8000")
    print("4. Documentación en http://localhost:8000/docs")

if __name__ == "__main__":
    main()
