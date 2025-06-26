# 🛒 Chatbot Tienda Alemana

Un chatbot inteligente para atención al cliente de Tienda Alemana, construido con FastAPI, React y tecnologías de IA.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Ejecución](#-ejecución)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Troubleshooting](#-troubleshooting)

## ✨ Características

- **Chatbot Inteligente**: Responde preguntas sobre productos, horarios, ubicaciones y servicios
- **RAG System**: Sistema de Recuperación Aumentada de Generación para consultas precisas
- **Frontend Moderno**: Interfaz React con diseño responsive
- **API RESTful**: Backend FastAPI con documentación automática
- **Integración con Ollama**: Modelos de lenguaje local para privacidad
- **Base de Conocimiento**: Procesamiento de documentos PDF para información específica

## 🏗️ Arquitectura

```
ChatBot_TiendaAlemana/
├── Backend/
│   ├── main_app.py          # API FastAPI
│   ├── rag_system.py        # Sistema RAG con LangChain
│   ├── setup_script.py      # Script de configuración automática
│   └── requirements.txt     # Dependencias Python
├── Frontend/
│   └── chatbot-react/      # Aplicación React
│       ├── src/
│       │   ├── index.html
│       │   ├── App.jsx
│       │   ├── components/
│       │   └── styles/
│       └── package.json
└── README.md
```

## 📋 Requisitos Previos

### Software Necesario

1. **Python 3.11+** (recomendado para compatibilidad)
   - [Descargar Python](https://www.python.org/downloads/)

2. **Node.js 18+** y npm
   - [Descargar Node.js](https://nodejs.org/)

3. **Ollama** (para modelos de IA local)
   - [Descargar Ollama](https://ollama.ai/)

### Verificar Instalaciones

```bash
# Verificar Python
python --version
# Debería mostrar: Python 3.11.x

# Verificar Node.js
node --version
npm --version

# Verificar Ollama
ollama --version
```

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/usuario/ChatBot_TiendaAlemana.git
cd ChatBot_TiendaAlemana
```

### 2. Configuración del Backend

#### Opción A: Configuración Automática (Recomendada)

```bash
cd Backend
python setup_script.py
```

Este script automáticamente:
- ✅ Verifica versión de Python
- ✅ Instala dependencias
- ✅ Configura Ollama y descarga modelos
- ✅ Crea directorios necesarios
- ✅ Genera archivo de configuración

#### Opción B: Configuración Manual

```bash
cd Backend

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
mkdir pdfs
mkdir chroma_db
```

### 3. Configuración del Frontend

#### Frontend React

```bash
cd Frontend/chatbot-react

# Instalar dependencias
npm install

```

## ⚙️ Configuración

### 1. Configurar Ollama

```bash
# Descargar modelo recomendado
ollama pull llama3.2:1b

# Verificar que funciona
ollama list
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la carpeta Backend:

```env
# Configuración del Chatbot Tienda Alemana

# Modelo de Ollama
OLLAMA_MODEL=llama3.2:1b

# URLs y Puertos
API_PORT=8000
OLLAMA_PORT=http://localhost:11434

# Directorios
PDF_DIRECTORY=./pdfs
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Logging
LOG_LEVEL=INFO
```

### 3. Agregar Documentos (Opcional)

Para mejorar las respuestas del chatbot, coloca archivos PDF con información de la tienda en:

```
Backend/pdfs/
├── catalogo_productos.pdf
├── horarios_sucursales.pdf
└── politicas_tienda.pdf
```

## 🚀 Ejecución

### 1. Ejecutar Backend

```bash
cd Backend

# Ejecutar servidor FastAPI
python main_app.py
```

### 2. Ejecutar Frontend

#### React App

```bash
cd Frontend/chatbot-react

# Ejecutar servidor de desarrollo
npm run dev
```

**Disponible en:** http://localhost:3000


## 💡 Uso

### 1. Verificar Conexión

- Abre el frontend en tu navegador
- Verifica que el indicador de conexión muestre "CONECTADO"
- Si aparece "DESCONECTADO", verifica que el backend esté ejecutándose

### 2. Interactuar con el Chatbot

#### Preguntas Frecuentes (Botones rápidos):
- "¿Cuáles son los horarios de atención?"
- "¿Dónde están ubicados?"
- "¿Qué productos venden?"
- "¿Hacen entregas a domicilio?"

#### Escribir Preguntas Personalizadas:
- "¿Tienen cerveza alemana?"
- "¿Cuánto cuesta el pan?"
- "¿Cómo puedo contactarlos?"

### 3. Funcionalidades

- ✅ **Respuestas en tiempo real**
- ✅ **Indicador de escritura**
- ✅ **Historial de conversación**
- ✅ **Preguntas frecuentes**
- ✅ **Diseño responsive**

## 🔗 API Endpoints

### Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información de la API |
| `/health` | GET | Estado del sistema |
| `/chat` | POST | Enviar mensaje al chatbot |
| `/products` | GET | Información de productos |
| `/stores` | GET | Información de sucursales |

### Ejemplo de Uso

```javascript
// Enviar mensaje al chatbot
const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: "¿Qué horarios tienen?" })
});

const data = await response.json();
console.log(data.answer);
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Error de Dependencias Python

```bash
# Usar Python 3.11 si hay problemas con 3.13
# Instalar versiones específicas
pip install --only-binary=all numpy pandas
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

#### 2. Ollama No Disponible

```bash
# Verificar que Ollama esté ejecutándose
ollama serve

# En otra terminal, verificar modelos
ollama list

# Descargar modelo si no existe
ollama pull llama3.2:1b
```

#### 3. Error de CORS

Verifica que el backend tenga configurado CORS para el origen del frontend:

```python
# En main_app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Agregar tu URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 4. Frontend No Conecta

- ✅ Verifica que el backend esté en http://localhost:8000
- ✅ Revisa la consola del navegador para errores
- ✅ Confirma que no hay firewall bloqueando

### Logs y Debugging

#### Backend:
```bash
# Ver logs detallados
python main_app.py

# Los logs mostrarán:
# - Estado de conexión Ollama
# - Carga de documentos
# - Errores de inicialización
```

#### Frontend:
- Abre las herramientas de desarrollador (F12)
- Revisa la pestaña Console para errores
- Network para ver las peticiones HTTP

**¡Tu chatbot de Tienda Alemana está listo! 🎉**
