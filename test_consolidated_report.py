#!/usr/bin/env python3
"""
Script de prueba para el reporte consolidado de proyecto
"""

import dashboard
import sqlite3

def test_project_consolidated_data():
    """Prueba la función get_project_consolidated_data"""
    
    # Conectar a la base de datos
    conn = dashboard.get_db_connection()
    
    # Obtener un proyecto de prueba
    projects = conn.execute('SELECT id, name FROM projects WHERE is_active = 1 LIMIT 1').fetchall()
    
    if not projects:
        print("❌ No hay proyectos en la base de datos para probar")
        return False
    
    project = projects[0]
    print(f"🧪 Probando con proyecto: {project['name']} (ID: {project['id']})")
    
    # Verificar si hay escaneos revisados
    scans = conn.execute('''
        SELECT COUNT(*) as count 
        FROM scans 
        WHERE project_id = ? AND reviewed = 1
    ''', (project['id'],)).fetchone()
    
    print(f"📊 Escaneos revisados en el proyecto: {scans['count']}")
    
    if scans['count'] == 0:
        print("⚠️ No hay escaneos revisados en este proyecto. Creando un escaneo de prueba...")
        # Crear un escaneo de prueba
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scans (url, scan_date, status_code, title, headers, project_id, reviewed)
            VALUES (?, datetime('now'), 200, 'Test Page', '{}', ?, 1)
        ''', ('https://test.example.com', project['id']))
        
        scan_id = cursor.lastrowid
        
        # Agregar una biblioteca de prueba
        cursor.execute('''
            INSERT INTO libraries (scan_id, library_name, version, type, latest_safe_version)
            VALUES (?, 'jquery', '3.6.0', 'js', '3.6.0')
        ''', (scan_id,))
        
        conn.commit()
        print("✅ Escaneo de prueba creado")
    
    conn.close()
    
    # Probar la función get_project_consolidated_data
    try:
        print("🔄 Ejecutando get_project_consolidated_data...")
        data = dashboard.get_project_consolidated_data(project['id'])
        
        if not data:
            print("❌ La función devolvió None")
            return False
        
        print("✅ Función ejecutada exitosamente")
        print(f"   - Proyecto: {data['project']['name']}")
        print(f"   - URLs analizadas: {data['project_stats']['total_urls']}")
        print(f"   - Bibliotecas consolidadas: {data['project_stats']['total_libraries']}")
        print(f"   - Vulnerabilidades: {data['project_stats']['total_vulnerabilities']}")
        print(f"   - Puntuación de seguridad: {data['consolidated_security_analysis']['security_score']}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en get_project_consolidated_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_url_access():
    """Prueba que la URL del reporte consolidado sea accesible"""
    try:
        from flask import Flask
        
        # Crear una app de prueba
        app = dashboard.app
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            # Intentar acceder a un proyecto específico
            conn = dashboard.get_db_connection()
            projects = conn.execute('SELECT id FROM projects WHERE is_active = 1 LIMIT 1').fetchall()
            conn.close()
            
            if not projects:
                print("❌ No hay proyectos para probar la URL")
                return False
            
            project_id = projects[0]['id']
            
            # Hacer request a la URL del reporte
            response = client.get(f'/report/project/{project_id}')
            
            if response.status_code == 200:
                print("✅ URL del reporte consolidado accesible")
                print(f"   - Status code: {response.status_code}")
                return True
            else:
                print(f"❌ Error en URL del reporte: {response.status_code}")
                print(f"   - Data: {response.get_data(as_text=True)[:200]}...")
                return False
                
    except Exception as e:
        print(f"❌ Error probando URL: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Iniciando pruebas del reporte consolidado...\n")
    
    # Test 1: Función de datos consolidados
    print("=" * 50)
    print("TEST 1: Función get_project_consolidated_data")
    print("=" * 50)
    test1_passed = test_project_consolidated_data()
    
    # Test 2: Acceso a URL
    print("\n" + "=" * 50)
    print("TEST 2: Acceso a URL del reporte")
    print("=" * 50)
    test2_passed = test_url_access()
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE PRUEBAS")
    print("=" * 50)
    print(f"Test 1 - Función de datos: {'✅ PASÓ' if test1_passed else '❌ FALLÓ'}")
    print(f"Test 2 - URL accesible: {'✅ PASÓ' if test2_passed else '❌ FALLÓ'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! El reporte consolidado está listo para usar.")
    else:
        print(f"\n⚠️ Algunas pruebas fallaron. Revisar los errores arriba.")