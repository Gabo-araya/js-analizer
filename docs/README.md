# 🛡️ NTG JavaScript & CSS Library Analyzer

Una aplicación Python completa para **análisis de seguridad web** que detecta versiones de librerías JavaScript y CSS, evalúa vulnerabilidades de seguridad, y proporciona herramientas avanzadas de gestión y exportación de datos a través de un dashboard web profesional con **autenticación basada en roles** y **gestión empresarial de clientes**.

[![Security Status](https://img.shields.io/badge/Security-Audited-green)]() 
[![Python](https://img.shields.io/badge/Python-3.8+-blue)]() 
[![Flask](https://img.shields.io/badge/Flask-2.3.3-lightblue)]() 
[![License](https://img.shields.io/badge/License-Open_Source-orange)]()

## ✨ Características Principales

### 🔐 Sistema de Autenticación y Roles
- ✅ **Autenticación segura** con hash de contraseñas Werkzeug
- ✅ **Roles de usuario**: Administrador y Analista con permisos diferenciados
- ✅ **Protección CSRF** completa en todos los formularios
- ✅ **Cambio de contraseña propia** para todos los usuarios
- ✅ **Gestión de usuarios** (solo administradores)

### 🏢 Gestión Empresarial de Clientes
- ✅ **CRUD completo** de clientes empresariales
- ✅ **Asignación de escaneos** a clientes específicos
- ✅ **Filtrado por cliente** en dashboard con preservación de contexto
- ✅ **Estadísticas por cliente** y reportes específicos
- ✅ **Exportación de datos** filtrada por cliente

### 🔍 Análisis Automático
- ✅ **Detección automática** de librerías JavaScript (jQuery, React, Vue.js, Angular, Bootstrap JS)
- ✅ **Detección de frameworks CSS** (Bootstrap, Font Awesome)
- ✅ **Análisis de archivos JS/CSS** con búsqueda de strings de versión
- ✅ **Captura de cabeceras HTTP** y análisis de seguridad

### 🛡️ Evaluación de Vulnerabilidades Mejorada
- ✅ **Detección visual de vulnerabilidades** con indicadores ⚠️
- ✅ **Contadores de vulnerabilidades** en listados de escaneos
- ✅ **Catálogo global de librerías** para comparación de versiones
- ✅ **Análisis de cabeceras de seguridad** (HSTS, CSP, X-Frame-Options, etc.)
- ✅ **Puntuación de seguridad** basada en headers presentes/ausentes

### 📊 Gestión Avanzada de Librerías
- ✅ **Catálogo global** centralizado de definiciones de librerías
- ✅ **Agregar librerías manualmente** no detectadas automáticamente
- ✅ **Editar información de librerías** (descripciones, versiones seguras)
- ✅ **Seguimiento de versiones** (actual, última segura, última disponible)
- ✅ **Eliminación individual y por lotes** con confirmaciones

### 📈 Dashboard Web Profesional
- ✅ **Interface moderna** con autenticación basada en roles
- ✅ **Menús adaptivos** según privilegios de usuario
- ✅ **Filtrado avanzado** por cliente con preservación de parámetros URL
- ✅ **Análisis desde web** (URLs individuales y por lotes)
- ✅ **Operaciones batch** con checkboxes y contadores dinámicos
- ✅ **Modales de confirmación** para todas las operaciones críticas

### 📄 Exportación Avanzada
- ✅ **Reportes PDF** profesionales con tablas y estilos
- ✅ **Exportación CSV** completa con todas las secciones
- ✅ **Libros Excel** multi-hoja con formato automático
- ✅ **Exportaciones específicas por cliente**
- ✅ **Información de vulnerabilidades** en todos los formatos

### 🔌 API REST Expandida
- ✅ **Endpoints completos** para acceso programático
- ✅ **Datos estructurados** en JSON
- ✅ **Estadísticas en tiempo real** del dashboard
- ✅ **API de clientes** para gestión externa
- ✅ **Filtrado por cliente** en endpoints API

### 📜 Sistema de Historial Avanzado
- ✅ **Base de datos separada** (history.db) para máximo rendimiento
- ✅ **Cero conflictos de concurrencia** en operaciones críticas
- ✅ **Historial completo** de todas las acciones CRUD del sistema
- ✅ **Filtros avanzados** por usuario, acción, tabla, fecha y búsqueda libre
- ✅ **Funcionalidad de deshacer** para cambios críticos
- ✅ **Exportación de historial** en Excel, CSV y PDF
- ✅ **Arquitectura escalable** con limpieza automática de registros antiguos

## 🚀 Instalación y Despliegue

> **🐳 RECOMENDADO: Despliegue con Podman/Docker**  
> Para producción, usa las **[📋 Instrucciones de Despliegue Completas](./DEPLOYMENT.md)**

### ⚡ Inicio Rápido (Desarrollo Local)

#### 1. Clonar el proyecto
```bash
git clone https://github.com/gabo-ntg/ntg-js-analyzer.git
cd ntg-js-analyzer
```

#### 2. Crear entorno virtual y instalar dependencias
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Configurar seguridad y logging (IMPORTANTE)
```bash
# Generar clave secreta segura
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
# Eliminar archivo de credenciales si existe
rm -f admin_credentials.txt
# Habilitar sistema de historial con BD separada
source logging_config.sh
```

#### 4. Ejecutar aplicación
```bash
# Con sistema de historial habilitado
source logging_config.sh && python dashboard.py
# Acceder a: http://localhost:5000
```

### 🐳 Despliegue en Producción (Recomendado)

#### Con Podman Compose
```bash
# Clonar y configurar
git clone https://github.com/gabo-ntg/ntg-js-analyzer.git
cd ntg-js-analyzer

# Configurar entorno seguro
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
echo "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" > .env
echo "FLASK_ENV=production" >> .env

# Desplegar
podman-compose up --build -d
```

📋 **Ver [DEPLOYMENT.md](./DEPLOYMENT.md) para instrucciones completas de producción**

## 🎯 Uso

### Método 1: Análisis Web (Recomendado)
1. **Iniciar el dashboard**:
   ```bash
   # Con sistema de historial habilitado
   source logging_config.sh && python dashboard.py
   ```

2. **Abrir navegador**: http://localhost:5000

3. **Iniciar sesión**: 
   - **Usuario por defecto**: `gabo`
   - **Contraseña por defecto**: `admin123`
   - **Rol**: Administrador (acceso completo)

4. **Gestión de usuarios** (solo administradores):
   - Crear usuarios con rol Administrador o Analista
   - Cambiar roles de usuarios existentes
   - Cambiar contraseñas de otros usuarios
   - Eliminar usuarios del sistema

5. **Gestión de clientes**:
   - Crear, editar y eliminar clientes empresariales
   - Asignar escaneos a clientes específicos
   - Filtrar análisis por cliente en el dashboard

6. **Opciones de análisis**:
   - **URL Individual**: Botón "➕ Analizar URL"
   - **Análisis por lotes**: Botón "📝 Análisis Masivo" (multiple URLs, una por línea)
   - **Asignación de cliente**: Seleccionar cliente al crear escaneos
   - **Soporte para comentarios**: Líneas que empiecen con # son ignoradas

### Método 2: Análisis por Línea de Comandos
1. **Configurar URLs** en `urls.txt`:
   ```
   https://getbootstrap.com
   https://jquery.com
   https://reactjs.org
   # Este es un comentario
   https://vuejs.org
   ```

2. **Ejecutar análisis**:
   ```bash
   # 🆕 Usando CLI modular
   python cli.py analyze --urls-file urls.txt --delay 1.0
   
   # Método antiguo (aún funciona)
   python scripts/analyzer_cli.py
   ```

### 🔧 Gestión Manual de Librerías

#### Agregar Librería Manual
1. En "Scan Details", click **"➕ Add Manual Library"**
2. Completar formulario:
   - **Nombre** (requerido)
   - **Tipo**: JavaScript o CSS
   - **Versión actual** encontrada en el sitio
   - **Última versión segura** (para detección de vulnerabilidades)
   - **Última versión disponible**
   - **Descripción** opcional

#### Editar Librerías
- Click **✏️** en cualquier librería (auto-detectada o manual)
- Modificar campos necesarios
- **Guardar cambios**

#### Detección de Vulnerabilidades
El sistema muestra **⚠️ badges rojos** cuando:
- Existe una versión segura conocida **Y**
- La versión actual es **diferente** a la segura **Y** 
- La versión actual es **menor** que la segura

## 📊 Secciones del Dashboard

### Página Principal
- **Autenticación y roles**: Menú de usuario con rol visible y cambio de contraseña
- **Estadísticas generales**: Total de análisis, librerías, archivos, clientes
- **Estadísticas adicionales**: Catálogo global, cobertura, actividad reciente
- **Filtros avanzados**: Por cliente con preservación de contexto
- **Análisis recientes**: Últimos escaneos con contadores de vulnerabilidades
- **Herramientas**: Análisis individual, por lotes, reset de BD

### Historial de Acciones (`/historial`) - Nuevo
- **Base de datos independiente**: Sistema de historial con BD separada para máximo rendimiento
- **Registro completo**: Todas las acciones CRUD (crear, actualizar, eliminar) del sistema
- **Filtros avanzados**: Por usuario, tipo de acción, tabla, rango de fechas y búsqueda libre
- **Funcionalidad de deshacer**: Revertir cambios críticos con validación de integridad
- **Exportación completa**: Excel, CSV y PDF con historial filtrado
- **Rendimiento optimizado**: Cero conflictos con operaciones de análisis principales

### Gestión de Usuarios (`/users`) - Solo Administradores
- **Lista de usuarios**: Con roles y acciones disponibles
- **Crear usuarios**: Formulario con selección de rol (Administrador/Analista)
- **Cambiar contraseñas**: Reset de contraseñas de otros usuarios
- **Cambiar roles**: Modificar permisos de usuarios existentes
- **Eliminar usuarios**: Con confirmación y validaciones de seguridad

### Gestión de Clientes (`/clients`)
- **Lista de clientes**: Con estadísticas y estado activo
- **CRUD completo**: Crear, editar, eliminar clientes empresariales
- **Estadísticas por cliente**: Contadores de escaneos y análisis
- **Filtrado**: Búsqueda y organización de clientes

### Catálogo Global (`/global-libraries`)
- **Definiciones centralizadas**: Librerías con versiones seguras conocidas
- **Gestión completa**: Agregar, editar, eliminar definiciones
- **Métricas de cobertura**: Estadísticas del catálogo vs detecciones

### Detalles de Análisis (`/scan/<id>`)
1. **📋 Información del Scan**: URL, título, estado, fecha, cliente asignado, contadores
2. **📚 Librerías Detectadas**: Con indicadores de vulnerabilidades mejorados y acciones
3. **📁 Archivos JS/CSS**: Todos los archivos encontrados con tamaños y estados
4. **🔍 Version Strings**: Líneas de código que contienen "version" o "versión"
5. **🌐 Cabeceras HTTP**: Headers completos de la respuesta
6. **🛡️ Análisis de Seguridad**: Headers presentes/faltantes con puntuación

### 📊 Exportaciones
Acceder via **"📊 Export Report"** dropdown:

#### PDF Report
- **Contenido**: Información completa en formato profesional
- **Incluye**: Tablas con librerías, análisis de seguridad, datos técnicos
- **Formato**: Tablas estilizadas, indicadores de vulnerabilidades

#### CSV Export  
- **Contenido**: Todos los datos en formato estructurado
- **Secciones**: Scan info, librerías, archivos, version strings, headers
- **Formato**: Separado por secciones con headers claros

#### Excel Workbook
- **6 hojas separadas**:
  1. **Scan Overview**: Resumen general
  2. **Libraries**: Librerías con vulnerabilidades
  3. **Security Analysis**: Headers de seguridad
  4. **JS CSS Files**: Archivos encontrados
  5. **Version Strings**: Strings de versión
  6. **HTTP Headers**: Headers completos
- **Formato profesional**: Colores, auto-ajuste de columnas, headers estilizados

## 🗂️ Estructura del Proyecto (Modularizada v3.0)

### 🆕 Estructura Modular del Proyecto
```
ntg-js-analyzer/
├── app/                   # 📦 Paquete principal modularizado
│   ├── __init__.py       # Factory Flask con blueprints
│   ├── models/           # Modelos de datos ORM-style
│   │   ├── scan.py       # Modelo de escaneos
│   │   ├── library.py    # Modelo de librerías
│   │   ├── user.py       # Modelo de usuarios
│   │   ├── client.py     # Modelo de clientes
│   │   └── history.py    # Modelo de historial
│   ├── services/         # Servicios de lógica de negocio
│   │   ├── analyzer_service.py    # Servicio de análisis
│   │   ├── security_analyzer.py   # Análisis de seguridad
│   │   ├── export_service.py      # Exportaciones
│   │   ├── history_manager.py     # Gestión de historial
│   │   └── library_detector.py    # Detección de librerías
│   ├── views/            # Blueprints organizados
│   │   ├── auth.py       # Autenticación
│   │   ├── main.py       # Dashboard principal
│   │   ├── scans.py      # Gestión de escaneos
│   │   ├── api.py        # Endpoints API
│   │   ├── exports.py    # Exportaciones
│   │   ├── clients.py    # Gestión de clientes
│   │   ├── users.py      # Gestión de usuarios
│   │   └── history.py    # Historial de acciones
│   ├── static/           # Assets estáticos
│   ├── templates/        # Templates HTML
│   └── utils/            # Utilidades y decoradores
├── config/               # Configuración centralizada
│   ├── config.py         # Config por entornos
│   └── security_config.py # Config de seguridad
├── scripts/              # Scripts de utilidad
│   ├── analyzer_cli.py   # Analizador CLI
│   └── migrate_history.py # Migración de historial
├── data/                 # Bases de datos
│   ├── analysis.db       # BD principal
│   └── history.db        # BD historial separada
├── cli.py                # 🆕 CLI principal unificado
├── wsgi.py               # 🆕 Punto de entrada WSGI
├── setup.py              # 🆕 Instalación como paquete
├── requirements.txt           # Dependencias Python
├── urls.txt                   # URLs para análisis por lotes
├── logging_config.sh          # Configuración del sistema de historial (NUEVO)
├── analysis.db                # Base de datos principal SQLite (auto-creada)
├── history.db                 # Base de datos de historial separada (NUEVO)
├── static/                    # Archivos estáticos (Flask)
│   ├── css/
│   │   └── main.css          # Estilos principales
│   └── js/
│       ├── index.js          # JavaScript dashboard
│       └── scan_detail.js    # JavaScript scan details
├── templates/                 # Templates HTML (español chileno)
│   ├── base.html             # Template base con autenticación
│   ├── index.html            # Dashboard con filtros de cliente
│   ├── scan_detail.html      # Detalles de análisis
│   ├── historial.html        # Interfaz de historial de acciones (ACTUALIZADO)
│   ├── login.html            # Página de autenticación
│   ├── users.html            # Gestión de usuarios (admin)
│   ├── clients.html          # Gestión de clientes
│   └── global_libraries.html # Catálogo global de librerías
├── CLAUDE.md                  # Documentación técnica (inglés)
├── CLAUDE_es.md              # Documentación técnica (español)
├── PRD_es.md                 # Documento de requerimientos
├── BD_SEPARADA_COMPLETADA.md # Documentación de implementación (NUEVO)
└── README.md                  # Este archivo
```

## 🛠️ Operaciones Avanzadas

### Operaciones por Lotes
- **Selección multiple**: Checkboxes en todas las tablas
- **"Select All"**: Checkbox en header para seleccionar todos
- **Contadores dinámicos**: "Delete Selected (X)" aparece automáticamente
- **Confirmación con preview**: Modal muestra elementos a eliminar

### Eliminación Individual
- **Botones 🗑️**: En cada fila de las tablas
- **Confirmación**: Modal con detalles del elemento
- **Coexistencia**: No interfiere con operaciones por lotes

### Gestión de Base de Datos
- **Arquitectura dual**: `analysis.db` (principal) + `history.db` (historial separado)
- **Reset completo**: Elimina archivo de BD y recrea esquema
- **Migración automática**: Actualiza esquema existente sin pérdida de datos
- **Eliminación cascada**: Eliminar scan borra todos los datos relacionados
- **Migración de historial**: Script automático para migrar datos existentes

### Sistema de Historial
- **Configuración**: Activar con `source logging_config.sh`
- **Performance**: Cero conflictos de BD durante análisis masivos
- **Migración**: Comando `python scripts/migrate_history.py` para datos existentes
- **Limpieza**: Mantenimiento automático de registros antiguos

## 📡 API Endpoints

### Información General
- `GET /api/scans` - Lista todos los análisis con contadores y filtros por cliente
- `GET /api/stats` - Estadísticas del dashboard con filtros opcionales por cliente

### Gestión de Clientes
- `GET /api/clients` - Lista todos los clientes activos
- **Filtrado**: Parámetro `client_id` disponible en endpoints de análisis

### Datos Específicos
- `GET /api/libraries` - Todas las librerías con contexto del sitio
- `GET /api/version-strings` - Todos los strings de versión encontrados
- `GET /api/global-libraries` - Catálogo global de definiciones de librerías

### Historial de Acciones (Nuevo)
- `GET /historial` - Interfaz web de historial con filtros avanzados
- `GET /historial/details/<id>` - Detalles completos de una acción específica
- `POST /historial/undo/<id>` - Deshacer una acción (con validaciones de integridad)
- `GET /historial/export` - Exportar historial filtrado (Excel/CSV/PDF)

### Detalles de Análisis
- `GET /scan/<id>` - Vista completa de análisis específico (HTML)

### Ejemplos de Uso
```bash
# Estadísticas generales
curl http://localhost:5000/api/stats

# Estadísticas filtradas por cliente
curl http://localhost:5000/api/stats?client_id=1

# Escaneos de un cliente específico
curl http://localhost:5000/api/scans?client_id=1

# Lista de clientes
curl http://localhost:5000/api/clients
```

## 🔧 Base de Datos

### Esquema Actualizado - Arquitectura Dual

#### Base de Datos Principal (`analysis.db`) - 7 tablas

#### Tabla `scans`
```sql
id, url, scan_date, status_code, title, headers (JSON), client_id (FK)
```

#### Tabla `libraries` 
```sql
id, scan_id, library_name, version, type, source_url,
description, latest_safe_version, latest_version, is_manual
```

#### Tabla `version_strings`
```sql
id, scan_id, file_url, file_type, line_number, 
line_content, version_keyword
```

#### Tabla `file_urls`
```sql
id, scan_id, file_url, file_type, file_size, status_code
```

#### Tabla `users` (Nueva)
```sql
id, username, password (hash), role ('admin'|'analyst')
```

#### Tabla `clients` (Nueva)
```sql
id, name, contact_info, is_active, created_date
```

#### Tabla `global_libraries` (Nueva)
```sql
id, library_name, description, latest_safe_version, 
latest_version, library_type
```

#### Base de Datos de Historial (`history.db`) - Separada para Performance
```sql
-- Tabla principal de historial (optimizada para concurrencia)
action_history: id, timestamp, username, user_role, action_type, 
                target_table, target_id, target_description, 
                data_before (JSON), data_after (JSON), success, 
                error_message, ip_address, user_agent, session_id, notes

-- Metadatos de auditoría
audit_metadata: id, created_at, schema_version, last_cleanup, 
                 total_records, notes

-- 6 índices especializados para consultas rápidas
Índices: timestamp, user_action, table_action, session, target, success
```

**Ventajas de la Arquitectura Dual:**
- ✅ **Cero conflictos** durante análisis masivos de URLs
- ✅ **Performance optimizada** para operaciones principales
- ✅ **Historial completo** sin impacto en rendimiento
- ✅ **Escalabilidad** independiente de cada base de datos

## 🎨 Personalización

### Agregar Detección de Nuevas Librerías
En `analyzer.py`, extender las funciones de detección:

```python
# Ejemplo: Detectar Lodash
lodash_scripts = soup.find_all('script', src=re.compile(r'lodash', re.I))
for script in lodash_scripts:
    src = script.get('src', '')
    version_match = re.search(r'lodash[-.]?(\d+\.\d+\.\d+)', src, re.I)
    if version_match:
        libraries.append({
            'name': 'Lodash',
            'version': version_match.group(1),
            'type': 'js',
            'source': urljoin(base_url, src)
        })
```

### Personalizar Headers de Seguridad
En `dashboard.py`, función `analyze_security_headers()`:

```python
security_headers = {
    'custom-security-header': {
        'name': 'Custom-Security-Header',
        'description': 'Descripción del header',
        'recommendation': 'valor-recomendado'
    }
}
```

### Configurar Puerto del Servidor
```python
# En dashboard.py, línea final:
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 🔍 Librerías Detectadas

### JavaScript
- **jQuery** - Todas las versiones
- **React** - Framework de Facebook
- **Vue.js** - Framework progresivo
- **Angular** - Framework de Google
- **Bootstrap JavaScript** - Componentes JS

### CSS
- **Bootstrap CSS** - Framework de estilos
- **Font Awesome** - Librería de iconos

## 🆘 Solución de Problemas

### Error: "database is locked" (Resuelto)
```bash
# ✅ SOLUCIONADO con BD separada para historial
# El sistema ahora usa history.db independiente
source logging_config.sh  # Habilitar BD separada
python dashboard.py        # Sistema sin conflictos
```

### Migrar historial existente
```bash
# Migrar datos de analysis.db a history.db
python scripts/migrate_history.py  # Una sola vez
```

### Error: "no such column: description"
```bash
# La aplicación migra automáticamente, pero si hay problemas:
rm analysis.db  # Eliminar BD existente
python dashboard.py  # Recrear con nuevo esquema
```

### Timeouts en URLs
```python
# En analyzer.py, ajustar timeout:
response = requests.get(url, headers=headers, timeout=30)
```

### Memoria para listas grandes
```python
# En analyzer.py, aumentar delay:
analyzer.analyze_urls(urls, delay=3)  # 3 segundos entre requests
```

### Puerto ocupado
```bash
# Verificar puertos en uso:
lsof -i :5000
# Cambiar puerto en dashboard.py o terminar proceso
```

### Archivos estáticos no cargan
```bash
# Verificar estructura:
ls -la static/css/ static/js/
# Deben existir main.css, index.js, scan_detail.js
```

## 🔒 Características de Seguridad

### 🛡️ Protecciones Implementadas
- ✅ **Autenticación robusta** con hash de contraseñas Werkzeug
- ✅ **Control de acceso basado en roles** (Administrador/Analista)
- ✅ **Protección CSRF** completa con Flask-WTF en todos los formularios
- ✅ **Prevención SQL Injection** con consultas parametrizadas exclusivamente
- ✅ **Protección SSRF** con validación avanzada de URLs y bloqueo de IPs privadas
- ✅ **Headers de seguridad** comprehensivos aplicados automáticamente
- ✅ **Configuración segura** por defecto con gestión de sesiones segura
- ✅ **Gestión de contraseñas** con autoservicio para todos los usuarios

### 📊 Headers de Seguridad Analizados
| Header | Propósito | Estado |
|--------|-----------|--------|
| **Strict-Transport-Security** | HSTS/SSL forzado | ✅ Implementado |
| **Content-Security-Policy** | Control de recursos | ✅ Implementado |
| **X-Frame-Options** | Anti-clickjacking | ✅ Implementado |
| **X-XSS-Protection** | Protección XSS | ✅ Implementado |
| **X-Content-Type-Options** | Anti-MIME sniffing | ✅ Implementado |
| **Referrer-Policy** | Control de referrer | ✅ Implementado |
| **Permissions-Policy** | Control de features | ✅ Implementado |

### 📈 Puntuación de Seguridad
- **🟢 80%+**: Excelente seguridad
- **🟡 50-79%**: Seguridad moderada  
- **🔴 <50%**: Mejoras necesarias

### ⚠️ Consideraciones de Seguridad
> **IMPORTANTE**: Antes de desplegar en producción:
> - Cambiar `FLASK_SECRET_KEY` por una clave fuerte generada
> - Eliminar `admin_credentials.txt` si existe  
> - Configurar `FLASK_ENV=production` y `FLASK_DEBUG=0`
> - Cambiar credenciales por defecto del usuario `gabo`
> - Crear usuarios con contraseñas fuertes para producción
> - Usar HTTPS con certificados válidos
> - Configurar firewall para acceso controlado

## 📝 Licencia

Este proyecto es de código abierto. Puedes usarlo, modificarlo y distribuirlo libremente para fines educativos y comerciales.

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📚 Documentación Adicional

- **[📋 Instrucciones de Despliegue](./DEPLOYMENT.md)** - Guía completa para producción con Podman
- **[🔧 Documentación Técnica EN](./CLAUDE.md)** - Arquitectura y desarrollo (inglés)
- **[🔧 Documentación Técnica ES](./CLAUDE_es.md)** - Arquitectura y desarrollo (español)
- **[📋 Documento de Requerimientos](./PRD_es.md)** - PRD completo en español chileno
- **[🗂️ BD Separada - Implementación](./BD_SEPARADA_COMPLETADA.md)** - Sistema de historial con BD independiente
- **[🐛 Reportar Issues](https://github.com/gabo-ntg/ntg-js-analyzer/issues)** - Problemas y sugerencias

## 🆘 Soporte

**¿Necesitas ayuda?**
1. Revisa la [documentación de despliegue](./DEPLOYMENT.md)
2. Consulta la [documentación técnica](./CLAUDE.md)
3. Abre un [issue en GitHub](https://github.com/gabo-ntg/ntg-js-analyzer/issues)

## 🏷️ Versión y Estado

- **Versión**: 3.0.0 (Arquitectura Modular)
- **Estado**: Producción estable con arquitectura Flask moderna
- **Última auditoría de seguridad**: Enero 2025
- **Reorganización**: Estructura modularizada siguiendo convenciones Flask/Python
- **Nuevas funcionalidades**: BD de historial separada, cero conflictos de concurrencia
- **Arquitectura**: Dual database (analysis.db + history.db)
- **Python**: 3.8+ requerido
- **Flask**: 2.3.3 con Flask-WTF para CSRF
- **Interfaz**: Completamente traducida a español chileno