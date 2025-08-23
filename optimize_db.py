#!/usr/bin/env python3
"""
Script para optimizar la base de datos SQLite y resolver problemas de concurrencia
"""

import sqlite3
import os
import time

def optimize_database():
    """Optimiza la base de datos SQLite para mejor concurrencia"""
    db_path = 'analysis.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return
    
    print("🔧 Optimizando base de datos SQLite...")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path, timeout=60.0)
        
        print("📊 Estado actual de la base de datos:")
        
        # Verificar modo de journal actual
        journal_mode = conn.execute('PRAGMA journal_mode').fetchone()[0]
        print(f"   Journal mode: {journal_mode}")
        
        # Verificar integridad
        integrity = conn.execute('PRAGMA integrity_check').fetchone()[0]
        print(f"   Integridad: {integrity}")
        
        # Obtener tamaño de página
        page_size = conn.execute('PRAGMA page_size').fetchone()[0]
        print(f"   Page size: {page_size}")
        
        # Obtener información WAL
        try:
            wal_info = conn.execute('PRAGMA wal_checkpoint(FULL)').fetchone()
            print(f"   WAL checkpoint: {wal_info}")
        except:
            print("   WAL checkpoint: N/A")
        
        print("\n🚀 Aplicando optimizaciones...")
        
        # Configurar para máxima concurrencia
        optimizations = [
            ('PRAGMA journal_mode = WAL', 'WAL mode habilitado'),
            ('PRAGMA synchronous = NORMAL', 'Sincronización optimizada'),
            ('PRAGMA cache_size = -128000', 'Cache aumentado a 128MB'),
            ('PRAGMA temp_store = memory', 'Temp store en memoria'),
            ('PRAGMA mmap_size = 268435456', 'Memory mapping a 256MB'),
            ('PRAGMA wal_autocheckpoint = 500', 'Auto-checkpoint configurado'),
            ('PRAGMA busy_timeout = 60000', 'Timeout aumentado a 60s'),
            ('PRAGMA optimize', 'Estadísticas optimizadas')
        ]
        
        for pragma, description in optimizations:
            try:
                result = conn.execute(pragma).fetchone()
                print(f"   ✅ {description}")
                if result:
                    print(f"      Resultado: {result[0]}")
            except Exception as e:
                print(f"   ⚠️ {description}: {e}")
        
        # Verificar tablas y índices
        print("\n📋 Verificando estructura:")
        
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for table in tables:
            table_name = table[0]
            count = conn.execute(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]
            print(f"   📄 {table_name}: {count} registros")
        
        # Verificar índices específicos del historial
        if 'action_history' in [t[0] for t in tables]:
            print("\n🔍 Índices de action_history:")
            indexes = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND tbl_name='action_history'
            """).fetchall()
            
            for index in indexes:
                print(f"   📊 {index[0]}")
        
        # Ejecutar VACUUM para compactar
        print("\n🧹 Compactando base de datos...")
        start_time = time.time()
        conn.execute('VACUUM')
        vacuum_time = time.time() - start_time
        print(f"   ✅ VACUUM completado en {vacuum_time:.2f}s")
        
        # Analizar estadísticas
        print("\n📈 Analizando estadísticas...")
        conn.execute('ANALYZE')
        print("   ✅ ANALYZE completado")
        
        conn.close()
        
        print("\n🎉 Optimización completada!")
        print("\n💡 Para evitar problemas de concurrencia:")
        print("   - Reinicia el servidor Flask")
        print("   - Considera usar: export ENABLE_ACTION_LOGGING=false (temporal)")
        print("   - Usa: export LOGGING_DEBUG=true para debug detallado")
        
    except Exception as e:
        print(f"❌ Error durante optimización: {e}")

if __name__ == '__main__':
    optimize_database()