# Guía de Despliegue en la Nube (OCI Compute) — BuildTechAI Agent

Este documento detalla el procedimiento paso a paso para desplegar y daemonizar el agente **BuildTechAI Agent** en una instancia virtual de **Oracle Cloud Infrastructure (OCI Compute)** ejecutando **Ubuntu 22.04 LTS**.

---

## Requisitos Previos

* Una cuenta activa en [Oracle Cloud Infrastructure (OCI)](https://cloud.oracle.com/).
* Una **API Key de Google Gemini** obtenida desde [Google AI Studio](https://aistudio.google.com/).
* Cliente SSH (Terminal en Linux/Mac o PowerShell/Git Bash en Windows) y un par de claves SSH (`id_rsa` / `id_rsa.pub`).

---

## 1. Aprovisionamiento de la Instancia en OCI

Paso 1. Inicia sesión en la **Consola de OCI**.

Paso 2. Navega a **Compute** > **Instances** y selecciona **Create Instance**.

Paso 3. Configura los parámetros de la instancia:
   * **Nombre:** `buildtech-agent-vm`
   * **Imagen:** `Ubuntu 22.04 LTS` (o Canonical Ubuntu Minimal).
   * **Shape:** `VM.Standard.A1.Flex` (Ampere ARM, 1-2 OCPUs, 6 GB RAM — *Always Free Tier*).
   * **Red (VCN):** Selecciona o crea una VCN con subnet pública y asigna una **IPv4 Pública**.
   * **SSH Key:** Sube tu clave pública SSH (`id_rsa.pub`).

Paso 4. Haz clic en **Create** y copia la **Dirección IP Pública** una vez que el estado sea `RUNNING`.

---

## 2. Configuración Inicial del Servidor

Conéctate a la instancia mediante SSH:

```bash
ssh -i /ruta/a/tu/clave_privada ubuntu@<TU_IP_PUBLICA>
```

Actualiza el sistema e instala las dependencias nativas requeridas por Python, ChromaDB y WeasyPrint:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git build-essential \
    libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev
```

---

## 3. Despliegue del Código y Entorno Virtual

Paso 1. Crea el directorio de la aplicación y la estructura de archivos:
   ```bash
   mkdir -p ~/buildtech_app/constructora_data
   cd ~/buildtech_app
   ```

Paso 2. Configura el entorno virtual de Python y sus dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install langchain langchain-google-genai langchain-community chromadb pypdf pandas weasyprint python-dotenv
   ```

Paso 3. Crea el archivo de variables de entorno `.env` para gestionar la API Key de forma segura:
   ```bash
   nano .env
   ```
   Agrega tu clave secreta:
   ```env
   GOOGLE_API_KEY=tu_google_api_key_aqui
   ```

Paso 4. Carga tus archivos de datos (`catalogo_y_proyectos.pdf`, `inventario_materiales.csv`, `nomina_y_personal.csv`) dentro de `~/buildtech_app/constructora_data/` y el archivo `app.py` en la raíz del proyecto.

---

##  4. Automatización con `systemd` (Daemonización)

Para garantizar que el agente se mantenga en ejecución constante y se reinicie automáticamente ante reinicios del servidor:

Paso 1. Crea el archivo de unidad de servicio:
   ```bash
   sudo nano /etc/systemd/system/buildtech.service
   ```

Paso 2. Agrega la siguiente configuración:
   ```ini
   [Unit]
   Description=Servicio Agente IA BuildTech (Nova Build SpA)
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/buildtech_app
   ExecStart=/home/ubuntu/buildtech_app/venv/bin/python app.py
   Restart=always
   RestartSec=5
   EnvironmentFile=/home/ubuntu/buildtech_app/.env

   [Install]
   WantedBy=multi-user.target
   ```

Paso 3. Recarga `systemd`, habilita e inicia el servicio:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable buildtech.service
   sudo systemctl start buildtech.service
   ```

Paso 4. Verifica el estado y los logs de ejecución:
   ```bash
   sudo systemctl status buildtech.service
   journalctl -u buildtech.service -f
   ```

---

## 5. Buenas Prácticas de Seguridad

* **Nunca subir el archivo `.env`** al repositorio. De igual forma, el repositorio contempla en uso de `.gitignore` para no incluir archivos de `.env` y `venv/` .
* En entornos de producción con API pública (e.g. FastAPI / Flask), configura el Firewall interno de Ubuntu (`iptables` / `ufw`) y la **Security List** de OCI abriendo únicamente el puerto expuesto.
