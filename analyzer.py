#!/usr/bin/env python3
import requests
import sqlite3
import re
import json
import ipaddress
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import Dict, List, Optional, Tuple

# Import our advanced library detectors
try:
    from library_detector import LibraryDetector, detect_libraries_advanced
    ADVANCED_DETECTION_AVAILABLE = True
    print("✅ Advanced library detection enabled")
except ImportError:
    print("⚠️ Advanced library detector not available, using basic detection")
    ADVANCED_DETECTION_AVAILABLE = False

# Import enhanced content-based detection
try:
    from library_signatures import detect_libraries_by_content, get_library_info
    CONTENT_DETECTION_AVAILABLE = True
    print("✅ Content-based library detection enabled")
except ImportError:
    print("⚠️ Content-based detection not available")
    CONTENT_DETECTION_AVAILABLE = False


# Import CDN analyzer
try:
    from cdn_analyzer import analyze_cdn_url, get_cdn_recommendations, cdn_analyzer
    CDN_ANALYZER_AVAILABLE = True
    print("✅ CDN dependency analyzer enabled")
    print(f"🌐 CDN Analyzer supports {len(cdn_analyzer.get_supported_cdns())} CDN providers")
except ImportError:
    print("⚠️ CDN analyzer not available")
    CDN_ANALYZER_AVAILABLE = False

class LibraryAnalyzer:
    def __init__(self, db_path="analysis.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if database needs migration for new library columns
        try:
            cursor.execute("SELECT description FROM libraries LIMIT 1")
        except sqlite3.OperationalError:
            # Columns don't exist, need to add them
            print("🔄 Migrating database: Adding new library management columns...")
            try:
                cursor.execute("ALTER TABLE libraries ADD COLUMN description TEXT")
                cursor.execute("ALTER TABLE libraries ADD COLUMN latest_safe_version TEXT")
                cursor.execute("ALTER TABLE libraries ADD COLUMN latest_version TEXT")
                cursor.execute("ALTER TABLE libraries ADD COLUMN is_manual INTEGER DEFAULT 0")
                print("✅ Database migration completed successfully!")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Migration warning: {e}")
                # Columns might already exist, continue

        # Check for project_id and reviewed columns in scans table
        try:
            cursor.execute("SELECT project_id, reviewed FROM scans LIMIT 1")
        except sqlite3.OperationalError:
            print("🔄 Migrating database: Adding new project and review columns to scans...")
            try:
                cursor.execute("ALTER TABLE scans ADD COLUMN project_id INTEGER")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Migration warning: {e}")
            try:
                cursor.execute("ALTER TABLE scans ADD COLUMN reviewed INTEGER DEFAULT 0")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Migration warning: {e}")

        conn.commit()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status_code INTEGER,
            title TEXT,
            headers TEXT,
            project_id INTEGER,
            reviewed INTEGER DEFAULT 0
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS libraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER,
            library_name TEXT NOT NULL,
            version TEXT,
            type TEXT, -- 'js' or 'css'
            source_url TEXT,
            description TEXT, -- Manual description
            latest_safe_version TEXT, -- Latest version without vulnerabilities
            latest_version TEXT, -- Latest available version
            is_manual INTEGER DEFAULT 0, -- 1 if manually added, 0 if auto-detected
            FOREIGN KEY (scan_id) REFERENCES scans (id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS version_strings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER,
            file_url TEXT NOT NULL,
            file_type TEXT, -- 'js' or 'css'
            line_number INTEGER,
            line_content TEXT,
            version_keyword TEXT, -- 'version' or 'versión'
            FOREIGN KEY (scan_id) REFERENCES scans (id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER,
            file_url TEXT NOT NULL,
            file_type TEXT, -- 'js' or 'css'
            file_size INTEGER, -- in bytes, null if unknown
            status_code INTEGER, -- HTTP response code when fetching file
            FOREIGN KEY (scan_id) REFERENCES scans (id)
        )
        ''')

        conn.commit()
        conn.close()

    def detect_js_libraries(self, soup, base_url):
        libraries = []

        if ADVANCED_DETECTION_AVAILABLE:
            # Use advanced detection system
            detector = LibraryDetector()

            # Get all script files
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script.get('src')
                if src:
                    full_url = urljoin(base_url, src)
                    filename = full_url.split('/')[-1]

                    # Try to get file content for deeper analysis
                    try:
                        content = self._fetch_file_content(full_url, max_size=5120)  # 5KB limit
                    except:
                        content = None

                    # Use advanced detection
                    detections = detect_libraries_advanced(full_url, filename, content)

                    for detection in detections:
                        if detection['type'] == 'js':
                            libraries.append({
                                'name': detection['library_name'].title(),
                                'version': detection['version'],
                                'type': 'js',
                                'source': full_url,
                                'confidence': detection['confidence'],
                                'detection_method': detection['detection_method']
                            })
        else:
            # Fallback to basic detection
            libraries = self._detect_js_libraries_basic(soup, base_url)

        return libraries

    def _detect_js_libraries_basic(self, soup, base_url):
        """Método básico de detección (fallback)"""
        libraries = []

        # jQuery detection
        jquery_scripts = soup.find_all('script', src=re.compile(r'jquery', re.I))
        for script in jquery_scripts:
            src = script.get('src', '')
            version_match = re.search(r'jquery[-.]?(\d+\.\d+\.\d+)', src, re.I)
            if version_match:
                libraries.append({
                    'name': 'jQuery',
                    'version': version_match.group(1),
                    'type': 'js',
                    'source': urljoin(base_url, src),
                    'confidence': 0.8,
                    'detection_method': 'basic_pattern'
                })

        # React detection
        react_scripts = soup.find_all('script', src=re.compile(r'react', re.I))
        for script in react_scripts:
            src = script.get('src', '')
            version_match = re.search(r'react[-.]?(\d+\.\d+\.\d+)', src, re.I)
            if version_match:
                libraries.append({
                    'name': 'React',
                    'version': version_match.group(1),
                    'type': 'js',
                    'source': urljoin(base_url, src),
                    'confidence': 0.8,
                    'detection_method': 'basic_pattern'
                })

        # Bootstrap JS detection
        bootstrap_scripts = soup.find_all('script', src=re.compile(r'bootstrap', re.I))
        for script in bootstrap_scripts:
            src = script.get('src', '')
            version_match = re.search(r'bootstrap[-.]?(\d+\.\d+\.\d+)', src, re.I)
            if version_match:
                libraries.append({
                    'name': 'Bootstrap JS',
                    'version': version_match.group(1),
                    'type': 'js',
                    'source': urljoin(base_url, src),
                    'confidence': 0.7,
                    'detection_method': 'basic_pattern'
                })

        # NTG Custom Libraries detection
        ntg_scripts = soup.find_all('script', src=re.compile(r'ntg_\w+\.js', re.I))
        for script in ntg_scripts:
            src = script.get('src', '')
            # Extract library name from filename
            filename_match = re.search(r'(ntg_\w+)\.js', src, re.I)
            if filename_match:
                library_name = filename_match.group(1)

                # Try to fetch content to get version from $Id pattern
                full_url = urljoin(base_url, src)
                try:
                    content = self._fetch_file_content(full_url, max_size=2048)  # 2KB should be enough for header
                    version = None

                    if content:
                        # Look for $Id pattern in first few lines
                        lines = content.split('\n')[:10]  # Check first 10 lines
                        for line in lines:
                            id_match = re.search(r'\$Id:\s+' + re.escape(library_name + '.js') + r'\s+(\d+)\s+', line)
                            if id_match:
                                version = id_match.group(1)
                                break

                    libraries.append({
                        'name': library_name,
                        'version': version or 'unknown',
                        'type': 'js',
                        'source': full_url,
                        'confidence': 0.9 if version else 0.6,
                        'detection_method': 'ntg_pattern' if version else 'filename_pattern'
                    })

                except Exception as e:
                    # Fallback: add without version
                    libraries.append({
                        'name': library_name,
                        'version': 'unknown',
                        'type': 'js',
                        'source': urljoin(base_url, src),
                        'confidence': 0.5,
                        'detection_method': 'filename_pattern'
                    })

        return libraries

    def _fetch_file_content(self, file_url, max_size=5120):
        """
        Fetch file content for analysis (limited size)
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(file_url, headers=headers, timeout=5, stream=True)
            if response.status_code == 200:
                # Read only first max_size bytes
                content = response.raw.read(max_size).decode('utf-8', errors='ignore')
                return content
        except:
            pass
        return None

    def detect_css_libraries(self, soup, base_url):
        """CSS library detection disabled - returning empty list"""
        return []

    def _detect_css_libraries_basic(self, soup, base_url):
        """Método básico de detección CSS (fallback)"""
        libraries = []

        # Bootstrap CSS detection
        bootstrap_links = soup.find_all('link', href=re.compile(r'bootstrap', re.I))
        for link in bootstrap_links:
            href = link.get('href', '')
            version_match = re.search(r'bootstrap[-.]?(\d+\.\d+\.\d+)', href, re.I)
            if version_match:
                libraries.append({
                    'name': 'Bootstrap CSS',
                    'version': version_match.group(1),
                    'type': 'css',
                    'source': urljoin(base_url, href),
                    'confidence': 0.7,
                    'detection_method': 'basic_pattern'
                })

        # Font Awesome detection
        fa_links = soup.find_all('link', href=re.compile(r'font-?awesome', re.I))
        for link in fa_links:
            href = link.get('href', '')
            version_match = re.search(r'font-?awesome[-.]?(\d+\.\d+\.\d+)', href, re.I)
            if version_match:
                libraries.append({
                    'name': 'Font Awesome',
                    'version': version_match.group(1),
                    'type': 'css',
                    'source': urljoin(base_url, href),
                    'confidence': 0.7,
                    'detection_method': 'basic_pattern'
                })

        return libraries

    def _enhance_with_contextual_detection(self, libraries, url, soup):
        """
        Enhance detection with contextual information from URL and page content
        """
        try:
            detector = LibraryDetector()
            url_lower = url.lower()

            # Get probable libraries based on URL context
            contextual_libs = detector.detect_contextual_libraries(url)

            # Analyze page content for additional context clues
            page_text = soup.get_text().lower()
            title = soup.find('title')
            title_text = title.text.lower() if title else ''

            # Context detection rules
            additional_context = []

            # Analytics context
            if any(word in url_lower or word in page_text or word in title_text for word in ['analytics', 'estadisticas', 'stats', 'metrics']):
                additional_context.extend(['chart.js', 'd3', 'datatables', 'plotly'])

            # Media/Gallery context
            if any(word in url_lower or word in page_text or word in title_text for word in ['gallery', 'galeria', 'prensa', 'photos', 'media']):
                additional_context.extend(['lightbox', 'swiper', 'fancybox'])

            # Forms context
            if any(word in url_lower or word in page_text for word in ['form', 'formulario', 'contact', 'registro', 'login']):
                additional_context.extend(['select2', 'datepicker', 'validation'])

            # Admin/Dashboard context
            if any(word in url_lower or word in title_text for word in ['admin', 'dashboard', 'panel', 'manage']):
                additional_context.extend(['datatables', 'select2', 'chart.js'])

            # E-commerce context
            if any(word in url_lower or word in page_text for word in ['shop', 'tienda', 'cart', 'carrito', 'buy', 'comprar']):
                additional_context.extend(['swiper', 'select2'])

            # Combine all contextual libraries
            all_contextual = list(set(contextual_libs + additional_context))

            # Try to detect missing contextual libraries
            missing_libraries = []
            detected_lib_names = [lib['name'].lower() for lib in libraries]

            for context_lib in all_contextual:
                if context_lib not in detected_lib_names and context_lib.replace('-', ' ').replace('.', ' ') not in ' '.join(detected_lib_names):
                    # Try to find evidence of this library in the page
                    if self._find_library_evidence(context_lib, soup, url):
                        missing_libraries.append({
                            'name': context_lib.title(),
                            'version': 'unknown',
                            'type': self._get_library_type(context_lib),
                            'source': url,
                            'confidence': 0.5,
                            'detection_method': 'contextual_inference'
                        })

            # Enhance confidence of existing detections that match context
            for lib in libraries:
                lib_name_lower = lib['name'].lower().replace(' ', '-')
                if lib_name_lower in all_contextual:
                    lib['confidence'] = min(lib.get('confidence', 0.7) + 0.15, 1.0)
                    lib['contextual_match'] = True

            # Add missing contextual libraries
            enhanced_libraries = libraries + missing_libraries

            print(f"  → Contextual analysis: Found {len(missing_libraries)} additional probable libraries")

            return enhanced_libraries

        except Exception as e:
            print(f"  → Contextual analysis failed: {str(e)}")
            return libraries

    def _find_library_evidence(self, library_name, soup, url):
        """
        Find evidence that a library might be used on the page
        """
        evidence_patterns = {
            'chart.js': ['canvas', 'chart', 'graph'],
            'd3': ['svg', 'd3', 'visualization'],
            'datatables': ['table', 'datatable', 'sorting'],
            'lightbox': ['lightbox', 'gallery', 'popup'],
            'swiper': ['slider', 'carousel', 'swiper'],
            'select2': ['select', 'dropdown', 'chosen'],
            'moment': ['date', 'time', 'calendar'],
            'lodash': ['_', 'utility', 'helper'],
            'font-awesome': ['fa-', 'icon', 'fas ', 'far ']
        }

        patterns = evidence_patterns.get(library_name, [])
        page_content = str(soup).lower()

        # Check for DOM elements or classes that suggest library usage
        for pattern in patterns:
            if pattern in page_content:
                return True

        return False

    def _get_library_type(self, library_name):
        """
        Get the type of library (js or css) based on its name
        """
        css_libraries = ['bootstrap', 'font-awesome', 'bulma', 'foundation']
        return 'css' if library_name in css_libraries else 'js'

    def scan_file_for_versions(self, file_url, file_type, scan_id):
        """
        Enhanced version scanning with multiple patterns and automatic library detection
        """
        version_strings = []
        detected_libraries = []

        # Diccionarios para evitar duplicados por URL fuente
        # Solo mantenemos la PRIMERA biblioteca y cadena de versión detectada por archivo
        first_library_per_source = {}
        first_version_string_per_source = {}

        # Patrones de versión solicitados por el usuario
        VERSION_PATTERNS = [
            # Patrón específico para bibliotecas NTG (debe ir primero por precedencia)
            (r'\$Id:\s+(ntg_\w+\.js)\s+(\d+)\s+', 'ntg_library'),

            # Patrones v/V con números
            (r'\bv\.?\s*(\d+(?:\.\d+)*)\b', 'v_pattern'),
            (r'\bV\.?\s*(\d+(?:\.\d+)*)\b', 'V_pattern'),

            # Versiones con formato x.x.x
            (r'\b(\d+\.\d+\.\d+)\b', 'semver'),
            (r'["\']?(\d+\.\d+\.\d+)["\']?', 'quoted_semver'),
            (r'\s(\d+\.\d+\.\d+)\s', 'spaced_semver'),

            # Patrones version con =
            (r'\bversion\s*=\s*["\']?(\d+\.\d+\.\d+)["\']?', 'version_equals'),
            (r'\bVersion\s*=\s*["\']?(\d+\.\d+\.\d+)["\']?', 'Version_equals'),

            # Patrones version con :
            (r'\bversion\s*:\s*["\']?(\d+\.\d+\.\d+)["\']?', 'version_colon'),
            (r'\bVersion\s*:\s*["\']?(\d+\.\d+\.\d+)["\']?', 'Version_colon'),

            # Patrones adicionales útiles
            (r'/\*.*?v\.?\s*(\d+\.\d+\.\d+).*?\*/', 'comment_version'),
            (r'//.*?v\.?\s*(\d+\.\d+\.\d+)', 'line_comment_version'),
            (r'\brelease[:\s]+["\']?(\d+\.\d+\.\d+)["\']?', 'release'),
            (r'\bbuild[:\s]+["\']?(\d+\.\d+\.\d+)["\']?', 'build'),
            (r'@version\s+(\d+\.\d+\.\d+)', 'jsdoc_version'),
            (r'-(\d+\.\d+\.\d+)\.(?:min\.)?(?:js|css)', 'filename_version'),
            (r'["\']version["\']\s*:\s*["\'](\d+\.\d+\.\d+)["\']', 'json_version'),
        ]

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(file_url, headers=headers, timeout=10)
            if response.status_code == 200:
                content = response.text
                lines = content.split('\n')

                for line_num, line in enumerate(lines, 1):
                    # SOLO LA PRIMERA CADENA DE VERSIÓN POR ARCHIVO
                    if file_url not in first_version_string_per_source:

                        # MANTENER funcionalidad existente para compatibilidad
                        if re.search(r'version', line, re.I):
                            first_version_string_per_source[file_url] = {
                                'scan_id': scan_id,
                                'file_url': file_url,
                                'file_type': file_type,
                                'line_number': line_num,
                                'line_content': line.strip()[:200],
                                'version_keyword': 'version'
                            }
                            continue

                        if re.search(r'versión', line, re.I):
                            first_version_string_per_source[file_url] = {
                                'scan_id': scan_id,
                                'file_url': file_url,
                                'file_type': file_type,
                                'line_number': line_num,
                                'line_content': line.strip()[:200],
                                'version_keyword': 'versión'
                            }
                            continue

                        # NUEVOS PATRONES: Buscar versiones específicas
                        for pattern, pattern_type in VERSION_PATTERNS:
                            matches = re.finditer(pattern, line, re.I)
                            for match in matches:
                                # Manejo especial para bibliotecas NTG
                                if pattern_type == 'ntg_library':
                                    library_filename = match.group(1)  # ntg_*.js
                                    version_number = match.group(2)    # número de versión
                                    library_name = library_filename.replace('.js', '')

                                    # Agregar biblioteca NTG detectada automáticamente
                                    if file_url not in first_library_per_source:
                                        # Verificar si existe en bibliotecas globales para asociar
                                        global_ntg_libs = self.get_ntg_global_libraries()
                                        global_library_id = None
                                        if library_name in global_ntg_libs:
                                            global_library_id = global_ntg_libs[library_name]['id']

                                        first_library_per_source[file_url] = {
                                            'name': library_name,
                                            'version': version_number,
                                            'type': file_type,
                                            'source': file_url,
                                            'detection_method': 'ntg_pattern',
                                            'confidence': 0.9,
                                            'global_library_id': global_library_id
                                        }

                                    # Agregar cadena de versión con información completa
                                    first_version_string_per_source[file_url] = {
                                        'scan_id': scan_id,
                                        'file_url': file_url,
                                        'file_type': file_type,
                                        'line_number': line_num,
                                        'line_content': line.strip()[:200],
                                        'version_keyword': f'{library_name}_v{version_number}'
                                    }
                                else:
                                    # Procesamiento normal para otros patrones
                                    version_number = match.group(1)

                                    # Agregar PRIMERA cadena de versión por archivo
                                    first_version_string_per_source[file_url] = {
                                        'scan_id': scan_id,
                                        'file_url': file_url,
                                        'file_type': file_type,
                                        'line_number': line_num,
                                        'line_content': line.strip()[:200],
                                        'version_keyword': pattern_type
                                    }
                                break  # Solo el primer match por patrón

                            # Si ya encontramos una cadena de versión, salir del bucle de patrones
                            if file_url in first_version_string_per_source:
                                break

                    # Detectar biblioteca automáticamente - SOLO LA PRIMERA POR URL
                    # (omitir bibliotecas NTG ya procesadas arriba)
                    if file_url not in first_library_per_source:
                        for pattern, pattern_type in VERSION_PATTERNS:
                            # Saltar patrón NTG ya procesado
                            if pattern_type == 'ntg_library':
                                continue

                            matches = re.finditer(pattern, line, re.I)
                            for match in matches:
                                version_number = match.group(1)
                                library_name = self._extract_library_name_from_context(line, file_url, version_number)
                                if library_name:
                                    first_library_per_source[file_url] = {
                                        'name': library_name,
                                        'version': version_number,
                                        'type': file_type,
                                        'source': file_url,
                                        'detection_method': 'version_pattern',
                                        'confidence': 0.6
                                    }
                                    break
                            if file_url in first_library_per_source:
                                break

        except Exception as e:
            print(f"  ✗ Error scanning {file_url}: {str(e)}")

        # 🆕 POST-PROCESAMIENTO NTG: Buscar bibliotecas NTG en archivos sin biblioteca detectada
        if content and file_url not in first_library_per_source:
            ntg_library = self.post_process_ntg_libraries(file_url, file_type, scan_id, content, first_library_per_source)
            if ntg_library:
                first_library_per_source[file_url] = ntg_library

        # 🚀 NUEVA DETECCIÓN POR CONTENIDO: Análisis inteligente del código fuente
        if CONTENT_DETECTION_AVAILABLE and content and file_url not in first_library_per_source:
            content_detections = self._detect_libraries_by_content_analysis(
                content, file_type, file_url, scan_id, first_version_string_per_source
            )
            if content_detections:
                # Tomar la detección con mayor confianza
                best_detection = max(content_detections, key=lambda x: x['confidence'])
                first_library_per_source[file_url] = best_detection

        # Convertir diccionarios a listas - solo UNA entrada por archivo fuente
        version_strings = list(first_version_string_per_source.values())
        detected_libraries = list(first_library_per_source.values())
        return version_strings, detected_libraries

    def _extract_library_name_from_context(self, line, file_url, version):
        """
        Intenta extraer el nombre de la biblioteca del contexto
        """
        line_lower = line.lower()
        url_lower = file_url.lower()

        # Bibliotecas conocidas en comentarios/líneas
        LIBRARY_PATTERNS = [
            ('jquery', 'jQuery'),
            ('bootstrap', 'Bootstrap'),
            ('react', 'React'),
            ('vue', 'Vue.js'),
            ('angular', 'Angular'),
            ('lodash', 'Lodash'),
            ('moment', 'Moment.js'),
            ('chart', 'Chart.js'),
            ('d3', 'D3.js'),
            ('three', 'Three.js'),
            ('axios', 'Axios'),
            ('underscore', 'Underscore.js'),
            ('backbone', 'Backbone.js'),
            ('ember', 'Ember.js'),
            ('knockout', 'Knockout.js'),
            ('handlebars', 'Handlebars.js'),
            ('mustache', 'Mustache.js'),
            ('font-awesome', 'Font Awesome'),
            ('fontawesome', 'Font Awesome'),
            ('material', 'Material UI'),
            ('semantic', 'Semantic UI'),
            ('foundation', 'Foundation'),
            ('bulma', 'Bulma'),
            ('tailwind', 'Tailwind CSS'),
        ]

        # Buscar en la línea
        for pattern, name in LIBRARY_PATTERNS:
            if pattern in line_lower or pattern in url_lower:
                return name

        # Buscar en la URL del archivo
        filename = file_url.split('/')[-1].lower()
        for pattern, name in LIBRARY_PATTERNS:
            if pattern in filename:
                return name

        # Si no se encuentra, retornar nombre genérico
        return f"Biblioteca desconocida ({filename.split('.')[0]})" if '.' in filename else "Biblioteca desconocida"

    def get_all_js_files(self, soup, base_url):
        """Get all JavaScript files from the page (CSS files excluded)"""
        files = []

        # Get all script files
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script.get('src')
            if src:
                full_url = urljoin(base_url, src)
                files.append({'url': full_url, 'type': 'js'})

        return files

    def store_file_urls_with_info(self, files, scan_id, cursor):
        """Store file URLs using an existing cursor/connection"""
        for file_info in files:
            file_url = file_info['url']
            file_type = file_info['type']

            # Try to get file information
            file_size = None
            status_code = None

            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }

                # Make a HEAD request to get file info without downloading content
                response = requests.head(file_url, headers=headers, timeout=3, allow_redirects=True)
                status_code = response.status_code

                # Get file size from headers if available
                content_length = response.headers.get('content-length')
                if content_length:
                    file_size = int(content_length)

            except Exception as e:
                print(f"  ! Could not get info for {file_url}: {str(e)}")
                status_code = 0

            # Store file URL information
            cursor.execute('''
            INSERT INTO file_urls (scan_id, file_url, file_type, file_size, status_code)
            VALUES (?, ?, ?, ?, ?)
            ''', (scan_id, file_url, file_type, file_size, status_code))

    def library_source_exists(self, cursor, scan_id, source_url):
        """
        Verificar si ya existe una biblioteca con la misma source_url para este scan
        Retorna True si existe, False si no existe
        """
        if not source_url or source_url.strip() == '':
            return False
        
        result = cursor.execute(
            'SELECT id FROM libraries WHERE scan_id = ? AND source_url = ?', 
            (scan_id, source_url.strip())
        ).fetchone()
        return result is not None

    def is_safe_url(self, url):
        """
        Checks if a URL is safe to request. Prevents SSRF attacks.
        """
        try:
            parsed_url = urlparse(url)

            # 1. Disallow non-http/https protocols
            if parsed_url.scheme not in ['http', 'https']:
                return False, "Invalid protocol. Only HTTP and HTTPS are allowed."

            # 2. Disallow requests to IP addresses
            hostname = parsed_url.hostname
            if not hostname:
                return False, "Hostname could not be determined."

            try:
                ip = ipaddress.ip_address(hostname)
                # 3. Block private, reserved, and loopback addresses
                if ip.is_private or ip.is_reserved or ip.is_loopback or ip.is_link_local:
                    return False, f"Request to internal or reserved IP address ({hostname}) is forbidden."
            except ValueError:
                # This is expected for valid hostnames, so we pass
                pass

            # 4. Check for the metadata service IP
            if hostname == '169.254.169.254':
                return False, "Request to cloud metadata service is forbidden."

            return True, "URL is safe."

        except Exception as e:
            return False, f"URL validation failed: {str(e)}"

    def analyze_url(self, url):
        conn = None
        try:
            is_safe, message = self.is_safe_url(url)
            if not is_safe:
                raise Exception(message)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Get page title
            title_tag = soup.find('title')
            title = title_tag.text.strip() if title_tag else 'No title'

            # Store scan info with improved connection handling
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            # Simple configuration for stability
            conn.execute('PRAGMA journal_mode=DELETE')
            conn.execute('PRAGMA synchronous=FULL')
            conn.execute('PRAGMA temp_store=memory')
            conn.execute('PRAGMA busy_timeout=30000')
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO scans (url, status_code, title, headers, project_id, reviewed)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (url, response.status_code, title, json.dumps(dict(response.headers)), None, 0))

            scan_id = cursor.lastrowid

            # Detect libraries with contextual enhancement (JavaScript only)
            js_libraries = self.detect_js_libraries(soup, url)

            all_libraries = js_libraries

            # Apply contextual detection enhancement
            if ADVANCED_DETECTION_AVAILABLE:
                all_libraries = self._enhance_with_contextual_detection(all_libraries, url, soup)

            # Store libraries (only if source_url is unique) with vulnerability analysis
            for lib in all_libraries:
                source_url = lib.get('source')
                if not self.library_source_exists(cursor, scan_id, source_url):
                    
                    cursor.execute('''
                    INSERT INTO libraries (scan_id, library_name, version, type, source_url, global_library_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (scan_id, lib['name'], lib['version'], lib['type'], source_url,
                          lib.get('global_library_id')))
                    
                    print(f"  → Stored library: {lib['name']} v{lib['version']}")
                else:
                    print(f"  → Skipped duplicate library: {lib['name']} (source already exists: {source_url})")

            # 🌐 ANÁLISIS CDN: Detectar dependencias de CDN y recomendaciones
            if CDN_ANALYZER_AVAILABLE:
                cdn_analysis = self._analyze_cdn_dependencies(all_libraries)
                if cdn_analysis['cdn_libraries']:
                    print(f"  🌐 CDN Analysis: {len(cdn_analysis['cdn_libraries'])} libraries from CDN")
                    if cdn_analysis['outdated_count'] > 0:
                        print(f"    ⚠️ {cdn_analysis['outdated_count']} outdated CDN libraries detected")

            # Get all JavaScript files
            js_files = self.get_all_js_files(soup, url)

            print(f"  → Found {len(js_files)} JavaScript files")

            # Store all file URLs with additional info using the same connection
            print(f"  → Storing file URLs and getting file information...")
            self.store_file_urls_with_info(js_files, scan_id, cursor)

            # Scan files for version strings and detect libraries
            all_version_strings = []
            all_detected_libraries = []
            print(f"  → Scanning all {len(js_files)} JavaScript files for version strings...")
            for file_info in js_files:
                version_strings, detected_libraries = self.scan_file_for_versions(file_info['url'], file_info['type'], scan_id)
                all_version_strings.extend(version_strings)
                all_detected_libraries.extend(detected_libraries)

            # Store version strings
            for vs in all_version_strings:
                cursor.execute('''
                INSERT INTO version_strings (scan_id, file_url, file_type, line_number, line_content, version_keyword)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (vs['scan_id'], vs['file_url'], vs['file_type'], vs['line_number'], vs['line_content'], vs['version_keyword']))

            # Store automatically detected libraries (only if source_url is unique)
            for lib in all_detected_libraries:
                source_url = lib.get('source')
                if not self.library_source_exists(cursor, scan_id, source_url):
                    cursor.execute('''
                    INSERT INTO libraries (scan_id, library_name, version, type, source_url, description, is_manual, global_library_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (scan_id, lib['name'], lib['version'], lib['type'], source_url,
                          f"Detectada automáticamente por patrón de versión ({lib['detection_method']})", 0,
                          lib.get('global_library_id')))
                    print(f"  → Stored auto-detected library: {lib['name']} from {source_url or 'No source'}")
                else:
                    print(f"  → Skipped duplicate auto-detected library: {lib['name']} (source already exists: {source_url})")

            conn.commit()

            print(f"✓ Analyzed {url} - Found {len(all_libraries)} libraries, {len(js_files)} files, {len(all_version_strings)} version strings, {len(all_detected_libraries)} auto-detected libraries")
            return True

        except Exception as e:
            print(f"✗ Error analyzing {url}: {str(e)}")

            # Store failed scan
            try:
                if not conn:
                    conn = sqlite3.connect(self.db_path, timeout=30.0)
                    conn.execute('PRAGMA journal_mode=DELETE')
                    conn.execute('PRAGMA synchronous=FULL')
                    conn.execute('PRAGMA busy_timeout=30000')
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO scans (url, status_code, title, headers, project_id, reviewed)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (url, 0, f"Error: {str(e)}", "{}", None, 0))
                conn.commit()
            except:
                pass  # If we can't store the error, just continue

            return False
        finally:
            if conn:
                conn.close()

    def analyze_urls(self, urls, delay=1):
        print(f"Starting analysis of {len(urls)} URLs...")

        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Analyzing: {url}")
            self.analyze_url(url)

            if delay > 0:
                time.sleep(delay)

        print("Analysis completed!")

    def get_ntg_global_libraries(self):
        """
        Obtiene todas las bibliotecas globales que empiecen con 'ntg_'
        Retorna diccionario {nombre_biblioteca: {id, data}}
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Buscar bibliotecas globales que empiecen con 'ntg_'
            ntg_libraries = cursor.execute('''
                SELECT id, library_name, type, latest_safe_version, latest_version, description
                FROM global_libraries
                WHERE library_name LIKE 'ntg_%'
                ORDER BY library_name
            ''').fetchall()

            conn.close()

            # Convertir a diccionario para búsqueda rápida
            result = {}
            for lib in ntg_libraries:
                result[lib['library_name']] = {
                    'id': lib['id'],
                    'name': lib['library_name'],
                    'type': lib['type'],
                    'latest_safe_version': lib['latest_safe_version'],
                    'latest_version': lib['latest_version'],
                    'description': lib['description']
                }

            return result

        except Exception as e:
            print(f"  ✗ Error getting NTG global libraries: {str(e)}")
            return {}

    def search_ntg_hrodrigu_pattern(self, content, file_url):
        """
        Busca patrones 'ntg_*' Y 'hrodrigu' en la misma línea
        Retorna nombre de biblioteca si encuentra coincidencia
        """
        try:
            lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()

                # Buscar línea que contenga AMBOS: ntg_* Y hrodrigu
                if 'hrodrigu' in line_lower and 'ntg_' in line_lower:
                    # Extraer nombre de biblioteca ntg_*
                    ntg_match = re.search(r'ntg_(\w+)', line_lower)
                    if ntg_match:
                        library_name = f"ntg_{ntg_match.group(1)}"
                        print(f"  → Found NTG pattern: {library_name} with hrodrigu at line {line_num}")
                        return library_name

            return None

        except Exception as e:
            print(f"  ✗ Error searching NTG pattern in {file_url}: {str(e)}")
            return None

    def post_process_ntg_libraries(self, file_url, file_type, scan_id, content, first_library_per_source):
        """
        Post-procesa archivos sin biblioteca detectada buscando patrones NTG+hrodrigu
        Retorna biblioteca detectada o None
        """
        try:
            # Solo procesar si no hay biblioteca detectada para este archivo
            if file_url in first_library_per_source:
                return None

            # Buscar patrón NTG+hrodrigu
            ntg_name = self.search_ntg_hrodrigu_pattern(content, file_url)
            if not ntg_name:
                return None

            # Verificar si existe en bibliotecas globales
            global_ntg_libs = self.get_ntg_global_libraries()
            if ntg_name not in global_ntg_libs:
                print(f"  → NTG library '{ntg_name}' not found in global catalog")
                return None

            # Crear biblioteca con asociación global
            global_lib = global_ntg_libs[ntg_name]
            detected_library = {
                'name': ntg_name,
                'version': 'unknown',  # Versión no disponible en este contexto
                'type': file_type,
                'source': file_url,
                'detection_method': 'ntg_hrodrigu_pattern',
                'confidence': 0.8,
                'global_library_id': global_lib['id']
            }

            print(f"  ✓ Auto-associated '{ntg_name}' with global library ID {global_lib['id']}")
            return detected_library

        except Exception as e:
            print(f"  ✗ Error in NTG post-processing for {file_url}: {str(e)}")
            return None

    def _detect_libraries_by_content_analysis(self, content, file_type, file_url, scan_id, version_strings_dict):
        """
        🚀 Nueva función: Detecta librerías mediante análisis inteligente del contenido
        Utiliza firmas de código específicas para identificar librerías con alta precisión
        """
        try:
            # Usar el nuevo motor de detección por contenido
            detections = detect_libraries_by_content(content, file_type)
            
            processed_detections = []
            for detection in detections:
                library_name = detection['library_name']
                version = detection.get('version', 'unknown')
                confidence = detection.get('confidence', 0.8)
                details = detection.get('details', [])
                
                # Crear entrada de librería detectada
                processed_detection = {
                    'name': detection['library_name'].title(),
                    'version': version,
                    'type': file_type,
                    'source': file_url,
                    'detection_method': 'content_analysis',
                    'confidence': confidence,
                    'analysis_details': details,
                    'matches': detection.get('matches', 0)
                }
                
                # Agregar versión string si se detectó versión
                if version != 'unknown' and file_url not in version_strings_dict:
                    version_strings_dict[file_url] = {
                        'scan_id': scan_id,
                        'file_url': file_url,
                        'file_type': file_type,
                        'line_number': 1,  # Línea estimada
                        'line_content': f'Library detected: {library_name} v{version}',
                        'version_keyword': f'{library_name}_content_analysis'
                    }
                
                processed_detections.append(processed_detection)
                
                print(f"  🎯 Content analysis detected: {library_name} v{version} (confidence: {confidence:.1f}, matches: {detection.get('matches', 0)})")
            
            return processed_detections
            
        except Exception as e:
            print(f"  ⚠️ Error in content analysis for {file_url}: {str(e)}")
            return []


    def _analyze_cdn_dependencies(self, libraries: List[Dict]) -> Dict:
        """
        🌐 Analiza dependencias de CDN y genera recomendaciones
        """
        if not CDN_ANALYZER_AVAILABLE:
            return {'cdn_libraries': [], 'outdated_count': 0, 'recommendations': []}
        
        try:
            cdn_libraries = []
            outdated_count = 0
            
            for lib in libraries:
                source_url = lib.get('source', '')
                if source_url:
                    cdn_analysis = analyze_cdn_url(source_url)
                    if cdn_analysis:
                        cdn_libraries.append({
                            **cdn_analysis,
                            'library_info': lib
                        })
                        
                        if cdn_analysis.get('is_outdated', False):
                            outdated_count += 1
                            print(f"    📦 {lib['name']} v{lib['version']} → v{cdn_analysis.get('latest_version', 'unknown')} available")
            
            # Generar recomendaciones
            recommendations = []
            if cdn_libraries:
                stats = get_cdn_recommendations(cdn_libraries)
                recommendations = stats.get('recommendations', [])
            
            return {
                'cdn_libraries': cdn_libraries,
                'outdated_count': outdated_count,
                'recommendations': recommendations,
                'total_cdn_usage': len(cdn_libraries)
            }
            
        except Exception as e:
            print(f"  ⚠️ Error in CDN analysis: {str(e)}")
            return {'cdn_libraries': [], 'outdated_count': 0, 'recommendations': []}

def main():
    analyzer = LibraryAnalyzer()

    # Read URLs from file
    try:
        with open('urls.txt', 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("urls.txt file not found. Creating sample file...")
        sample_urls = [
            "https://getbootstrap.com",
            "https://jquery.com",
            "https://reactjs.org"
        ]
        with open('urls.txt', 'w') as f:
            for url in sample_urls:
                f.write(f"{url}\n")
        urls = sample_urls

    analyzer.analyze_urls(urls)

if __name__ == "__main__":
    main()
