#!/usr/bin/env python3
"""
Analizador automatizado de dependencias CDN
Identifica y analiza librerías servidas desde CDNs populares
"""

import re
import requests
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin
import json

class CDNAnalyzer:
    """
    Analizador de dependencias CDN con identificación automática
    """
    
    def __init__(self):
        self.cdn_patterns = self._initialize_cdn_patterns()
        self.cache = {}  # Cache simple para evitar requests repetidas

    def _initialize_cdn_patterns(self) -> Dict:
        """
        Inicializa patrones de reconocimiento para CDNs populares
        """
        return {
            # =================== CDNJS (CloudFlare) ===================
            'cdnjs': {
                'domains': ['cdnjs.cloudflare.com'],
                'pattern': r'cdnjs\.cloudflare\.com/ajax/libs/([^/]+)/([^/]+)/',
                'api_url': 'https://api.cdnjs.com/libraries/{library}',
                'name': 'CDNJS',
                'reliability': 'high',
                'security_score': 9
            },
            
            # =================== jsDelivr ===================
            'jsdelivr': {
                'domains': ['cdn.jsdelivr.net'],
                'pattern': r'cdn\.jsdelivr\.net/npm/([^@/]+)@([^/]+)',
                'api_url': 'https://data.jsdelivr.com/v1/package/npm/{library}',
                'name': 'jsDelivr',
                'reliability': 'high',
                'security_score': 9
            },
            
            # =================== unpkg ===================
            'unpkg': {
                'domains': ['unpkg.com'],
                'pattern': r'unpkg\.com/([^@/]+)@([^/]+)',
                'api_url': 'https://unpkg.com/{library}@{version}/package.json',
                'name': 'unpkg',
                'reliability': 'medium',
                'security_score': 7
            },
            
            # =================== Google CDN ===================
            'google': {
                'domains': ['ajax.googleapis.com', 'fonts.googleapis.com', 'fonts.gstatic.com'],
                'pattern': r'ajax\.googleapis\.com/ajax/libs/([^/]+)/([^/]+)/',
                'name': 'Google CDN',
                'reliability': 'high',
                'security_score': 9
            },
            
            # =================== Microsoft CDN ===================
            'microsoft': {
                'domains': ['ajax.aspnetcdn.com'],
                'pattern': r'ajax\.aspnetcdn\.com/ajax/([^/]+)/([^/]+)/',
                'name': 'Microsoft CDN',
                'reliability': 'high',
                'security_score': 8
            },
            
            # =================== Bootstrap CDN ===================
            'bootstrapcdn': {
                'domains': ['maxcdn.bootstrapcdn.com', 'stackpath.bootstrapcdn.com'],
                'pattern': r'(?:maxcdn\.bootstrapcdn\.com|stackpath\.bootstrapcdn\.com)/bootstrap/([^/]+)/',
                'name': 'Bootstrap CDN',
                'reliability': 'high',
                'security_score': 8
            },
            
            # =================== jQuery CDN ===================
            'jquery': {
                'domains': ['code.jquery.com'],
                'pattern': r'code\.jquery\.com/jquery-([^/]+)\.(?:min\.)?js',
                'name': 'jQuery CDN',
                'reliability': 'high',
                'security_score': 9
            }
        }

    def analyze_url(self, url: str) -> Optional[Dict]:
        """
        Analiza una URL para determinar si es un CDN y extraer información
        """
        if not url:
            return None
            
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Verificar contra cada CDN conocido
        for cdn_key, cdn_info in self.cdn_patterns.items():
            if any(cdn_domain in domain for cdn_domain in cdn_info['domains']):
                return self._analyze_cdn_url(url, cdn_key, cdn_info)
        
        return None

    def _analyze_cdn_url(self, url: str, cdn_key: str, cdn_info: Dict) -> Dict:
        """
        Analiza URL específica de CDN conocido
        """
        result = {
            'is_cdn': True,
            'cdn_name': cdn_info['name'],
            'cdn_key': cdn_key,
            'reliability': cdn_info.get('reliability', 'unknown'),
            'security_score': cdn_info.get('security_score', 5),
            'library_name': None,
            'version': None,
            'latest_version': None,
            'is_outdated': False,
            'url': url
        }
        
        # Extraer nombre de librería y versión usando patrón regex
        if 'pattern' in cdn_info:
            pattern_match = re.search(cdn_info['pattern'], url)
            if pattern_match:
                result['library_name'] = pattern_match.group(1)
                if len(pattern_match.groups()) >= 2:
                    result['version'] = pattern_match.group(2)
        
        # Verificar última versión disponible
        if result['library_name'] and 'api_url' in cdn_info:
            latest_version = self._get_latest_version(cdn_key, cdn_info, result['library_name'])
            if latest_version:
                result['latest_version'] = latest_version
                if result['version']:
                    result['is_outdated'] = self._is_version_outdated(result['version'], latest_version)
        
        return result

    def _get_latest_version(self, cdn_key: str, cdn_info: Dict, library_name: str) -> Optional[str]:
        """
        Obtiene la última versión disponible de una librería en el CDN
        """
        cache_key = f"{cdn_key}:{library_name}"
        
        # Verificar cache
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            if cdn_key == 'cdnjs':
                return self._get_cdnjs_latest_version(library_name)
            elif cdn_key == 'jsdelivr':
                return self._get_jsdelivr_latest_version(library_name)
            elif cdn_key == 'unpkg':
                return self._get_unpkg_latest_version(library_name)
            else:
                return None
        except Exception as e:
            print(f"  ⚠️ Error fetching latest version for {library_name} from {cdn_key}: {str(e)}")
            return None

    def _get_cdnjs_latest_version(self, library_name: str) -> Optional[str]:
        """
        Obtiene última versión desde CDNJS API
        """
        try:
            api_url = f"https://api.cdnjs.com/libraries/{library_name}"
            response = requests.get(api_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('version')
                
                # Cache result
                cache_key = f"cdnjs:{library_name}"
                self.cache[cache_key] = latest_version
                
                return latest_version
        except:
            pass
        return None

    def _get_jsdelivr_latest_version(self, library_name: str) -> Optional[str]:
        """
        Obtiene última versión desde jsDelivr API
        """
        try:
            api_url = f"https://data.jsdelivr.com/v1/package/npm/{library_name}"
            response = requests.get(api_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                versions = data.get('versions', [])
                if versions:
                    # Tomar la primera versión (más reciente)
                    latest_version = versions[0].get('version')
                    
                    # Cache result
                    cache_key = f"jsdelivr:{library_name}"
                    self.cache[cache_key] = latest_version
                    
                    return latest_version
        except:
            pass
        return None

    def _get_unpkg_latest_version(self, library_name: str) -> Optional[str]:
        """
        Obtiene última versión desde unpkg
        """
        try:
            # unpkg redirect nos da la última versión
            api_url = f"https://unpkg.com/{library_name}/package.json"
            response = requests.get(api_url, timeout=5, allow_redirects=True)
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('version')
                
                # Cache result
                cache_key = f"unpkg:{library_name}"
                self.cache[cache_key] = latest_version
                
                return latest_version
        except:
            pass
        return None

    def _is_version_outdated(self, current_version: str, latest_version: str) -> bool:
        """
        Determina si la versión actual está desactualizada
        """
        try:
            # Limpiar versiones
            current_clean = re.sub(r'[^\d\.]', '', current_version)
            latest_clean = re.sub(r'[^\d\.]', '', latest_version)
            
            if not current_clean or not latest_clean:
                return False
            
            current_parts = [int(x) for x in current_clean.split('.')]
            latest_parts = [int(x) for x in latest_clean.split('.')]
            
            # Comparar versiones
            max_len = max(len(current_parts), len(latest_parts))
            current_normalized = current_parts + [0] * (max_len - len(current_parts))
            latest_normalized = latest_parts + [0] * (max_len - len(latest_parts))
            
            for i in range(max_len):
                if current_normalized[i] < latest_normalized[i]:
                    return True
                elif current_normalized[i] > latest_normalized[i]:
                    return False
            
            return False  # Versiones iguales
            
        except:
            return False  # En caso de error, asumir que no está desactualizada

    def analyze_multiple_urls(self, urls: List[str]) -> List[Dict]:
        """
        Analiza múltiples URLs de CDN
        """
        results = []
        for url in urls:
            analysis = self.analyze_url(url)
            if analysis:
                results.append(analysis)
        return results

    def get_cdn_statistics(self, analyses: List[Dict]) -> Dict:
        """
        Genera estadísticas de uso de CDN
        """
        if not analyses:
            return {}
        
        cdn_usage = {}
        outdated_count = 0
        total_libraries = len(analyses)
        security_scores = []
        
        for analysis in analyses:
            cdn_name = analysis.get('cdn_name', 'Unknown')
            cdn_usage[cdn_name] = cdn_usage.get(cdn_name, 0) + 1
            
            if analysis.get('is_outdated', False):
                outdated_count += 1
            
            if 'security_score' in analysis:
                security_scores.append(analysis['security_score'])
        
        avg_security_score = sum(security_scores) / len(security_scores) if security_scores else 0
        
        return {
            'total_cdn_libraries': total_libraries,
            'cdn_distribution': cdn_usage,
            'outdated_libraries': outdated_count,
            'outdated_percentage': (outdated_count / total_libraries * 100) if total_libraries > 0 else 0,
            'average_security_score': round(avg_security_score, 1),
            'recommendations': self._generate_recommendations(analyses)
        }

    def _generate_recommendations(self, analyses: List[Dict]) -> List[str]:
        """
        Genera recomendaciones basadas en el análisis de CDN
        """
        recommendations = []
        
        outdated_libs = [a for a in analyses if a.get('is_outdated', False)]
        low_security_cdns = [a for a in analyses if a.get('security_score', 10) < 7]
        
        if outdated_libs:
            recommendations.append(f"Actualizar {len(outdated_libs)} librería(s) desactualizada(s)")
        
        if low_security_cdns:
            recommendations.append(f"Considerar migrar {len(low_security_cdns)} librería(s) a CDNs más seguros")
        
        # Recomendaciones específicas por CDN
        cdn_counts = {}
        for analysis in analyses:
            cdn = analysis.get('cdn_key', 'unknown')
            cdn_counts[cdn] = cdn_counts.get(cdn, 0) + 1
        
        if 'unpkg' in cdn_counts and cdn_counts['unpkg'] > 2:
            recommendations.append("Considerar usar CDNJS o jsDelivr en lugar de unpkg para mejor rendimiento")
        
        if not any(cdn in cdn_counts for cdn in ['cdnjs', 'jsdelivr', 'google']):
            recommendations.append("Considerar usar CDNs más confiables como CDNJS, jsDelivr o Google CDN")
        
        return recommendations

    def get_supported_cdns(self) -> List[Dict]:
        """
        Retorna lista de CDNs soportados
        """
        return [
            {
                'key': key,
                'name': info['name'],
                'domains': info['domains'],
                'reliability': info.get('reliability', 'unknown'),
                'security_score': info.get('security_score', 5)
            }
            for key, info in self.cdn_patterns.items()
        ]


# Instancia global del analizador CDN
cdn_analyzer = CDNAnalyzer()


def analyze_cdn_url(url: str) -> Optional[Dict]:
    """
    Función de conveniencia para analizar una URL de CDN
    """
    return cdn_analyzer.analyze_url(url)


def analyze_multiple_cdn_urls(urls: List[str]) -> List[Dict]:
    """
    Función de conveniencia para analizar múltiples URLs de CDN
    """
    return cdn_analyzer.analyze_multiple_urls(urls)


def get_cdn_recommendations(analyses: List[Dict]) -> Dict:
    """
    Función de conveniencia para obtener recomendaciones de CDN
    """
    return cdn_analyzer.get_cdn_statistics(analyses)