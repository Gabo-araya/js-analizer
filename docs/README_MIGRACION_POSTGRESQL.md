# 🔄 Guía de Migración: SQLite → PostgreSQL

## 📋 Resumen

Este documento te guía paso a paso para migrar tu proyecto ntg-js-analyzer de SQLite a PostgreSQL usando el script automatizado `migrate_to_postgresql.py`.

## 🚀 Inicio Rápido

### 1. **Preparar PostgreSQL**

```bash
# Iniciar PostgreSQL con Docker
docker-compose -f docker-compose-postgres.yml up -d

# Verificar que está funcionando
docker-compose -f docker-compose-postgres.yml ps
```

### 2. **Instalar Dependencias PostgreSQL**

```bash
# Instalar nuevas dependencias
pip install -r requirements-postgres.txt

# O instalar manualmente las principales
pip install psycopg2-binary SQLAlchemy Flask-SQLAlchemy
```

### 3. **Ejecutar Migración**

```bash
# Ejecutar el script de migración
python migrate_to_postgresql.py

# El script te pedirá confirmación antes de proceder
```

### 4. **Verificar Migración**

Accede a Adminer en http://localhost:8080 para verificar los datos:
- **Sistema**: PostgreSQL
- **Servidor**: postgres  
- **Usuario**: ntg_user
- **Contraseña**: ntg_password
- **Base de datos**: ntg_analyzer

## 📊 ¿Qué Migra el Script?

### ✅ **Tablas Incluidas:**
- `users` → Usuarios del sistema
- `clients` → Clientes 
- `global_libraries` → Catálogo de librerías
- `scans` → Escaneos realizados
- `libraries` → Librerías detectadas
- `file_urls` → URLs de archivos encontrados
- `version_strings` → Strings de versión
- `action_history` → Historial de acciones (solo de analysis.db)

### 🔧 **Optimizaciones Aplicadas:**
- **JSONB nativo**: Headers de scans como JSONB en lugar de TEXT
- **Tipos BOOLEAN**: Campos como `reviewed`, `is_active`, `is_manual`
- **INET para IPs**: Campo `ip_address` usa tipo nativo INET
- **Foreign Keys reales**: Integridad referencial completa
- **Índices optimizados**: Para consultas frecuentes

### 📈 **Estadísticas Esperadas:**
```
Tablas migradas: 8
Total registros: ~7,000
Duración: 30-60 segundos
```

## ⚙️ Configuración Avanzada

### **Variables de Entorno**

```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=ntg_analyzer
export POSTGRES_USER=ntg_user
export POSTGRES_PASSWORD=tu_password_seguro
```

### **Configuración Personalizada**

Edita el script `migrate_to_postgresql.py` para cambiar:

```python
postgres_config = {
    'host': 'tu_servidor_postgres',
    'port': '5432',
    'database': 'tu_database',
    'user': 'tu_usuario',
    'password': 'tu_password'
}
```

## 🔍 Verificaciones Post-Migración

### **1. Verificar Estructura**

```sql
-- Conectar a PostgreSQL y verificar
\dt  -- Listar tablas
\d scans  -- Ver estructura de tabla scans
```

### **2. Verificar Datos**

```sql
-- Contar registros por tabla
SELECT 'scans' as tabla, COUNT(*) FROM scans
UNION ALL
SELECT 'libraries', COUNT(*) FROM libraries
UNION ALL  
SELECT 'users', COUNT(*) FROM users;
```

### **3. Verificar Integridad**

```sql
-- Verificar foreign keys
SELECT 
    COUNT(*) as total_scans,
    COUNT(client_id) as scans_con_cliente,
    COUNT(*) - COUNT(client_id) as scans_sin_cliente
FROM scans;
```

## 🚨 Resolución de Problemas

### **Error: "could not connect to server"**
```bash
# Verificar que PostgreSQL está corriendo
docker-compose -f docker-compose-postgres.yml ps

# Ver logs si hay problemas
docker-compose -f docker-compose-postgres.yml logs postgres
```

### **Error: "permission denied for database"**
```bash
# Recrear contenedor con permisos correctos
docker-compose -f docker-compose-postgres.yml down -v
docker-compose -f docker-compose-postgres.yml up -d
```

### **Error: "analysis.db not found"**
```bash
# Verificar que estás en el directorio correcto
ls -la analysis.db

# O especificar ruta completa en el script
sqlite_path = "/ruta/completa/a/analysis.db"
```

### **Error de codificación UTF-8**
Si hay problemas con caracteres especiales:

```python
# En migrate_to_postgresql.py, agregar al inicio:
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
```

## 📦 Estructura de Archivos Nuevos

```
ntg-js-analyzer/
├── migrate_to_postgresql.py      # Script de migración
├── docker-compose-postgres.yml   # PostgreSQL con Docker
├── requirements-postgres.txt     # Dependencias adicionales
└── README_MIGRACION_POSTGRESQL.md # Esta guía
```

## 🔧 Siguiente Paso: Configurar la Aplicación

Una vez completada la migración exitosamente, necesitarás:

1. **Actualizar dashboard.py** para usar PostgreSQL en lugar de SQLite
2. **Configurar SQLAlchemy** para connection pooling
3. **Actualizar funciones de conexión** de la aplicación

¿Quieres que cree también el código para adaptar dashboard.py a PostgreSQL?

## 📝 Notas Importantes

- ✅ **El script es idempotente**: Puede ejecutarse múltiples veces
- ✅ **Incluye verificaciones**: Valida datos antes y después
- ✅ **Respeta foreign keys**: Migra en el orden correcto
- ✅ **Maneja errores**: Continúa aunque falle una tabla
- ⚠️ **Backup recomendado**: Respalda analysis.db antes de migrar
- ⚠️ **Solo analysis.db**: Ignora history.db como solicitaste

---

*Migración automatizada para ntg-js-analyzer v2.0*