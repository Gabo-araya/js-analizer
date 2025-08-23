# CRUSH.md - Development Guide

## Build/Run Commands
```bash
# Setup environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Security setup (REQUIRED)
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
rm -f admin_credentials.txt

# Run main application
python dashboard.py  # Web dashboard at http://localhost:5000

# Run CLI analyzer
python analyzer.py   # Reads URLs from urls.txt

# Production deployment
podman-compose up --build -d  # See DEPLOYMENT.md
```

## Code Style Guidelines
- **Imports**: Standard library first, third-party, then local imports
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Security**: Always use parameterized SQL queries, validate all user inputs
- **Error handling**: Use try-catch blocks for external requests and DB operations
- **Templates**: Use Spanish Chilean translations, Bootstrap icons, CSRF tokens in all forms
- **Database**: Auto-migration pattern with try-catch for new columns
- **Comments**: Minimal comments unless complex security logic
- **Flask routes**: Use decorators @login_required, @admin_required for access control
- **SQL**: Use `cursor.execute("SELECT * FROM table WHERE id = ?", (id,))` pattern
- **Headers**: Apply security headers via @app.after_request decorator