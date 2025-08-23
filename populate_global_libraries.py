#!/usr/bin/env python3
"""
Script para poblar el catálogo global de librerías con datos del js-file-extractor.html
"""
import sqlite3
import json

# Base de datos de librerías conocidas (extraída del archivo HTML)
KNOWN_LIBRARIES = {
    'jquery': {
        'current': '3.7.1',
        'type': 'js',
        'description': 'Biblioteca JavaScript rápida, pequeña y rica en funciones',
        'vulnerability_info': 'Versiones anteriores a 3.5.0 tienen vulnerabilidades XSS conocidas',
        'source_url': 'https://jquery.com/'
    },
    'bootstrap': {
        'current': '5.3.2',
        'type': 'css',
        'description': 'Framework CSS para desarrollo responsive y mobile-first',
        'vulnerability_info': 'Versiones anteriores a 4.6.2 tienen vulnerabilidades de XSS',
        'source_url': 'https://getbootstrap.com/'
    },
    'd3': {
        'current': '7.8.5',
        'type': 'js',
        'description': 'Biblioteca JavaScript para manipular documentos basados en datos',
        'vulnerability_info': 'Versiones anteriores a 7.0.0 pueden tener problemas de rendimiento',
        'source_url': 'https://d3js.org/'
    },
    'chart.js': {
        'current': '4.4.1',
        'type': 'js',
        'description': 'Biblioteca JavaScript simple pero flexible para gráficos',
        'vulnerability_info': 'Versiones anteriores a 3.9.1 tienen vulnerabilidades menores',
        'source_url': 'https://www.chartjs.org/'
    },
    'lightbox': {
        'current': '2.11.4',
        'type': 'js',
        'description': 'Script para superponer imágenes sobre la página actual',
        'vulnerability_info': 'Versiones anteriores a 2.11.0 pueden tener problemas de accesibilidad',
        'source_url': 'https://lokeshdhakar.com/projects/lightbox2/'
    },
    'swiper': {
        'current': '11.0.5',
        'type': 'js',
        'description': 'Slider móvil táctil más moderno con aceleración de hardware',
        'vulnerability_info': 'Versiones anteriores a 8.4.0 pueden tener problemas de rendimiento',
        'source_url': 'https://swiperjs.com/'
    },
    'moment': {
        'current': '2.29.4',
        'type': 'js',
        'description': 'Biblioteca para parsing, validación, manipulación y formateo de fechas',
        'vulnerability_info': 'DEPRECATED: Se recomienda migrar a Day.js o date-fns',
        'source_url': 'https://momentjs.com/'
    },
    'font-awesome': {
        'current': '6.5.1',
        'type': 'css',
        'description': 'Biblioteca de iconos vectoriales y herramientas CSS',
        'vulnerability_info': 'Sin vulnerabilidades conocidas en versiones recientes',
        'source_url': 'https://fontawesome.com/'
    },
    'angular': {
        'current': '17.1.0',
        'type': 'js',
        'description': 'Framework web TypeScript de código abierto',
        'vulnerability_info': 'Versiones anteriores a 16.2.0 tienen vulnerabilidades de seguridad',
        'source_url': 'https://angular.io/'
    },
    'react': {
        'current': '18.2.0',
        'type': 'js',
        'description': 'Biblioteca JavaScript para construir interfaces de usuario',
        'vulnerability_info': 'Versiones anteriores a 17.0.2 pueden tener problemas de memoria',
        'source_url': 'https://reactjs.org/'
    },
    'vue': {
        'current': '3.4.15',
        'type': 'js',
        'description': 'Framework JavaScript progresivo para construir UI',
        'vulnerability_info': 'Versiones anteriores a 3.2.0 tienen vulnerabilidades menores',
        'source_url': 'https://vuejs.org/'
    },
    'lodash': {
        'current': '4.17.21',
        'type': 'js',
        'description': 'Biblioteca de utilidades JavaScript moderna',
        'vulnerability_info': 'Versiones anteriores a 4.17.21 tienen vulnerabilidades críticas',
        'source_url': 'https://lodash.com/'
    }
}

def get_db_connection():
    conn = sqlite3.connect('analysis.db')
    conn.row_factory = sqlite3.Row
    return conn

def populate_global_libraries():
    """Poblar el catálogo global con librerías conocidas"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    added_count = 0
    updated_count = 0
    
    for library_name, info in KNOWN_LIBRARIES.items():
        # Verificar si la librería ya existe
        cursor.execute("SELECT id, latest_version FROM global_libraries WHERE library_name = ?", (library_name,))
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar solo si la versión es más nueva
            if existing['latest_version'] != info['current']:
                cursor.execute('''
                    UPDATE global_libraries 
                    SET latest_version = ?, latest_safe_version = ?, description = ?, 
                        vulnerability_info = ?, source_url = ?, updated_date = CURRENT_TIMESTAMP
                    WHERE library_name = ?
                ''', (
                    info['current'], info['current'], info['description'],
                    info['vulnerability_info'], info['source_url'], library_name
                ))
                updated_count += 1
                print(f"✅ Actualizada: {library_name} -> v{info['current']}")
            else:
                print(f"⏸️  Sin cambios: {library_name} ya está actualizada")
        else:
            # Agregar nueva librería
            cursor.execute('''
                INSERT INTO global_libraries 
                (library_name, type, latest_safe_version, latest_version, description, vulnerability_info, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                library_name, info['type'], info['current'], info['current'],
                info['description'], info['vulnerability_info'], info['source_url']
            ))
            added_count += 1
            print(f"🆕 Agregada: {library_name} v{info['current']}")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Resumen:")
    print(f"   🆕 Librerías agregadas: {added_count}")
    print(f"   ✅ Librerías actualizadas: {updated_count}")
    print(f"   📚 Total en catálogo: {len(KNOWN_LIBRARIES)}")

if __name__ == "__main__":
    print("🚀 Poblando catálogo global de librerías...")
    try:
        populate_global_libraries()
        print("✅ Catálogo poblado exitosamente!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")