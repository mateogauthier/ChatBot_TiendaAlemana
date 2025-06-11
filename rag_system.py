import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from typing import List, Dict
import ollama
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener el directorio de PDFs desde las variables de entorno
PDF_DIRECTORY = os.getenv('PDF_DIRECTORY')
# Obtener el nombre del modelo de Ollama desde las variables de entorno
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL')
# Definir el directorio de persistencia para Chroma
CHROMA_PERSIST_DIRECTORY = os.getenv('CHROMA_PERSIST_DIRECTORY')

class RAGSystem:
    def __init__(self, pdf_directory: str = PDF_DIRECTORY, model_name: str = OLLAMA_MODEL):
        """
        Inicializa el sistema RAG
        
        Args:
            pdf_directory: Directorio donde están los PDFs
            model_name: Nombre del modelo de Ollama a usar
        """
        self.pdf_directory = pdf_directory
        self.model_name = model_name
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        
        # Verificar que Ollama esté funcionando
        self._check_ollama()
        
        # Inicializar componentes
        self._setup_embeddings()
        self._load_and_process_documents()
        self._setup_llm()
        self._create_qa_chain()
    
    def _check_ollama(self):
        """Verifica que Ollama esté ejecutándose y el modelo esté disponible"""
        try:
            # Verificar conexión con Ollama
            models = ollama.list()
            print("Ollama conectado exitosamente")
            
            # Verificar si el modelo está disponible
            model_names = [model['name'] for model in models['models']]
            if not any(self.model_name in name for name in model_names):
                print(f"Descargando modelo {self.model_name}...")
                ollama.pull(self.model_name)
                print(f"Modelo {self.model_name} descargado exitosamente")
                
        except Exception as e:
            raise Exception(f"Error conectando con Ollama: {e}")
    
    def _setup_embeddings(self):
        """Configura el modelo de embeddings"""
        print("Configurando embeddings...")
        # Usar HuggingFace embeddings (funciona sin API key)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        print("Embeddings configurados correctamente")
    
    def _load_and_process_documents(self):
        """Carga y procesa los documentos PDF"""
        print("Cargando y procesando documentos...")
        
        # Verificar que el directorio existe
        if not os.path.exists(self.pdf_directory):
            os.makedirs(self.pdf_directory)
            print(f"Directorio {self.pdf_directory} creado. Coloca los PDFs ahí.")
            return
        
        documents = []
        pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.pdf')]
        
        if not pdf_files:
            print("No se encontraron archivos PDF. Creando datos de ejemplo...")
            return
        
        # Cargar documentos PDF
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.pdf_directory, pdf_file)
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            documents.extend(docs)
            print(f"Cargado: {pdf_file}")
        
        # Dividir documentos en chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        splits = text_splitter.split_documents(documents)
        print(f"Documentos divididos en {len(splits)} chunks")
        
        # Crear vectorstore
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIRECTORY
        )
        
        print("Vectorstore creado exitosamente")
    
    def _setup_llm(self):
        """Configura el modelo de lenguaje Ollama"""
        print("Configurando modelo de lenguaje...")
        self.llm = Ollama(
            model=self.model_name,
            temperature=0.1,  # Respuestas más determinísticas
            num_ctx=4096     # Contexto más amplio
        )
        print("Modelo de lenguaje configurado correctamente")
    
    def _create_qa_chain(self):
        """Crea la cadena de pregunta-respuesta"""
        print("Creando cadena QA...")
        
        # Template personalizado para el contexto de Tienda Alemana
        template = """
        Eres un asistente virtual de Tienda Alemana, una cadena de supermercados en Uruguay.
        Tu trabajo es ayudar a los clientes con información sobre productos, precios, stock, 
        ubicaciones dentro de la tienda, y datos de las sucursales.
        
        Contexto de la consulta:
        {context}
        
        Pregunta del cliente: {question}
        
        Instrucciones:
        - Responde de manera amigable y profesional
        - Si la información está disponible en el contexto, úsala para responder
        - Si no tienes la información exacta, indícalo claramente
        - Incluye precios en pesos uruguayos ($) cuando sea relevante
        - Menciona ubicaciones específicas (góndolas/secciones) cuando sea apropiado
        - Para horarios, especifica días y horarios exactos
        
        Respuesta:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Traer los 3 documentos más relevantes
            ),
            chain_type_kwargs={"prompt": prompt}
        )
        
        print("Cadena QA creada exitosamente")
    
    def query(self, question: str) -> str:
        """
        Procesa una consulta del usuario
        
        Args:
            question: Pregunta del usuario
            
        Returns:
            str: Respuesta del chatbot
        """
        try:
            response = self.qa_chain.run(question)
            return response
        except Exception as e:
            return f"Lo siento, ocurrió un error al procesar tu consulta: {str(e)}"
    
    def get_products_summary(self) -> Dict:
        """Obtiene resumen de productos"""
        try:
            response = self.query("Lista todos los productos disponibles con sus precios")
            return {"summary": response}
        except Exception as e:
            return {"error": str(e)}
    
    def get_stores_summary(self) -> Dict:
        """Obtiene resumen de sucursales"""
        try:
            response = self.query("Lista todas las sucursales con sus direcciones y horarios")
            return {"summary": response}
        except Exception as e:
            return {"error": str(e)}
