# Plan de Migración Completa: Client → Project

## Problema Identificado

Se inició una migración parcial de "Cliente" a "Proyecto" pero no fue completada. Actualmente tenemos inconsistencias:

### ✅ Ya Migrado (Parcial)
- Rutas Flask: `/clients` → `/projects`
- Función de rutas: `client_detail()` → `project_detail()`
- Parámetros de rutas: `<int:client_id>` → `<int:project_id>`
- Algunas referencias en templates
- Terminología en UI: "Cliente" → "Proyecto"

### ❌ NO Migrado (Inconsistente)
- **Base de datos**: Tabla sigue siendo `clients`, columnas siguen siendo `client_id`
- **Templates**: Parámetros URL siguen usando `client_id`
- **JavaScript**: Classes y handlers siguen usando `client`
- **Data attributes**: siguen usando `data-client-*`
- **Variables Python**: siguen usando `client_id` internamente

## Fase 1: Análisis del Estado Actual

### Base de Datos (analysis.db)
```sql
-- TABLAS ACTUALES
CREATE TABLE clients (           -- ❌ Debe ser 'projects'
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    website TEXT,
    created_date TIMESTAMP,
    updated_date TIMESTAMP,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE scans (
    id INTEGER PRIMARY KEY,
    url TEXT,
    scan_date TIMESTAMP,
    status_code INTEGER,
    title TEXT,
    headers TEXT,
    client_id INTEGER           -- ❌ Debe ser 'project_id'
);
```

### Templates con Inconsistencias
- `templates/statistics.html:183` - `/?client_id=`
- `templates/manual_libraries_by_global.html:185` - `client_id=`
- `templates/scan_detail.html:246` - `/?client_id=`
- `templates/index.html:145` - `/?client_id=`
- `templates/index.html:391` - `/?client_id=`
- Todas las templates usan `data-client-*` attributes
- JavaScript classes: `bulk-edit-client-btn`

### Python Code (dashboard.py)
```python
# ❌ Variables y queries siguen usando client_id internamente
client_id_param = request.args.get('client_id', '')  # Línea 1000
where_conditions.append("s.client_id = ?")           # Múltiples líneas
cursor.execute('SELECT * FROM clients WHERE id = ?') # Múltiples líneas
```

## Fase 2: Plan de Migración Completa

### 2.1 Migración de Base de Datos

**Opción A: Renombrar Tablas y Columnas (Recomendado)**
```sql
-- Paso 1: Renombrar tabla
ALTER TABLE clients RENAME TO projects;

-- Paso 2: Renombrar columna en scans
ALTER TABLE scans RENAME COLUMN client_id TO project_id;

-- Paso 3: Verificar índices y foreign keys si existen
```

**Opción B: Crear Nuevas Tablas y Migrar Datos**
```sql
-- Crear nueva tabla projects
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    website TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1
);

-- Migrar datos
INSERT INTO projects SELECT * FROM clients;

-- Actualizar scans
ALTER TABLE scans ADD COLUMN project_id INTEGER;
UPDATE scans SET project_id = client_id;
ALTER TABLE scans DROP COLUMN client_id;

-- Eliminar tabla antigua
DROP TABLE clients;
```

### 2.2 Actualizar Código Python (dashboard.py)

#### Actualizaciones en Schema Creation
```python
# Cambiar líneas 271-281
CREATE TABLE IF NOT EXISTS projects (  # clients → projects
    ...
)

# Cambiar línea 284-289
# Add project_id column to scans table if it doesn't exist  # client_id → project_id
cursor.execute("SELECT project_id FROM scans LIMIT 1")     # client_id → project_id
cursor.execute("ALTER TABLE scans ADD COLUMN project_id INTEGER")  # client_id → project_id
```

#### Actualizaciones en Variables y Queries
```python
# Cambiar TODAS las instancias de:
client_id_param → project_id_param
s.client_id → s.project_id
clients c → projects p
LEFT JOIN clients → LEFT JOIN projects
FROM clients → FROM projects
WHERE client_id → WHERE project_id
cursor.execute('...clients...') → cursor.execute('...projects...')
```

### 2.3 Actualizar Templates

#### URL Parameters
```html
<!-- Cambiar TODOS los parámetros de URL -->
/?client_id=           → /?project_id=
&client_id=            → &project_id=
url_for('index', client_id=...) → url_for('index', project_id=...)
```

#### Data Attributes y Form Names
```html
<!-- Mantener data-client-* por compatibilidad con JS existente -->
<!-- PERO cambiar form field names -->
<select name="client_id">  → <select name="project_id">
<input name="client_id">   → <input name="project_id">
```

### 2.4 Actualizar JavaScript

#### Classes CSS y Event Handlers
```javascript
// secure_event_handlers.js
.bulk-edit-client-btn → .bulk-edit-project-btn
editClientForm → editProjectForm
deleteClientForm → deleteProjectForm
bulkEditClientModal → bulkEditProjectModal
scanClientSelect → scanProjectSelect
```

#### Data Attributes Handling
```javascript
// Mantener data-client-* attributes pero actualizar form field names
document.getElementById('scanClientSelect') → document.getElementById('scanProjectSelect')
```

### 2.5 Actualizar Static Files y CSS

```css
/* Cambiar cualquier referencia a client en CSS */
.client-card → .project-card
.client-list → .project-list
```

## Fase 3: Implementación por Pasos

### Paso 1: Preparación y Backup
```bash
# Backup base de datos
cp analysis.db analysis.db.backup.$(date +%Y%m%d_%H%M%S)

# Crear branch para migración
git checkout -b feature/complete-client-to-project-migration
```

### Paso 2: Migración de Base de Datos
1. Crear script de migración SQL
2. Actualizar schema creation en dashboard.py
3. Probar con base de datos de prueba

### Paso 3: Actualizar Python Code
1. Variables globales y parámetros de request
2. Queries SQL (FROM, JOIN, WHERE clauses)
3. Template context variables

### Paso 4: Actualizar Templates
1. URL parameters en todos los href y form actions
2. Form field names
3. JavaScript variable names y selectors

### Paso 5: Actualizar JavaScript y CSS
1. Event handler classes
2. Form IDs y selectors
3. Modal IDs

### Paso 6: Testing
1. Funcionalidad de proyectos (crear, editar, eliminar)
2. Asociación de scans con proyectos
3. Filtrado por proyecto
4. Export/Import de datos de proyecto
5. Todas las rutas y enlaces

## Fase 4: Archivos Afectados

### Python Files
- `dashboard.py` - Migración completa de schema y queries

### Templates
- `templates/index.html` - URL parameters, form fields
- `templates/clients.html` - Renombrar a `projects.html`, actualizar todo
- `templates/client_detail.html` - Renombrar a `project_detail.html`, actualizar todo
- `templates/scan_detail.html` - URL parameters
- `templates/statistics.html` - URL parameters
- `templates/manual_libraries_by_global.html` - URL parameters
- `templates/base.html` - Navigation links si aplica

### JavaScript Files
- `static/js/secure_event_handlers.js` - Classes y selectors
- `static/js/index.js` - Si tiene referencias a client
- `static/js/scan_detail.js` - Si tiene referencias a client

### CSS Files (si aplica)
- Cualquier archivo CSS con classes client-*

## Fase 5: Script de Migración de Base de Datos

```python
def migrate_clients_to_projects():
    """Migra la base de datos de clients a projects"""
    conn = sqlite3.connect('analysis.db')
    cursor = conn.cursor()
    
    try:
        # Verificar si ya fue migrado
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        if cursor.fetchone():
            print("✅ La migración ya fue ejecutada")
            return
        
        # Renombrar tabla clients a projects
        cursor.execute("ALTER TABLE clients RENAME TO projects")
        print("✅ Tabla clients renombrada a projects")
        
        # Renombrar columna client_id a project_id en scans
        cursor.execute("ALTER TABLE scans RENAME COLUMN client_id TO project_id")
        print("✅ Columna client_id renombrada a project_id en tabla scans")
        
        conn.commit()
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
```

## Fase 6: Checklist de Validación

### Base de Datos
- [ ] Tabla `clients` renombrada a `projects`
- [ ] Columna `client_id` renombrada a `project_id` en tabla `scans`
- [ ] Datos preservados correctamente
- [ ] Queries funcionando

### Python Code
- [ ] Variables `client_id_param` → `project_id_param`
- [ ] Queries `FROM clients` → `FROM projects`
- [ ] Queries `client_id` → `project_id`
- [ ] Template context variables actualizadas

### Templates
- [ ] URL parameters `client_id=` → `project_id=`
- [ ] Form field names actualizados
- [ ] Template file names cambiados
- [ ] Breadcrumbs y títulos actualizados

### JavaScript
- [ ] Classes CSS actualizadas
- [ ] Form IDs actualizados
- [ ] Event handlers actualizados

### Funcionalidad
- [ ] Crear proyecto funciona
- [ ] Editar proyecto funciona
- [ ] Eliminar proyecto funciona
- [ ] Asociar scan a proyecto funciona
- [ ] Filtrar por proyecto funciona
- [ ] Export/Import funciona
- [ ] Navegación completa funciona

## Riesgos y Consideraciones

### Riesgos
- **Data Loss**: Migración de base de datos puede fallar
- **Breaking Changes**: URLs existentes en bookmarks dejarán de funcionar
- **Testing**: Cambios masivos requieren testing exhaustivo

### Mitigaciones
- **Backup completo** antes de cualquier cambio
- **Testing en base de datos de prueba** primero
- **Migración por fases** con rollback plan
- **Documentación** de todos los cambios

## Conclusión

Esta migración es MASIVA y requiere cambios en:
- 1 tabla de base de datos
- 1 columna de foreign key
- ~50+ líneas de código Python
- ~20+ archivos de templates
- Múltiples archivos JavaScript
- Posibles archivos CSS

**Estimación**: 4-6 horas de trabajo + testing extensivo

**Recomendación**: Ejecutar en ambiente de desarrollo primero, con backup completo.