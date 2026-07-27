import os
import streamlit as st
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y VARIABLES DE ENTORNO
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BuildTech AI Agent — Nova Build SpA",
    page_icon="🏗️",
    layout="centered"
)

load_dotenv()

# Manejo seguro de la API Key (prioriza Streamlit Secrets en la nube, luego .env)
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

if not os.getenv("GOOGLE_API_KEY"):
    st.error("La variable `GOOGLE_API_KEY` no está configurada. Revisa los Secrets de Streamlit o tu archivo `.env`.")
    st.stop()

# -----------------------------------------------------------------------------
# 2. CARGA DEL AGENTE
# -----------------------------------------------------------------------------
# Importamos directamente desde el módulo cargado
try:
    from src.agente_constructora import agent_executor
except Exception as import_error:
    st.error(f"Error al importar la lógica del agente (`src/agente_constructora.py`): {import_error}")
    st.info("Asegúrate de que no haya errores de importación en el script principal.")
    st.stop()

@st.cache_resource(show_spinner="Cargando base de conocimiento y agente AI...")
def obtener_agente():
    return agent_executor

try:
    agente = obtener_agente()
except Exception as e:
    st.error(f"Error al inicializar el agente: {e}")
    st.info("Asegúrate de haber generado primero los datos ejecutando: `python src/generate_data.py` en tu entorno local antes de subir la carpeta `constructora_data`.")
    st.stop()

# -----------------------------------------------------------------------------
# 3. INTERFAZ GRÁFICA (DASHBOARD CHAT)
# -----------------------------------------------------------------------------
st.title("🏗️ BuildTech AI Agent")
st.caption("Asistente inteligente para gestión de proyectos, inventario y personal — Nova Build SpA")

# Inicializar el historial del chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "¡Hola! Soy el asistente virtual de Nova Build SpA. Puedo ayudarte con consultas sobre avances de obras, stock de materiales en bodega y personal de nómina. ¿En qué te puedo colaborar hoy?"
        }
    ]

# Mostrar el historial de mensajes guardados
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Capturar entrada del usuario
if prompt := st.chat_input("Escribe tu consulta sobre obras, materiales o personal..."):
    # Agregar mensaje del usuario al chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generar respuesta con el agente ReAct
    with st.chat_message("assistant"):
        with st.spinner("Consultando bases de datos y catálogo..."):
            try:
                response = agente.invoke({"input": prompt})
                respuesta_texto = response["output"]
                st.write(respuesta_texto)
                
                # Guardar respuesta en el historial
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            except Exception as e:
                error_msg = f"Ocurrió un error al procesar tu solicitud: {e}"
                st.error(error_msg)
