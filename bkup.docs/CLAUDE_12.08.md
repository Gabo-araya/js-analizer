# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Python Flask application that analyzes websites to detect JavaScript and CSS library versions, assess vulnerabilities, and provide export capabilities. The application consists of two main components:

1. **Web Scraper** (`analyzer.py`) - Command-line tool that visits URLs and detects library versions
2. **Flask Dashboard** (`dashboard.py`) - Web interface for analysis, management, and export functionality

## Core Commands

### Run Web Dashboard
```bash
python dashboard.py
```
Starts Flask web server on http://localhost:5000 for web-based analysis and management.

### Run Command-line Analysis  
```bash
python analyzer.py
```
Reads URLs from `urls.txt` and analyzes each site, storing results in SQLite database.

### Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Management
```bash
# Reset database (removes analysis.db file)
# Available via web interface or manual file deletion
rm analysis.db
```

## Architecture

### Data Flow
1. URLs analyzed via web interface or command-line (`urls.txt`)
2. For each URL: fetches HTML, parses with BeautifulSoup, runs library detection
3. Downloads JS/CSS files and scans content for version keywords
4. Analyzes HTTP security headers with scoring system
5. Results stored in SQLite database with automatic migration support
6. Web dashboard provides comprehensive viewing, editing, and export capabilities

### Database Schema (4 tables)
- **scans**: url, scan_date, status_code, title, headers (JSON)
- **libraries**: scan_id (FK), library_name, version, type, source_url, description, latest_safe_version, latest_version, is_manual
- **version_strings**: scan_id (FK), file_url, file_type, line_number, line_content, version_keyword  
- **file_urls**: scan_id (FK), file_url, file_type, file_size, status_code

### Library Detection System

**Automatic Detection Functions:**
- `detect_js_libraries()` - jQuery, React, Vue.js, Angular, Bootstrap JS
- `detect_css_libraries()` - Bootstrap CSS, Font Awesome
- `scan_file_for_versions()` - Downloads files and searches for version strings
- `get_all_js_css_files()` - Extracts all script/stylesheet URLs

**Manual Library Management:**
- Add/Edit/Delete libraries with vulnerability tracking
- Version comparison: current vs latest_safe vs latest_available
- Vulnerability logic: shows ⚠️ when `current < latest_safe AND current != latest_safe AND latest_safe exists`

### Security Analysis
- Analyzes 7 security headers: HSTS, CSP, X-Frame-Options, X-XSS-Protection, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
- Generates percentage-based security scores
- Provides specific recommendations for missing headers

## Flask Routes Structure

**Main Interface:**
- `/` - Dashboard with statistics and analysis tools
- `/scan/<id>` - Detailed scan view with 6 data sections
- `/analyze-url` (POST) - Single URL analysis
- `/batch-analyze` (POST) - Bulk URL analysis

**Library Management:**
- `/add-manual-library` (POST) - Add custom library entries
- `/edit-library/<id>` (POST) - Update library information
- `/delete-library/<id>` (POST) - Remove libraries

**Export Functionality:**
- `/export/pdf/<scan_id>` - Professional PDF reports
- `/export/csv/<scan_id>` - Complete CSV data export
- `/export/excel/<scan_id>` - Multi-sheet Excel workbooks

**Batch Operations:**
- Multiple delete endpoints for version strings, file URLs, and libraries
- Checkbox-based selection with confirmation modals

**API Endpoints:**
- `/api/scans`, `/api/libraries`, `/api/version-strings`, `/api/stats`

## Key Features

### Vulnerability Detection
- Visual ⚠️ indicators for potentially outdated libraries
- Three-condition vulnerability logic consistently applied across interface and exports
- Manual library tracking with version comparison capabilities

### Batch Operations  
- Checkbox selection with "Select All" functionality
- Dynamic counters and confirmation modals
- Individual and bulk operations work independently

### Export Capabilities
- **PDF**: Professional reports with styled tables
- **CSV**: Section-separated data export  
- **Excel**: Multi-sheet workbooks with formatting and auto-sizing

### Manual Library Management
- Add libraries not detected automatically
- Rich forms with descriptions and version tracking
- Edit both auto-detected and manually added entries

## Static Files Organization

### Frontend Structure
- **CSS** (`static/css/main.css`): Bootstrap-based styling with custom enhancements
- **JavaScript**:
  - `static/js/index.js` - Dashboard functionality and form handling
  - `static/js/scan_detail.js` - Scan details page interactions
- **Templates**:
  - `base.html` - Base template with navigation and flash messages
  - `index.html` - Dashboard with statistics and tools
  - `scan_detail.html` - Comprehensive scan analysis view

## Configuration and Extension

### Adding New Library Detection
Extend detection functions in `analyzer.py`:
```python
# Example pattern for new library
new_lib_scripts = soup.find_all('script', src=re.compile(r'library-name', re.I))
```

### Security Header Configuration
Extend `analyze_security_headers()` in `dashboard.py` with new header definitions.

### Database Migration
Application automatically migrates existing databases to add new columns - no manual intervention required.

## Development Notes

### Error Handling
- Comprehensive try-catch blocks throughout
- User-friendly error messages via Flask flash system
- Graceful handling of network failures and parsing errors

### Performance Considerations  
- File analysis limited to first 10 files per site
- Database connections use proper timeout and cleanup
- Request delays built into batch operations

### Dependencies
- Flask 2.3.3, BeautifulSoup4 4.12.2, ReportLab 4.0.4, OpenPyXL 3.1.2
- Pandas 2.3.1 for data processing
- Security-pinned versions for Pillow and urllib3