#!/usr/bin/env python3
"""
Script de configuración mejorado para el chatbot de Tienda Alemana
Este script verifica compatibilidad y instala dependencias con versiones fijas
"""

import subprocess
import sys
import os
import shutil
import platform
from pathlib import Path

def run_command(command, capture_output=True):
    """Ejecuta un comando y maneja errores"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=capture_output, 
            text=True
        )
        return True, result.stdout if capture_output else ""
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if capture_output and e.stderr else str(e)
        return False, error_msg

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro} encontrado")
    
    if version.major != 3:
        print("❌ Se requiere Python 3.x")
        return False
    
    if version.minor < 8:
        print("❌ Se requiere Python 3.8 o superior")
        print("   Versión actual:", f"{version.major}.{version.minor}")
        return False
    
    if version.minor > 11:
        print("⚠️  Python 3.12+ puede tener problemas de compatibilidad")
        print("   Se recomienda Python 3.8-3.11")
    
    print("✅ Versión de Python compatible")
    return True

def check_pip():
    """Verifica que pip esté disponible y actualizado"""
    print("📦 Verificando pip...")
    
    success, _ = run_command("pip --version")
    if not success:
        print("❌ pip no está disponible")
        return False
    
    print("✅ pip disponible")
    
    # Actualizar pip
    print("   Actualizando pip...")
    success, output = run_command("python -m pip install --upgrade pip")
    if success:
        print("✅ pip actualizado")
    else:
        print("⚠️  No se pudo actualizar pip, continuando...")
    
    return True

def check_system_requirements():
    """Verifica requisitos del sistema"""
    print("💻 Verificando sistema operativo...")
    
    system = platform.system()
    print(f"   Sistema: {system} {platform.release()}")
    
    if system == "Windows":
        print("   Nota: En Windows, asegúrate de tener Visual C++ Build Tools")
    elif system == "Darwin":  # macOS
        print("   Nota: En macOS, asegúrate de tener Xcode Command Line Tools")
    
    print("✅ Sistema compatible")
    return True

def install_requirements():
    """Instala las dependencias desde requirements.txt"""
    print("📚 Instalando dependencias...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ Archivo requirements.txt no encontrado")
        return False
    
    print("   Esto puede tomar varios minutos...")
    success, output = run_command(
        "pip install -r requirements.txt", 
        capture_output=False
    )
    
    if success:
        print("✅ Dependencias instaladas correctamente")
        return True
    else:
        print("❌ Error instalando dependencias")
        print("   Intenta ejecutar manualmente: pip install -r requirements.txt")
        return False

def check_ollama():
    """Verifica si Ollama está instalado y funcionando"""
    print("🦙 Verificando Ollama...")
    
    # Verificar si ollama está en el PATH
    if not shutil.which("ollama"):
        print("❌ Ollama no está instalado")
        print("   Descarga e instala desde: https://ollama.ai/")
        print("   Instrucciones de instalación:")
        
        system = platform.system()
        if system == "Windows":
            print("   - Descarga el instalador .exe desde ollama.ai")
            print("   - Ejecuta el instalador y sigue las instrucciones")
        elif system == "Darwin":  # macOS
            print("   - brew install ollama")
            print("   - O descarga desde ollama.ai")
        else:  # Linux
            print("   - curl -fsSL https://ollama.ai/install.sh | sh")
        
        return False
    
    # Verificar si el servicio está corriendo
    success, output = run_command("ollama list")
    if not success:
        print("❌ El servicio de Ollama no está corriendo")
        print("   Ejecuta en otra terminal: ollama serve")
        return False
    
    print("✅ Ollama está funcionando correctamente")
    return True

def setup_directories():
    """Crea los directorios necesarios"""
    print("📁 Creando directorios...")
    
    directories = [
        "pdfs",
        "chroma_db", 
        "logs"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Directorio '{directory}' creado")
        else:
            print(f"✅ Directorio '{directory}' ya existe")
    
    return True

def download_ollama_model(model_name="llama3.1:8b"):
    """Descarga el modelo de Ollama si no está disponible"""
    print(f"🤖 Verificando modelo {model_name}...")
    
    success, output = run_command("ollama list")
    if not success:
        print("❌ No se puede verificar modelos de Ollama")
        return False
    
    if model_name in output:
        print(f"✅ Modelo {model_name} ya está disponible")
        return True
    
    print(f"📥 Descargando modelo {model_name}...")
    print("   Esto puede tomar varios minutos dependiendo de tu conexión...")
    
    success, output = run_command(f"ollama pull {model_name}", capture_output=False)
    
    if success:
        print(f"✅ Modelo {model_name} descargado correctamente")
        return True
    else:
        print(f"❌ Error descargando modelo {model_name}")
        print("   Modelos alternativos más pequeños:")
        print("   - llama3.1:7b (más rápido)")
        print("   - mistral:7b (alternativa)")
        return False

def create_env_file():
    """Crea el archivo .env desde .env.example"""
    print("⚙️  Configurando archivo de entorno...")
    
    if os.path.exists(".env"):
        print("✅ Archivo .env ya existe")
        return True
    
    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print("✅ Archivo .env creado desde .env.example")
        print("   Revisa y ajusta las configuraciones en .env si es necesario")
    else:
        print("⚠️  Archivo .env.example no encontrado")
        print("   Crea manualmente un archivo .env con las configuraciones necesarias")
    
    return True

def test_installation():
    """Prueba básica de la instalación"""
    print("🧪 Probando instalación...")
    
    try:
        import fastapi
        import langchain
        import chromadb
        import ollama
        print("✅ Importaciones básicas exitosas")
        return True
    except ImportError as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def main():
    """Función principal de configuración"""
    print("🤖 Configurando Chatbot de Tienda Alemana")
    print("=" * 60)
    print("Este script instalará todas las dependencias necesarias")
    print("con versiones fijas para garantizar compatibilidad.")
    print("=" * 60)
    
    steps = [
        ("Verificar Python", check_python_version),
        ("Verificar pip", check_pip),
        ("Verificar sistema", check_system_requirements),
        ("Instalar dependencias", install_requirements),
        ("Verificar Ollama", check_ollama),
        ("Crear directorios", setup_directories),
        ("Descargar modelo Ollama", download_ollama_model),
        ("Configurar entorno", create_env_file),
        ("Probar instalación", test_installation)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        if not step_function():
            print(f"❌ Error en: {step_name}")
            failed_steps.append(step_name)
            
            # Solo detener en errores críticos
            if step_name in ["Verificar Python", "Instalar dependencias"]:
                print("\n💥 Error crítico, deteniendo instalación")
                sys.exit(1)
    
    print("\n" + "=" * 60)
    
    if failed_steps:
        print("⚠️  Instalación completada con advertencias:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nRevisa los errores anteriores antes de continuar.")
    else:
        print("🎉 ¡Instalación completada exitosamente!")
    
    print("\n📖 Próximos pasos:")
    print("1. Coloca los PDFs de Tienda Alemana en la carpeta 'pdfs/'")
    print("2. Ajusta la configuración en '.env' si es necesario")
    print("3. Ejecuta: python main_app.py")
    print("4. La API estará disponible en http://localhost:8000")
    print("5. Documentación en http://localhost:8000/docs")
    print("\n📋 Para verificar que todo funciona:")
    print("   curl http://localhost:8000/health")

if __name__ == "__main__":
    main()