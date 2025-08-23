# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Python web application that analyzes websites to detect JavaScript and CSS library versions, with vulnerability assessment and extensive export capabilities. It consists of two main components:

1. **Web Scraper** (`analyzer.py`) - Visits URLs and detects library versions using BeautifulSoup and regex patterns
2. **Flask Dashboard** (`dashboard.py`) - Provides web interface, manual library management, batch operations, and export functionality

## Core Commands

### Run Analysis
```bash
python analyzer.py
```
Reads URLs from `urls.txt` and analyzes each site, storing results in SQLite database.

### Start Dashboard
```bash
python dashboard.py
```
Starts Flask web server on http://localhost:5000 to view analysis results.

### Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Key Dependencies
- Flask 2.3.3 (web framework)
- BeautifulSoup4 4.12.2 (HTML parsing)
- ReportLab 4.0.4 (PDF generation)
- OpenPyXL 3.1.2 (Excel export)
- Pandas 2.1.1 (data processing)

## Architecture

### Data Flow
1. `analyzer.py` reads URLs from `urls.txt` or processes URLs from web interface
2. For each URL: fetches HTML, parses with BeautifulSoup, runs library detection functions
3. Extracts all JS/CSS file URLs and scans their content for "version" and "versión" keywords
4. Analyzes HTTP security headers and generates security scores
5. Results stored in SQLite (`analysis.db`) with four main tables
6. `dashboard.py` provides comprehensive web interface for viewing, managing, and exporting data

### Database Schema
- **scans table**: url, scan_date, status_code, title, headers (JSON)
- **libraries table**: scan_id (FK), library_name, version, type (js/css), source_url, description, latest_safe_version, latest_version, is_manual
- **version_strings table**: scan_id (FK), file_url, file_type (js/css), line_number, line_content, version_keyword
- **file_urls table**: scan_id (FK), file_url, file_type, file_size, status_code

### Library Detection System
**Automatic Detection Functions:**
- `detect_js_libraries()` - jQuery, React, Vue.js, Angular, Bootstrap JS
- `detect_css_libraries()` - Bootstrap CSS, Font Awesome
- `scan_file_for_versions()` - Downloads JS/CSS files and searches for version keywords
- `get_all_js_css_files()` - Extracts all script and stylesheet URLs

**Manual Library Management:**
- Add/Edit/Delete libraries manually with vulnerability information
- Track current version vs latest safe version vs latest available version
- Vulnerability detection logic: `current < latest_safe AND current != latest_safe AND latest_safe exists`

### Security Analysis
- Analyzes 7 key security headers: HSTS, CSP, X-Frame-Options, X-XSS-Protection, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
- Generates security scores (percentage of headers present)
- Provides recommendations for missing headers

### Flask Routes Structure

**Main Interface:**
- `/` - Dashboard with stats, recent scans, and analysis tools
- `/scan/<id>` - Detailed scan view with all data sections
- `/analyze-url` (POST) - Single URL analysis from web interface
- `/batch-analyze` (POST) - Multiple URL analysis from textarea

**Library Management:**
- `/add-manual-library` (POST) - Add library with vulnerability info
- `/edit-library/<id>` (POST) - Update existing library
- `/delete-library/<id>` (POST) - Remove library

**Batch Operations:**
- `/batch-delete-version-strings` (POST) - Delete multiple version strings
- `/batch-delete-file-urls` (POST) - Delete multiple file URLs
- `/delete-file-url/<id>` (POST) - Delete individual file URL
- `/delete-version-string/<id>` (POST) - Delete individual version string

**Export Functionality:**
- `/export/pdf/<scan_id>` - Professional PDF report
- `/export/csv/<scan_id>` - Comprehensive CSV export
- `/export/excel/<scan_id>` - Multi-sheet Excel workbook

**API Endpoints:**
- `/api/scans` - All scan data with counts
- `/api/libraries` - All libraries with site context
- `/api/version-strings` - All version strings found
- `/api/stats` - Dashboard statistics

**Administrative:**
- `/reset-database` (POST) - Complete database reset
- `/delete-scan/<id>` (POST) - Remove entire scan with cascading deletes

## Static Files Organization

### CSS (`static/css/main.css`)
- Library badges styling (JS/CSS color coding)
- Loading overlay animations
- Modal enhancements
- Table and card improvements
- Responsive design utilities

### JavaScript
- **`static/js/index.js`**: Dashboard functionality (form submissions, batch analysis, loading states)
- **`static/js/scan_detail.js`**: Scan details page (checkbox selections, modal handlers, library management)

### Templates
- **`base.html`**: Clean base template with static file references
- **`index.html`**: Dashboard with stats cards and analysis tools
- **`scan_detail.html`**: Comprehensive scan view with 6 main sections

## Key Features

### Vulnerability Detection
- Visual indicators (⚠️) for potentially vulnerable libraries
- Three-condition logic: `latest_safe_version exists AND version != latest_safe_version AND version < latest_safe_version`
- Consistent across web interface and all export formats

### Batch Operations
- Checkbox selection with "Select All" functionality
- Dynamic counters and button states
- Bulk deletion with confirmation previews
- Individual and batch operations coexist

### Export Capabilities
- **PDF**: Professional report with tables and styling
- **CSV**: Complete data export with section headers
- **Excel**: Multi-sheet workbook with formatting and auto-column sizing

### Manual Library Management
- Add libraries not detected automatically
- Track vulnerability status with version comparison
- Rich forms with descriptions and version tracking
- Edit both auto-detected and manual entries

## Configuration

### Database Migration
The app automatically migrates existing databases to add new columns for manual library management.

### URL Sources
- `urls.txt` file for command-line analysis
- Web interface for single URL analysis
- Textarea input for batch URL analysis (supports comments with #)

### Security Headers Analysis
Configure in `analyze_security_headers()` function - easily extensible for new headers.

### Library Detection Patterns
Extend detection by adding regex patterns to detection functions following existing examples.

## Development Notes

### Error Handling
- Comprehensive try-catch blocks with user feedback
- Database connection management with timeouts
- Graceful handling of failed URL analysis

### Performance Considerations
- Database connections use timeouts and proper cleanup
- File analysis limited to first 10 files to prevent overload
- Batch operations include delays to respect server limits

### Code Organization
- Follows Flask best practices with static file separation
- Modular JavaScript for different page functionalities
- CSS organized by component categories
- Database schema supports both automatic and manual data entry

## Testing Commands

### Database Verification
```bash
python3 -c "from dashboard import get_db_connection; conn = get_db_connection(); print('Database connection successful')"
```

### Static Files Check
```bash
ls -la static/css/ static/js/
```

### Function Testing
```bash
python3 -c "from dashboard import analyze_security_headers; print(analyze_security_headers({'x-frame-options': 'SAMEORIGIN'}))"
```

## Database Location
SQLite database (`analysis.db`) is created automatically in project root directory with automatic migration for schema updates.