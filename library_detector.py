#!/usr/bin/env python3
"""
Sistema avanzado de detección de librerías JavaScript y CSS
Basado en patrones RegEx del js-file-extractor.html
"""
import re
import requests
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Optional

class LibraryDetector:
    
    # Patrones de detección para librerías conocidas
    LIBRARY_PATTERNS = {
        'jquery': {
            'patterns': [
                r'jquery[-.]?(\d+\.\d+\.\d+)',
                r'jquery[-.]?v?(\d+\.\d+)',
                r'jquery[-.]?(\d+)',
                r'jquery[.-]min\.js',
                r'jquery[.-]slim[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.9,
            'aliases': ['jq', '$']
        },
        'bootstrap': {
            'patterns': [
                r'bootstrap[-.]?(\d+\.\d+\.\d+)',
                r'bootstrap[-.]?v?(\d+\.\d+)',
                r'bootstrap[.-]min\.(js|css)',
                r'bootstrap[.-]bundle[.-]min\.js'
            ],
            'type': 'css',  # Puede ser js también
            'confidence_boost': 0.8,
            'aliases': ['bs', 'twbs']
        },
        'd3': {
            'patterns': [
                r'd3[-.]?(\d+\.\d+\.\d+)',
                r'd3[-.]?v?(\d+)',
                r'd3[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.9,
            'aliases': []
        },
        'chart.js': {
            'patterns': [
                r'chart(?:\.js)?[-.]?(\d+\.\d+\.\d+)',
                r'chartjs[-.]?(\d+\.\d+\.\d+)',
                r'chart[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.8,
            'aliases': ['chartjs']
        },
        'lightbox': {
            'patterns': [
                r'lightbox[-.]?(\d+\.\d+\.\d+)',
                r'lightbox[0-9]*[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.7,
            'aliases': ['lightbox2']
        },
        'swiper': {
            'patterns': [
                r'swiper[-.]?(\d+\.\d+\.\d+)',
                r'swiper[.-]bundle[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.8,
            'aliases': []
        },
        'moment': {
            'patterns': [
                r'moment[-.]?(\d+\.\d+\.\d+)',
                r'moment[.-]min\.js',
                r'moment[.-]with[.-]locales[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.8,
            'aliases': []
        },
        'font-awesome': {
            'patterns': [
                r'font-?awesome[-.]?(\d+\.\d+\.\d+)',
                r'fontawesome[-.]?(\d+\.\d+\.\d+)',
                r'fa[-.]?(\d+\.\d+\.\d+)',
                r'all[.-]min\.css'  # Font Awesome specific
            ],
            'type': 'css',
            'confidence_boost': 0.7,
            'aliases': ['fa', 'fontawesome']
        },
        'angular': {
            'patterns': [
                r'angular[-.]?(\d+\.\d+\.\d+)',
                r'angular[.-]min\.js',
                r'@angular/core'
            ],
            'type': 'js',
            'confidence_boost': 0.9,
            'aliases': ['ng']
        },
        'react': {
            'patterns': [
                r'react[-.]?(\d+\.\d+\.\d+)',
                r'react[.-]dom[.-]min\.js',
                r'react[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.9,
            'aliases': []
        },
        'vue': {
            'patterns': [
                r'vue[-.]?(\d+\.\d+\.\d+)',
                r'vue[.-]min\.js',
                r'vuejs[-.]?(\d+\.\d+\.\d+)'
            ],
            'type': 'js',
            'confidence_boost': 0.9,
            'aliases': ['vuejs']
        },
        'lodash': {
            'patterns': [
                r'lodash[-.]?(\d+\.\d+\.\d+)',
                r'lodash[.-]min\.js',
                r'underscore[-.]?(\d+\.\d+\.\d+)'
            ],
            'type': 'js',
            'confidence_boost': 0.8,
            'aliases': ['_', 'underscore']
        },
        'datatables': {
            'patterns': [
                r'(?:jquery\.)?datatables[-.]?(\d+\.\d+\.\d+)',
                r'datatables[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.8,
            'aliases': ['dt']
        },
        'select2': {
            'patterns': [
                r'select2[-.]?(\d+\.\d+\.\d+)',
                r'select2[.-]min\.js'
            ],
            'type': 'js',
            'confidence_boost': 0.8,
            'aliases': []
        }
    }
    
    # Patrones contextuales basados en tipo de página
    CONTEXTUAL_PATTERNS = {
        'estadisticas': ['chart.js', 'd3', 'datatables', 'plotly'],
        'prensa': ['lightbox', 'swiper', 'gallery', 'fancybox'],
        'formularios': ['select2', 'datepicker', 'validation'],
        'admin': ['datatables', 'select2', 'bootstrap', 'jquery'],
        'portal': ['bootstrap', 'jquery', 'font-awesome'],
        'ecommerce': ['swiper', 'select2', 'cart', 'payment'],
        'analytics': ['google-analytics', 'gtag', 'matomo', 'hotjar']
    }

    def __init__(self):
        self.detected_libraries = []

    def detect_from_filename(self, filename: str, file_url: str = None) -> List[Dict]:
        """
        Detectar librerías desde el nombre del archivo
        """
        detections = []
        filename_lower = filename.lower()
        
        for library_name, config in self.LIBRARY_PATTERNS.items():
            for pattern in config['patterns']:
                match = re.search(pattern, filename_lower, re.IGNORECASE)
                if match:
                    version = match.group(1) if match.groups() else 'unknown'
                    
                    # Calcular confianza basada en el patrón
                    confidence = self._calculate_confidence(match, filename, config)
                    
                    detection = {
                        'library_name': library_name,
                        'version': version,
                        'type': config['type'],
                        'confidence': confidence,
                        'detection_method': 'filename_pattern',
                        'matched_pattern': pattern,
                        'source_file': filename,
                        'source_url': file_url
                    }
                    
                    detections.append(detection)
                    break  # Solo el primer patrón que coincida
        
        return detections

    def detect_from_content(self, content: str, file_url: str = None) -> List[Dict]:
        """
        Detectar librerías desde el contenido del archivo
        """
        detections = []
        
        # Patrones para detectar en comentarios y headers
        header_patterns = [
            r'/\*!\s*(.+?)\s+v?(\d+\.\d+\.\d+)',  # /* LibraryName v1.2.3 */
            r'//\s*(.+?)\s+v?(\d+\.\d+\.\d+)',     # // LibraryName v1.2.3
            r'@version\s+(\d+\.\d+\.\d+)',         # @version 1.2.3
            r'@name\s+(.+)',                       # @name LibraryName
        ]
        
        for pattern in header_patterns:
            matches = re.finditer(pattern, content[:2000], re.IGNORECASE)  # Solo los primeros 2KB
            for match in matches:
                lib_info = self._analyze_header_match(match)
                if lib_info:
                    detection = {
                        'library_name': lib_info['name'],
                        'version': lib_info['version'],
                        'type': 'js',  # Asumimos JS para contenido
                        'confidence': 0.9,
                        'detection_method': 'content_header',
                        'matched_pattern': pattern,
                        'source_url': file_url
                    }
                    detections.append(detection)
        
        return detections

    def detect_contextual_libraries(self, url: str) -> List[str]:
        """
        Detectar librerías probables basadas en el contexto de la URL
        """
        url_lower = url.lower()
        probable_libraries = []
        
        for context, libraries in self.CONTEXTUAL_PATTERNS.items():
            if context in url_lower:
                probable_libraries.extend(libraries)
        
        # Siempre incluir librerías básicas comunes
        probable_libraries.extend(['jquery', 'bootstrap', 'font-awesome'])
        
        return list(set(probable_libraries))  # Remover duplicados

    def enhance_detection_with_context(self, detections: List[Dict], url: str) -> List[Dict]:
        """
        Mejorar las detecciones con información contextual
        """
        contextual_libs = self.detect_contextual_libraries(url)
        
        for detection in detections:
            if detection['library_name'] in contextual_libs:
                detection['confidence'] = min(detection['confidence'] + 0.1, 1.0)
                detection['contextual_match'] = True
        
        return detections

    def _calculate_confidence(self, match: re.Match, filename: str, config: Dict) -> float:
        """
        Calcular nivel de confianza de la detección
        """
        confidence = config.get('confidence_boost', 0.5)
        
        # Boost si el nombre del archivo contiene el nombre de la librería exacto
        if config.get('aliases'):
            for alias in config['aliases']:
                if alias.lower() in filename.lower():
                    confidence += 0.1
        
        # Boost si tiene versión específica
        if match.groups() and len(match.group(1).split('.')) == 3:
            confidence += 0.1
        
        # Boost si es archivo minificado
        if '.min.' in filename:
            confidence += 0.05
        
        return min(confidence, 1.0)

    def _analyze_header_match(self, match: re.Match) -> Optional[Dict]:
        """
        Analizar coincidencias en headers de archivos
        """
        groups = match.groups()
        if len(groups) >= 2:
            name = groups[0].strip()
            version = groups[1] if len(groups) > 1 else 'unknown'
            
            # Normalizar nombres conocidos
            name_lower = name.lower()
            for lib_name in self.LIBRARY_PATTERNS.keys():
                if lib_name in name_lower or name_lower in lib_name:
                    return {'name': lib_name, 'version': version}
            
            return {'name': name, 'version': version}
        
        return None

    def compare_versions(self, version1: str, version2: str) -> int:
        """
        Comparar dos versiones semánticas
        Retorna: -1 si version1 < version2, 0 si iguales, 1 si version1 > version2
        """
        if version1 == 'unknown' or version2 == 'unknown':
            return 0
        
        try:
            # Limpiar versiones
            v1_clean = re.sub(r'[^0-9\.]', '', str(version1))
            v2_clean = re.sub(r'[^0-9\.]', '', str(version2))
            
            v1_parts = [int(x) for x in v1_clean.split('.') if x.isdigit()]
            v2_parts = [int(x) for x in v2_clean.split('.') if x.isdigit()]
            
            # Pad con zeros
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            for i in range(max_len):
                if v1_parts[i] < v2_parts[i]:
                    return -1
                elif v1_parts[i] > v2_parts[i]:
                    return 1
            
            return 0
        except:
            return 0

    def get_file_size_estimate(self, file_url: str) -> Optional[int]:
        """
        Obtener tamaño estimado del archivo
        """
        try:
            response = requests.head(file_url, timeout=5)
            content_length = response.headers.get('Content-Length')
            if content_length:
                return int(content_length)
        except:
            pass
        return None

# Función helper para usar en analyzer.py
def detect_libraries_advanced(file_url: str, filename: str = None, content: str = None) -> List[Dict]:
    """
    Función principal para detectar librerías con el sistema avanzado
    """
    detector = LibraryDetector()
    all_detections = []
    
    if not filename:
        filename = file_url.split('/')[-1]
    
    # Detectar desde nombre de archivo
    filename_detections = detector.detect_from_filename(filename, file_url)
    all_detections.extend(filename_detections)
    
    # Detectar desde contenido si está disponible
    if content:
        content_detections = detector.detect_from_content(content, file_url)
        all_detections.extend(content_detections)
    
    # Mejorar con contexto
    all_detections = detector.enhance_detection_with_context(all_detections, file_url)
    
    return all_detections