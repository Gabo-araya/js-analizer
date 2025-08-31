# CLAUDE.md

Este archivo proporciona orientación a Claude Code (claude.ai/code) cuando trabaja con código en este repositorio.

## Visión General del Proyecto

Esta es una **aplicación web Flask de Python enfocada en seguridad** que analiza sitios web para detectar versiones de librerías JavaScript y CSS, evaluar vulnerabilidades de seguridad, y proporcionar reportes integrales a través de un dashboard profesional. El sistema incluye:

1. **Web Scraper/Analizador** (`analyzer.py`) - Herramienta de línea de comandos para análisis automatizado de URLs con protección SSRF
2. **Dashboard Flask** (`dashboard.py`) - Interfaz web segura con autenticación basada en roles, gestión de clientes, protección CSRF, y reportes avanzados
3. **Capa de Seguridad** (`security_config.py`) - Configuraciones y validaciones de seguridad integrales
4. **Sistema de Gestión de Usuarios** - Control de acceso basado en roles con roles de Administrador y Analista
5. **Sistema de Gestión de Clientes** - Capacidades de organización y seguimiento de clientes empresariales

## Arquitectura de Seguridad (AUDITADA - Enero 2025)

### 🛡️ Funcionalidades de Seguridad Implementadas
- ✅ **Autenticación**: Hash de contraseñas Werkzeug, gestión segura de sesiones
- ✅ **Control de Acceso Basado en Roles**: Roles de Administrador y Analista con permisos diferenciados
- ✅ **Protección CSRF**: Flask-WTF con tokens en todos los formularios
- ✅ **Prevención de Inyección SQL**: Consultas parametrizadas exclusivamente
- ✅ **Protección SSRF**: Validación de URL, bloqueo de IP privadas, filtrado de puertos
- ✅ **Headers de Seguridad**: Headers HTTP de seguridad integrales vía `@app.after_request`
- ✅ **Validación de Entrada**: Sanitización y validación en todas las entradas de usuario
- ✅ **Configuración Segura**: Secretos basados en entorno, detección de producción
- ✅ **Gestión de Contraseñas**: Funcionalidad de cambio de contraseña de autoservicio

## Comandos Core

### Desarrollo y Ejecución
```bash
# ⚠️ SEGURIDAD PRIMERO: Configurar entorno seguro
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
export FLASK_ENV=production  # Para despliegue de producción
rm -f admin_credentials.txt  # Remover si existe

# Configurar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard web (interfaz principal)
python dashboard.py
# Se ejecuta en http://localhost:5000

# Ejecutar análisis de línea de comandos
python analyzer.py
# Lee URLs desde urls.txt y las analiza
```

### Despliegue de Producción (RECOMENDADO)
```bash
# Usar Podman/Docker para producción
podman-compose up --build -d
# Ver DEPLOYMENT.md para instrucciones completas
```

### Despliegue VPS Ubuntu Server (NUEVO)
```bash
# Despliegue completo en servidor VPS con persistencia y respaldos
# Ver DEPLOYMENT.md sección "Despliegue en VPS Ubuntu Server con Podman"

# Comandos clave para VPS:
# 1. Preparar servidor
sudo apt update && sudo apt install -y podman podman-compose sqlite3

# 2. Configurar persistencia
mkdir -p ~/js-analyzer/{data,logs,backups}
touch ~/js-analyzer/analysis.db

# 3. Configurar respaldos automáticos
# Ver scripts en DEPLOYMENT.md:
# - backup-database.sh (diario)
# - backup-to-github.sh (semanal a GitHub)
# - auto-restart.sh (monitoreo)
# - status-check.sh (diagnóstico)

# 4. Configurar cron para automatización
crontab -e
# 0 2 * * * - Backup diario BD
# 0 4 * * 6 - Backup semanal GitHub
# */15 * * * * - Auto-restart si falla
```

### Gestión de Base de Datos
```bash
# Resetear base de datos completamente (elimina analysis.db)
rm analysis.db
# La base de datos se recreará automáticamente en la próxima ejecución

# La migración manual de base de datos es automática - no se necesitan comandos
```

### Operaciones Docker
```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build

# Construir imagen independiente
docker build -t js-analyzer .

# Ejecutar con Podman (alternativa a Docker)
# Ver PODMAN_MANUAL.md para instrucciones detalladas
```

## Arquitectura

### Estructura de Aplicación
- **Arquitectura de dos niveles**: Aplicación web Flask + base de datos SQLite
- **Sistema de autenticación**: Login basado en sesión con gestión de usuarios basada en roles
- **Gestión de clientes**: Organización y seguimiento de clientes empresariales
- **Interfaz dual**: Dashboard web + analizador de línea de comandos
- **Sistema de exportación**: Generación PDF, CSV, Excel con formato profesional
- **Acceso basado en roles**: Roles de usuario Administrador y Analista con permisos diferenciados

### Schema de Base de Datos (7 tablas principales)
- **scans**: Registros principales de análisis (url, scan_date, status_code, title, headers JSON, client_id FK)
- **libraries**: Librerías detectadas con seguimiento de vulnerabilidades (scan_id FK, library_name, version, type, source_url, description, latest_safe_version, latest_version, is_manual)
- **version_strings**: Strings de versión en bruto encontrados en archivos (scan_id FK, file_url, file_type, line_number, line_content, version_keyword)
- **file_urls**: Todos los archivos JS/CSS descubiertos (scan_id FK, file_url, file_type, file_size, status_code)
- **users**: Cuentas de usuario con roles (username, password_hash, role)
- **clients**: Organizaciones cliente (name, contact_info, is_active)
- **global_libraries**: Catálogo global de librerías (library_name, description, latest_safe_version, latest_version, library_type)

### Sistema de Análisis de Seguridad
- **Análisis de headers de seguridad HTTP**: 7 headers evaluados (HSTS, CSP, X-Frame-Options, X-XSS-Protection, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
- **Lógica de detección de vulnerabilidades**: Muestra ⚠️ cuando version_actual < latest_safe_version Y actual != latest_safe Y latest_safe existe
- **Puntuación de seguridad**: Puntajes basados en porcentajes con recomendaciones específicas

### Motor de Detección de Librerías
**Detección Automática (`analyzer.py`):**
- `detect_js_libraries()`: jQuery, React, Vue.js, Angular, Bootstrap JS vía patrones script src
- `detect_css_libraries()`: Bootstrap CSS, Font Awesome vía patrones link href
- `scan_file_for_versions()`: Descarga archivos JS/CSS y busca strings de versión usando regex
- `get_all_js_css_files()`: Extrae todas las URLs de script y stylesheet desde HTML

**Gestión Manual (`dashboard.py`):**
- Agregar/editar/eliminar librerías con metadata rica
- Seguimiento de versiones (actual vs latest_safe vs latest_available)
- Indicadores de vulnerabilidades en todas las interfaces y exportaciones

### Arquitectura de Rutas Flask
**Rutas de Análisis Core:**
- `/`: Dashboard con estadísticas, filtrado por cliente, y herramientas de análisis en lotes
- `/scan/<id>`: Vista detallada de análisis (6 secciones de datos)
- `/analyze-url` (POST): Análisis de URL individual
- `/batch-analyze` (POST): Análisis de múltiples URLs

**Rutas de Autenticación:**
- `/login`: Autenticación basada en sesión
- `/logout`: Limpieza de sesión
- `/users`: Interfaz de gestión de usuarios (solo admin)
- `/change_own_password` (POST): Cambio de contraseña de autoservicio

**Rutas de Gestión de Clientes:**
- `/clients`: Interfaz CRUD de clientes
- `/add_client` (POST): Crear nuevo cliente
- `/edit_client/<id>` (POST): Actualizar información de cliente
- `/delete_client/<id>` (POST): Remover cliente

**Rutas de Gestión de Usuarios (Solo Admin):**
- `/add_user` (POST): Crear nuevos usuarios
- `/change_password/<id>` (POST): Reset de contraseña por admin
- `/change_role/<id>` (POST): Modificar roles de usuario
- `/delete_user/<id>` (POST): Remover usuarios

**Rutas de Gestión de Librerías:**
- `/add-manual-library` (POST): Agregar librerías personalizadas
- `/edit-library/<id>` (POST): Actualizar información de librería
- `/delete-library/<id>` (POST): Remover librerías
- `/global-libraries`: Gestión del catálogo global de librerías

**Rutas de Exportación:**
- `/export/pdf/<scan_id>`: Reportes PDF profesionales con ReportLab
- `/export/csv/<scan_id>`: Exportación CSV estructurada
- `/export/excel/<scan_id>`: Libros Excel multi-hoja con OpenPyXL
- `/export/clients/csv`: Exportación de datos de clientes
- `/export-statistics/csv`: Exportación de estadísticas de vulnerabilidades (CSV)
- `/export-statistics/json`: Exportación de estadísticas de vulnerabilidades (JSON)
- `/import-statistics` (POST): Importación de datos de estadísticas

**Endpoints API:**
- `/api/scans`, `/api/libraries`, `/api/version-strings`, `/api/stats`: Acceso a datos JSON
- `/api/clients`: Acceso API a datos de clientes

**Rutas de Estadísticas:**
- `/statistics`: Página de estadísticas de vulnerabilidades con búsqueda y paginación
- `/toggle_reviewed/<scan_id>` (POST): Marcar/desmarcar escaneo como revisado

### Flujo de Datos
1. Autenticación de usuario con control de acceso basado en roles
2. Asignación de cliente y configuración de organización
3. Análisis de URL vía interfaz web o procesamiento en lotes por línea de comandos
4. Parsing HTML con BeautifulSoup para extraer tags script/link
5. Descarga de archivos JS/CSS y escaneo de contenido para patrones de versión
6. Análisis de headers HTTP con algoritmo de puntuación de seguridad
7. Evaluación de vulnerabilidades con comparación de catálogo global de librerías
8. Almacenamiento en base de datos con migración automática de schema
9. Dashboard web proporciona operaciones CRUD con acciones en lote y filtrado por cliente
10. Generación de exportación con formato profesional y reportes específicos por cliente

## Estructura de Archivos Template y Estáticos

### Arquitectura Frontend
- **Diseño responsivo basado en Bootstrap** con mejoras CSS personalizadas
- **Interactividad JavaScript**:
  - `static/js/index.js`: Funcionalidad del dashboard, operaciones en lote, contadores dinámicos
  - `static/js/scan_detail.js`: Interacciones de detalles de escaneo, gestión de modales
- **Herencia de templates**:
  - `base.html`: Navegación con menús basados en roles, mensajes flash, layout común, modal de cambio de contraseña propio
  - `index.html`: Dashboard con estadísticas, filtrado por cliente, y herramientas de análisis
  - `scan_detail.html`: Análisis integral de escaneo con 6 secciones de datos
  - `login.html`: Interfaz de autenticación en español chileno con íconos Bootstrap
  - `users.html`: Gestión de usuarios con administración de roles (solo admin)
  - `clients.html`: Interfaz de gestión de clientes
  - `statistics.html`: Página de estadísticas de vulnerabilidades con import/export (NUEVO)
  - `global_libraries.html`: Gestión del catálogo global de librerías

### Patrones de Templates Jinja2
- Usar `default(0)` no `default:0` para valores por defecto de filtros
- Visualización de puntuación de seguridad: `{{ security_analysis.security_score }}%` (sin punto y coma en style)
- Indicadores de vulnerabilidades: patrón `{% if condition %} ⚠️ {% endif %}` en todos los templates
- Renderizado condicional basado en roles: `{% if session.user_role == 'admin' %}` para contenido solo de admin
- Traducción a español chileno en todos los templates con íconos Bootstrap
- Preservación de parámetros URL: Usar campos ocultos de formulario para mantener client_id y filtros de búsqueda

## Funcionalidades Clave y Detalles de Implementación

### Sistema de Control de Acceso Basado en Roles
- **Dos roles de usuario**: Administrador y Analista con permisos diferenciados
- **Privilegios de Administrador**: Acceso completo incluyendo gestión de usuarios, cambios de rol, creación/eliminación de usuarios
- **Privilegios de Analista**: Acceso completo a clientes, escaneos, catálogo global, importaciones de datos (excluye gestión de usuarios)
- **Protección de rutas**: Decoradores específicos por rol (`@admin_required`) para operaciones restringidas
- **Adaptación de UI**: Visibilidad de menú basada en roles y acceso a funcionalidades

### Sistema de Gestión de Clientes
- **Operaciones CRUD completas**: Crear, leer, actualizar, eliminar clientes
- **Asignación de cliente**: Asociar escaneos con clientes específicos
- **Capacidades de filtrado**: Filtrado del dashboard por cliente con preservación de parámetros URL
- **Seguimiento de estadísticas**: Métricas específicas por cliente y resúmenes de análisis
- **Organización de datos**: Organización jerárquica para entornos empresariales

### Sistema de Operaciones en Lotes
- **Selección basada en checkbox** con funcionalidad "Seleccionar Todo"
- **Contadores dinámicos**: Botones "Eliminar Seleccionados (X)" aparecen/desaparecen basado en selección
- **Modales de confirmación** con vista previa de elementos a eliminar
- **Modos de operación independientes**: Botones de eliminación individual coexisten con operaciones en lote
- **Preservación de filtrado por cliente**: Mantiene contexto de cliente durante operaciones en lote

### Arquitectura del Sistema de Exportación
- **PDF**: ReportLab con estilo profesional de tablas, análisis de seguridad, indicadores de vulnerabilidades
- **CSV**: Formato separado por secciones con headers claros para cada tipo de datos
- **Excel**: Libros multi-hoja con formato condicional, auto-sizing, headers con estilo
- **Exportaciones específicas por cliente**: Exportaciones filtradas basadas en asignación de cliente

### Sistema de Autenticación
- **Login basado en sesión** con patrón decorador (`@login_required`)
- **Autorización basada en roles**: Decorador `@admin_required` para funciones administrativas
- **Tabla de usuarios** con hash de contraseñas usando seguridad Werkzeug
- **Cambio de contraseña de autoservicio**: Los usuarios pueden cambiar sus propias contraseñas
- **Protección de rutas**: Todas las rutas principales decoradas con `@login_required`
- **Protección CSRF**: Tokens CSRF Flask-WTF en formularios

### Mejora de Evaluación de Vulnerabilidades
- **Contadores de vulnerabilidades del dashboard**: Mostrar conteos de vulnerabilidades por escaneo en listado
- **Catálogo global de librerías**: Gestión centralizada de definiciones de librerías y versiones seguras
- **Detección mejorada**: Identificación mejorada de vulnerabilidades con comparación de catálogo

### Patrón de Migración de Base de Datos
La aplicación maneja automáticamente actualizaciones de schema:
```python
# Patrón usado para agregar nuevas columnas (tablas users, clients, global_libraries)
try:
    cursor.execute("SELECT role FROM users LIMIT 1")
except sqlite3.OperationalError:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'admin'")

# Patrón de creación de nueva tabla
cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    contact_info TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
```

## Patrones de Desarrollo

### Agregar Nuevos Roles de Usuario
Extender sistema de roles en `dashboard.py`:
```python
# Agregar nuevo decorador de verificación de rol
def new_role_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        user_role = session.get('user_role', '')
        if user_role not in ['admin', 'nuevo_rol']:
            flash('Acceso denegado', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
```

### Agregar Funcionalidades Específicas por Cliente
Implementar filtrado por cliente en rutas:
```python
# Patrón estándar de filtrado por cliente
client_id_param = request.args.get('client_id')
where_clause = "WHERE 1=1"
query_params = []

if client_id_param and client_id_param != 'null':
    where_clause += " AND s.client_id = ?"
    query_params.append(int(client_id_param))
elif client_id_param == 'null':
    where_clause += " AND s.client_id IS NULL"
```

### Agregar Nueva Detección de Librerías
Extender funciones de detección en `analyzer.py`:
```python
# Agregar a detect_js_libraries() o detect_css_libraries()
new_lib_scripts = soup.find_all('script', src=re.compile(r'nombre-libreria', re.I))
for script in new_lib_scripts:
    # Extraer versión usando patrones regex
    # Agregar a lista de librerías con formato estándar
```

### Configuración de Headers de Seguridad
Extender `analyze_security_headers()` en `dashboard.py`:
```python
security_headers = {
    'nuevo-header': {
        'name': 'Nuevo-Header',
        'description': 'Descripción del header',
        'recommendation': 'Valor recomendado'
    }
}
```

### Patrones de Manejo de Errores
- **Bloques try-catch** alrededor de todas las requests externas y operaciones de base de datos
- **Mensajes de error amigables** vía sistema flash() de Flask
- **Degradación gradual** para fallos de red y errores de parsing
- **Manejo de timeout de requests** con delays configurables para operaciones en lote

## Rendimiento y Limitaciones

### Restricciones Actuales
- **Límite de análisis de archivos**: Primeros 10 archivos JS/CSS por sitio para prevenir descargas excesivas
- **Delays de requests**: Delays incorporados para operaciones en lote para evitar sobrecargar sitios objetivo
- **Gestión de memoria**: Descargas de archivos grandes tienen límites de tamaño para prevenir problemas de memoria

### Rendimiento de Base de Datos
- **SQLite con indexado apropiado** en foreign keys y columnas consultadas frecuentemente
- **Gestión de conexiones**: Limpieza apropiada y manejo de timeouts
- **Eliminaciones en cascada**: Eliminación de escaneo remueve todos los registros relacionados automáticamente

## Configuración de Seguridad (CRÍTICA)

### ⚠️ Lista de Verificación de Seguridad Pre-Producción
```bash
# 1. Generar clave secreta segura
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# 2. Remover archivos sensibles
rm -f admin_credentials.txt

# 3. Configurar entorno de producción
export FLASK_ENV=production
export FLASK_DEBUG=0

# 4. Verificar configuración segura
grep -E "(SECRET_KEY|DEBUG|FLASK_ENV)" .env
```

### Configuración de Seguridad Flask
- **Clave Secreta**: DEBE usar clave fuerte basada en entorno (`FLASK_SECRET_KEY`)
- **Modo Debug**: DESHABILITADO en producción (`FLASK_ENV=production`)
- **Seguridad de Sesión**: HTTPOnly, Secure (HTTPS), SameSite=Lax
- **Protección CSRF**: Habilitada globalmente con Flask-WTF
- **Validación de Requests**: Todas las URLs externas validadas para protección SSRF

### Headers de Seguridad Aplicados (dashboard.py:2015-2042)
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "politica-restrictiva"
    # + Más headers de seguridad
```

### Dependencias (Auditadas por Seguridad)
- **Core**: Flask 2.3.3, BeautifulSoup4 4.12.2, requests 2.32.4
- **Exportación**: ReportLab 4.0.4, OpenPyXL 3.1.2, Pandas 2.3.1
- **Seguridad**: Flask-WTF 1.2.1 para protección CSRF, Werkzeug para hash de contraseñas
- **Parsing**: lxml 4.9.3 para procesamiento XML/HTML
- **Endurecidas**: pillow>=10.3.0, urllib3>=2.5.0 (versiones aseguradas por Snyk)

## Resultados de Auditoría de Seguridad (Enero 2025)

### ✅ FORTALEZAS DE SEGURIDAD
1. **Autenticación y Sesiones**: Implementación robusta con hash Werkzeug
2. **Protección CSRF**: Flask-WTF apropiadamente implementado en todos los formularios
3. **Inyección SQL**: Consultas parametrizadas usadas exclusivamente
4. **Protección SSRF**: Validación integral de URL con bloqueo de IP privadas
5. **Headers HTTP**: Implementación completa de headers de seguridad
6. **Validación de Entrada**: Patrones apropiados de sanitización y validación

### ⚠️ VULNERABILIDADES DE SEGURIDAD IDENTIFICADAS
1. **CRÍTICA**: Credenciales expuestas en `admin_credentials.txt`
2. **ALTA**: Clave secreta débil en archivos ejemplo `.env`
3. **MEDIA**: Información de debug en logs de consola
4. **BAJA**: Implementación de rate limiting faltante

### 🚨 REMEDIACIÓN INMEDIATA REQUERIDA
```bash
# 1. Remover credenciales expuestas (CRÍTICA)
rm -f admin_credentials.txt

# 2. Generar clave secreta fuerte (ALTA)
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# 3. Configurar entorno de producción (MEDIA)
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### 🔒 Puntuación de Seguridad: 7.5/10
- **Arquitectura Defensiva**: Excelente
- **Calidad de Implementación**: Muy Buena
- **Seguridad de Configuración**: Necesita Mejora
- **Evaluación General**: Listo para producción después de rotación de credenciales

## Guías de Seguridad para Desarrollo

### Al Trabajar con Este Codebase:
1. **SIEMPRE** verificar secretos hardcodeados antes de commits
2. **NUNCA** hacer commit de archivos `.env` o archivos de credenciales
3. **VERIFICAR** protección SSRF al agregar procesamiento de URLs
4. **ASEGURAR** tokens CSRF en nuevos formularios
5. **USAR** consultas SQL parametrizadas exclusivamente
6. **VALIDAR** todas las entradas de usuario con sanitización
7. **PROBAR** headers de seguridad después de cambios de rutas

## Despliegue de Producción

### Usar Despliegue Containerizado (Recomendado)
- Ver `DEPLOYMENT.md` para instrucciones completas de Podman/Docker
- Configuración de seguridad automatizada
- Entorno aislado con persistencia de volúmenes
- Logging y monitoreo de grado de producción

### 🏢 Despliegue VPS Ubuntu Server (NUEVO - v2.1)
- **Persistencia completa** de base de datos SQLite con volúmenes Docker/Podman
- **Sistema de respaldos automáticos**:
  - Respaldos diarios locales con retención configurable
  - Respaldos semanales a GitHub en rama `database-backups`
  - Scripts automatizados con cron para ejecución programada
- **Monitoreo y alta disponibilidad**:
  - Verificación de salud cada 15 minutos con auto-restart
  - Sistema de diagnóstico completo (`status-check.sh`)
  - Logs centralizados en directorio persistente
- **Actualizaciones automatizadas**:
  - Script de actualización desde GitHub (`update-from-github.sh`)
  - Preservación de configuración durante actualizaciones
  - Rollback automático en caso de fallas
- **Seguridad VPS**:
  - Configuración fail2ban para protección contra ataques
  - Soporte SSL/TLS con Let's Encrypt
  - Firewall UFW preconfigurado
  - Usuario dedicado sin privilegios root
- **Scripts de administración incluidos**:
  ```bash
  # Estructura de scripts VPS:
  ~/js-analyzer/
  ├── backup-database.sh      # Backup diario SQLite
  ├── backup-to-github.sh     # Backup semanal a GitHub
  ├── update-from-github.sh   # Actualización automática
  ├── status-check.sh         # Monitoreo sistema
  └── auto-restart.sh         # Reinicio automático
  ```

Ver sección **"🏢 Despliegue en VPS Ubuntu Server con Podman"** en `DEPLOYMENT.md` para instrucciones paso a paso.
