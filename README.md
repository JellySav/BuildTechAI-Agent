# BuildTechAI-Agent — Agente Inteligente para Gestión Constructora
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestration-121011?style=flat&logo=chainlink)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-8E75B2?style=flat&logo=google)](https://ai.google.dev/)
[![Oracle Cloud](https://img.shields.io/badge/OCI-Compute%20Deployed-F80000?style=flat&logo=oracle)](https://www.oracle.com/cloud/)

> **Proyecto desarrollado para el Challenge Alura Latam / Oracle Cloud Infrastructure (OCI)**  
> Agente multi-herramienta con IA capaz de resolver consultas operativas en lenguaje natural sobre **Captación de Clientes y Proyectos**, **Gestión de Inventario** y **Nómina de Personal/Subcontratistas** para la empresa *Constructora Nova Build SpA*.

## Contexto del Problema

En las empresas de la construcción, la información crítica suele encontrarse dispersa entre catálogos de obras en PDF, hojas de cálculo de insumos de bodega y listas de asistencia o contratos de personal. Esta fragmentación genera pérdida de tiempo operativo y demoras en las respuestas a clientes y directores de obra.

**BuildTech AI Agent** unifica el acceso a estos silos documental mediante un sistema **RAG (Retrieval-Augmented Generation)** y análisis tabular interactivo.


## Arquitectura del Sistema

El agente utiliza un orquestador basado en la lógica **ReAct (Reasoning + Acting)** que enruta las preguntas del usuario hacia la herramienta especializada según el tipo de consulta:



## Stack Tecnológico

* **Lenguaje principal:** Python 3.10+
* **Orquestación de IA:** LangChain / LangGraph
* **Modelo de Lenguaje (LLM):** Google Gemini 1.5 Flash
* **Vector Database:** ChromaDB (`text-embedding-004`)
* **Procesamiento de Datos:** Pandas, PyPDF, WeasyPrint
* **Infraestructura Cloud:** Oracle Cloud Infrastructure (OCI) — Instancia OCI Compute (Ubuntu Server)

---

## Estructura del Repositorio

```text
.
├── constructora_data/
│   ├── catalogo_y_proyectos.pdf   # Documento no estructurado (Catálogo y Obras)
│   ├── inventario_materiales.csv  # Base estructurada de insumos y proveedores
│   └── nomina_y_personal.csv      # Base estructurada de personal y subcontratistas
├── src/
│   ├── agente_constructora.py     # Script principal del agente multi-herramienta
│   └── generate_data.py           # Generador del dataset inicial
├── .env.example                   # Plantilla de variables de entorno
├── requirements.txt               # Lista de dependencias del proyecto
└── README.md                      # Documentación del proyecto
```

##  Ejemplos de Consultas Resueltas por el Agente
1. Captación y Comercial (PDF - RAG)
Pregunta: "¿Qué porcentaje de avance tiene la Torre Miramar y qué opinan sus clientes?"

Respuesta del Agente: La Torre Miramar en Valparaíso presenta un 65% de avance en su ejecución. Inmobiliaria del Mar destacó la precisión en los plazos y la alta resistencia de la estructura ante marejadas e inviernos.

2. Gestión de Inventarios (CSV - Pandas)
Pregunta: "¿Cuál es la distribuidora que nos vende Cemento Melón y qué precio ofrece al por mayor?"

Respuesta del Agente: El proveedor principal es Distribuidora El Teniente. El precio unitario es de $4.800 CLP, pero ofrece un precio al por mayor de $4.200 CLP a partir de 100 sacos.

3. Nómina y Talento (CSV - RRHH)
Pregunta: "¿Qué trabajadora o subcontratista cuenta con certificación LEED y tiene posibilidad de ascenso?"

Respuesta del Agente: María Paz Salamanca, Ingeniera Civil Estructural, cuenta con la certificación LEED Green Associate y está catalogada como candidata a Jefa de Proyecto.



## Instalación y Ejecución Local
1. Clonar el repositorio
```Bash
git clone [https://github.com/tu-usuario/buildtech-ai-agent.git](https://github.com/tu-usuario/buildtech-ai-agent.git)
cd buildtech-ai-agent
```

2. Crear un entorno virtual e instalar dependencias
```Bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar variables de entorno
Crea un archivo .env basado en .env.example:
```bash
Fragmento de código
GOOGLE_API_KEY="TU_GEMINI_API_KEY"
```

4. Ejecutar el agente
```Bash
python src/agente_constructora.py
```

## Deploy en Oracle Cloud Infrastructure (OCI)
El agente está diseñado para ejecutarse tanto en entornos locales/Colab como desplegado en una instancia **OCI Compute (Ampere ARM / Ubuntu 22.04)** de Oracle Cloud Infrastructure.

Para ver las instrucciones detalladas de aprovisionamiento de servidor, configuración de entorno, variables y daemonización con `systemd`, consulta la [Guía de Despliegue en OCI (DEPLOYMENT.md)](./DEPLOYMENT.md).

```
Entorno Cloud: Oracle Linux / Ubuntu Server en OCI.

Estado de la Instancia: Active / Running

Ip Pública / Endpoint de prueba: http://<IP_PUBLICA_OCI>:8000 (O adjunta captura de pantalla en la carpeta /img)
```

## Autor / Créditos
Desarrollado como parte del Challenge Alura Latam & Oracle Next Education (ONE).

Desarrollado por: Yael (Eavny)

Contacto / LinkedIn: [![Mi LinkedIn]([https://img.shields.io/badge/OCI-Compute%20Deployed-F80000?style=flat&logo=oracle](https://www.linkedin.com/in/yael-astorga-computer-science-student/))]
