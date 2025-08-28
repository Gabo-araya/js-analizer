#!/usr/bin/env python3
"""
Sistema avanzado de firmas para detección de librerías JavaScript y CSS
Implementa detección por contenido real de archivos, no solo patrones de URL
"""

import re
from typing import Dict, List, Tuple, Optional

class LibrarySignature:
    """
    Representa una firma única de librería con múltiples patrones de detección
    """
    def __init__(self, name: str, library_type: str, confidence: float = 0.8):
        self.name = name
        self.library_type = library_type  # 'js' or 'css'
        self.confidence = confidence
        self.content_patterns: List[Tuple[str, str]] = []  # (pattern, version_group)
        self.header_patterns: List[str] = []
        self.variable_patterns: List[str] = []
        self.function_patterns: List[str] = []
        self.comment_patterns: List[str] = []

    def add_content_pattern(self, pattern: str, version_group: str = None):
        """Añade patrón de contenido con grupo de captura de versión"""
        self.content_patterns.append((pattern, version_group or 'version'))

    def add_header_pattern(self, pattern: str):
        """Añade patrón para headers/comentarios de archivo"""
        self.header_patterns.append(pattern)

    def add_variable_pattern(self, pattern: str):
        """Añade patrón para variables globales"""
        self.variable_patterns.append(pattern)

    def add_function_pattern(self, pattern: str):
        """Añade patrón para funciones específicas"""
        self.function_patterns.append(pattern)

    def add_comment_pattern(self, pattern: str):
        """Añade patrón para comentarios con versión"""
        self.comment_patterns.append(pattern)


class LibraryDetectionEngine:
    """
    Motor avanzado de detección de librerías por análisis de contenido
    """
    def __init__(self):
        self.signatures: Dict[str, LibrarySignature] = {}
        self._initialize_signatures()

    def _initialize_signatures(self):
        """
        Inicializa las firmas de detección para librerías populares
        """
        
        # =================== LIBRERÍAS JAVASCRIPT ===================
        
        # jQuery
        jquery = LibrarySignature("jQuery", "js", 0.9)
        jquery.add_content_pattern(r'jQuery\.fn\.jquery\s*=\s*["\']([^"\']+)["\']', 'version')
        jquery.add_content_pattern(r'jQuery\s+v(\d+\.\d+\.\d+)', 'version')
        jquery.add_variable_pattern(r'jQuery\.fn\.jquery')
        jquery.add_function_pattern(r'jQuery\s*=\s*function')
        jquery.add_comment_pattern(r'jQuery\s+JavaScript\s+Library\s+v(\d+\.\d+\.\d+)')
        self.signatures['jquery'] = jquery

        # React
        react = LibrarySignature("React", "js", 0.9)
        react.add_content_pattern(r'React\.version\s*=\s*["\']([^"\']+)["\']', 'version')
        react.add_content_pattern(r'ReactVersion\s*=\s*["\']([^"\']+)["\']', 'version')
        react.add_variable_pattern(r'React\.createElement')
        react.add_variable_pattern(r'ReactDOM\.render')
        react.add_function_pattern(r'function\s+React\s*\(')
        react.add_header_pattern(r'React\s+v(\d+\.\d+\.\d+)')
        self.signatures['react'] = react

        # Vue.js
        vue = LibrarySignature("Vue", "js", 0.9)
        vue.add_content_pattern(r'Vue\.version\s*=\s*["\']([^"\']+)["\']', 'version')
        vue.add_content_pattern(r'version:\s*["\']([^"\']+)["\'].*Vue', 'version')
        vue.add_variable_pattern(r'Vue\.prototype')
        vue.add_variable_pattern(r'Vue\.component')
        vue.add_function_pattern(r'function\s+Vue\s*\(')
        vue.add_comment_pattern(r'Vue\.js\s+v(\d+\.\d+\.\d+)')
        self.signatures['vue'] = vue

        # Angular
        angular = LibrarySignature("Angular", "js", 0.9)
        angular.add_content_pattern(r'angular\.version\s*=\s*\{[^}]*full:\s*["\']([^"\']+)["\']', 'version')
        angular.add_content_pattern(r'AngularJS\s+v(\d+\.\d+\.\d+)', 'version')
        angular.add_variable_pattern(r'angular\.module')
        angular.add_variable_pattern(r'angular\.bootstrap')
        angular.add_function_pattern(r'function\s+angular\s*\(')
        angular.add_comment_pattern(r'AngularJS\s+v(\d+\.\d+\.\d+)')
        self.signatures['angular'] = angular

        # Lodash
        lodash = LibrarySignature("Lodash", "js", 0.9)
        lodash.add_content_pattern(r'_.VERSION\s*=\s*["\']([^"\']+)["\']', 'version')
        lodash.add_content_pattern(r'lodash\.VERSION\s*=\s*["\']([^"\']+)["\']', 'version')
        lodash.add_variable_pattern(r'_\.forEach')
        lodash.add_variable_pattern(r'_\.map')
        lodash.add_function_pattern(r'function\s+_\s*\(')
        lodash.add_comment_pattern(r'Lo-Dash\s+(\d+\.\d+\.\d+)')
        self.signatures['lodash'] = lodash

        # D3.js
        d3 = LibrarySignature("D3", "js", 0.9)
        d3.add_content_pattern(r'd3\.version\s*=\s*["\']([^"\']+)["\']', 'version')
        d3.add_variable_pattern(r'd3\.select')
        d3.add_variable_pattern(r'd3\.selectAll')
        d3.add_function_pattern(r'function\s+d3\s*\(')
        d3.add_comment_pattern(r'D3\.js\s+(\d+\.\d+\.\d+)')
        self.signatures['d3'] = d3

        # Moment.js
        moment = LibrarySignature("Moment", "js", 0.9)
        moment.add_content_pattern(r'moment\.version\s*=\s*["\']([^"\']+)["\']', 'version')
        moment.add_content_pattern(r'Moment\.js\s+(\d+\.\d+\.\d+)', 'version')
        moment.add_variable_pattern(r'moment\(\)')
        moment.add_function_pattern(r'function\s+moment\s*\(')
        moment.add_comment_pattern(r'Moment\.js\s+(\d+\.\d+\.\d+)')
        self.signatures['moment'] = moment

        # Bootstrap JS
        bootstrap = LibrarySignature("Bootstrap", "js", 0.8)
        bootstrap.add_content_pattern(r'Bootstrap\s+v(\d+\.\d+\.\d+)', 'version')
        bootstrap.add_content_pattern(r'bootstrap\.js\s+v(\d+\.\d+\.\d+)', 'version')
        bootstrap.add_variable_pattern(r'\$\.fn\.modal')
        bootstrap.add_variable_pattern(r'\$\.fn\.dropdown')
        bootstrap.add_comment_pattern(r'Bootstrap\s+v(\d+\.\d+\.\d+)')
        self.signatures['bootstrap'] = bootstrap

        # Chart.js
        chartjs = LibrarySignature("Chart.js", "js", 0.9)
        chartjs.add_content_pattern(r'Chart\.version\s*=\s*["\']([^"\']+)["\']', 'version')
        chartjs.add_variable_pattern(r'Chart\.Line')
        chartjs.add_variable_pattern(r'Chart\.Bar')
        chartjs.add_function_pattern(r'function\s+Chart\s*\(')
        chartjs.add_comment_pattern(r'Chart\.js\s+(\d+\.\d+\.\d+)')
        self.signatures['chartjs'] = chartjs

        # =================== LIBRERÍAS CSS ===================
        
        # Bootstrap CSS
        bootstrap_css = LibrarySignature("Bootstrap", "css", 0.8)
        bootstrap_css.add_comment_pattern(r'Bootstrap\s+v(\d+\.\d+\.\d+)')
        bootstrap_css.add_content_pattern(r'Bootstrap\s+v(\d+\.\d+\.\d+)', 'version')
        bootstrap_css.add_content_pattern(r'\.container\s*\{[^}]*max-width', None)
        bootstrap_css.add_content_pattern(r'\.row\s*\{[^}]*display:\s*-ms-flexbox', None)
        self.signatures['bootstrap-css'] = bootstrap_css

        # Font Awesome
        fontawesome = LibrarySignature("Font Awesome", "css", 0.8)
        fontawesome.add_comment_pattern(r'Font\s+Awesome\s+(\d+\.\d+\.\d+)')
        fontawesome.add_content_pattern(r'Font\s+Awesome\s+(\d+\.\d+\.\d+)', 'version')
        fontawesome.add_content_pattern(r'\.fa-[a-z-]+:before\s*\{', None)
        fontawesome.add_content_pattern(r'@font-face.*FontAwesome', None)
        self.signatures['fontawesome'] = fontawesome

        # Animate.css
        animate_css = LibrarySignature("Animate.css", "css", 0.8)
        animate_css.add_comment_pattern(r'Animate\.css\s+-\s+v(\d+\.\d+\.\d+)')
        animate_css.add_content_pattern(r'@-webkit-keyframes\s+bounce', None)
        animate_css.add_content_pattern(r'\.animated\s*\{', None)
        self.signatures['animate-css'] = animate_css

        # Normalize.css
        normalize = LibrarySignature("Normalize.css", "css", 0.8)
        normalize.add_comment_pattern(r'normalize\.css\s+v(\d+\.\d+\.\d+)')
        normalize.add_content_pattern(r'normalize\.css\s+v(\d+\.\d+\.\d+)', 'version')
        normalize.add_content_pattern(r'html\s*\{[^}]*line-height:\s*1\.15', None)
        self.signatures['normalize'] = normalize

    def detect_library_in_content(self, content: str, file_type: str) -> List[Dict]:
        """
        Detecta librerías en el contenido de un archivo
        """
        detections = []
        content_lower = content.lower()
        
        # Solo procesar firmas del tipo de archivo correcto
        relevant_signatures = {
            name: sig for name, sig in self.signatures.items() 
            if sig.library_type == file_type
        }

        for lib_name, signature in relevant_signatures.items():
            detection = self._analyze_signature(content, content_lower, signature)
            if detection:
                detection['library_name'] = lib_name
                detection['confidence'] = signature.confidence
                detection['detection_method'] = 'content_analysis'
                detections.append(detection)

        return detections

    def _analyze_signature(self, content: str, content_lower: str, signature: LibrarySignature) -> Optional[Dict]:
        """
        Analiza una firma específica contra el contenido
        """
        matches = 0
        version = None
        detection_details = []

        # Verificar patrones de contenido (con versión)
        for pattern, version_group in signature.content_patterns:
            matches_found = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))
            if matches_found:
                matches += len(matches_found)
                detection_details.append(f"content_pattern: {len(matches_found)} matches")
                
                # Extraer versión si hay grupo de captura
                if version_group and not version:
                    for match in matches_found:
                        try:
                            version = match.group(1)
                            break
                        except (IndexError, AttributeError):
                            continue

        # Verificar patrones de header/comentarios
        for pattern in signature.header_patterns:
            matches_found = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))
            if matches_found:
                matches += len(matches_found)
                detection_details.append(f"header_pattern: {len(matches_found)} matches")
                
                # Extraer versión de headers
                if not version:
                    for match in matches_found:
                        try:
                            version = match.group(1)
                            break
                        except (IndexError, AttributeError):
                            continue

        # Verificar patrones de variables
        for pattern in signature.variable_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                matches += 1
                detection_details.append(f"variable_pattern: {pattern}")

        # Verificar patrones de funciones
        for pattern in signature.function_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                matches += 1
                detection_details.append(f"function_pattern: {pattern}")

        # Verificar patrones de comentarios
        for pattern in signature.comment_patterns:
            matches_found = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))
            if matches_found:
                matches += len(matches_found)
                detection_details.append(f"comment_pattern: {len(matches_found)} matches")
                
                # Extraer versión de comentarios
                if not version:
                    for match in matches_found:
                        try:
                            version = match.group(1)
                            break
                        except (IndexError, AttributeError):
                            continue

        # Considerar detección positiva si hay al menos 2 matches
        if matches >= 2:
            return {
                'version': version or 'unknown',
                'matches': matches,
                'details': detection_details
            }

        return None

    def get_supported_libraries(self) -> List[str]:
        """
        Retorna lista de librerías soportadas por tipo
        """
        return {
            'js': [name for name, sig in self.signatures.items() if sig.library_type == 'js'],
            'css': [name for name, sig in self.signatures.items() if sig.library_type == 'css']
        }


# Instancia global del motor de detección
detection_engine = LibraryDetectionEngine()


def detect_libraries_by_content(file_content: str, file_type: str) -> List[Dict]:
    """
    Función principal para detectar librerías por contenido de archivo
    
    Args:
        file_content: Contenido del archivo JS/CSS
        file_type: Tipo de archivo ('js' o 'css')
        
    Returns:
        Lista de librerías detectadas con metadata
    """
    return detection_engine.detect_library_in_content(file_content, file_type)


def get_library_info(library_name: str) -> Optional[Dict]:
    """
    Obtiene información detallada de una librería soportada
    """
    if library_name in detection_engine.signatures:
        sig = detection_engine.signatures[library_name]
        return {
            'name': sig.name,
            'type': sig.library_type,
            'confidence': sig.confidence,
            'patterns_count': len(sig.content_patterns) + len(sig.header_patterns) + 
                            len(sig.variable_patterns) + len(sig.function_patterns)
        }
    return None