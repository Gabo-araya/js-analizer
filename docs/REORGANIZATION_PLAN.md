# 🗂️ Plan de Reorganización - Convenciones Flask y Python

## 📋 Estructura Actual vs Propuesta

### ❌ Problemas Identificados:
1. **Archivo único grande**: `dashboard.py` (~5000 líneas) viola principio de responsabilidad única
2. **Archivos sueltos**: Scripts y utilidades mezclados en raíz
3. **Configuración dispersa**: Variables de configuración en múltiples archivos
4. **Falta de modularización**: Lógica de negocio mezclada con rutas
5. **Documentación desorganizada**: Múltiples archivos de docs en raíz

### ✅ Estructura Propuesta (Convenciones Flask):

```
ntg-js-analyzer/
├── app/                          # Paquete principal de la aplicación
│   ├── __init__.py              # Factory de aplicación Flask
│   ├── models/                  # Modelos de datos y DB
│   │   ├── __init__.py
│   │   ├── database.py          # Configuración de BD
│   │   ├── scan.py             # Modelo Scan
│   │   ├── library.py          # Modelo Library  
│   │   ├── user.py             # Modelo User
│   │   ├── client.py           # Modelo Client
│   │   └── history.py          # Modelo History
│   ├── views/                   # Blueprints y rutas
│   │   ├── __init__.py
│   │   ├── main.py             # Rutas principales (/dashboard)
│   │   ├── auth.py             # Autenticación (/login, /logout)
│   │   ├── scans.py            # Gestión de escaneos
│   │   ├── clients.py          # Gestión de clientes
│   │   ├── users.py            # Gestión de usuarios  
│   │   ├── history.py          # Historial de acciones
│   │   ├── api.py              # Endpoints API REST
│   │   └── exports.py          # Exportaciones (PDF, Excel, CSV)
│   ├── services/                # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── analyzer_service.py  # Servicio de análisis web
│   │   ├── library_detector.py # Detección de librerías
│   │   ├── security_analyzer.py # Análisis de seguridad
│   │   ├── export_service.py   # Servicios de exportación
│   │   └── history_service.py  # Servicios de historial
│   ├── utils/                   # Utilidades y helpers
│   │   ├── __init__.py
│   │   ├── decorators.py       # Decoradores (auth, logging)
│   │   ├── validators.py       # Validaciones
│   │   ├── formatters.py       # Formateo de datos
│   │   └── security.py         # Utilidades de seguridad
│   └── static/                  # Archivos estáticos (sin cambios)
│       ├── css/
│       ├── js/
│       └── img/
├── templates/                   # Templates HTML (sin cambios)
├── config/                      # Configuración
│   ├── __init__.py
│   ├── config.py               # Configuración principal
│   ├── database.py             # Configuración de BD
│   └── logging.py              # Configuración de logging
├── scripts/                     # Scripts de utilidad
│   ├── __init__.py
│   ├── migrate_history.py      # Migración de historial
│   ├── populate_libraries.py   # Poblar catálogo
│   ├── analyzer_cli.py         # Analizador CLI (renombrado)
│   └── database_tools.py       # Herramientas de BD
├── migrations/                  # Migraciones de BD (futuro)
├── tests/                       # Tests unitarios y de integración
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_services.py
│   └── conftest.py
├── docs/                        # Documentación organizada
│   ├── README.md               # Documentación principal
│   ├── DEPLOYMENT.md           # Despliegue
│   ├── API.md                  # Documentación API
│   ├── SECURITY.md             # Seguridad
│   ├── HISTORY_SYSTEM.md       # Sistema de historial
│   └── archive/                # Documentos históricos
├── data/                        # Datos y BD
│   ├── analysis.db             # BD principal
│   ├── history.db              # BD historial
│   └── backups/                # Respaldos
├── logs/                        # Archivos de log
├── docker/                      # Archivos Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── podman-compose.yml
├── requirements/                # Dependencias organizadas
│   ├── base.txt               # Dependencias base
│   ├── dev.txt                # Dependencias desarrollo
│   └── prod.txt               # Dependencias producción
├── .env.example                # Variables de entorno ejemplo
├── .gitignore                  # Git ignore
├── setup.py                    # Setup del paquete
├── wsgi.py                     # Punto de entrada WSGI
├── cli.py                      # Comandos CLI de la aplicación
└── requirements.txt            # Dependencias principales (compat)
```

## 🔄 Plan de Migración

### Fase 1: Crear estructura de directorios
### Fase 2: Reorganizar código principal (dashboard.py)
### Fase 3: Mover y organizar scripts
### Fase 4: Reorganizar documentación
### Fase 5: Actualizar imports y configuración
### Fase 6: Verificar funcionamiento

## 📦 Beneficios de la Reorganización

### ✅ Mantenibilidad
- **Separación de responsabilidades**: Cada módulo tiene una función específica
- **Código más limpio**: Archivos más pequeños y enfocados
- **Fácil navegación**: Estructura predecible

### ✅ Escalabilidad  
- **Blueprints de Flask**: Rutas organizadas por funcionalidad
- **Servicios independientes**: Lógica de negocio reutilizable
- **Tests organizados**: Cobertura por módulos

### ✅ Convenciones Python
- **PEP 8**: Estructura de paquetes estándar
- **Imports relativos**: Organización clara de dependencias
- **Factory pattern**: Inicialización flexible de Flask

### ✅ DevOps
- **Docker organizado**: Archivos de contenedores en directorio específico
- **Configuración centralizada**: Variables de entorno y configuración
- **Scripts de administración**: Herramientas organizadas