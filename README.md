# 🛒 Chatbot Tienda Alemana

Sistema de chatbot inteligente para atención al cliente utilizando RAG (Retrieval-Augmented Generation) con Ollama y FastAPI.

## Requisitos Previos

- Python 3.13.3+
- [Ollama](https://ollama.ai/) instalado

## Instalación Rápida

### 1. Instalar Ollama
Descarga e instala desde [ollama.ai](https://ollama.ai/)

### 2. Configuración automática
```bash
python setup_script.py
```

Este script instala todas las dependencias y configura el sistema automáticamente.

### 3. Agregar documentos PDF
Coloca los PDFs con información de la tienda en la carpeta `pdfs/`

### 4. Revisar el .env
Renombrar el ".env.txt" que se genero con el script de startup en la carpeta del proyecto a ".env"

## Ejecutar la Aplicación

### 1. Iniciar el backend
```bash
python main_app.py
```

### 2. Abrir el frontend
Abre `Frontend/index.html` en tu navegador

## Verificar que funciona

- API: http://localhost:8000
- Estado: http://localhost:8000/health
- Documentación: http://localhost:8000/docs

## Estructura del Proyecto

```
ChatBot_TiendaAlemana/
├── Frontend/index.html     # Interfaz web
├── pdfs/                   # Coloca aquí los PDFs
├── main_app.py            # Servidor FastAPI
├── rag_system.py          # Sistema RAG
├── setup_script.py        # Configuración automática
└── .env                   # Variables de entorno
```

## Solución de Problemas

**Si no conecta:**
```bash
# Verificar que Ollama esté corriendo
ollama serve
```

**Si falta el modelo:**
```bash
ollama pull llama3.1
```

**Para actualizar documentos:**
1. Agregar nuevos PDFs a la carpeta `pdfs/`
2. Eliminar carpeta `chroma_db/`
3. Reiniciar la aplicación
