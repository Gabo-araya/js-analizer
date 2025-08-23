# Project Overview

This project is a web-based security analysis tool for JavaScript and CSS libraries. It's a Python Flask application that scans websites, identifies outdated or vulnerable libraries, and provides a dashboard for managing the results. The application uses a SQLite database to store scan results and features role-based authentication for managing users and clients.

**Key Technologies:**

*   **Backend:** Python, Flask
*   **Frontend:** HTML, CSS, JavaScript
*   **Database:** SQLite
*   **Containerization:** Docker, Podman

**Core Functionality:**

*   **Web Interface:** A user-friendly dashboard for initiating scans, viewing results, and managing the application.
*   **Library Analysis:** Scans websites to detect JavaScript and CSS libraries, comparing them against a global catalog of known libraries and their secure versions.
*   **Vulnerability Detection:** Identifies potential vulnerabilities by comparing detected library versions with known secure versions.
*   **Reporting:** Generates reports in PDF, CSV, and Excel formats.
*   **User and Client Management:** Supports multiple users with different roles (Admin, Analyst) and allows for managing clients and their associated scans.
*   **API:** Provides a REST API for programmatic access to scan data and statistics.

# Building and Running

## Local Development

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set the Flask secret key:**
    ```bash
    export FLASK_SECRET_KEY=$(openssl rand -hex 32)
    ```

4.  **Run the application:**
    ```bash
    python dashboard.py
    ```

The application will be available at `http://localhost:5000`.

## Production (Docker/Podman)

1.  **Set the Flask secret key in a `.env` file:**
    ```bash
    export FLASK_SECRET_KEY=$(openssl rand -hex 32)
    echo "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" > .env
    echo "FLASK_ENV=production" >> .env
    ```

2.  **Build and run the container:**
    ```bash
    docker-compose up --build -d
    ```
    or with Podman:
    ```bash
    podman-compose up --build -d
    ```

# Development Conventions

*   **Database:** The application uses a SQLite database (`analysis.db`) which is created automatically.
*   **Styling:** The project uses a `main.css` file for styling the web interface.
*   **Frontend Logic:** JavaScript for the frontend is located in `static/js/`.
*   **Templates:** The HTML templates are in the `templates` directory.
*   **Core Logic:** The main application logic is split between `analyzer.py` (for the command-line analysis) and `dashboard.py` (for the Flask web application).

---

## Preguntas Frecuentes (FAQ)

### ¿Cómo funciona la relación entre las bibliotecas de un escaneo y las bibliotecas globales?

**Respuesta corta: Mediante una asociación opcional.**

-   **Asociación:** Al añadir o editar una biblioteca manual en un escaneo, puedes **asociarla opcionalmente** a una biblioteca del Catálogo Global.
-   **Vista de Detalle del Escaneo:**
    -   Si una biblioteca está asociada, la tabla mostrará las versiones ("Segura" y "Última") de la biblioteca global junto a las versiones detectadas en el escaneo.
    -   Aparecerá un icono de enlace <i class="bi bi-link-45deg"></i> junto al nombre de la biblioteca para indicar que está asociada.
    -   Se mostrará un checkmark verde (✅) si la versión segura o la última versión de la biblioteca del escaneo coincide con la versión correspondiente de la biblioteca global.
-   **Independencia de los datos:** Aunque estén asociadas, los datos de la biblioteca del escaneo (versión, versión segura, etc.) siguen siendo independientes. Cambiar la biblioteca global **no** alterará los datos ya guardados en escaneos anteriores. La asociación simplemente permite visualizar y comparar los datos globales en la vista de detalle.

### Si cambio la versión en una biblioteca global, ¿cambia en las bibliotecas de un escaneo existente?

**Respuesta corta: No.**

Los datos de las bibliotecas dentro de un escaneo (tanto las detectadas automáticamente como las manuales) son **independientes** del catálogo global una vez que se han guardado.

Si actualizas la "última versión" o la "última versión segura" en el catálogo global, estos cambios **no se propagarán** a las bibliotecas que ya existen en los resultados de escaneos anteriores. Sin embargo, gracias a la nueva funcionalidad de asociación, podrás ver la nueva información global directamente en la tabla de detalles del escaneo para una comparación más fácil.
