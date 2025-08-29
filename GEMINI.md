# GEMINI Project Context

## Project Overview

This project is a web-based security analysis tool designed to scan websites, identify their JavaScript libraries, and report on potential vulnerabilities. It consists of two main parts: a command-line analysis tool (`analyzer.py`) and a Flask-based web dashboard (`dashboard.py`).

The core functionality involves:
1.  **Scanning:** Fetching a URL's content and identifying all linked JavaScript files.
2.  **Detection:** Analyzing these files to detect known libraries and their versions using a multi-layered approach (filename patterns, content signatures).
3.  **Storage:** Saving the scan results, detected libraries, and other metadata into a SQLite database (`analysis.db`).
4.  **Reporting:** Displaying the results in a comprehensive web dashboard, which includes security header analysis, library details, project management, and user authentication.

The system is designed to be modular, with separate components for library detection (`library_detector.py`), content-based signature matching (`library_signatures.py`), and CDN analysis (`cdn_analyzer.py`).

**Key Technologies:**

*   **Backend:** Python, Flask
*   **Database:** SQLite (with capabilities for PostgreSQL migration)
*   **Frontend:** HTML, CSS, JavaScript (served via Flask templates)
*   **Containerization:** Docker and Podman are supported via `docker-compose.yml` and `podman-compose.yml`.

## Building and Running

### Local Development

1.  **Create a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set the Flask secret key (for session security):**
    ```bash
    export FLASK_SECRET_KEY=$(openssl rand -hex 32)
    ```

4.  **Run the web dashboard:**
    ```bash
    python dashboard.py
    ```
    The application will be available at `http://localhost:5000`. A default 'admin' user will be created with a randomly generated password printed to the console and saved in `admin_credentials.txt`.

5.  **Run a command-line analysis:**
    -   Add URLs to `urls.txt`.
    -   Execute the analyzer:
    ```bash
    python analyzer.py
    ```

### Production (Docker)

1.  **Create a `.env` file with the secret key:**
    ```bash
    echo "FLASK_SECRET_KEY=$(openssl rand -hex 32)" > .env
    ```

2.  **Build and run the container:**
    ```bash
    docker-compose up --build -d
    ```

## Development Conventions

*   **Modularity:** The application is broken into logical Python modules. `analyzer.py` handles the core scanning logic, while `dashboard.py` contains the Flask web application.
*   **Database:** The primary database is `analysis.db` (SQLite). The schema is defined and initialized in both `analyzer.py` and `dashboard.py`, including migrations for adding new columns.
*   **Library Detection:** Detection logic is layered:
    *   `library_detector.py`: Uses RegEx patterns on filenames.
    *   `library_signatures.py`: Uses highly specific patterns (function names, variable declarations, comments) on file content for more accurate identification.
*   **Security:**
    *   User authentication is handled via Flask sessions, with passwords hashed using `werkzeug.security`.
    *   The `security_config.py` file implements rate limiting to prevent brute-force attacks.
    *   A Content Security Policy (CSP) and other security headers are analyzed and reported in the scan details.
*   **Frontend:** All frontend assets are located in the `static/` directory, and HTML files are in the `templates/` directory, following standard Flask conventions.
*   **Configuration:** The application is configured via environment variables (e.g., `FLASK_SECRET_KEY`), which are documented in the `docker-compose.yml` file.
