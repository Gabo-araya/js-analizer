#!/usr/bin/env python3
"""
Database Migration Script: clients → projects
Migra completamente la base de datos de clients a projects
"""

import sqlite3
import sys
import os

def migrate_clients_to_projects():
    """Migra la base de datos de clients a projects"""
    db_path = 'analysis.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔄 Iniciando migración clients → projects...")
        
        # Verificar si ya fue migrado
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        if cursor.fetchone():
            print("✅ La migración ya fue ejecutada")
            return True
        
        # Verificar que existe tabla clients
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
        if not cursor.fetchone():
            print("❌ Tabla 'clients' no existe")
            return False
        
        # Verificar que existe columna client_id en scans
        cursor.execute("PRAGMA table_info(scans)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'client_id' not in columns:
            print("❌ Columna 'client_id' no existe en tabla scans")
            return False
        
        # Paso 1: Renombrar tabla clients a projects
        cursor.execute("ALTER TABLE clients RENAME TO projects")
        print("✅ Tabla 'clients' renombrada a 'projects'")
        
        # Paso 2: Verificar si ya existe project_id
        cursor.execute("PRAGMA table_info(scans)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'project_id' not in columns:
            # Crear columna project_id y copiar datos
            cursor.execute("ALTER TABLE scans ADD COLUMN project_id INTEGER")
            cursor.execute("UPDATE scans SET project_id = client_id")
            print("✅ Columna 'project_id' creada y datos copiados")
        
        # Paso 3: Eliminar columna client_id (SQLite no soporta DROP COLUMN directamente)
        # Necesitamos recrear la tabla
        print("🔄 Recreando tabla scans sin client_id...")
        
        # Obtener schema actual de scans
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='scans'")
        original_schema = cursor.fetchone()[0]
        
        # Crear tabla temporal sin client_id
        cursor.execute('''
        CREATE TABLE scans_temp (
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
        
        # Copiar datos (excluyendo client_id)
        cursor.execute('''
        INSERT INTO scans_temp (id, url, scan_date, status_code, title, headers, project_id, reviewed)
        SELECT id, url, scan_date, status_code, title, headers, project_id, 
               CASE WHEN reviewed IS NULL THEN 0 ELSE reviewed END
        FROM scans
        ''')
        
        # Eliminar tabla original y renombrar temporal
        cursor.execute("DROP TABLE scans")
        cursor.execute("ALTER TABLE scans_temp RENAME TO scans")
        
        print("✅ Tabla 'scans' recreada sin columna 'client_id'")
        
        # Commit todos los cambios
        conn.commit()
        
        # Verificar migración
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        projects_exists = cursor.fetchone() is not None
        
        cursor.execute("PRAGMA table_info(scans)")
        scan_columns = [col[1] for col in cursor.fetchall()]
        project_id_exists = 'project_id' in scan_columns
        client_id_exists = 'client_id' in scan_columns
        
        if projects_exists and project_id_exists and not client_id_exists:
            print("✅ Migración completada exitosamente")
            print("   - Tabla 'clients' → 'projects' ✓")
            print("   - Columna 'client_id' → 'project_id' ✓")
            print("   - Columna 'client_id' eliminada ✓")
            return True
        else:
            print("❌ Error: Migración incompleta")
            return False
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = migrate_clients_to_projects()
    sys.exit(0 if success else 1)