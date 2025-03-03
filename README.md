# LaborAI

LaborAI es una aplicación web diseñada para proporcionar respuestas rápidas y precisas a consultas sobre legislación laboral argentina. Utiliza el modelo Ollama ajustado con BERT para la generación de pares de preguntas y respuestas, basándose en datos que comprenden cuatro leyes completas de la legislación laboral argentina.

## Descripción

LaborAI utiliza tecnologías avanzadas de procesamiento del lenguaje natural (NLP) para entender y responder preguntas sobre la legislación laboral argentina. El backend de la aplicación está construido con FastAPI y Uvicorn, mientras que el frontend está desarrollado con Angular y Tailwind CSS.

## Herramientas Utilizadas

### Backend

- **FastAPI**: Framework moderno para construir APIs con Python.
- **Uvicorn**: Servidor ASGI de alto rendimiento para ejecutar aplicaciones FastAPI.
- **LangChain**: Biblioteca para la construcción de aplicaciones de lenguaje natural.
- **Ollama**: Modelo de lenguaje utilizado para procesar y generar respuestas.
- **HuggingFace Transformers**: Biblioteca para embeddings y modelos de NLP.
- **Chroma**: Base de datos de vectores para búsquedas eficientes.
- **BeautifulSoup**: Biblioteca para la extracción de datos de archivos HTML y XML.
- **AsyncHtmlLoader**: Cargador asíncrono para documentos HTML.

## Instalación y Ejecución

### Backend

1. **Crear un Entorno Virtual de Python**

    ```bash
    python3 -m venv .venv
    ```

2. **Instalar los Requisitos**

    ```bash
    .venv/bin/pip install pip --upgrade
    .venv/bin/pip install -r requirements.txt
    ```

3. **Activar el Entorno Virtual**

    ```bash
    # Windows Command Prompt
    .venv\Scripts\activate.bat

    # Windows PowerShell
    .venv\Scripts\Activate.ps1

    # macOS y Linux
    source .venv/bin/activate
    ```

4. **Instalar y Configurar Ollama**

    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ollama serve &
    ollama pull llama3-chatqa
    ```

5. **Ejecutar la Aplicación FastAPI**

    ```bash
    uvicorn api:app --reload --host 0.0.0.0 --port 8000
    ```

6. **Ejemplo de Request**

    ```bash
    curl --location 'http://0.0.0.0:8000/question' \
    --header 'Content-Type: application/json' \
    --data '{
        "question": "Cual es el concepto de trabajo?"
    }'
    ```