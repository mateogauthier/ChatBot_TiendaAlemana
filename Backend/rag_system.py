import os
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import requests

class RAGSystem:
    def __init__(self):
        """Inicializar el sistema RAG"""
        print("Inicializando sistema RAG...")
        
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        self.ready = False
        
        try:
            self._setup_ollama()
            self._setup_embeddings()
            self._load_documents()
            self._setup_llm()
            
            # Solo crear la cadena QA si tenemos vectorstore
            if self.vectorstore:
                self._create_qa_chain()
                self.ready = True
            else:
                print("Sistema RAG inicializado sin documentos. Funcionando en modo básico.")
                self.ready = True
                
        except Exception as e:
            print(f"Error durante la inicialización: {e}")
            self.ready = False

    def is_ready(self) -> bool:
        """Verificar si el sistema está listo para usar"""
        return self.ready

    def _setup_ollama(self):
        """Verificar conexión con Ollama"""
        try:
            response = requests.get("http://localhost:11434")
            if response.status_code == 200:
                print("Ollama conectado exitosamente")
            else:
                print("Ollama no disponible, pero continuando...")
        except Exception as e:
            print(f"Error conectando con Ollama: {e}")

    def _setup_embeddings(self):
        """Configurar el modelo de embeddings"""
        print("Configurando embeddings...")
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            print("Embeddings configurados correctamente")
        except Exception as e:
            print(f"Error configurando embeddings: {e}")
            raise

    def _load_documents(self):
        """Cargar y procesar documentos PDF"""
        print("Cargando y procesando documentos...")
        
        pdfs_dir = "./pdfs"
        if not os.path.exists(pdfs_dir):
            os.makedirs(pdfs_dir)
            print("Directorio ./pdfs creado. Coloca los PDFs ahí.")

        pdf_files = [f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print("No se encontraron archivos PDF. El sistema funcionará sin conocimiento específico.")
            self.vectorstore = None
            return

        documents = []
        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(os.path.join(pdfs_dir, pdf_file))
                docs = loader.load()
                documents.extend(docs)
                print(f"Cargado: {pdf_file}")
            except Exception as e:
                print(f"Error cargando {pdf_file}: {e}")

        if not documents:
            print("No se pudieron cargar documentos.")
            self.vectorstore = None
            return

        # Dividir documentos en chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)

        # Crear vectorstore
        try:
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory="./chroma_db"
            )
            print(f"Vectorstore creado con {len(splits)} documentos")
        except Exception as e:
            print(f"Error creando vectorstore: {e}")
            self.vectorstore = None

    def _setup_llm(self):
        """Configurar el modelo de lenguaje"""
        print("Configurando modelo de lenguaje...")
        try:
            self.llm = OllamaLLM(
                model="llama3.2:1b",
                base_url="http://localhost:11434"
            )
            print("Modelo de lenguaje configurado correctamente")
        except Exception as e:
            print(f"Error configurando LLM: {e}")
            self.llm = None

    def _create_qa_chain(self):
        """Crear la cadena de pregunta-respuesta"""
        if not self.vectorstore or not self.llm:
            print("No se puede crear la cadena QA: falta vectorstore o LLM")
            return

        print("Creando cadena QA...")
        
        template = """
        Eres un asistente virtual de Tienda Alemana. Usa la siguiente información para responder las preguntas de manera amigable y útil.
        Si no tienes información específica, proporciona una respuesta general pero útil sobre la tienda.

        Contexto: {context}

        Pregunta: {question}

        Respuesta en español:
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        try:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=False
            )
            print("Cadena QA creada exitosamente")
        except Exception as e:
            print(f"Error creando cadena QA: {e}")
            self.qa_chain = None

    def query(self, question: str) -> str:
        """Procesar una consulta"""
        if not self.ready:
            return "El sistema está inicializándose. Por favor, intenta de nuevo en unos momentos."

        # Si tenemos el sistema RAG completo, usarlo
        if self.qa_chain:
            try:
                result = self.qa_chain.invoke({"query": question})
                return result.get("result", "No pude generar una respuesta.")
            except Exception as e:
                print(f"Error en consulta RAG: {e}")
                return self._get_fallback_response(question)
        
        # Respuesta de respaldo
        return self._get_fallback_response(question)

    def _get_fallback_response(self, question: str) -> str:
        """Respuestas de respaldo cuando el sistema RAG no está disponible"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["horario", "hora", "abierto", "cerrado"]):
            return "Nuestros horarios de atención son de lunes a viernes de 9:00 AM a 6:00 PM, y sábados de 9:00 AM a 2:00 PM."
        
        elif any(word in question_lower for word in ["ubicación", "dirección", "donde", "dónde"]):
            return "Nos encontramos en el centro de la ciudad. Para obtener la dirección exacta, por favor contáctanos directamente."
        
        elif any(word in question_lower for word in ["producto", "venden", "tienen", "ofrecen"]):
            return "Ofrecemos una amplia variedad de productos alemanes de alta calidad, incluyendo alimentos, bebidas y artículos especializados."
        
        elif any(word in question_lower for word in ["delivery", "entrega", "domicilio", "envío"]):
            return "Sí, ofrecemos servicio de entrega a domicilio. Consulta nuestras zonas de cobertura y horarios de entrega."
        
        elif any(word in question_lower for word in ["contacto", "teléfono", "email", "comunicar"]):
            return "Puedes contactarnos durante nuestros horarios de atención o visitarnos en nuestra tienda."
        
        else:
            return "Gracias por tu consulta. Para información más específica, te recomendamos contactarnos directamente o visitar nuestra tienda."
