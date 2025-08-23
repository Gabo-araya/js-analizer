# Plan de Implementación: Detección Avanzada de Tecnologías Web

## Resumen Ejecutivo

Este documento presenta un plan detallado paso a paso para expandir significativamente las capacidades de detección de tecnologías web del sistema NTG-JS-Analyzer, evolucionando desde la detección básica actual de bibliotecas JS/CSS hacia un sistema integral de identificación de tecnologías, frameworks, servicios y arquitecturas web.

## Análisis del Estado Actual

### ✅ Implementación Actual
El sistema actual implementa detección básica de bibliotecas mediante:
- **Patrones regex en URLs de scripts**: jQuery, React, Vue.js, Angular
- **Patrones regex en URLs de CSS**: Bootstrap, Font Awesome
- **Análisis limitado**: Solo bibliotecas populares pre-definidas
- **Scope estrecho**: Únicamente JS/CSS libraries

### ⚠️ Limitaciones Identificadas
- **Cobertura limitada**: Solo ~10 bibliotecas detectadas
- **Metodología simple**: Dependiente solo de nombres de archivo
- **Sin contexto arquitectónico**: No identifica frameworks completos, CMS, servers
- **Falta de inteligencia**: No detecta versiones por contenido o comportamiento
- **Sin categorización avanzada**: No clasifica por propósito (analytics, CDN, security)

## Visión del Sistema Expandido

### 🎯 Objetivos de la Expansión

1. **Cobertura Masiva**: Detectar 500+ tecnologías web
2. **Inteligencia Multi-Vector**: Combinar HTML, headers, comportamiento, DNS
3. **Categorización Semántica**: Clasificar por propósito y función
4. **Análisis de Stack Completo**: Identificar arquitecturas y patrones completos
5. **Datos Enriquecidos**: Metadata, versiones, vulnerabilidades, EOL status

### 📊 Categorías de Tecnologías Objetivo

```python
TECHNOLOGY_CATEGORIES = {
    'cms': ['WordPress', 'Drupal', 'Joomla', 'Magento', 'Shopify'],
    'frameworks': ['React', 'Angular', 'Vue.js', 'Laravel', 'Django', 'Rails'],
    'servers': ['Apache', 'Nginx', 'IIS', 'Cloudflare', 'AWS CloudFront'],
    'analytics': ['Google Analytics', 'Adobe Analytics', 'Hotjar', 'Mixpanel'],
    'cdn': ['Cloudflare', 'AWS CloudFront', 'Fastly', 'KeyCDN'],
    'security': ['reCAPTCHA', 'Cloudflare Security', 'Sucuri', 'Wordfence'],
    'advertising': ['Google Ads', 'Facebook Pixel', 'AdSense', 'Criteo'],
    'ecommerce': ['WooCommerce', 'Shopify', 'PrestaShop', 'OpenCart'],
    'hosting': ['AWS', 'Google Cloud', 'Azure', 'Heroku', 'Vercel'],
    'databases': ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis'],
    'languages': ['PHP', 'Python', 'Node.js', 'Java', '.NET'],
    'build_tools': ['Webpack', 'Vite', 'Rollup', 'Parcel'],
    'testing': ['Jest', 'Mocha', 'Cypress', 'Selenium'],
    'monitoring': ['New Relic', 'DataDog', 'Sentry', 'LogRocket']
}
```

## Arquitectura del Sistema Expandido

### 🏗️ Componentes Arquitectónicos

```
┌─────────────────────────────────────────────────────────┐
│                Technology Detection Engine               │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│  │   Analyzer  │ │  Signature  │ │    Intelligence     │ │
│  │  Orchestrator│ │   Engine    │ │     Enricher        │ │
│  └─────────────┘ └─────────────┘ └─────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│  │    HTML     │ │   Headers   │ │      Network        │ │
│  │   Parser    │ │   Analyzer  │ │     Analyzer        │ │
│  └─────────────┘ └─────────────┘ └─────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│  │    DNS      │ │   Content   │ │      Behavior       │ │
│  │  Resolver   │ │   Scanner   │ │     Analyzer        │ │
│  └─────────────┘ └─────────────┘ └─────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Plan de Implementación Detallado

### Fase 1: Fundación y Infraestructura (Semanas 1-2)

#### Paso 1.1: Diseño de Base de Datos Expandida

**Objetivo**: Crear esquema de base de datos para almacenar datos ricos de tecnologías.

**Implementación**:

```sql
-- Nueva tabla para tecnologías detectadas
CREATE TABLE IF NOT EXISTS detected_technologies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL,
    technology_name TEXT NOT NULL,
    category TEXT NOT NULL, -- cms, framework, analytics, etc.
    version TEXT,
    confidence_score REAL DEFAULT 0.0, -- 0.0 to 1.0
    detection_method TEXT, -- 'html_pattern', 'header', 'dns', 'behavior'
    evidence TEXT, -- JSON with detection evidence
    metadata TEXT, -- JSON with additional data
    is_vulnerable BOOLEAN DEFAULT FALSE,
    vulnerability_info TEXT,
    eol_status TEXT, -- 'supported', 'eol', 'unknown'
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES scans (id)
);

-- Tabla de firmas de tecnologías
CREATE TABLE IF NOT EXISTS technology_signatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technology_name TEXT NOT NULL,
    category TEXT NOT NULL,
    signature_type TEXT NOT NULL, -- 'html_pattern', 'header', 'url_pattern'
    pattern TEXT NOT NULL,
    confidence_weight REAL DEFAULT 1.0,
    version_regex TEXT, -- Para extraer versión
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de metadata de tecnologías
CREATE TABLE IF NOT EXISTS technology_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technology_name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    website_url TEXT,
    documentation_url TEXT,
    latest_version TEXT,
    latest_secure_version TEXT,
    eol_date DATE,
    popularity_rank INTEGER,
    security_score REAL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Paso 1.2: Arquitectura de Clases Base

**Implementación**:

```python
# technology_detector.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import re
import json

class DetectionMethod(Enum):
    HTML_PATTERN = "html_pattern"
    HEADER_ANALYSIS = "header"
    URL_PATTERN = "url_pattern"
    DNS_ANALYSIS = "dns"
    CONTENT_ANALYSIS = "content"
    BEHAVIOR_ANALYSIS = "behavior"
    NETWORK_ANALYSIS = "network"

class TechnologyCategory(Enum):
    CMS = "cms"
    FRAMEWORK = "framework"
    ANALYTICS = "analytics"
    CDN = "cdn"
    SERVER = "server"
    SECURITY = "security"
    ADVERTISING = "advertising"
    ECOMMERCE = "ecommerce"
    HOSTING = "hosting"
    DATABASE = "database"
    LANGUAGE = "language"
    BUILD_TOOL = "build_tool"
    TESTING = "testing"
    MONITORING = "monitoring"

@dataclass
class TechnologyDetection:
    name: str
    category: TechnologyCategory
    version: Optional[str] = None
    confidence: float = 0.0
    detection_method: DetectionMethod = DetectionMethod.HTML_PATTERN
    evidence: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.evidence is None:
            self.evidence = {}
        if self.metadata is None:
            self.metadata = {}

class BaseTechnologyDetector(ABC):
    """Clase base abstracta para detectores de tecnología"""
    
    def __init__(self):
        self.signatures = self.load_signatures()
        
    @abstractmethod
    def detect(self, data: Dict[str, Any]) -> List[TechnologyDetection]:
        """Detecta tecnologías en los datos proporcionados"""
        pass
    
    @abstractmethod 
    def load_signatures(self) -> List[Dict[str, Any]]:
        """Carga firmas de detección específicas del detector"""
        pass

class TechnologyDetectionEngine:
    """Motor principal de detección de tecnologías"""
    
    def __init__(self):
        self.detectors = self._initialize_detectors()
        self.confidence_threshold = 0.3
        
    def _initialize_detectors(self) -> List[BaseTechnologyDetector]:
        """Inicializa todos los detectores disponibles"""
        return [
            HTMLPatternDetector(),
            HeaderAnalysisDetector(),
            ContentAnalysisDetector(),
            DNSAnalysisDetector(),
            NetworkAnalysisDetector()
        ]
    
    async def analyze_website(self, scan_data: Dict[str, Any]) -> List[TechnologyDetection]:
        """Análisis integral de tecnologías en un sitio web"""
        all_detections = []
        
        # Ejecutar todos los detectores
        for detector in self.detectors:
            try:
                detections = await detector.detect(scan_data)
                all_detections.extend(detections)
            except Exception as e:
                print(f"Error in detector {detector.__class__.__name__}: {str(e)}")
        
        # Consolidar y filtrar detecciones
        consolidated = self._consolidate_detections(all_detections)
        filtered = self._filter_by_confidence(consolidated)
        enriched = await self._enrich_with_metadata(filtered)
        
        return enriched
    
    def _consolidate_detections(self, detections: List[TechnologyDetection]) -> List[TechnologyDetection]:
        """Consolida detecciones duplicadas y mejora confidence scores"""
        consolidated = {}
        
        for detection in detections:
            key = f"{detection.name}:{detection.category.value}"
            
            if key in consolidated:
                # Combinar evidencia y mejorar confidence
                existing = consolidated[key]
                existing.confidence = max(existing.confidence, detection.confidence)
                existing.evidence.update(detection.evidence)
                
                # Preferir versión más específica
                if detection.version and (not existing.version or len(detection.version) > len(existing.version)):
                    existing.version = detection.version
            else:
                consolidated[key] = detection
                
        return list(consolidated.values())
    
    def _filter_by_confidence(self, detections: List[TechnologyDetection]) -> List[TechnologyDetection]:
        """Filtra detecciones por umbral de confianza"""
        return [d for d in detections if d.confidence >= self.confidence_threshold]
    
    async def _enrich_with_metadata(self, detections: List[TechnologyDetection]) -> List[TechnologyDetection]:
        """Enriquece detecciones con metadata adicional"""
        enriched = []
        
        for detection in detections:
            # Buscar metadata en base de datos
            metadata = await self._get_technology_metadata(detection.name)
            if metadata:
                detection.metadata.update(metadata)
                
            # Verificar vulnerabilidades
            vulnerabilities = await self._check_vulnerabilities(detection.name, detection.version)
            if vulnerabilities:
                detection.metadata['vulnerabilities'] = vulnerabilities
                
            enriched.append(detection)
            
        return enriched
```

### Fase 2: Detectores Especializados (Semanas 3-4)

#### Paso 2.1: Detector de Patrones HTML

**Implementación**:

```python
class HTMLPatternDetector(BaseTechnologyDetector):
    """Detecta tecnologías mediante análisis de patrones HTML"""
    
    def load_signatures(self) -> List[Dict[str, Any]]:
        return [
            # CMS Detection
            {
                'name': 'WordPress',
                'category': TechnologyCategory.CMS,
                'patterns': [
                    r'/wp-content/',
                    r'/wp-includes/',
                    r'<meta name="generator" content="WordPress ([^"]*)"',
                ],
                'version_patterns': [
                    r'WordPress ([0-9.]+)',
                    r'/wp-includes/js/jquery/jquery\.js\?ver=([0-9.]+)',
                ],
                'confidence_base': 0.9
            },
            {
                'name': 'Drupal',
                'category': TechnologyCategory.CMS,
                'patterns': [
                    r'Drupal\.settings',
                    r'/sites/default/files/',
                    r'<meta name="Generator" content="Drupal ([^"]*)"',
                ],
                'version_patterns': [
                    r'Drupal ([0-9.]+)',
                ],
                'confidence_base': 0.9
            },
            
            # Framework Detection  
            {
                'name': 'React',
                'category': TechnologyCategory.FRAMEWORK,
                'patterns': [
                    r'react\.js',
                    r'react\.min\.js',
                    r'data-reactroot',
                    r'__REACT_DEVTOOLS_GLOBAL_HOOK__',
                ],
                'version_patterns': [
                    r'react@([0-9.]+)',
                    r'react\.js\?v=([0-9.]+)',
                ],
                'confidence_base': 0.8
            },
            {
                'name': 'Angular',
                'category': TechnologyCategory.FRAMEWORK,
                'patterns': [
                    r'ng-app',
                    r'ng-controller',
                    r'angular\.js',
                    r'angular\.min\.js',
                ],
                'version_patterns': [
                    r'angular@([0-9.]+)',
                    r'angular\.js\?v=([0-9.]+)',
                ],
                'confidence_base': 0.8
            },
            
            # Analytics Detection
            {
                'name': 'Google Analytics',
                'category': TechnologyCategory.ANALYTICS,
                'patterns': [
                    r'google-analytics\.com/analytics\.js',
                    r'gtag\(',
                    r'ga\(',
                    r'GoogleAnalyticsObject',
                ],
                'version_patterns': [],
                'confidence_base': 0.95
            },
            
            # CDN Detection
            {
                'name': 'Cloudflare',
                'category': TechnologyCategory.CDN,
                'patterns': [
                    r'cloudflare\.com',
                    r'cf-ray',
                    r'__cf_bm',
                ],
                'version_patterns': [],
                'confidence_base': 0.85
            }
        ]
    
    async def detect(self, data: Dict[str, Any]) -> List[TechnologyDetection]:
        """Detecta tecnologías mediante patrones HTML"""
        detections = []
        html_content = data.get('html_content', '')
        
        if not html_content:
            return detections
            
        for signature in self.signatures:
            detection = self._analyze_signature(html_content, signature)
            if detection:
                detections.append(detection)
                
        return detections
    
    def _analyze_signature(self, html: str, signature: Dict[str, Any]) -> Optional[TechnologyDetection]:
        """Analiza una firma específica contra el HTML"""
        matches = 0
        evidence = {}
        version = None
        
        # Verificar patrones principales
        for pattern in signature['patterns']:
            if re.search(pattern, html, re.IGNORECASE):
                matches += 1
                evidence[f'pattern_{len(evidence)}'] = pattern
        
        if matches == 0:
            return None
            
        # Extraer versión si es posible
        for version_pattern in signature.get('version_patterns', []):
            match = re.search(version_pattern, html, re.IGNORECASE)
            if match:
                version = match.group(1)
                evidence['version_source'] = version_pattern
                break
        
        # Calcular confidence basado en coincidencias
        base_confidence = signature.get('confidence_base', 0.5)
        pattern_confidence = min(1.0, matches / len(signature['patterns']))
        final_confidence = base_confidence * pattern_confidence
        
        return TechnologyDetection(
            name=signature['name'],
            category=signature['category'],
            version=version,
            confidence=final_confidence,
            detection_method=DetectionMethod.HTML_PATTERN,
            evidence=evidence
        )
```

#### Paso 2.2: Detector de Headers HTTP

**Implementación**:

```python
class HeaderAnalysisDetector(BaseTechnologyDetector):
    """Detecta tecnologías mediante análisis de headers HTTP"""
    
    def load_signatures(self) -> List[Dict[str, Any]]:
        return [
            # Servers
            {
                'name': 'Apache',
                'category': TechnologyCategory.SERVER,
                'headers': {
                    'server': [r'Apache/([0-9.]+)', r'Apache'],
                },
                'confidence_base': 0.95
            },
            {
                'name': 'Nginx',
                'category': TechnologyCategory.SERVER,
                'headers': {
                    'server': [r'nginx/([0-9.]+)', r'nginx'],
                },
                'confidence_base': 0.95
            },
            {
                'name': 'IIS',
                'category': TechnologyCategory.SERVER,
                'headers': {
                    'server': [r'Microsoft-IIS/([0-9.]+)', r'IIS'],
                },
                'confidence_base': 0.95
            },
            
            # CDN/Cloud Services
            {
                'name': 'Cloudflare',
                'category': TechnologyCategory.CDN,
                'headers': {
                    'server': [r'cloudflare'],
                    'cf-ray': [r'.*'],
                    'cf-cache-status': [r'.*'],
                },
                'confidence_base': 0.9
            },
            {
                'name': 'AWS CloudFront',
                'category': TechnologyCategory.CDN,
                'headers': {
                    'server': [r'CloudFront'],
                    'x-amz-cf-id': [r'.*'],
                    'x-amz-cf-pop': [r'.*'],
                },
                'confidence_base': 0.9
            },
            
            # Frameworks/Languages
            {
                'name': 'PHP',
                'category': TechnologyCategory.LANGUAGE,
                'headers': {
                    'x-powered-by': [r'PHP/([0-9.]+)', r'PHP'],
                    'server': [r'PHP/([0-9.]+)'],
                },
                'confidence_base': 0.85
            },
            {
                'name': 'ASP.NET',
                'category': TechnologyCategory.FRAMEWORK,
                'headers': {
                    'x-powered-by': [r'ASP\.NET'],
                    'x-aspnet-version': [r'([0-9.]+)'],
                },
                'confidence_base': 0.9
            }
        ]
    
    async def detect(self, data: Dict[str, Any]) -> List[TechnologyDetection]:
        """Detecta tecnologías mediante headers HTTP"""
        detections = []
        headers = data.get('headers', {})
        
        if not headers:
            return detections
            
        # Normalizar headers a lowercase
        normalized_headers = {k.lower(): v for k, v in headers.items()}
        
        for signature in self.signatures:
            detection = self._analyze_header_signature(normalized_headers, signature)
            if detection:
                detections.append(detection)
                
        return detections
    
    def _analyze_header_signature(self, headers: Dict[str, str], signature: Dict[str, Any]) -> Optional[TechnologyDetection]:
        """Analiza firma de headers específica"""
        matches = 0
        evidence = {}
        version = None
        total_patterns = 0
        
        for header_name, patterns in signature['headers'].items():
            total_patterns += len(patterns)
            header_value = headers.get(header_name, '')
            
            for pattern in patterns:
                match = re.search(pattern, header_value, re.IGNORECASE)
                if match:
                    matches += 1
                    evidence[f'{header_name}_match'] = {
                        'pattern': pattern,
                        'value': header_value
                    }
                    
                    # Intentar extraer versión
                    if match.groups() and not version:
                        version = match.group(1)
        
        if matches == 0:
            return None
        
        # Calcular confidence
        base_confidence = signature.get('confidence_base', 0.5)
        pattern_confidence = matches / total_patterns
        final_confidence = base_confidence * pattern_confidence
        
        return TechnologyDetection(
            name=signature['name'],
            category=signature['category'],
            version=version,
            confidence=final_confidence,
            detection_method=DetectionMethod.HEADER_ANALYSIS,
            evidence=evidence
        )
```

### Fase 3: Detectores Avanzados (Semanas 5-6)

#### Paso 3.1: Detector de Análisis de Contenido

**Implementación**:

```python
class ContentAnalysisDetector(BaseTechnologyDetector):
    """Detecta tecnologías mediante análisis profundo de contenido"""
    
    def load_signatures(self) -> List[Dict[str, Any]]:
        return [
            # JavaScript Framework Footprints
            {
                'name': 'Vue.js',
                'category': TechnologyCategory.FRAMEWORK,
                'content_patterns': [
                    r'Vue\.createApp\(',
                    r'new Vue\(',
                    r'v-if=',
                    r'v-for=',
                    r'@click=',
                ],
                'js_variables': ['Vue', '__VUE__'],
                'confidence_base': 0.8
            },
            {
                'name': 'Next.js',
                'category': TechnologyCategory.FRAMEWORK,
                'content_patterns': [
                    r'__NEXT_DATA__',
                    r'_next/static/',
                    r'next/router',
                ],
                'meta_tags': [
                    ('generator', 'Next.js'),
                ],
                'confidence_base': 0.9
            },
            
            # E-commerce Platforms
            {
                'name': 'Shopify',
                'category': TechnologyCategory.ECOMMERCE,
                'content_patterns': [
                    r'Shopify\.theme',
                    r'shop\.myshopify\.com',
                    r'/apps/shopify/',
                ],
                'meta_tags': [
                    ('generator', 'Shopify'),
                ],
                'confidence_base': 0.95
            },
            {
                'name': 'WooCommerce',
                'category': TechnologyCategory.ECOMMERCE,
                'content_patterns': [
                    r'woocommerce',
                    r'wp-content/plugins/woocommerce',
                    r'wc-ajax',
                ],
                'confidence_base': 0.9
            },
            
            # Analytics and Tracking
            {
                'name': 'Facebook Pixel',
                'category': TechnologyCategory.ANALYTICS,
                'content_patterns': [
                    r'fbevents\.js',
                    r'fbq\(',
                    r'facebook\.com/tr',
                ],
                'confidence_base': 0.95
            },
            {
                'name': 'Hotjar',
                'category': TechnologyCategory.ANALYTICS,
                'content_patterns': [
                    r'hotjar\.com',
                    r'hj\(',
                    r'_hjSettings',
                ],
                'confidence_base': 0.95
            }
        ]
    
    async def detect(self, data: Dict[str, Any]) -> List[TechnologyDetection]:
        """Detecta tecnologías mediante análisis de contenido"""
        detections = []
        html_content = data.get('html_content', '')
        js_files = data.get('js_files', [])
        
        for signature in self.signatures:
            detection = await self._analyze_content_signature(
                html_content, js_files, signature
            )
            if detection:
                detections.append(detection)
                
        return detections
    
    async def _analyze_content_signature(
        self, 
        html: str, 
        js_files: List[str], 
        signature: Dict[str, Any]
    ) -> Optional[TechnologyDetection]:
        """Analiza firma de contenido específica"""
        matches = 0
        total_checks = 0
        evidence = {}
        version = None
        
        # Verificar patrones en HTML
        content_patterns = signature.get('content_patterns', [])
        total_checks += len(content_patterns)
        
        for pattern in content_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                matches += 1
                evidence[f'html_pattern_{len(evidence)}'] = pattern
        
        # Verificar meta tags
        meta_tags = signature.get('meta_tags', [])
        total_checks += len(meta_tags)
        
        for name, expected_value in meta_tags:
            pattern = rf'<meta name="{name}" content="[^"]*{expected_value}[^"]*"'
            if re.search(pattern, html, re.IGNORECASE):
                matches += 1
                evidence[f'meta_tag_{name}'] = expected_value
        
        # Verificar variables JavaScript
        js_variables = signature.get('js_variables', [])
        total_checks += len(js_variables)
        
        for var_name in js_variables:
            pattern = rf'\b{var_name}\s*[=:]'
            if re.search(pattern, html, re.IGNORECASE):
                matches += 1
                evidence[f'js_var_{var_name}'] = True
        
        # Análisis de archivos JS adicionales
        for js_content in js_files[:5]:  # Limitar análisis a primeros 5 archivos
            for pattern in content_patterns:
                if re.search(pattern, js_content, re.IGNORECASE):
                    matches += 1
                    evidence[f'js_file_pattern_{len(evidence)}'] = pattern
        
        if matches == 0 or total_checks == 0:
            return None
        
        # Calcular confidence
        base_confidence = signature.get('confidence_base', 0.5)
        pattern_confidence = min(1.0, matches / total_checks)
        final_confidence = base_confidence * pattern_confidence
        
        return TechnologyDetection(
            name=signature['name'],
            category=signature['category'],
            version=version,
            confidence=final_confidence,
            detection_method=DetectionMethod.CONTENT_ANALYSIS,
            evidence=evidence
        )
```

#### Paso 3.2: Detector DNS y Network

**Implementación**:

```python
import dns.resolver
import socket
import ssl
from urllib.parse import urlparse

class DNSAnalysisDetector(BaseTechnologyDetector):
    """Detecta tecnologías mediante análisis DNS y certificados"""
    
    def load_signatures(self) -> List[Dict[str, Any]]:
        return [
            # Hosting Providers
            {
                'name': 'AWS',
                'category': TechnologyCategory.HOSTING,
                'dns_patterns': [
                    r'amazonaws\.com',
                    r'aws\.amazon\.com',
                    r'compute-\d+\.amazonaws\.com',
                ],
                'confidence_base': 0.9
            },
            {
                'name': 'Google Cloud',
                'category': TechnologyCategory.HOSTING,
                'dns_patterns': [
                    r'googleusercontent\.com',
                    r'googleapis\.com',
                    r'gcp\.goog',
                ],
                'confidence_base': 0.9
            },
            {
                'name': 'Cloudflare',
                'category': TechnologyCategory.CDN,
                'dns_patterns': [
                    r'cloudflare\.com',
                ],
                'nameserver_patterns': [
                    r'cloudflare\.com',
                ],
                'confidence_base': 0.95
            },
            
            # CDN Services
            {
                'name': 'Fastly',
                'category': TechnologyCategory.CDN,
                'dns_patterns': [
                    r'fastly\.com',
                    r'fastlylb\.net',
                ],
                'confidence_base': 0.9
            }
        ]
    
    async def detect(self, data: Dict[str, Any]) -> List[TechnologyDetection]:
        """Detecta tecnologías mediante análisis DNS"""
        detections = []
        url = data.get('url', '')
        
        if not url:
            return detections
            
        parsed = urlparse(url)
        domain = parsed.hostname
        
        if not domain:
            return detections
        
        # Análisis DNS
        dns_data = await self._analyze_dns(domain)
        
        # Análisis de certificado SSL
        ssl_data = await self._analyze_ssl_certificate(domain, parsed.port or 443)
        
        # Combinar datos
        analysis_data = {
            'dns': dns_data,
            'ssl': ssl_data
        }
        
        for signature in self.signatures:
            detection = self._analyze_dns_signature(analysis_data, signature)
            if detection:
                detections.append(detection)
                
        return detections
    
    async def _analyze_dns(self, domain: str) -> Dict[str, Any]:
        """Analiza registros DNS del dominio"""
        dns_data = {
            'a_records': [],
            'cname_records': [],
            'mx_records': [],
            'txt_records': [],
            'nameservers': []
        }
        
        try:
            # A Records
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                dns_data['a_records'] = [str(record) for record in a_records]
            except:
                pass
            
            # CNAME Records  
            try:
                cname_records = dns.resolver.resolve(domain, 'CNAME')
                dns_data['cname_records'] = [str(record) for record in cname_records]
            except:
                pass
            
            # MX Records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                dns_data['mx_records'] = [str(record) for record in mx_records]
            except:
                pass
            
            # TXT Records
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                dns_data['txt_records'] = [str(record) for record in txt_records]
            except:
                pass
            
            # Nameservers
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                dns_data['nameservers'] = [str(record) for record in ns_records]
            except:
                pass
                
        except Exception as e:
            dns_data['error'] = str(e)
        
        return dns_data
    
    async def _analyze_ssl_certificate(self, domain: str, port: int = 443) -> Dict[str, Any]:
        """Analiza certificado SSL del dominio"""
        ssl_data = {}
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    ssl_data.update({
                        'issuer': dict(x[0] for x in cert.get('issuer', [])),
                        'subject': dict(x[0] for x in cert.get('subject', [])),
                        'version': cert.get('version'),
                        'serial_number': cert.get('serialNumber'),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter'),
                        'san': cert.get('subjectAltName', [])
                    })
                    
        except Exception as e:
            ssl_data['error'] = str(e)
        
        return ssl_data
    
    def _analyze_dns_signature(self, analysis_data: Dict[str, Any], signature: Dict[str, Any]) -> Optional[TechnologyDetection]:
        """Analiza firma DNS específica"""
        matches = 0
        evidence = {}
        total_checks = 0
        
        dns_data = analysis_data.get('dns', {})
        
        # Verificar patrones DNS
        dns_patterns = signature.get('dns_patterns', [])
        total_checks += len(dns_patterns) if dns_patterns else 0
        
        for pattern in dns_patterns:
            # Buscar en todos los tipos de registros DNS
            all_records = (
                dns_data.get('a_records', []) +
                dns_data.get('cname_records', []) +
                dns_data.get('mx_records', []) +
                dns_data.get('txt_records', [])
            )
            
            for record in all_records:
                if re.search(pattern, str(record), re.IGNORECASE):
                    matches += 1
                    evidence[f'dns_pattern_{len(evidence)}'] = {
                        'pattern': pattern,
                        'record': str(record)
                    }
                    break
        
        # Verificar nameservers
        ns_patterns = signature.get('nameserver_patterns', [])
        total_checks += len(ns_patterns) if ns_patterns else 0
        
        for pattern in ns_patterns:
            for ns in dns_data.get('nameservers', []):
                if re.search(pattern, str(ns), re.IGNORECASE):
                    matches += 1
                    evidence[f'ns_pattern_{len(evidence)}'] = {
                        'pattern': pattern,
                        'nameserver': str(ns)
                    }
                    break
        
        if matches == 0 or total_checks == 0:
            return None
        
        # Calcular confidence
        base_confidence = signature.get('confidence_base', 0.5)
        pattern_confidence = matches / total_checks
        final_confidence = base_confidence * pattern_confidence
        
        return TechnologyDetection(
            name=signature['name'],
            category=signature['category'],
            confidence=final_confidence,
            detection_method=DetectionMethod.DNS_ANALYSIS,
            evidence=evidence
        )
```

### Fase 4: Inteligencia y Enriquecimiento (Semanas 7-8)

#### Paso 4.1: Sistema de Enriquecimiento de Datos

**Implementación**:

```python
class TechnologyIntelligenceEnricher:
    """Sistema de enriquecimiento de inteligencia de tecnologías"""
    
    def __init__(self):
        self.vulnerability_sources = [
            CVEDatabaseSource(),
            NPMAdvisorySource(),
            GitHubAdvisorySource(),
            SnykDatabaseSource()
        ]
        self.metadata_sources = [
            WikipediaSource(),
            StackShareSource(), 
            BuiltWithSource()
        ]
    
    async def enrich_detections(self, detections: List[TechnologyDetection]) -> List[TechnologyDetection]:
        """Enriquece detecciones con inteligencia adicional"""
        enriched = []
        
        for detection in detections:
            # Enriquecer con vulnerabilidades
            vulnerabilities = await self._get_vulnerabilities(detection)
            if vulnerabilities:
                detection.metadata['vulnerabilities'] = vulnerabilities
                detection.metadata['is_vulnerable'] = True
            
            # Enriquecer con metadata general
            metadata = await self._get_technology_metadata(detection)
            detection.metadata.update(metadata)
            
            # Calcular risk score
            risk_score = self._calculate_risk_score(detection)
            detection.metadata['risk_score'] = risk_score
            
            # Verificar EOL status
            eol_status = await self._check_eol_status(detection)
            detection.metadata['eol_status'] = eol_status
            
            enriched.append(detection)
            
        return enriched
    
    async def _get_vulnerabilities(self, detection: TechnologyDetection) -> List[Dict[str, Any]]:
        """Obtiene vulnerabilidades para una tecnología específica"""
        vulnerabilities = []
        
        for source in self.vulnerability_sources:
            try:
                vulns = await source.get_vulnerabilities(
                    detection.name, 
                    detection.version
                )
                vulnerabilities.extend(vulns)
            except Exception as e:
                print(f"Error getting vulnerabilities from {source.__class__.__name__}: {str(e)}")
        
        # Deduplicar por CVE ID
        seen_cves = set()
        unique_vulns = []
        for vuln in vulnerabilities:
            cve_id = vuln.get('cve_id')
            if cve_id and cve_id not in seen_cves:
                seen_cves.add(cve_id)
                unique_vulns.append(vuln)
            elif not cve_id:
                unique_vulns.append(vuln)
        
        return unique_vulns
    
    async def _get_technology_metadata(self, detection: TechnologyDetection) -> Dict[str, Any]:
        """Obtiene metadata general de la tecnología"""
        metadata = {
            'description': '',
            'website_url': '',
            'documentation_url': '',
            'github_url': '',
            'latest_version': '',
            'popularity_rank': None,
            'license': '',
            'first_release_date': '',
            'language': '',
            'company': ''
        }
        
        for source in self.metadata_sources:
            try:
                source_metadata = await source.get_metadata(detection.name)
                metadata.update(source_metadata)
            except Exception as e:
                print(f"Error getting metadata from {source.__class__.__name__}: {str(e)}")
        
        return metadata
    
    def _calculate_risk_score(self, detection: TechnologyDetection) -> float:
        """Calcula puntuación de riesgo basada en múltiples factores"""
        risk_factors = {
            'has_vulnerabilities': 0.0,
            'vulnerability_severity': 0.0,
            'version_age': 0.0,
            'eol_status': 0.0,
            'popularity': 0.0
        }
        
        # Factor de vulnerabilidades
        vulnerabilities = detection.metadata.get('vulnerabilities', [])
        if vulnerabilities:
            risk_factors['has_vulnerabilities'] = 0.4
            
            # Severidad de vulnerabilidades
            max_severity = max([
                self._severity_to_score(v.get('severity', 'UNKNOWN'))
                for v in vulnerabilities
            ])
            risk_factors['vulnerability_severity'] = max_severity * 0.3
        
        # Factor de edad de versión
        version_age = self._calculate_version_age(detection)
        risk_factors['version_age'] = min(version_age / 365, 1.0) * 0.2  # Normalizado por año
        
        # Factor EOL
        eol_status = detection.metadata.get('eol_status', 'unknown')
        if eol_status == 'eol':
            risk_factors['eol_status'] = 0.3
        elif eol_status == 'deprecated':
            risk_factors['eol_status'] = 0.2
        
        # Factor de popularidad (tecnologías menos populares pueden tener más riesgo)
        popularity_rank = detection.metadata.get('popularity_rank')
        if popularity_rank and popularity_rank > 1000:
            risk_factors['popularity'] = 0.1
        
        return sum(risk_factors.values())
    
    def _severity_to_score(self, severity: str) -> float:
        """Convierte severidad de vulnerabilidad a score numérico"""
        severity_map = {
            'CRITICAL': 1.0,
            'HIGH': 0.8,
            'MEDIUM': 0.5,
            'LOW': 0.2,
            'UNKNOWN': 0.3
        }
        return severity_map.get(severity.upper(), 0.3)
    
    async def _check_eol_status(self, detection: TechnologyDetection) -> str:
        """Verifica status de End of Life de la tecnología"""
        # Esta función consultaría bases de datos EOL como endoflife.date
        # Por simplicidad, aquí se muestra la estructura
        
        eol_database = {
            'jQuery': {'1.x': '2016-01-01', '2.x': '2016-01-01'},
            'Angular': {'1.x': '2021-12-31'},
            'PHP': {'5.6': '2018-12-31', '7.0': '2018-12-03'},
            # Más datos EOL...
        }
        
        tech_eol = eol_database.get(detection.name, {})
        if detection.version:
            major_version = detection.version.split('.')[0] + '.x'
            eol_date = tech_eol.get(major_version)
            
            if eol_date:
                from datetime import datetime
                eol_datetime = datetime.strptime(eol_date, '%Y-%m-%d')
                if datetime.now() > eol_datetime:
                    return 'eol'
        
        return 'supported'
```

### Fase 5: Integración y Reporting (Semanas 9-10)

#### Paso 5.1: Integración con Sistema Principal

**Implementación**:

```python
# Modificaciones en dashboard.py
def analyze_url_enhanced(url):
    """Versión mejorada del análisis con detección de tecnologías"""
    
    try:
        # Análisis existente
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Datos para el análisis de tecnologías
        scan_data = {
            'url': url,
            'html_content': response.text,
            'headers': dict(response.headers),
            'status_code': response.status_code,
            'js_files': [],  # Se obtendría de get_all_js_css_files()
            'css_files': []
        }
        
        # Análisis de tecnologías
        tech_engine = TechnologyDetectionEngine()
        detected_technologies = await tech_engine.analyze_website(scan_data)
        
        # Guardar resultados
        scan_id = save_scan_to_db(url, response, soup)
        save_technologies_to_db(scan_id, detected_technologies)
        
        return {
            'scan_id': scan_id,
            'technologies': detected_technologies,
            'traditional_analysis': analyze_traditional(soup, url)  # Análisis existente
        }
        
    except Exception as e:
        print(f"Error in enhanced analysis: {str(e)}")
        return None

def save_technologies_to_db(scan_id, technologies):
    """Guarda tecnologías detectadas en la base de datos"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for tech in technologies:
        cursor.execute('''
            INSERT INTO detected_technologies 
            (scan_id, technology_name, category, version, confidence_score, 
             detection_method, evidence, metadata, is_vulnerable, vulnerability_info, eol_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            scan_id,
            tech.name,
            tech.category.value,
            tech.version,
            tech.confidence,
            tech.detection_method.value,
            json.dumps(tech.evidence),
            json.dumps(tech.metadata),
            tech.metadata.get('is_vulnerable', False),
            json.dumps(tech.metadata.get('vulnerabilities', [])),
            tech.metadata.get('eol_status', 'unknown')
        ))
    
    conn.commit()
    conn.close()
```

#### Paso 5.2: Actualización de Templates de Reporte

**Implementación**:

```html
<!-- Adición a enhanced_report.html -->

<!-- Technology Stack Analysis -->
<div class="section-card">
    <div class="section-header">
        <i class="bi bi-stack"></i> Análisis de Stack Tecnológico
    </div>
    <div class="section-content">
        {% if technologies %}
            <!-- Technology Overview Cards -->
            <div class="row mb-4">
                {% for category, techs in technologies|groupby('category') %}
                <div class="col-md-3 mb-3">
                    <div class="card border-primary h-100">
                        <div class="card-body text-center">
                            <i class="bi bi-{{ category_icons[category] }} display-6 text-primary"></i>
                            <h5 class="mt-2">{{ category_names[category] }}</h5>
                            <h3 class="text-primary">{{ techs|length }}</h3>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Technology Risk Matrix -->
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="simple-chart">
                        <div class="chart-title">Distribución de Riesgo</div>
                        {% set high_risk = technologies|selectattr('metadata.risk_score', '>', 0.7)|list|length %}
                        {% set medium_risk = technologies|selectattr('metadata.risk_score', '>', 0.4)|selectattr('metadata.risk_score', '<=', 0.7)|list|length %}
                        {% set low_risk = technologies|selectattr('metadata.risk_score', '<=', 0.4)|list|length %}
                        
                        <div class="pie-chart-alternative">
                            <div class="stat-circle" style="background-color: #e74c3c;">
                                <div class="number">{{ high_risk }}</div>
                                <div class="label">Alto Riesgo</div>
                            </div>
                            <div class="stat-circle" style="background-color: #f39c12;">
                                <div class="number">{{ medium_risk }}</div>
                                <div class="label">Medio Riesgo</div>
                            </div>
                            <div class="stat-circle" style="background-color: #27ae60;">
                                <div class="number">{{ low_risk }}</div>
                                <div class="label">Bajo Riesgo</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="simple-chart">
                        <div class="chart-title">Status de Soporte</div>
                        {% set supported = technologies|selectattr('metadata.eol_status', 'equalto', 'supported')|list|length %}
                        {% set eol = technologies|selectattr('metadata.eol_status', 'equalto', 'eol')|list|length %}
                        {% set unknown = technologies|selectattr('metadata.eol_status', 'equalto', 'unknown')|list|length %}
                        
                        <div class="pie-chart-alternative">
                            <div class="stat-circle" style="background-color: #27ae60;">
                                <div class="number">{{ supported }}</div>
                                <div class="label">Soportado</div>
                            </div>
                            <div class="stat-circle" style="background-color: #e74c3c;">
                                <div class="number">{{ eol }}</div>
                                <div class="label">EOL</div>
                            </div>
                            <div class="stat-circle" style="background-color: #95a5a6;">
                                <div class="number">{{ unknown }}</div>
                                <div class="label">Desconocido</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Detailed Technology Table -->
            <h5><i class="bi bi-list-ul"></i> Tecnologías Detectadas ({{ technologies|length }})</h5>
            <table class="library-table">
                <thead>
                    <tr>
                        <th>Tecnología</th>
                        <th>Categoría</th>
                        <th>Versión</th>
                        <th>Confianza</th>
                        <th>Riesgo</th>
                        <th>Estado</th>
                        <th>Vulnerabilidades</th>
                    </tr>
                </thead>
                <tbody>
                    {% for tech in technologies|sort(attribute='metadata.risk_score', reverse=true) %}
                    {% set risk_score = tech.metadata.get('risk_score', 0) %}
                    {% set risk_class = 'status-vulnerable' if risk_score > 0.7 else 'status-unknown' if risk_score > 0.4 else 'status-safe' %}
                    <tr class="{{ risk_class }}">
                        <td>
                            <strong>{{ tech.name }}</strong>
                            {% if tech.metadata.get('website_url') %}
                                <a href="{{ tech.metadata.website_url }}" target="_blank" class="ms-2">
                                    <i class="bi bi-box-arrow-up-right small"></i>
                                </a>
                            {% endif %}
                        </td>
                        <td><span class="badge bg-secondary">{{ tech.category.value.upper() }}</span></td>
                        <td>{{ tech.version or 'No detectada' }}</td>
                        <td>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar" style="width: {{ (tech.confidence * 100)|round }}%">
                                    {{ (tech.confidence * 100)|round }}%
                                </div>
                            </div>
                        </td>
                        <td>
                            {% if risk_score > 0.7 %}
                                <span class="badge bg-danger">Alto</span>
                            {% elif risk_score > 0.4 %}
                                <span class="badge bg-warning">Medio</span>
                            {% else %}
                                <span class="badge bg-success">Bajo</span>
                            {% endif %}
                        </td>
                        <td>
                            {% if tech.metadata.get('eol_status') == 'eol' %}
                                <span class="badge bg-danger">EOL</span>
                            {% elif tech.metadata.get('eol_status') == 'supported' %}
                                <span class="badge bg-success">Soportado</span>
                            {% else %}
                                <span class="badge bg-secondary">Desconocido</span>
                            {% endif %}
                        </td>
                        <td>
                            {% set vulns = tech.metadata.get('vulnerabilities', []) %}
                            {% if vulns %}
                                <span class="badge bg-danger">{{ vulns|length }}</span>
                                <button class="btn btn-sm btn-outline-danger ms-1" 
                                        data-bs-toggle="modal" 
                                        data-bs-target="#vulnModal{{ loop.index }}">
                                    Ver
                                </button>
                            {% else %}
                                <span class="badge bg-success">0</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <div class="text-center p-4">
                <i class="bi bi-stack display-4 text-muted"></i>
                <h5 class="mt-3">No se Detectaron Tecnologías</h5>
                <p class="text-muted">No se pudieron identificar tecnologías específicas en este sitio web.</p>
            </div>
        {% endif %}
    </div>
</div>
```

## Cronograma de Implementación

### 📅 Timeline Detallado

| Semana | Fase | Entregables | Responsable |
|--------|------|-------------|-------------|
| 1 | Fundación | ✅ Esquema DB<br>✅ Clases base<br>✅ Arquitectura | Backend Dev |
| 2 | Fundación | ✅ Motor principal<br>✅ Sistema de firmas<br>✅ Tests unitarios | Backend Dev |
| 3 | Detectores | ✅ HTML Pattern Detector<br>✅ Header Analysis Detector | Backend Dev |
| 4 | Detectores | ✅ Content Analysis Detector<br>✅ Integración con sistema | Backend Dev |
| 5 | Avanzado | ✅ DNS Analysis Detector<br>✅ Network Analysis Detector | Backend Dev + DevOps |
| 6 | Avanzado | ✅ SSL Certificate Analysis<br>✅ Behavioral Detection | Backend Dev |
| 7 | Inteligencia | ✅ Vulnerability Integration<br>✅ Metadata Enrichment | Security Analyst |
| 8 | Inteligencia | ✅ Risk Scoring<br>✅ EOL Detection<br>✅ Intelligence APIs | Security Analyst |
| 9 | Integración | ✅ Dashboard Integration<br>✅ Report Templates | Frontend Dev |
| 10 | Finalización | ✅ Testing<br>✅ Documentation<br>✅ Deployment | Full Team |

## Métricas de Éxito

### 🎯 KPIs Técnicos
- **Cobertura**: Detectar 500+ tecnologías diferentes
- **Precisión**: >95% accuracy en detecciones con confidence >0.8
- **Performance**: <5 segundos adicionales por análisis
- **Falsos Positivos**: <2% en detecciones de alta confianza

### 📊 KPIs de Negocio
- **Valor Agregado**: 40% más insights por reporte
- **Adopción**: 80% de usuarios utilizan nuevas funcionalidades
- **Satisfacción**: NPS >8 en funcionalidades de tecnologías
- **Retención**: 15% incremento en uso regular

## Consideraciones de Implementación

### 🔒 Seguridad
- Todas las consultas DNS/network con timeouts estrictos
- Rate limiting en APIs externas
- Sanitización de datos de entrada
- Logging seguro sin exposición de datos sensibles

### ⚡ Performance
- Análisis asíncrono para no bloquear UI
- Caché Redis para resultados de APIs externas
- Batch processing para análisis masivos
- Lazy loading de datos enriquecidos

### 🔧 Mantenibilidad
- Firmas de detección en archivos JSON separados
- Versionado de signatures database
- Testing automatizado con >80% cobertura
- Documentación API completa

---

*Este plan de implementación proporciona una ruta clara y detallada para expandir significativamente las capacidades de detección de tecnologías del sistema, evolucionando desde la funcionalidad básica actual hacia un sistema de inteligencia tecnológica integral.*