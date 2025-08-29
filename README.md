# Analizador de Seguridad Web - Detector de Vulnerabilidades JavaScript/CSS

## Descripción del Proyecto

Este proyecto es una **herramienta de análisis de seguridad web** especializada en la detección de librerías JavaScript y CSS vulnerables. Es una aplicación Flask de Python que escanea sitios web, identifica librerías desactualizadas o vulnerables, y proporciona un dashboard profesional para gestionar los resultados. La aplicación utiliza una base de datos SQLite para almacenar resultados de escaneos y cuenta con autenticación basada en roles para la gestión de usuarios y proyectos.

**🔧 Tecnologías Principales:**

*   **Backend:** Python 3.x, Flask 2.3.3
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
*   **Base de Datos:** SQLite con migraciones automáticas
*   **Contenedorización:** Docker, Podman
*   **Seguridad:** Flask-WTF (CSRF), Werkzeug (hash contraseñas), headers HTTP seguros

**🚀 Funcionalidades Core:**

*   **Dashboard Web Profesional:** Interfaz amigable con estadísticas en tiempo real, filtrado avanzado y operaciones en lote
*   **Análisis Automatizado de Librerías:** Detección automática de JavaScript (jQuery, React, Vue.js, Angular) y CSS (Bootstrap, Font Awesome)
*   **Detección de Vulnerabilidades:** Comparación con catálogo global de versiones seguras y alertas de seguridad
*   **Sistema de Reportes:** Exportación profesional en PDF, CSV y Excel con formato corporativo
*   **Gestión de Usuarios y Proyectos:** Soporte multi-usuario con roles (Administrador, Analista) y organización por proyectos empresariales
*   **API REST:** Acceso programático a datos de escaneos y estadísticas
*   **Análisis de Headers HTTP:** Evaluación de 7 headers de seguridad con puntuación automática
*   **Sistema de Estadísticas:** Página dedicada de estadísticas de vulnerabilidades con importación/exportación de datos

# 🚀 Instalación y Ejecución

## Desarrollo Local

1.  **Crear entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **⚠️ IMPORTANTE - Configurar clave secreta segura:**
    ```bash
    export FLASK_SECRET_KEY=$(openssl rand -hex 32)
    export FLASK_ENV=development  # Para desarrollo
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    python dashboard.py
    ```

La aplicación estará disponible en `http://localhost:5000`.

**Credenciales por defecto:** admin / admin123 (cambiar inmediatamente)

## 🐳 Producción (Docker/Podman) - RECOMENDADO

### Configuración Básica
1.  **Configurar variables de entorno seguras:**
    ```bash
    export FLASK_SECRET_KEY=$(openssl rand -hex 32)
    echo "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" > .env
    echo "FLASK_ENV=production" >> .env
    echo "FLASK_DEBUG=0" >> .env
    ```

2.  **Construir y ejecutar contenedor:**
    ```bash
    docker-compose up --build -d
    ```
    o con Podman:
    ```bash
    podman-compose up --build -d
    ```

### 🏢 Despliegue VPS Ubuntu Server (NUEVO)

**Despliegue completo en servidor VPS con persistencia y respaldos automáticos:**

```bash
# 1. Preparar servidor
sudo apt update && sudo apt install -y podman podman-compose sqlite3 git

# 2. Clonar repositorio
git clone <repository-url> ntg-js-analyzer
cd ntg-js-analyzer

# 3. Configurar persistencia
mkdir -p ~/ntg-js-analyzer/{data,logs,backups}
touch ~/ntg-js-analyzer/data/analysis.db

# 4. Configurar variables de entorno
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
echo "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" > .env
echo "FLASK_ENV=production" >> .env

# 5. Ejecutar con Podman
podman-compose up --build -d

# 6. Configurar respaldos automáticos (opcional)
# Ver DEPLOYMENT.md para scripts de backup completos
```

**Scripts incluidos para administración VPS:**
- `backup-database.sh` - Respaldo diario de BD
- `backup-to-github.sh` - Respaldo semanal a GitHub
- `auto-restart.sh` - Reinicio automático si falla
- `status-check.sh` - Verificación de estado del sistema

# 🛠️ Arquitectura y Convenciones de Desarrollo

## Estructura del Proyecto

*   **📁 Base de Datos:** SQLite (`analysis.db`) con creación y migración automática de schema
*   **🎨 Estilos:** CSS personalizado en `static/css/main.css` + Bootstrap 5
*   **⚡ Frontend:** JavaScript modular en `static/js/` (index.js, scan_detail.js)
*   **🖼️ Templates:** Plantillas Jinja2 en `templates/` con herencia de `base.html`
*   **🧠 Lógica Principal:** 
    - `analyzer.py` - Analizador de línea de comandos con protección SSRF
    - `dashboard.py` - Aplicación Flask web con autenticación y roles

## Schema de Base de Datos (7 Tablas)

- **`scans`** - Registros principales de análisis con headers HTTP y puntuación de seguridad
- **`libraries`** - Librerías detectadas con seguimiento de vulnerabilidades
- **`version_strings`** - Strings de versión en bruto encontrados en archivos
- **`file_urls`** - Archivos JS/CSS descubiertos durante el escaneo
- **`users`** - Cuentas de usuario con roles (Admin/Analista)
- **`projects`** - Proyectos/clientes empresariales (antes `clients`)
- **`global_libraries`** - Catálogo global de librerías con versiones seguras

## Sistema de Seguridad Integrado

### 🛡️ Protecciones Implementadas
- **Autenticación:** Hash Werkzeug + gestión segura de sesiones
- **CSRF:** Protección Flask-WTF en todos los formularios
- **SSRF:** Validación de URL + bloqueo de IPs privadas
- **Headers HTTP:** 7 headers de seguridad automáticos
- **Inyección SQL:** Consultas parametrizadas exclusivamente
- **Control de Acceso:** Roles diferenciados con decoradores `@admin_required`

### 🔍 Análisis de Vulnerabilidades
- **Detección Automática:** jQuery, React, Vue.js, Angular, Bootstrap, Font Awesome
- **Catálogo Global:** Base de datos centralizada de versiones seguras
- **Indicadores Visuales:** ⚠️ para versiones vulnerables en toda la UI
- **Puntuación de Seguridad:** Evaluación automática de headers HTTP (0-100%)

# 📊 Funcionalidades Avanzadas

## Sistema de Gestión de Usuarios y Roles

### 👥 Roles Disponibles
- **🔑 Administrador:** Acceso completo incluyendo gestión de usuarios, cambio de roles, CRUD usuarios
- **📊 Analista:** Acceso completo a proyectos, escaneos, catálogo global, importación de datos (excluye gestión de usuarios)

### 🔐 Funciones de Seguridad de Usuarios
- Cambio de contraseña de autoservicio
- Protección de rutas con decoradores específicos por rol
- Adaptación automática de UI basada en permisos

## Sistema de Estadísticas y Reportes

### 📈 Página de Estadísticas (NUEVO)
- **Búsqueda Avanzada:** Filtrado por librerías, versiones, y estados de revisión
- **Paginación:** Navegación eficiente para grandes conjuntos de datos
- **Import/Export:** Importación y exportación de estadísticas en CSV y JSON
- **Marcadores de Revisión:** Sistema para marcar escaneos como revisados

### 📄 Exportaciones Profesionales
- **PDF:** Reportes con formato corporativo usando ReportLab
- **Excel:** Libros multi-hoja con formato condicional y auto-sizing
- **CSV:** Formato estructurado por secciones con headers claros

## Sistema de Operaciones en Lote

### ⚡ Dashboard Avanzado
- **Selección Múltiple:** Checkboxes con función "Seleccionar Todo"
- **Contadores Dinámicos:** Botones contextuales que aparecen/desaparecen según selección
- **Modales de Confirmación:** Vista previa de elementos a eliminar
- **Preservación de Filtros:** Mantiene contexto de proyecto durante operaciones

---

# ❓ Preguntas Frecuentes (FAQ)

## ¿Cómo funciona la relación entre las librerías de un escaneo y el catálogo global?

**Respuesta:** Mediante asociación opcional.

- **🔗 Asociación:** Al añadir/editar una librería manual, puedes asociarla opcionalmente al Catálogo Global
- **📋 Vista de Detalle:**
  - Si está asociada: muestra versiones del catálogo global junto a las detectadas
  - Icono de enlace 🔗 indica asociación
  - ✅ aparece si las versiones coinciden con el catálogo global
- **🔒 Independencia:** Los datos del escaneo son independientes - cambiar el catálogo global NO afecta escaneos existentes

## ¿Cómo se detectan las vulnerabilidades?

**Criterio:** Una librería es vulnerable cuando:
- `versión_actual < última_versión_segura` 
- AND `versión_actual ≠ última_versión_segura`
- AND existe una `última_versión_segura` definida

## ¿Qué headers de seguridad se analizan?

Se evalúan **7 headers críticos:**
- `Strict-Transport-Security` (HSTS)
- `Content-Security-Policy` (CSP) 
- `X-Frame-Options`
- `X-XSS-Protection`
- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`

La **puntuación de seguridad** se calcula como porcentaje de headers presentes y correctamente configurados.

---

# 🚨 Consideraciones de Seguridad

## ⚠️ Antes de Despliegue en Producción

### Lista de Verificación Crítica
```bash
# 1. CRÍTICO: Eliminar archivos con credenciales
rm -f admin_credentials.txt

# 2. CRÍTICO: Generar clave secreta fuerte
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# 3. CRÍTICO: Configurar modo producción
export FLASK_ENV=production
export FLASK_DEBUG=0

# 4. Verificar configuración
echo "Verificar que no existan credenciales hardcodeadas"
grep -r "admin123\|password\|secret" . --exclude-dir=venv
```

### 🔐 Configuraciones de Seguridad Automáticas
- Headers HTTP seguros aplicados automáticamente
- Protección CSRF habilitada globalmente
- Validación SSRF en todas las URLs externas
- Limpieza automática de sesiones
- Hash seguro de contraseñas con Werkzeug

**🏆 Puntuación de Seguridad:** 7.5/10 (Listo para producción tras rotación de credenciales)
