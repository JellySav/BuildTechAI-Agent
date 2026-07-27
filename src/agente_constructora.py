import os
import pandas as pd
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# 1. Cargar variables de entorno (.env)
load_dotenv()

# Ajustar rutas relativas al proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "constructora_data")

# Verificar clave API
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("ERROR: La variable GOOGLE_API_KEY no está configurada en el archivo .env")

# 2. Inicializar VectorDB para RAG (PDF)
pdf_path = os.path.join(DATA_DIR, "catalogo_y_proyectos.pdf")
if not os.path.exists(pdf_path):
    raise FileNotFoundError(
        f"No se encontró el archivo {pdf_path}. Por favor, ejecutar primero 'python src/generate_data.py'"
    )

loader = PyPDFLoader(pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Usamos ChromaDB en memoria de forma limpia
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 3. Definición de Herramientas (Tools)

@tool
def consultar_catalogo_proyectos(query: str) -> str:
    """Útil para responder preguntas sobre avances de obras, características de proyectos, opiniones de clientes y catálogo comercial."""
    results = retriever.invoke(query)
    if not results:
        return "No se encontró información relevante en el catálogo de proyectos."
    return "\n\n".join([f"Fragmento:\n{doc.page_content}" for doc in results])

@tool
def consultar_inventario_materiales(query: str) -> str:
    """Útil para consultar información sobre stock de materiales, proveedores, precios unitarios, precios al por mayor y ubicación en bodega."""
    csv_path = os.path.join(DATA_DIR, "inventario_materiales.csv")
    if not os.path.exists(csv_path):
        return "Error: No existe el archivo de inventario."
    df = pd.read_csv(csv_path)
    return f"Base de datos de inventario:\n{df.to_string(index=False)}"

@tool
def consultar_nomina_personal(query: str) -> str:
    """Útil para responder preguntas sobre el equipo de trabajo, certificaciones del personal, subcontratistas, salarios y posibilidades de ascenso."""
    csv_path = os.path.join(DATA_DIR, "nomina_y_personal.csv")
    if not os.path.exists(csv_path):
        return "Error: No existe el archivo de nómina."
    df = pd.read_csv(csv_path)
    return f"Base de datos de nómina y personal:\n{df.to_string(index=False)}"

tools = [consultar_catalogo_proyectos, consultar_inventario_materiales, consultar_nomina_personal]

# 4. Inicialización del Modelo LLM y Agente ReAct
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=5
)

# 5. Bucle de ejecución interactivo (Solo se ejecuta si corres el archivo directo desde la terminal)
if __name__ == "__main__":
    print("=" * 60)
    print("🏗️ BuildTech AI Agent — Nova Build SpA")
    print("=" * 60)

    while True:
        user_input = input("\n👤 Consulta: ").strip()
        if user_input.lower() in ["salir", "exit", "quit"]:
            break
        response = agent_executor.invoke({"input": user_input})
        print(f"\n🤖 Respuesta:\n{response['output']}")
