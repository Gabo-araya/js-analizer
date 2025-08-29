# Contexto del Proyecto (GEMINI)

## Descripción General del Proyecto

Este proyecto es una herramienta de análisis de seguridad basada en la web, diseñada para escanear sitios web, identificar sus bibliotecas de JavaScript e informar sobre posibles vulnerabilidades. Se compone de dos partes principales: una herramienta de análisis por línea de comandos (`analyzer.py`) y un panel de control web basado en Flask (`dashboard.py`).

La funcionalidad principal incluye:
1.  **Escaneo:** Obtener el contenido de una URL e identificar todos los archivos JavaScript enlazados.
2.  **Detección:** Analizar estos archivos para detectar bibliotecas conocidas y sus versiones utilizando un enfoque de múltiples capas (patrones de nombres de archivo, firmas de contenido).
3.  **Almacenamiento:** Guardar los resultados del escaneo, las bibliotecas detectadas y otros metadatos en una base de datos SQLite (`analysis.db`).
4.  **Informes:** Mostrar los resultados en un panel de control web completo, que incluye análisis de cabeceras de seguridad, detalles de bibliotecas, gestión de proyectos y autenticación de usuarios.

El sistema está diseñado para ser modular, con componentes separados para la detección de bibliotecas (`library_detector.py`), la coincidencia de firmas basadas en contenido (`library_signatures.py`) y el análisis de CDN (`cdn_analyzer.py`).

**Tecnologías Clave:**

*   **Backend:** Python, Flask
*   **Base de datos:** SQLite (con capacidad para migrar a PostgreSQL)
*   **Frontend:** HTML, CSS, JavaScript (servidos a través de plantillas de Flask)
*   **Contenerización:** Soporte para Docker y Podman a través de `docker-compose.yml` y `podman-compose.yml`.

## Compilación y Ejecución

### Desarrollo Local

1.  **Crear un entorno virtual de Python:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Establecer la clave secreta de Flask (para la seguridad de la sesión):**
    ```bash
    export FLASK_SECRET_KEY=$(openssl rand -hex 32)
    ```

4.  **Ejecutar el panel de control web:**
    ```bash
    python dashboard.py
    ```
    La aplicación estará disponible en `http://localhost:5000`. Se creará un usuario 'admin' por defecto con una contraseña generada aleatoriamente, que se mostrará en la consola y se guardará en `admin_credentials.txt`.

5.  **Ejecutar un análisis por línea de comandos:**
    -   Añadir URLs al archivo `urls.txt`.
    -   Ejecutar el analizador:
    ```bash
    python analyzer.py
    ```

### Producción (Docker)

1.  **Crear un archivo `.env` con la clave secreta:**
    ```bash
    echo "FLASK_SECRET_KEY=$(openssl rand -hex 32)" > .env
    ```

2.  **Construir y ejecutar el contenedor:**
    ```bash
    docker-compose up --build -d
    ```

## Convenciones de Desarrollo

*   **Modularidad:** La aplicación se divide en módulos lógicos de Python. `analyzer.py` maneja la lógica central de escaneo, mientras que `dashboard.py` contiene la aplicación web de Flask.
*   **Base de datos:** La base de datos principal es `analysis.db` (SQLite). El esquema se define e inicializa tanto en `analyzer.py` como en `dashboard.py`, incluyendo migraciones para añadir nuevas columnas.
*   **Detección de Bibliotecas:** La lógica de detección se organiza en capas:
    *   `library_detector.py`: Usa patrones de RegEx en los nombres de archivo.
    *   `library_signatures.py`: Usa patrones muy específicos (nombres de funciones, declaraciones de variables, comentarios) en el contenido del archivo para una identificación más precisa.
*   **Seguridad:**
    *   La autenticación de usuarios se maneja a través de sesiones de Flask, con contraseñas hasheadas usando `werkzeug.security`.
    *   El archivo `security_config.py` implementa limitación de peticiones (rate limiting) para prevenir ataques de fuerza bruta.
    *   Se analiza y reporta una Política de Seguridad de Contenido (CSP) y otras cabeceras de seguridad en los detalles del escaneo.
*   **Frontend:** Todos los recursos del frontend se encuentran en el directorio `static/`, y los archivos HTML están en el directorio `templates/`, siguiendo las convenciones estándar de Flask.
*   **Configuración:** La aplicación se configura mediante variables de entorno (ej. `FLASK_SECRET_KEY`), que están documentadas en el archivo `docker-compose.yml`.
