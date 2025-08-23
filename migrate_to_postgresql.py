#!/usr/bin/env python3
"""
Script de Migración: SQLite (analysis.db) → PostgreSQL
Migra únicamente los datos de analysis.db a una base de datos PostgreSQL unificada.
"""

import sqlite3
import psycopg2
import psycopg2.extras
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class DatabaseMigrator:
    def __init__(self, sqlite_path: str = "analysis.db", 
                 postgres_config: Dict[str, str] = None):
        self.sqlite_path = sqlite_path
        self.postgres_config = postgres_config or {
            'host': 'localhost',
            'port': '5432',
            'database': 'ntg_analyzer',
            'user': 'ntg_user',
            'password': 'ntg_password'
        }
        self.stats = {
            'tables_migrated': 0,
            'total_records': 0,
            'errors': [],
            'start_time': datetime.now()
        }

    def log(self, message: str, level: str = "INFO"):
        """Log con timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def create_postgresql_schema(self, pg_cursor):
        """Crea el esquema optimizado de PostgreSQL"""
        self.log("Creando esquema PostgreSQL...")
        
        schema_sql = """
        -- Eliminar tablas si existen (para re-ejecutar el script)
        DROP TABLE IF EXISTS action_history CASCADE;
        DROP TABLE IF EXISTS version_strings CASCADE;
        DROP TABLE IF EXISTS file_urls CASCADE;
        DROP TABLE IF EXISTS libraries CASCADE;
        DROP TABLE IF EXISTS scans CASCADE;
        DROP TABLE IF EXISTS global_libraries CASCADE;
        DROP TABLE IF EXISTS clients CASCADE;
        DROP TABLE IF EXISTS users CASCADE;

        -- === TABLAS PRINCIPALES ===

        -- Usuarios y autenticación
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL DEFAULT 'analyst',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Clientes
        CREATE TABLE clients (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            description TEXT,
            contact_email VARCHAR(255),
            contact_phone VARCHAR(50),
            website VARCHAR(500),
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Catálogo global de librerías
        CREATE TABLE global_libraries (
            id SERIAL PRIMARY KEY,
            library_name VARCHAR(255) UNIQUE NOT NULL,
            type VARCHAR(10) CHECK (type IN ('js', 'css')),
            latest_safe_version VARCHAR(50),
            latest_version VARCHAR(50),
            description TEXT,
            vulnerability_info TEXT,
            source_url VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Escaneos principales
        CREATE TABLE scans (
            id SERIAL PRIMARY KEY,
            url VARCHAR(2000) NOT NULL,
            status_code INTEGER,
            title TEXT,
            headers JSONB,
            reviewed BOOLEAN DEFAULT false,
            client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Librerías detectadas
        CREATE TABLE libraries (
            id SERIAL PRIMARY KEY,
            scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
            library_name VARCHAR(255) NOT NULL,
            version VARCHAR(50),
            type VARCHAR(10) CHECK (type IN ('js', 'css')),
            source_url VARCHAR(2000),
            description TEXT,
            latest_safe_version VARCHAR(50),
            latest_version VARCHAR(50),
            is_manual BOOLEAN DEFAULT false,
            global_library_id INTEGER REFERENCES global_libraries(id) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- URLs de archivos encontrados
        CREATE TABLE file_urls (
            id SERIAL PRIMARY KEY,
            scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
            file_url VARCHAR(2000) NOT NULL,
            file_type VARCHAR(10) CHECK (file_type IN ('js', 'css')),
            file_size BIGINT,
            status_code INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Strings de versión encontrados
        CREATE TABLE version_strings (
            id SERIAL PRIMARY KEY,
            scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
            file_url VARCHAR(2000) NOT NULL,
            file_type VARCHAR(10) CHECK (file_type IN ('js', 'css')),
            line_number INTEGER,
            line_content TEXT,
            version_keyword VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Historial de acciones (unificado)
        CREATE TABLE action_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            username VARCHAR(100) NOT NULL,
            user_role VARCHAR(50) NOT NULL,
            action_type VARCHAR(50) NOT NULL,
            target_table VARCHAR(100) NOT NULL,
            target_id INTEGER,
            target_description TEXT,
            data_before JSONB,
            data_after JSONB,
            ip_address INET,
            user_agent TEXT,
            success BOOLEAN DEFAULT true,
            error_message TEXT,
            session_id VARCHAR(255),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- === ÍNDICES OPTIMIZADOS ===
        CREATE INDEX idx_scans_client_id ON scans(client_id);
        CREATE INDEX idx_scans_created_at ON scans(created_at);
        CREATE INDEX idx_scans_url_hash ON scans USING hash(url);

        CREATE INDEX idx_libraries_scan_id ON libraries(scan_id);
        CREATE INDEX idx_libraries_name_version ON libraries(library_name, version);
        CREATE INDEX idx_libraries_global_lib ON libraries(global_library_id);

        CREATE INDEX idx_file_urls_scan_id ON file_urls(scan_id);
        CREATE INDEX idx_version_strings_scan_id ON version_strings(scan_id);

        -- Índices especializados para historial
        CREATE INDEX idx_history_user_id ON action_history(user_id);
        CREATE INDEX idx_history_created_at ON action_history(created_at);
        CREATE INDEX idx_history_action_type ON action_history(action_type);
        CREATE INDEX idx_history_target ON action_history(target_table, target_id);
        """
        
        try:
            pg_cursor.execute(schema_sql)
            self.log("✅ Esquema PostgreSQL creado exitosamente")
        except Exception as e:
            self.log(f"❌ Error creando esquema: {e}", "ERROR")
            raise

    def extract_sqlite_data(self, table_name: str) -> List[Dict[str, Any]]:
        """Extrae datos de una tabla SQLite"""
        try:
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Convertir a lista de diccionarios
            data = []
            for row in rows:
                row_dict = dict(row)
                # Convertir campos que requieren transformación
                row_dict = self.transform_row_data(table_name, row_dict)
                data.append(row_dict)
            
            conn.close()
            self.log(f"📊 Extraídos {len(data)} registros de tabla '{table_name}'")
            return data
            
        except Exception as e:
            self.log(f"❌ Error extrayendo datos de {table_name}: {e}", "ERROR")
            return []

    def transform_row_data(self, table_name: str, row_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transforma datos específicos por tabla para PostgreSQL"""
        
        # Transformaciones específicas por tabla
        if table_name == 'scans':
            # Convertir headers de TEXT a JSONB
            if 'headers' in row_data and row_data['headers']:
                try:
                    # Si ya es string JSON, parsearlo
                    if isinstance(row_data['headers'], str):
                        row_data['headers'] = json.loads(row_data['headers'])
                except (json.JSONDecodeError, TypeError):
                    # Si falla, dejar como objeto vacío
                    row_data['headers'] = {}
            else:
                row_data['headers'] = {}
                
            # Convertir reviewed INTEGER a BOOLEAN
            if 'reviewed' in row_data:
                row_data['reviewed'] = bool(row_data['reviewed'])
        
        elif table_name == 'clients':
            # Convertir is_active INTEGER a BOOLEAN
            if 'is_active' in row_data:
                row_data['is_active'] = bool(row_data['is_active'])
        
        elif table_name == 'libraries':
            # Convertir is_manual INTEGER a BOOLEAN
            if 'is_manual' in row_data:
                row_data['is_manual'] = bool(row_data['is_manual'])
        
        elif table_name == 'users':
            # Renombrar password a password_hash para claridad
            if 'password' in row_data:
                row_data['password_hash'] = row_data.pop('password')
        
        elif table_name == 'action_history':
            # Transformar datos JSON
            for json_field in ['data_before', 'data_after']:
                if json_field in row_data and row_data[json_field]:
                    try:
                        if isinstance(row_data[json_field], str):
                            row_data[json_field] = json.loads(row_data[json_field])
                    except (json.JSONDecodeError, TypeError):
                        row_data[json_field] = None
            
            # Convertir success INTEGER a BOOLEAN
            if 'success' in row_data:
                row_data['success'] = bool(row_data['success'])
        
        return row_data

    def insert_postgresql_data(self, pg_cursor, table_name: str, data: List[Dict[str, Any]]):
        """Inserta datos en PostgreSQL usando bulk insert"""
        if not data:
            self.log(f"⚠️  No hay datos para insertar en tabla '{table_name}'")
            return
        
        try:
            # Obtener columnas de la primera fila
            columns = list(data[0].keys())
            
            # Preparar valores para inserción
            values_list = []
            for row in data:
                values = tuple(row.get(col) for col in columns)
                values_list.append(values)
            
            # Construir query de inserción
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            
            insert_query = f"""
                INSERT INTO {table_name} ({columns_str}) 
                VALUES ({placeholders})
            """
            
            # Ejecutar inserción masiva
            psycopg2.extras.execute_batch(
                pg_cursor, 
                insert_query, 
                values_list,
                page_size=1000  # Procesar en lotes de 1000
            )
            
            self.log(f"✅ Insertados {len(data)} registros en tabla '{table_name}'")
            self.stats['total_records'] += len(data)
            
        except Exception as e:
            error_msg = f"Error insertando en {table_name}: {e}"
            self.log(f"❌ {error_msg}", "ERROR")
            self.stats['errors'].append(error_msg)
            raise

    def migrate_table(self, pg_cursor, table_name: str, sqlite_table_name: str = None):
        """Migra una tabla completa de SQLite a PostgreSQL"""
        sqlite_table_name = sqlite_table_name or table_name
        
        self.log(f"🔄 Migrando tabla '{sqlite_table_name}' -> '{table_name}'...")
        
        # Extraer datos de SQLite
        data = self.extract_sqlite_data(sqlite_table_name)
        
        if data:
            # Insertar en PostgreSQL
            self.insert_postgresql_data(pg_cursor, table_name, data)
            self.stats['tables_migrated'] += 1
        else:
            self.log(f"⚠️  Tabla '{sqlite_table_name}' está vacía o no existe")

    def get_sqlite_tables(self) -> List[str]:
        """Obtiene lista de tablas relevantes de SQLite"""
        try:
            conn = sqlite3.connect(self.sqlite_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                AND name NOT LIKE 'sqlite_%'
                AND name NOT IN ('sqlite_sequence', 'sqlite_stat1')
                ORDER BY name
            """)
            
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            self.log(f"📋 Tablas encontradas en SQLite: {', '.join(tables)}")
            return tables
            
        except Exception as e:
            self.log(f"❌ Error obteniendo tablas de SQLite: {e}", "ERROR")
            return []

    def verify_migration(self, pg_cursor):
        """Verifica que la migración fue exitosa"""
        self.log("🔍 Verificando migración...")
        
        verification_queries = [
            "SELECT COUNT(*) FROM users",
            "SELECT COUNT(*) FROM clients", 
            "SELECT COUNT(*) FROM global_libraries",
            "SELECT COUNT(*) FROM scans",
            "SELECT COUNT(*) FROM libraries",
            "SELECT COUNT(*) FROM file_urls",
            "SELECT COUNT(*) FROM version_strings",
            "SELECT COUNT(*) FROM action_history"
        ]
        
        for query in verification_queries:
            try:
                pg_cursor.execute(query)
                count = pg_cursor.fetchone()[0]
                table_name = query.split('FROM ')[1]
                self.log(f"  ✅ {table_name}: {count} registros")
            except Exception as e:
                self.log(f"  ❌ Error verificando {query}: {e}", "ERROR")

    def run_migration(self):
        """Ejecuta la migración completa"""
        self.log("🚀 Iniciando migración SQLite → PostgreSQL")
        self.log(f"📂 Archivo SQLite: {self.sqlite_path}")
        self.log(f"🐘 PostgreSQL: {self.postgres_config['host']}:{self.postgres_config['port']}/{self.postgres_config['database']}")
        
        # Verificar que existe el archivo SQLite
        if not os.path.exists(self.sqlite_path):
            self.log(f"❌ No se encontró el archivo SQLite: {self.sqlite_path}", "ERROR")
            return False
        
        try:
            # Conectar a PostgreSQL
            pg_conn = psycopg2.connect(**self.postgres_config)
            pg_conn.autocommit = False  # Usar transacciones
            pg_cursor = pg_conn.cursor()
            
            self.log("✅ Conectado a PostgreSQL")
            
            # Crear esquema
            self.create_postgresql_schema(pg_cursor)
            pg_conn.commit()
            
            # Orden de migración (respetando foreign keys)
            migration_order = [
                'users',
                'clients', 
                'global_libraries',
                'scans',
                'libraries',
                'file_urls',
                'version_strings',
                'action_history'
            ]
            
            # Migrar cada tabla
            for table_name in migration_order:
                try:
                    self.migrate_table(pg_cursor, table_name)
                    pg_conn.commit()  # Commit después de cada tabla
                except Exception as e:
                    self.log(f"❌ Error migrando tabla {table_name}: {e}", "ERROR")
                    pg_conn.rollback()
                    # Continuar con la siguiente tabla
                    continue
            
            # Verificar migración
            self.verify_migration(pg_cursor)
            
            # Finalizar
            pg_conn.commit()
            pg_cursor.close()
            pg_conn.close()
            
            # Mostrar estadísticas finales
            duration = datetime.now() - self.stats['start_time']
            self.log("🎉 Migración completada exitosamente!")
            self.log(f"📊 Estadísticas finales:")
            self.log(f"  - Tablas migradas: {self.stats['tables_migrated']}")
            self.log(f"  - Total registros: {self.stats['total_records']}")
            self.log(f"  - Duración: {duration}")
            self.log(f"  - Errores: {len(self.stats['errors'])}")
            
            if self.stats['errors']:
                self.log("⚠️  Errores encontrados:")
                for error in self.stats['errors']:
                    self.log(f"    - {error}")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error general de migración: {e}", "ERROR")
            return False


def main():
    """Función principal"""
    print("=" * 60)
    print("🔄 MIGRADOR SQLite → PostgreSQL")
    print("📦 ntg-js-analyzer Database Migration Tool")
    print("=" * 60)
    
    # Configuración PostgreSQL (modificar según tu setup)
    postgres_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'database': os.getenv('POSTGRES_DB', 'ntg_analyzer'),
        'user': os.getenv('POSTGRES_USER', 'ntg_user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'ntg_password')
    }
    
    # Verificar variables de entorno
    print("\n📋 Configuración:")
    for key, value in postgres_config.items():
        if key == 'password':
            print(f"  {key}: {'*' * len(value)}")
        else:
            print(f"  {key}: {value}")
    
    print(f"\n📂 SQLite source: analysis.db")
    
    # Confirmar antes de proceder
    response = input("\n¿Proceder con la migración? (y/N): ").strip().lower()
    if response not in ['y', 'yes', 'sí', 'si']:
        print("❌ Migración cancelada por el usuario")
        return
    
    # Ejecutar migración
    migrator = DatabaseMigrator(
        sqlite_path="analysis.db",
        postgres_config=postgres_config
    )
    
    success = migrator.run_migration()
    
    if success:
        print("\n🎉 ¡Migración completada exitosamente!")
        print("\n📝 Próximos pasos:")
        print("  1. Verificar datos en PostgreSQL")
        print("  2. Configurar aplicación para usar PostgreSQL")
        print("  3. Realizar backup de analysis.db original")
        print("  4. Actualizar string de conexión en dashboard.py")
    else:
        print("\n❌ Migración falló. Revisa los logs arriba.")
        sys.exit(1)


if __name__ == "__main__":
    main()