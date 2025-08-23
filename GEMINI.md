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
