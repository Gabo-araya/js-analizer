#!/usr/bin/env python3
"""
Script de emergencia para resolver problemas de database lock persistentes
"""

import os
import sqlite3
import shutil
import time

def fix_database_lock():
    """Resuelve problemas de bloqueo persistente en SQLite"""
    
    print("🔧 REPARACIÓN DE EMERGENCIA - Database Lock Issues")
    print("=" * 50)
    
    db_path = 'analysis.db'
    wal_path = 'analysis.db-wal'
    shm_path = 'analysis.db-shm'
    
    # Paso 1: Verificar archivos WAL
    print("\n📋 Verificando archivos de base de datos...")
    
    files_info = []
    for file_path in [db_path, wal_path, shm_path]:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            files_info.append(f"   ✅ {file_path}: {size:,} bytes")
        else:
            files_info.append(f"   ❌ {file_path}: No existe")
    
    for info in files_info:
        print(info)
    
    # Paso 2: Intentar checkpoint manual
    if os.path.exists(wal_path):
        wal_size = os.path.getsize(wal_path)
        if wal_size > 0:
            print(f"\n⚠️  WAL file tiene {wal_size:,} bytes - intentando checkpoint...")
            
            try:
                conn = sqlite3.connect(db_path, timeout=5.0)
                conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
                conn.close()
                print("   ✅ Checkpoint completado")
            except Exception as e:
                print(f"   ❌ Error en checkpoint: {e}")
    
    # Paso 3: Forzar cierre de conexiones
    print("\n🔌 Cerrando todas las conexiones...")
    import gc
    gc.collect()
    time.sleep(1)
    
    # Paso 4: Backup de seguridad
    print("\n💾 Creando backup de seguridad...")
    backup_name = f"analysis_backup_{int(time.time())}.db"
    try:
        shutil.copy2(db_path, backup_name)
        print(f"   ✅ Backup creado: {backup_name}")
    except Exception as e:
        print(f"   ❌ Error creando backup: {e}")
    
    # Paso 5: Eliminar archivos WAL si están corruptos
    if os.path.exists(wal_path) and os.path.getsize(wal_path) > 10000000:  # > 10MB
        print("\n⚠️  WAL file muy grande, eliminando...")
        try:
            os.remove(wal_path)
            print("   ✅ WAL eliminado")
        except Exception as e:
            print(f"   ❌ Error eliminando WAL: {e}")
    
    if os.path.exists(shm_path):
        try:
            os.remove(shm_path)
            print("   ✅ SHM eliminado")
        except Exception as e:
            print(f"   ❌ Error eliminando SHM: {e}")
    
    # Paso 6: Reconfigurar base de datos
    print("\n🔄 Reconfigurando base de datos...")
    
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        
        # Resetear configuración
        pragmas = [
            ('PRAGMA journal_mode = DELETE', 'Modo journal reseteado a DELETE'),
            ('PRAGMA synchronous = FULL', 'Sincronización completa'),
            ('PRAGMA temp_store = file', 'Temp store en archivo'),
            ('PRAGMA cache_size = -2000', 'Cache estándar'),
        ]
        
        for pragma, desc in pragmas:
            try:
                result = conn.execute(pragma).fetchone()
                print(f"   ✅ {desc}: {result[0] if result else 'OK'}")
            except Exception as e:
                print(f"   ❌ {desc}: {e}")
        
        # Ejecutar integrity check
        print("\n🔍 Verificando integridad...")
        integrity = conn.execute('PRAGMA integrity_check').fetchone()[0]
        print(f"   Integridad: {integrity}")
        
        # VACUUM para limpiar
        print("\n🧹 Ejecutando VACUUM...")
        conn.execute('VACUUM')
        print("   ✅ VACUUM completado")
        
        # Volver a WAL mode pero con configuración conservadora
        print("\n🔄 Reconfigurando a WAL mode conservador...")
        conn.execute('PRAGMA journal_mode = WAL')
        conn.execute('PRAGMA wal_autocheckpoint = 100')  # Checkpoint frecuente
        conn.execute('PRAGMA busy_timeout = 30000')
        
        conn.close()
        print("   ✅ Reconfiguración completada")
        
    except Exception as e:
        print(f"❌ Error reconfigurando: {e}")
    
    print("\n" + "=" * 50)
    print("✅ REPARACIÓN COMPLETADA")
    print("\n📋 Recomendaciones:")
    print("1. Reinicia el servidor Flask completamente")
    print("2. Prueba con: export ENABLE_ACTION_LOGGING=false")
    print("3. Si persiste, considera usar PostgreSQL")
    
    return True

if __name__ == '__main__':
    fix_database_lock()