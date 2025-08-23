# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **security-focused Python Flask web application** that analyzes websites to detect JavaScript and CSS library versions, assess security vulnerabilities, and provide comprehensive reporting through a professional dashboard. The system includes:

1. **Web Scraper/Analyzer** (`analyzer.py`) - Command-line tool for automated URL analysis with SSRF protection
2. **Flask Dashboard** (`dashboard.py`) - Secure web interface with role-based authentication, client management, CSRF protection, and advanced reporting
3. **Security Layer** (`security_config.py`) - Comprehensive security configurations and validations
4. **User Management System** - Role-based access control with Administrator and Analyst roles
5. **Client Management System** - Enterprise client organization and tracking capabilities

## Security Architecture (AUDITED - January 2025)

### 🛡️ Security Features Implemented
- ✅ **Authentication**: Werkzeug password hashing, secure session management
- ✅ **Role-Based Access Control**: Administrator and Analyst roles with differentiated permissions
- ✅ **CSRF Protection**: Flask-WTF with tokens on all forms
- ✅ **SQL Injection Prevention**: Parameterized queries exclusively
- ✅ **SSRF Protection**: URL validation, private IP blocking, port filtering
- ✅ **Security Headers**: Comprehensive HTTP security headers via `@app.after_request`
- ✅ **Input Validation**: Sanitization and validation on all user inputs
- ✅ **Secure Configuration**: Environment-based secrets, production detection
- ✅ **Password Management**: User self-service password change functionality

## Core Commands

### Development and Running
```bash
# ⚠️ SECURITY FIRST: Configure secure environment
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
export FLASK_ENV=production  # For production deployment
rm -f admin_credentials.txt  # Remove if exists

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run web dashboard (primary interface)
python dashboard.py
# Runs on http://localhost:5000

# Run command-line analysis
python analyzer.py
# Reads URLs from urls.txt and analyzes them
```

### Production Deployment (RECOMMENDED)
```bash
# Use Podman/Docker for production
podman-compose up --build -d
# See DEPLOYMENT.md for complete instructions
```

### Database Management
```bash
# Reset database completely (removes analysis.db)
rm analysis.db
# Database will be recreated automatically on next run

# Manual database migration is automatic - no commands needed
```

### Docker Operations
```bash
# Build and run with Docker Compose
docker-compose up --build

# Build standalone image
docker build -t ntg-js-analyzer .

# Run with Podman (alternative to Docker)
# See PODMAN_MANUAL.md for detailed instructions
```

## Architecture

### Application Structure
- **Two-tier architecture**: Flask web app + SQLite database
- **Authentication system**: Session-based login with role-based user management
- **Client management**: Enterprise client organization and tracking
- **Dual interface**: Web dashboard + command-line analyzer
- **Export system**: PDF, CSV, Excel generation with professional formatting
- **Role-based access**: Administrator and Analyst user roles with differentiated permissions

### Database Schema (7 core tables)
- **scans**: Main analysis records (url, scan_date, status_code, title, headers JSON, client_id FK)
- **libraries**: Detected libraries with vulnerability tracking (scan_id FK, library_name, version, type, source_url, description, latest_safe_version, latest_version, is_manual)
- **version_strings**: Raw version strings found in files (scan_id FK, file_url, file_type, line_number, line_content, version_keyword)  
- **file_urls**: All JS/CSS files discovered (scan_id FK, file_url, file_type, file_size, status_code)
- **users**: User accounts with roles (username, password_hash, role)
- **clients**: Client organizations (name, contact_info, is_active)
- **global_libraries**: Global library catalog (library_name, description, latest_safe_version, latest_version, library_type)

### Security Analysis System
- **HTTP security headers analysis**: 7 headers evaluated (HSTS, CSP, X-Frame-Options, X-XSS-Protection, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
- **Vulnerability detection logic**: Shows ⚠️ when current version < latest_safe_version AND current != latest_safe AND latest_safe exists
- **Security scoring**: Percentage-based scores with specific recommendations

### Library Detection Engine
**Automatic Detection (`analyzer.py`):**
- `detect_js_libraries()`: jQuery, React, Vue.js, Angular, Bootstrap JS via script src patterns
- `detect_css_libraries()`: Bootstrap CSS, Font Awesome via link href patterns
- `scan_file_for_versions()`: Downloads JS/CSS files and searches for version strings using regex
- `get_all_js_css_files()`: Extracts all script and stylesheet URLs from HTML

**Manual Management (`dashboard.py`):**
- Add/edit/delete libraries with rich metadata
- Version tracking (current vs latest_safe vs latest_available)
- Vulnerability indicators across all interfaces and exports

### Flask Route Architecture
**Core Analysis Routes:**
- `/`: Dashboard with statistics, client filtering, and batch analysis tools
- `/scan/<id>`: Detailed analysis view (6 data sections)
- `/analyze-url` (POST): Single URL analysis
- `/batch-analyze` (POST): Multiple URL analysis

**Authentication Routes:**
- `/login`: Session-based authentication
- `/logout`: Session cleanup  
- `/users`: User management interface (admin only)
- `/change_own_password` (POST): Self-service password change

**Client Management Routes:**
- `/clients`: Client CRUD interface
- `/add_client` (POST): Create new client
- `/edit_client/<id>` (POST): Update client information
- `/delete_client/<id>` (POST): Remove client

**User Management Routes (Admin Only):**
- `/add_user` (POST): Create new users
- `/change_password/<id>` (POST): Admin password reset
- `/change_role/<id>` (POST): Modify user roles
- `/delete_user/<id>` (POST): Remove users

**Library Management Routes:**
- `/add-manual-library` (POST): Add custom libraries
- `/edit-library/<id>` (POST): Update library information
- `/delete-library/<id>` (POST): Remove libraries
- `/global-libraries`: Global library catalog management

**Export Routes:**
- `/export/pdf/<scan_id>`: Professional PDF reports with ReportLab
- `/export/csv/<scan_id>`: Structured CSV export
- `/export/excel/<scan_id>`: Multi-sheet Excel workbooks with OpenPyXL
- `/export/clients/csv`: Client data export

**API Endpoints:**
- `/api/scans`, `/api/libraries`, `/api/version-strings`, `/api/stats`: JSON data access
- `/api/clients`: Client data API access

### Data Flow
1. User authentication with role-based access control
2. Client assignment and organization setup
3. URL analysis via web interface or command-line batch processing
4. HTML parsing with BeautifulSoup to extract script/link tags
5. JS/CSS file download and content scanning for version patterns
6. HTTP header analysis with security scoring algorithm
7. Vulnerability assessment with global library catalog comparison
8. Database storage with automatic schema migration
9. Web dashboard provides CRUD operations with bulk actions and client filtering
10. Export generation with professional formatting and client-specific reports

## Template and Static File Structure

### Frontend Architecture
- **Bootstrap-based responsive design** with custom CSS enhancements
- **JavaScript interactivity**:
  - `static/js/index.js`: Dashboard functionality, batch operations, dynamic counters
  - `static/js/scan_detail.js`: Scan details interactions, modal management
- **Template inheritance**:
  - `base.html`: Navigation with role-based menus, flash messages, common layout, self-service password change modal
  - `index.html`: Dashboard with statistics, client filtering, and analysis tools
  - `scan_detail.html`: Comprehensive scan analysis with 6 data sections
  - `login.html`: Chilean Spanish authentication interface with Bootstrap icons
  - `users.html`: User management with role administration (admin only)
  - `clients.html`: Client management interface
  - `global_libraries.html`: Global library catalog management

### Jinja2 Template Patterns
- Use `default(0)` not `default:0` for filter defaults
- Security score display: `{{ security_analysis.security_score }}%` (no semicolon in style)
- Vulnerability indicators: `{% if condition %} ⚠️ {% endif %}` pattern throughout templates
- Role-based conditional rendering: `{% if session.user_role == 'admin' %}` for admin-only content
- Chilean Spanish translation throughout all templates with Bootstrap icons
- URL parameter preservation: Use hidden form fields to maintain client_id and search filters

## Key Features and Implementation Details

### Role-Based Access Control System
- **Two user roles**: Administrator and Analyst with differentiated permissions
- **Administrator privileges**: Full access including user management, role changes, user creation/deletion
- **Analyst privileges**: Full access to clients, scans, global catalog, data imports (excludes user management)
- **Route protection**: Role-specific decorators (`@admin_required`) for restricted operations
- **UI adaptation**: Role-based menu visibility and feature access

### Client Management System
- **Full CRUD operations**: Create, read, update, delete clients
- **Client assignment**: Associate scans with specific clients
- **Filtering capabilities**: Dashboard filtering by client with URL parameter preservation
- **Statistics tracking**: Client-specific metrics and analysis summaries
- **Data organization**: Hierarchical organization for enterprise environments

### Batch Operations System
- **Checkbox-based selection** with "Select All" functionality
- **Dynamic counters**: "Delete Selected (X)" buttons appear/disappear based on selection
- **Confirmation modals** with preview of items to be deleted
- **Independent operation modes**: Individual delete buttons coexist with batch operations
- **Client filtering preservation**: Maintains client context during batch operations

### Export System Architecture
- **PDF**: ReportLab with professional table styling, security analysis, vulnerability indicators
- **CSV**: Section-separated format with clear headers for each data type
- **Excel**: Multi-sheet workbooks with conditional formatting, auto-sizing, styled headers
- **Client-specific exports**: Filtered exports based on client assignment

### Authentication System
- **Session-based login** with decorator pattern (`@login_required`)
- **Role-based authorization**: `@admin_required` decorator for administrative functions
- **User table** with password hashing using Werkzeug security
- **Self-service password change**: Users can change their own passwords
- **Route protection**: All main routes decorated with `@login_required`
- **CSRF protection**: Flask-WTF CSRF tokens on forms

### Vulnerability Assessment Enhancement
- **Dashboard vulnerability counters**: Show vulnerability counts per scan in listing
- **Global library catalog**: Centralized management of library definitions and safe versions
- **Enhanced detection**: Improved vulnerability identification with catalog comparison

### Database Migration Pattern
The application automatically handles schema updates:
```python
# Pattern used for adding new columns (users, clients, global_libraries tables)
try:
    cursor.execute("SELECT role FROM users LIMIT 1")
except sqlite3.OperationalError:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'admin'")

# New table creation pattern
cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    contact_info TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
```

## Development Patterns

### Adding New User Roles
Extend role system in `dashboard.py`:
```python
# Add new role check decorator
def new_role_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        user_role = session.get('user_role', '')
        if user_role not in ['admin', 'new_role']:
            flash('Acceso denegado', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
```

### Adding Client-Specific Features
Implement client filtering in routes:
```python
# Standard client filtering pattern
client_id_param = request.args.get('client_id')
where_clause = "WHERE 1=1"
query_params = []

if client_id_param and client_id_param != 'null':
    where_clause += " AND s.client_id = ?"
    query_params.append(int(client_id_param))
elif client_id_param == 'null':
    where_clause += " AND s.client_id IS NULL"
```

### Adding New Library Detection
Extend detection functions in `analyzer.py`:
```python
# Add to detect_js_libraries() or detect_css_libraries()
new_lib_scripts = soup.find_all('script', src=re.compile(r'library-name', re.I))
for script in new_lib_scripts:
    # Extract version using regex patterns
    # Add to libraries list with standard format
```

### Security Header Configuration
Extend `analyze_security_headers()` in `dashboard.py`:
```python
security_headers = {
    'new-header': {
        'name': 'New-Header',
        'description': 'Header description',
        'recommendation': 'Recommended value'
    }
}
```

### Error Handling Patterns
- **Try-catch blocks** around all external requests and database operations
- **User-friendly error messages** via Flask flash() system
- **Graceful degradation** for network failures and parsing errors
- **Request timeout handling** with configurable delays for batch operations

## Performance and Limitations

### Current Constraints
- **File analysis limit**: First 10 JS/CSS files per site to prevent excessive downloads
- **Request delays**: Built-in delays for batch operations to avoid overwhelming target sites
- **Memory management**: Large file downloads have size limits to prevent memory issues

### Database Performance
- **SQLite with proper indexing** on foreign keys and frequently queried columns
- **Connection management**: Proper cleanup and timeout handling
- **Cascading deletes**: Scan deletion removes all related records automatically

## Security Configuration (CRITICAL)

### ⚠️ Pre-Production Security Checklist
```bash
# 1. Generate secure secret key
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# 2. Remove sensitive files
rm -f admin_credentials.txt

# 3. Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=0

# 4. Verify secure configuration
grep -E "(SECRET_KEY|DEBUG|FLASK_ENV)" .env
```

### Flask Security Configuration
- **Secret Key**: MUST use strong, environment-based key (`FLASK_SECRET_KEY`)
- **Debug Mode**: DISABLED in production (`FLASK_ENV=production`)
- **Session Security**: HTTPOnly, Secure (HTTPS), SameSite=Lax
- **CSRF Protection**: Enabled globally with Flask-WTF
- **Request Validation**: All external URLs validated for SSRF protection

### Security Headers Applied (dashboard.py:2015-2042)
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff' 
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "restrictive-policy"
    # + More security headers
```

### Dependencies (Security Audited)
- **Core**: Flask 2.3.3, BeautifulSoup4 4.12.2, requests 2.32.4
- **Export**: ReportLab 4.0.4, OpenPyXL 3.1.2, Pandas 2.3.1
- **Security**: Flask-WTF 1.2.1 for CSRF protection, Werkzeug for password hashing
- **Parsing**: lxml 4.9.3 for XML/HTML processing
- **Hardened**: pillow>=10.3.0, urllib3>=2.5.0 (Snyk-secured versions)

## Security Audit Results (January 2025)

### ✅ SECURITY STRENGTHS
1. **Authentication & Sessions**: Robust implementation with Werkzeug hashing
2. **CSRF Protection**: Flask-WTF properly implemented on all forms  
3. **SQL Injection**: Parameterized queries used exclusively
4. **SSRF Protection**: Comprehensive URL validation with private IP blocking
5. **HTTP Headers**: Complete security header implementation
6. **Input Validation**: Proper sanitization and validation patterns

### ⚠️ SECURITY VULNERABILITIES IDENTIFIED
1. **CRITICAL**: Exposed credentials in `admin_credentials.txt` 
2. **HIGH**: Weak secret key in `.env` example files
3. **MEDIUM**: Debug information in console logs
4. **LOW**: Missing rate limiting implementation

### 🚨 IMMEDIATE REMEDIATION REQUIRED
```bash
# 1. Remove exposed credentials (CRITICAL)
rm -f admin_credentials.txt

# 2. Generate strong secret key (HIGH) 
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# 3. Set production environment (MEDIUM)
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### 🔒 Security Score: 7.5/10
- **Defensive Architecture**: Excellent
- **Implementation Quality**: Very Good  
- **Configuration Security**: Needs Improvement
- **Overall Assessment**: Production-ready after credential rotation

## Development Security Guidelines

### When Working with This Codebase:
1. **ALWAYS** check for hardcoded secrets before commits
2. **NEVER** commit `.env` files or credential files
3. **VERIFY** SSRF protection when adding URL processing
4. **ENSURE** CSRF tokens on new forms
5. **USE** parameterized SQL queries exclusively
6. **VALIDATE** all user inputs with sanitization
7. **TEST** security headers after route changes

## Production Deployment

### Use Containerized Deployment (Recommended)
- See `DEPLOYMENT.md` for complete Podman/Docker instructions
- Automated security configuration
- Isolated environment with volume persistence
- Production-grade logging and monitoring