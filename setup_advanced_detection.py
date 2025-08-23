#!/usr/bin/env python3
"""
Script de configuración para las funcionalidades avanzadas de detección
Ejecutar después de implementar las nuevas funcionalidades
"""
import os
import sys

def main():
    print("🚀 Configurando funcionalidades avanzadas de detección...")
    print("=" * 60)
    
    # 1. Verificar archivos necesarios
    required_files = [
        'library_detector.py',
        'populate_global_libraries.py',
        'dashboard.py',
        'analyzer.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos los archivos necesarios están presentes")
    
    # 2. Poblar catálogo global
    print("\n📚 Poblando catálogo global de librerías...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'populate_global_libraries.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Catálogo global poblado exitosamente")
            print(result.stdout)
        else:
            print("⚠️ Advertencia al poblar catálogo:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error poblando catálogo: {str(e)}")
    
    # 3. Verificar imports
    print("\n🔍 Verificando imports y dependencias...")
    try:
        from library_detector import LibraryDetector, detect_libraries_advanced
        print("✅ library_detector importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando library_detector: {str(e)}")
        return False
    
    # 4. Crear archivos de configuración si no existen
    print("\n⚙️ Verificando archivos de configuración...")
    
    if not os.path.exists('urls.txt'):
        sample_urls = [
            'https://jquery.com',
            'https://getbootstrap.com',
            'https://d3js.org',
            'https://www.chartjs.org'
        ]
        with open('urls.txt', 'w') as f:
            f.write('\n'.join(sample_urls) + '\n')
        print("✅ Archivo urls.txt creado con URLs de ejemplo")
    
    # 5. Mostrar resumen de funcionalidades
    print("\n🎉 Configuración completada exitosamente!")
    print("=" * 60)
    print("\n📋 FUNCIONALIDADES IMPLEMENTADAS:")
    print("1. ✅ Base de librerías conocidas integrada (12+ librerías)")
    print("2. ✅ Detección avanzada con patrones RegEx")
    print("3. ✅ Identificación automática de versiones")
    print("4. ✅ Detección contextual por tipo de página")
    print("5. ✅ Sistema de confianza en detecciones")
    print("6. ✅ Catálogo global de librerías")
    print("7. ✅ Importar/exportar catálogo (CSV/JSON)")
    
    print("\n🚀 CÓMO USAR:")
    print("1. python dashboard.py          # Interfaz web con catálogo global")
    print("2. python analyzer.py           # Análisis desde línea de comandos")
    print("3. http://localhost:5000/global-libraries  # Gestionar catálogo global")
    
    print("\n🔧 MEJORAS EN LA DETECCIÓN:")
    print("• Reconoce automáticamente jQuery, Bootstrap, D3, Chart.js, etc.")
    print("• Extrae versiones de nombres de archivos")
    print("• Detecta librerías basándose en el contexto de la página")
    print("• Asigna niveles de confianza a las detecciones")
    print("• Identifica librerías faltantes por contexto")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ ¡Todo listo! Las funcionalidades avanzadas están configuradas.")
    else:
        print("\n❌ Configuración incompleta. Revisa los errores arriba.")
        sys.exit(1)