from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from rag_system import RAGSystem

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Tienda Alemana Chatbot API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar el sistema RAG
rag_system = None

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    success: bool
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Inicializar el sistema RAG al arrancar la aplicación"""
    global rag_system
    try:
        rag_system = RAGSystem()
        print("Sistema RAG inicializado correctamente")
    except Exception as e:
        print(f"Error al inicializar el sistema RAG: {e}")

@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": "Tienda Alemana Chatbot API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Verificar el estado de la API"""
    return {
        "status": "healthy",
        "rag_system_ready": rag_system is not None
    }

@app.post("/chat", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    """
    Endpoint principal para hacer consultas al chatbot
    
    Args:
        request: Objeto que contiene la pregunta del usuario
        
    Returns:
        QueryResponse: Respuesta del chatbot con la información solicitada
    """
    if not rag_system:
        raise HTTPException(
            status_code=500, 
            detail="Sistema RAG no inicializado"
        )
    
    try:
        # Procesar la consulta
        answer = rag_system.query(request.question)
        
        return QueryResponse(
            answer=answer,
            success=True
        )
        
    except Exception as e:
        return QueryResponse(
            answer="Lo siento, ocurrió un error al procesar tu consulta.",
            success=False,
            error=str(e)
        )

@app.get("/products")
async def get_products():
    """Endpoint para obtener información de productos disponibles"""
    if not rag_system:
        raise HTTPException(status_code=500, detail="Sistema RAG no inicializado")
    
    try:
        # Obtener información de productos desde la base de conocimiento
        products_info = rag_system.get_products_summary()
        return {"products": products_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {e}")

@app.get("/stores")
async def get_stores():
    """Endpoint para obtener información de sucursales"""
    if not rag_system:
        raise HTTPException(status_code=500, detail="Sistema RAG no inicializado")
    
    try:
        stores_info = rag_system.get_stores_summary()
        return {"stores": stores_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sucursales: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
