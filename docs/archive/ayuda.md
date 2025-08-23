# 📖 Guía Completa del Analizador de Librerías JS/CSS

**Versión 2.0** | **Actualizado: Agosto 2025**

---

## 📋 Tabla de Contenidos

1. [Introducción y Conceptos Básicos](#introducción)
2. [Autenticación y Roles de Usuario](#autenticación)
3. [Panel de Control (Dashboard)](#dashboard)
4. [Gestión de Clientes](#clientes)
5. [Análisis de Sitios Web](#análisis)
6. [Detalles de Escaneos](#detalles)
7. [Sistema de Revisión](#revisión)
8. [Catálogo Global de Librerías](#catálogo)
9. [Estadísticas de Vulnerabilidades](#estadísticas)
10. [Exportación de Reportes](#exportación)
11. [Gestión de Usuarios (Solo Administradores)](#usuarios)
12. [Flujos de Trabajo Típicos](#flujos)
13. [Solución de Problemas](#problemas)

---

## 🎯 Introducción y Conceptos Básicos {#introducción}

### ¿Qué es el Analizador de Librerías JS/CSS?

Esta aplicación web permite **analizar sitios web** para detectar automáticamente las librerías JavaScript y CSS que utilizan, identificar **vulnerabilidades de seguridad** conocidas y generar reportes detallados para la gestión de riesgos.

### Conceptos Clave

| Término | Definición | Ejemplo |
|---------|------------|---------|
| **Escaneo** | Análisis completo de un sitio web | Análisis de `https://ejemplo.com` |
| **Librería** | Framework o biblioteca JS/CSS detectada | jQuery 2.1.0, Bootstrap 4.5.2 |
| **Vulnerabilidad** | Versión de librería con problemas de seguridad conocidos | jQuery < 3.0.0 tiene vulnerabilidades XSS |
| **Cliente** | Organización o empresa propietaria del sitio | "Empresa ABC", "Proyecto XYZ" |
| **Revisión** | Estado que indica si un escaneo fue evaluado por un usuario | ✅ Revisado / 🕐 Pendiente |

### Tipos de Datos Analizados

1. **Librerías JavaScript**: jQuery, React, Vue.js, Angular, etc.
2. **Frameworks CSS**: Bootstrap, Font Awesome, Bulma, etc.
3. **Headers HTTP**: Cabeceras de seguridad (HSTS, CSP, X-Frame-Options)
4. **Archivos JS/CSS**: Lista completa de recursos cargados
5. **Strings de Versión**: Líneas de código que contienen información de versiones

---

## 🔐 Autenticación y Roles de Usuario {#autenticación}

### Tipos de Usuario

#### **👑 Administrador**
- **Permisos completos** en toda la aplicación
- Gestión de usuarios (crear, editar, eliminar)
- Acceso a todas las funcionalidades
- Cambio de roles de otros usuarios

#### **👤 Analista**
- Gestión de clientes, escaneos y librerías
- Análisis y revisión de vulnerabilidades
- Generación de reportes
- **NO puede** gestionar usuarios

### Proceso de Login

1. **Acceder a la aplicación** → `http://localhost:5000`
2. **Introducir credenciales**:
   ```
   Usuario por defecto: gabo
   Contraseña por defecto: admin123
   Rol: Administrador
   ```
3. **Dashboard** se muestra según permisos del rol

### Gestión de Contraseñas

#### **Cambio de Contraseña Propia**
1. **Hacer clic** en el menú de usuario (esquina superior derecha)
2. **Seleccionar** "Cambiar Contraseña"
3. **Completar formulario**:
   - Contraseña actual
   - Nueva contraseña
   - Confirmar nueva contraseña
4. **Guardar cambios**

**Ejemplo:**
```
👤 Usuario: juan.perez
🔑 Contraseña actual: ********
🆕 Nueva contraseña: ********
✅ Confirmar: ********
```

---

## 📊 Panel de Control (Dashboard) {#dashboard}

### Vista General

El dashboard es la **página principal** donde se visualizan todos los escaneos realizados con estadísticas en tiempo real.

**URL:** `http://localhost:5000/`

### Secciones del Dashboard

#### **1. Estadísticas Generales**
```
┌─────────────────────────────────────────────────────────┐
│ 📊 ESTADÍSTICAS GENERALES                              │
├─────────────────────────────────────────────────────────┤
│ 🌐 Escaneos: 156    📚 Librerías: 89    🏢 Clientes: 12 │
│ 📁 Archivos: 234    ⚠️ Vulnerabilidades: 23             │
└─────────────────────────────────────────────────────────┘
```

#### **2. Filtros y Búsqueda**
- **Por Cliente**: Dropdown para filtrar escaneos de un cliente específico
- **Búsqueda**: Campo de texto para buscar por URL, título o librerías
- **Sin Cliente**: Opción especial para escaneos no asignados

**Ejemplo de filtros:**
```
🔍 Buscar: "bootstrap"
🏢 Cliente: [Empresa ABC ▼]
📊 Resultados: 15 escaneos encontrados
```

#### **3. Tabla de Escaneos Recientes**

| Columna | Información | Ejemplo |
|---------|-------------|---------|
| **Sitio** | URL y título del sitio web | `https://ejemplo.com` <br> "Mi Sitio Web" |
| **Cliente** | Empresa asignada (si existe) | 🏢 Empresa ABC |
| **Estado** | Código de respuesta HTTP | 🟢 200 / 🔴 404 |
| **Contadores** | Librerías, archivos, vulnerabilidades | 📚 12 📁 45 ⚠️ 3 |
| **Estado Revisión** | Si fue revisado por usuario | ✅ Revisado / 🕐 Pendiente |
| **Fecha** | Cuándo se realizó el escaneo | 2025-08-14 15:30 |
| **Acciones** | Botones de acción disponibles | Ver, Editar, Revisar, Eliminar |

#### **4. Acciones Disponibles**

**Por Escaneo:**
- 🔍 **Ver Detalles**: Ir a análisis completo
- ✏️ **Editar Cliente**: Asignar/cambiar cliente
- ✅ **Toggle Revisión**: Marcar como revisado/pendiente
- 🗑️ **Eliminar**: Borrar escaneo completo

**Generales:**
- ➕ **Analizar URL**: Escanear un sitio nuevo
- 📝 **Análisis Masivo**: Analizar múltiples URLs
- 🔄 **Reset BD**: Limpiar base de datos completa

### Navegación y Paginación

- **50 escaneos por página**
- **Navegación numérica**: ◀ 1 2 3 4 5 ▶
- **Preservación de filtros**: Los filtros se mantienen al cambiar página

---

## 🏢 Gestión de Clientes {#clientes}

### Propósito

Organizar escaneos por **empresa o proyecto**, facilitando la gestión y el seguimiento de múltiples clientes.

**URL:** `http://localhost:5000/clients`

### Información de Clientes

#### **Datos Almacenados**
- **Nombre**: Identificador único del cliente
- **Descripción**: Información adicional sobre el cliente
- **Contacto**: Email y teléfono
- **Sitio Web**: URL principal del cliente
- **Estado**: Activo/Inactivo
- **Fechas**: Creación y última actualización

#### **Ejemplo de Cliente**
```
📋 INFORMACIÓN DEL CLIENTE
────────────────────────────
🏢 Nombre: Empresa ABC S.A.
📝 Descripción: Empresa de tecnología financiera
📧 Email: contacto@empresaabc.com
📞 Teléfono: +56 9 1234 5678
🌐 Sitio Web: https://empresaabc.com
📊 Escaneos: 25 análisis realizados
✅ Estado: Activo
📅 Creado: 2025-01-15
```

### Operaciones CRUD

#### **Crear Cliente**
1. **Hacer clic** en "➕ Nuevo Cliente"
2. **Completar formulario**:
   ```
   🏢 Nombre: [Requerido] Empresa XYZ
   📝 Descripción: [Opcional] Descripción del cliente
   📧 Email: [Opcional] contacto@ejemplo.com
   📞 Teléfono: [Opcional] +56 9 8765 4321
   🌐 Sitio Web: [Opcional] https://ejemplo.com
   ```
3. **Guardar**: El cliente aparece en la lista

#### **Editar Cliente**
1. **Hacer clic** en ✏️ junto al cliente
2. **Modificar datos** necesarios
3. **Guardar cambios**

#### **Eliminar Cliente**
1. **Hacer clic** en 🗑️ junto al cliente
2. **Confirmar eliminación** en modal
3. **Nota**: Los escaneos asociados NO se eliminan, quedan sin cliente

### Asignación de Escaneos

#### **Durante el Análisis**
```
📝 ANÁLISIS MASIVO
─────────────────
🌐 URLs:
https://sitio1.com
https://sitio2.com

🏢 Cliente: [Empresa ABC ▼]  ← Seleccionar aquí
⏱️ Delay: 2 segundos
```

#### **Después del Análisis**
- **Desde Dashboard**: Botón "✏️ Editar" en cada escaneo
- **Desde Detalles**: Botón "Editar Cliente" en página de escaneo

---

## 🔍 Análisis de Sitios Web {#análisis}

### Tipos de Análisis

#### **1. Análisis Individual**
**Para analizar un solo sitio web:**

1. **Ir al Dashboard** → `http://localhost:5000/`
2. **Hacer clic** en "➕ Analizar URL"
3. **Completar formulario**:
   ```
   🌐 URL: https://ejemplo.com
   🏢 Cliente: [Seleccionar cliente] (opcional)
   ```
4. **Iniciar análisis** → Esperar 30-60 segundos
5. **Ver resultados** automáticamente

#### **2. Análisis Masivo**
**Para analizar múltiples sitios:**

1. **Hacer clic** en "📝 Análisis Masivo"
2. **Introducir URLs** (una por línea):
   ```
   https://sitio1.com
   https://sitio2.com
   https://sitio3.com
   # Este es un comentario (se ignora)
   https://sitio4.com
   ```
3. **Configurar opciones**:
   - 🏢 **Cliente**: Asignar a todos los escaneos
   - ⏱️ **Delay**: Tiempo entre requests (recomendado: 2 segundos)
4. **Iniciar análisis masivo**

### Proceso de Análisis

#### **Pasos Automáticos**
1. **Descarga HTML** → Obtiene el código fuente de la página
2. **Extrae archivos JS/CSS** → Identifica todos los recursos cargados
3. **Detecta librerías** → Busca frameworks conocidos automáticamente
4. **Analiza versiones** → Descarga archivos para encontrar strings de versión
5. **Evalúa headers** → Revisa cabeceras de seguridad HTTP
6. **Almacena datos** → Guarda toda la información en base de datos

#### **Detección Automática de Librerías**

**JavaScript:**
- ✅ jQuery (todas las versiones)
- ✅ React (Facebook)
- ✅ Vue.js (Framework progresivo)
- ✅ Angular (Google)
- ✅ Bootstrap JS (Componentes)

**CSS:**
- ✅ Bootstrap CSS (Framework de estilos)
- ✅ Font Awesome (Iconos)

#### **Indicadores de Progreso**
```
🔄 ANALIZANDO SITIO WEB...
──────────────────────────
⏳ Esto puede tomar entre 30-60 segundos
📡 Descargando contenido...
🔍 Analizando librerías...
💾 Guardando resultados...
```

### Limitaciones y Consideraciones

#### **Limitaciones Técnicas**
- **Timeout**: 30 segundos máximo por URL
- **Archivos analizados**: Primeros 10 JS/CSS por sitio
- **Tamaño de archivo**: Máximo 5MB por archivo
- **JavaScript dinámico**: No ejecuta código JS, solo analiza archivos estáticos

#### **Sitios que Pueden Fallar**
- 🚫 Sitios con autenticación requerida
- 🚫 Aplicaciones SPA complejas (React/Angular puro)
- 🚫 Sitios con anti-bot protection
- 🚫 URLs que requieren JavaScript para cargar contenido

#### **Recomendaciones**
- ✅ Usar URLs de páginas públicas
- ✅ Incluir protocolo (http:// o https://)
- ✅ Esperar entre análisis masivos
- ✅ Verificar manualmente resultados complejos

---

## 📄 Detalles de Escaneos {#detalles}

### Navegación a Detalles

**Acceso desde:**
- Dashboard → Botón "🔍 Detalles"
- Estadísticas → Botón "👁️ Ver"
- URL directa → `http://localhost:5000/scan/123`

### Estructura de la Página

#### **1. Encabezado del Escaneo**
```
🌐 Mi Sitio Web Ejemplo
https://ejemplo.com ↗️

📊 Escaneo 2 de 5 para esta URL    🟢 Estado: Revisado
```

#### **2. Barra de Herramientas Mejorada**
```
[📥 Exportar ▼] [🔄 Re-escanear] [🕐 Historial] [✅ Revisado] [◀ Anterior 2/5 Siguiente ▶] [🗑️ Eliminar]
```

**Acciones disponibles:**
- **📥 Exportar**: PDF, CSV, Excel, HTML
- **🔄 Re-escanear**: Analizar URL nuevamente
- **🕐 Historial**: Ver escaneos anteriores de la misma URL
- **✅ Revisado**: Toggle estado de revisión
- **Navegación**: Entre escaneos de la misma URL
- **🗑️ Eliminar**: Borrar escaneo completo

#### **3. Pestañas de Información**

##### **📋 Resumen de Seguridad**
```
┌─────────────────────────────────────────────┐
│ 🏢 INFORMACIÓN DEL CLIENTE                  │
├─────────────────────────────────────────────┤
│ Cliente: Empresa ABC                        │
│ Estado: Activo                              │
│ Contacto: contacto@empresa.com              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 🛡️ ANÁLISIS DE HEADERS DE SEGURIDAD        │
├─────────────────────────────────────────────┤
│ Puntuación: 75% (Buena seguridad)          │
│                                             │
│ ✅ Strict-Transport-Security: max-age=...   │
│ ✅ X-Content-Type-Options: nosniff          │
│ ❌ Content-Security-Policy: (Faltante)      │
│ ❌ X-Frame-Options: (Faltante)              │
└─────────────────────────────────────────────┘
```

##### **📚 Librerías Detectadas**
```
┌────────────────────────────────────────────────────────────────┐
│ LIBRERÍA          │ VERSIÓN │ TIPO │ VULNERABILIDAD │ ACCIONES │
├────────────────────────────────────────────────────────────────┤
│ jQuery            │ 2.1.0   │ JS   │ ⚠️ 3 vulns     │ ✏️ 🗑️    │
│ Bootstrap         │ 4.5.2   │ CSS  │ ✅ Segura      │ ✏️ 🗑️    │
│ Font Awesome      │ 5.0.0   │ CSS  │ ⚠️ 1 vuln      │ ✏️ 🗑️    │
└────────────────────────────────────────────────────────────────┘

➕ Agregar Librería Manual
```

**Información por librería:**
- **Nombre**: Identificador de la librería
- **Versión Actual**: Versión detectada en el sitio
- **Tipo**: JavaScript (JS) o CSS
- **Última Versión Segura**: Recomendada sin vulnerabilidades
- **Última Versión**: Más reciente disponible
- **Origen**: URL donde se encontró
- **Estado**: Auto-detectada o agregada manualmente

##### **📁 Archivos JS/CSS**
```
┌──────────────────────────────────────────────────────────────┐
│ ARCHIVO                                    │ TIPO │ TAMAÑO   │
├──────────────────────────────────────────────────────────────┤
│ https://cdn.jquery.com/jquery-2.1.0.min.js │ JS   │ 84.3 KB │
│ https://ejemplo.com/assets/main.css         │ CSS  │ 12.1 KB │
│ https://ejemplo.com/js/custom.js            │ JS   │ 5.8 KB  │
└──────────────────────────────────────────────────────────────┘
```

##### **🔍 Cadenas de Versión**
```
┌─────────────────────────────────────────────────────────────────────┐
│ ARCHIVO                     │ LÍNEA │ CONTENIDO                     │
├─────────────────────────────────────────────────────────────────────┤
│ jquery-2.1.0.min.js        │ 1     │ /*! jQuery v2.1.0 */          │
│ bootstrap.min.css          │ 5     │ * Bootstrap v4.5.2            │
│ main.js                    │ 23    │ version: "1.0.0"              │
└─────────────────────────────────────────────────────────────────────┘
```

### Gestión Manual de Librerías

#### **Agregar Librería Manual**
1. **Hacer clic** en "➕ Agregar Librería Manual"
2. **Seleccionar del catálogo** (opcional):
   ```
   📚 Catálogo Global: [Seleccionar librería ▼]
   ```
3. **Completar información**:
   ```
   📝 Nombre: React
   🔧 Tipo: [JavaScript ▼]
   📦 Versión Actual: 16.8.0
   🛡️ Última Versión Segura: 18.2.0
   🚀 Última Versión: 18.2.0
   🌐 URL Origen: https://ejemplo.com/js/react.js
   📄 Descripción: Framework para interfaces
   ```
4. **Guardar**: La librería aparece en la lista

#### **Editar Librería**
1. **Hacer clic** en ✏️ junto a la librería
2. **Modificar campos** necesarios
3. **Guardar cambios**

#### **Eliminar Librerías**
**Individual:**
1. **Hacer clic** en 🗑️ junto a la librería
2. **Confirmar** en modal de confirmación

**Por lotes:**
1. **Seleccionar** checkboxes de librerías a eliminar
2. **Hacer clic** en "🗑️ Eliminar Seleccionadas (X)"
3. **Confirmar** en modal con preview

---

## ✅ Sistema de Revisión {#revisión}

### Propósito del Sistema

El sistema de revisión permite **marcar escaneos** como "revisados" después de que un analista ha evaluado las vulnerabilidades encontradas, facilitando el seguimiento del trabajo realizado.

### Estados de Revisión

| Estado | Indicador | Significado | Acción Disponible |
|--------|-----------|-------------|-------------------|
| **Pendiente** | 🕐 Pendiente | No ha sido revisado por ningún usuario | Marcar como Revisado |
| **Revisado** | ✅ Revisado | Un usuario ya evaluó este escaneo | Marcar como Pendiente |

### Ubicaciones del Toggle

#### **1. Dashboard Principal** (`/`)
```
┌─────────────────────────────────────────────────────────────────┐
│ SITIO              │ CLIENTE │ ESTADO │ CONTADORES       │ FECHA │
├─────────────────────────────────────────────────────────────────┤
│ https://ejemplo.com│ ABC     │ 🟢 200 │ 📚12 📁45 ⚠️3   │ Ayer  │
│ Mi Sitio Web       │         │        │ 🕐 Pendiente     │       │
│                    │         │        │ [🟡 Revisado]    │       │
└─────────────────────────────────────────────────────────────────┘
```

#### **2. Página de Estadísticas** (`/statistics`)
Similar al dashboard, con botones compactos (solo íconos).

#### **3. Página de Detalles** (`/scan/123`)
```
🌐 Mi Sitio Web
https://ejemplo.com

🟡 Estado: Pendiente de Revisión

[📥 Exportar] [🔄 Re-escanear] [🟡 Marcar como Revisado*] [🗑️]
```

### Flujo de Trabajo de Revisión

#### **Caso de Uso Típico**
1. **Analista identifica escaneo pendiente** → Badge 🕐 Pendiente
2. **Hace clic en "Detalles"** → Va a página de análisis completo
3. **Revisa pestaña "Librerías"** → Evalúa cada vulnerabilidad
4. **Analiza severity y riesgo** → Determina criticidad
5. **Completa revisión** → Hace clic en "Marcar como Revisado"
6. **Confirmación** → ✅ "Escaneo marcado como revisado exitosamente"
7. **Estado actualizado** → Badge cambia a ✅ Revisado

#### **Ejemplo de Revisión de Vulnerabilidades**
```
📚 LIBRERÍA: jQuery 2.1.0

⚠️ VULNERABILIDADES IDENTIFICADAS:
──────────────────────────────────
• CVE-2020-11022: XSS via HTML parsing
• CVE-2020-11023: XSS via selector injection
• CVE-2015-9251: Cross-site scripting vulnerability

🛡️ RECOMENDACIÓN: Actualizar a jQuery 3.6.0+

👤 EVALUACIÓN DEL ANALISTA:
• Criticidad: ALTA (sitio público con formularios)
• Prioridad: Inmediata
• Acción: Notificar al cliente para actualización urgente

✅ MARCAR COMO REVISADO
```

### Indicadores Visuales Avanzados

#### **Estado Pendiente**
- 🔘 **Badge gris**: "Pendiente"
- 🟡 **Botón amarillo**: "Marcar como Revisado"
- ✨ **Animación**: Punto pulsante en botón (página de detalles)

#### **Estado Revisado**
- ✅ **Badge verde**: "Revisado"
- 🟢 **Botón verde**: "Revisado" (para desmarcar)
- 🚫 **Sin animación**: Estado estable

### Funcionalidad Técnica

#### **Seguridad**
- ✅ **Login requerido**: Solo usuarios autenticados
- ✅ **CSRF Protection**: Tokens en todos los formularios
- ✅ **Preservación de contexto**: Vuelve a página anterior

#### **Persistencia**
- ✅ **Base de datos**: Campo `reviewed` (0/1)
- ✅ **Historial**: Se mantiene el estado indefinidamente
- ✅ **Auditoría**: Se podría agregar logging de cambios

---

## 📚 Catálogo Global de Librerías {#catálogo}

### Propósito

El catálogo global es una **base de datos centralizada** de definiciones de librerías conocidas que facilita la gestión manual y proporciona información consistente sobre versiones seguras.

**URL:** `http://localhost:5000/global-libraries`

### Información Almacenada

#### **Datos por Librería**
- **Nombre**: Identificador único (ej: "jQuery")
- **Tipo**: JavaScript o CSS
- **Última Versión Segura**: Versión recomendada sin vulnerabilidades
- **Última Versión**: Versión más reciente disponible
- **Descripción**: Información sobre la librería
- **Información de Vulnerabilidades**: Descripción de problemas conocidos
- **URL de Origen**: Enlace oficial o documentación

#### **Ejemplo de Entrada del Catálogo**
```
📚 JQUERY
─────────────────────────────────
🔧 Tipo: JavaScript
🛡️ Última Versión Segura: 3.6.0
🚀 Última Versión: 3.7.1
📄 Descripción: Librería JavaScript para manipulación DOM
⚠️ Vulnerabilidades: Versiones < 3.4.0 tienen vulnerabilidades XSS
🌐 URL: https://jquery.com/
📅 Creado: 2025-01-15
📅 Actualizado: 2025-08-14
```

### Operaciones CRUD

#### **Crear Definición de Librería**
1. **Hacer clic** en "➕ Nueva Librería Global"
2. **Completar formulario**:
   ```
   📝 Nombre: [Requerido] Bootstrap
   🔧 Tipo: [CSS ▼]
   🛡️ Última Versión Segura: 5.3.0
   🚀 Última Versión: 5.3.1
   📄 Descripción: Framework CSS para diseño responsive
   ⚠️ Info Vulnerabilidades: Versiones < 4.6.0 vulnerables a XSS
   🌐 URL: https://getbootstrap.com/
   ```
3. **Guardar**: Aparece en catálogo global

#### **Editar Definición**
1. **Hacer clic** en ✏️ junto a la librería
2. **Modificar información** (especialmente versiones)
3. **Guardar cambios**

#### **Eliminar Definición**
1. **Hacer clic** en 🗑️
2. **Confirmar eliminación**
3. **Nota**: NO afecta librerías ya detectadas en escaneos

### Integración con Análisis Manual

#### **Uso en Agregar Librería Manual**
```
➕ AGREGAR LIBRERÍA MANUAL
───────────────────────────
📚 Catálogo Global: [Bootstrap (CSS) ▼]  ← Seleccionar aquí

Auto-completado:
📝 Nombre: Bootstrap
🔧 Tipo: CSS
🛡️ Última Versión Segura: 5.3.0
🚀 Última Versión: 5.3.1

Manual (usuario completa):
📦 Versión Actual: 4.1.0  ← Usuario ingresa versión encontrada
🌐 URL Origen: https://ejemplo.com/css/bootstrap.css
```

#### **Beneficios del Catálogo**
- ✅ **Consistencia**: Misma información para todas las detecciones
- ✅ **Rapidez**: Auto-completa campos comunes
- ✅ **Precisión**: Versiones seguras actualizadas centralizadamente
- ✅ **Mantenimiento**: Un lugar para actualizar información

### Estadísticas del Catálogo

#### **Métricas Disponibles**
```
📊 ESTADÍSTICAS DEL CATÁLOGO
────────────────────────────
📚 Total Definiciones: 45 librerías
🔧 JavaScript: 28 librerías
🎨 CSS: 17 librerías
📈 Cobertura: 78% (librerías detectadas que están en catálogo)
📅 Última Actualización: Hace 2 días
```

---

## 📈 Estadísticas de Vulnerabilidades {#estadísticas}

### Propósito

La sección de estadísticas proporciona una **vista consolidada** de todos los escaneos que contienen vulnerabilidades, independientemente del cliente, facilitando la priorización de tareas de seguridad.

**URL:** `http://localhost:5000/statistics`

### Vista General

#### **Tarjetas de Resumen**
```
┌─────────────────────────────────────────────────────────────────┐
│ 🛡️ Escaneos      🐛 Total         📁 Sitios       📊 Porcentaje  │
│    Vulnerables      Vulnerabilidades Afectados     Vulnerable    │
│                                                                 │
│      23              87              18            14.8%        │
└─────────────────────────────────────────────────────────────────┘
```

#### **Funcionalidades de Búsqueda**
```
🔍 BUSCAR EN VULNERABILIDADES
────────────────────────────────
🌐 Buscar: "jquery"  [🔍 Buscar] [❌ Limpiar]

ℹ️ INFORMACIÓN
──────────────
📊 Total encontrados: 23 escaneos vulnerables
📄 Página: 1 de 3
```

### Tabla de Resultados

#### **Columnas Mostradas**
| Columna | Información | Ejemplo |
|---------|-------------|---------|
| **URL/Sitio** | Título y URL del sitio | "Mi Sitio Web"<br>`https://ejemplo.com` |
| **Cliente** | Empresa asignada | 🏢 Empresa ABC |
| **Estado** | Respuesta HTTP | 🟢 200 / 🔴 404 |
| **Vulnerabilidades** | Contador de vulnerabilidades | 🛡️ 3 |
| **Librerías** | Estadísticas del escaneo | 📚 12 📁 45 ✅ Revisado |
| **Fecha** | Fecha del escaneo | 2025-08-14 |
| **Acciones** | Botones disponibles | Ver, Vulns, Toggle |

#### **Ejemplo de Fila**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🌐 Portal Empresa ABC                    🏢 Empresa ABC    🟢 200   │
│    https://portal.empresaabc.com                                     │
│                                                                     │
│ 🛡️ 5 vulnerabilidades    📚 18  📁 42  ✅ Revisado    2025-08-14   │
│                                                                     │
│ [👁️ Ver] [🛡️ Vulns] [✅]                                            │
└─────────────────────────────────────────────────────────────────────┘
```

### Acciones Disponibles

#### **Por Escaneo**
- **👁️ Ver**: Ir a detalles completos del escaneo
- **🛡️ Vulns**: Ir directamente a pestaña de librerías (`/scan/123#libraries`)
- **✅ Toggle**: Marcar/desmarcar como revisado

#### **Filtrado y Búsqueda**
```
🔍 EJEMPLOS DE BÚSQUEDA
──────────────────────
"jquery"        → Escaneos con librerías jQuery vulnerables
"empresa"       → Escaneos de clientes con "empresa" en el nombre
"ejemplo.com"   → Escaneos de URLs que contienen "ejemplo.com"
"bootstrap css" → Librerías Bootstrap CSS con problemas
```

### Flujo de Trabajo Típico

#### **Gestión de Vulnerabilidades**
1. **Acceder a estadísticas** → Ver todos los sitios vulnerables
2. **Identificar criticidad** → Ordenar por cantidad de vulnerabilidades
3. **Filtrar por cliente** → Si es necesario priorizar un cliente
4. **Revisar vulnerabilidades**:
   ```
   🛡️ Hacer clic en "Vulns" → Va directo a librerías vulnerables
   📊 Evaluar cada vulnerabilidad → Criticidad y impacto
   📝 Documentar recomendaciones → En notas o sistema externo
   ✅ Marcar como revisado → Toggle de revisión
   ```
5. **Seguimiento** → El escaneo sale de la lista de pendientes

#### **Casos de Uso Específicos**

**Auditoría de Seguridad:**
```
📋 PROCESO DE AUDITORÍA
──────────────────────
1. Acceder a /statistics
2. Exportar lista completa → CSV o Excel
3. Revisar cada vulnerabilidad crítica
4. Generar reporte ejecutivo
5. Marcar todo como revisado
```

**Gestión por Prioridades:**
```
🚨 VULNERABILIDADES CRÍTICAS (5+ vulns)
🟡 VULNERABILIDADES MODERADAS (2-4 vulns)  
🟢 VULNERABILIDADES MENORES (1 vuln)
```

### Paginación y Navegación

- **20 resultados por página**
- **Preservación de búsqueda** en navegación
- **Enlaces directos** para compartir filtros específicos

---

## 📊 Exportación de Reportes {#exportación}

### Tipos de Reportes Disponibles

El sistema ofrece **múltiples formatos** de exportación para diferentes necesidades organizacionales.

### Formatos Disponibles

#### **1. 📄 Reporte PDF**
**Uso:** Presentaciones ejecutivas, documentación formal

**Características:**
- ✅ **Formato profesional** con tablas estilizadas
- ✅ **Información completa** de vulnerabilidades
- ✅ **Gráficos y estadísticas** visuales
- ✅ **Headers y footers** con metadatos

**Contenido:**
```
📄 REPORTE PDF - ANÁLISIS DE SEGURIDAD
────────────────────────────────────────
🏢 Cliente: Empresa ABC
🌐 Sitio: https://ejemplo.com
📅 Fecha: 2025-08-14
👤 Generado por: juan.perez

📊 RESUMEN EJECUTIVO
• Total Librerías: 12
• Vulnerabilidades: 5 críticas, 2 moderadas
• Puntuación Seguridad: 65%

📚 LIBRERÍAS VULNERABLES
┌────────────────────────────────────────┐
│ LIBRERÍA     │ VERSIÓN │ CRITICIDAD    │
├────────────────────────────────────────┤
│ jQuery       │ 2.1.0   │ 🔴 CRÍTICA    │
│ Bootstrap    │ 3.3.7   │ 🟡 MODERADA   │
└────────────────────────────────────────┘

🛡️ RECOMENDACIONES
• Actualizar jQuery a versión 3.6.0+
• Implementar Content Security Policy
• Revisar configuración de headers
```

#### **2. 📊 Exportación CSV**
**Uso:** Análisis de datos, importación a Excel, análisis masivo

**Estructura:**
```csv
SCAN_INFO
id,url,scan_date,status_code,title,client_name
123,https://ejemplo.com,2025-08-14,200,Mi Sitio,Empresa ABC

LIBRARIES
library_name,version,type,latest_safe_version,vulnerability
jQuery,2.1.0,js,3.6.0,YES
Bootstrap,4.5.2,css,5.3.0,NO

SECURITY_HEADERS
header_name,present,value,recommendation
HSTS,YES,max-age=31536000,Good
CSP,NO,,Implement CSP policy
```

#### **3. 📈 Libro Excel (Multi-hoja)**
**Uso:** Análisis detallado, reportes departamentales

**Hojas incluidas:**
1. **📋 Scan Overview**: Resumen general
2. **📚 Libraries**: Librerías con formato condicional
3. **🛡️ Security Analysis**: Headers de seguridad
4. **📁 JS CSS Files**: Archivos encontrados
5. **🔍 Version Strings**: Strings de versión detectados
6. **🌐 HTTP Headers**: Headers completos

**Formato profesional:**
- ✅ **Encabezados estilizados** con colores
- ✅ **Formato condicional** (rojo para vulnerabilidades)
- ✅ **Auto-ajuste** de columnas
- ✅ **Filtros automáticos** en tablas

#### **4. 🌐 Reporte HTML Mejorado**
**Uso:** Visualización web, compartir enlaces

**Características:**
- ✅ **Interface interactiva** con pestañas
- ✅ **Gráficos dinámicos** con Chart.js
- ✅ **Responsive design** para móviles
- ✅ **Enlaces clickeables** a recursos externos

### Proceso de Exportación

#### **Desde Página de Detalles**
1. **Ir a escaneo específico** → `/scan/123`
2. **Hacer clic** en "📥 Exportar ▼"
3. **Seleccionar formato**:
   ```
   📄 Reportes
   ├─ 🌐 Reporte HTML Mejorado
   
   📥 Descargas  
   ├─ 📄 Exportar como PDF
   ├─ 📊 Exportar como CSV
   └─ 📈 Exportar como Excel
   ```
4. **Descarga automática** o apertura en nueva pestaña

#### **Metadatos Incluidos**
```
📋 INFORMACIÓN DEL REPORTE
──────────────────────────
🏢 Cliente: Empresa ABC
🌐 URL: https://ejemplo.com  
📅 Fecha Escaneo: 2025-08-14 15:30
📅 Fecha Reporte: 2025-08-14 16:45
👤 Generado por: juan.perez
🔄 Versión: 2.0
🎯 Propósito: Análisis de vulnerabilidades
```

### Casos de Uso por Formato

#### **PDF - Para Ejecutivos**
```
👔 AUDIENCIA: C-Level, Gerentes
📊 CONTENIDO: Resumen ejecutivo, métricas clave
🎯 PROPÓSITO: Toma de decisiones, presupuestos
📧 DISTRIBUCIÓN: Email, presentaciones
```

#### **Excel - Para Analistas**
```
🔍 AUDIENCIA: Equipos técnicos, analistas
📊 CONTENIDO: Datos detallados, análisis avanzado
🎯 PROPÓSITO: Investigación, correlaciones
💻 USO: Análisis offline, dashboards personalizados
```

#### **CSV - Para Integración**
```
⚙️ AUDIENCIA: Sistemas automatizados
📊 CONTENIDO: Datos estructurados, campos separados
🎯 PROPÓSITO: ETL, análisis masivo, reporting
🔄 USO: Importación a sistemas de SIEM, BI
```

#### **HTML - Para Colaboración**
```
🌐 AUDIENCIA: Equipos distribuidos
📊 CONTENIDO: Interface interactiva
🎯 PROPÓSITO: Compartir resultados, colaboración
🔗 USO: Enlaces por email, wikis corporativos
```

---

## 👥 Gestión de Usuarios (Solo Administradores) {#usuarios}

### Acceso Exclusivo

Esta funcionalidad está **disponible únicamente** para usuarios con rol **Administrador**.

**URL:** `http://localhost:5000/users`

### Información de Usuarios

#### **Datos Almacenados**
- **Username**: Identificador único de usuario
- **Password**: Hash seguro (Werkzeug)
- **Role**: Administrador o Analista
- **Estado**: Activo/Inactivo
- **Fecha de creación**: Timestamp automático

#### **Ejemplo de Usuario**
```
👤 INFORMACIÓN DEL USUARIO
──────────────────────────
🆔 Username: juan.perez
🛡️ Rol: Analista
✅ Estado: Activo
📅 Creado: 2025-06-15
🔑 Última contraseña: Hace 30 días
```

### Operaciones CRUD

#### **Crear Usuario**
1. **Hacer clic** en "➕ Nuevo Usuario"
2. **Completar formulario**:
   ```
   👤 Username: [Requerido] maria.lopez
   🔑 Contraseña: [Requerida] ********
   🔄 Confirmar: [Requerida] ********
   🛡️ Rol: [Analista ▼]
   ```
3. **Validaciones automáticas**:
   - Username único
   - Contraseña mínimo 6 caracteres
   - Confirmación coincidente
4. **Guardar**: Usuario aparece en lista

#### **Cambiar Contraseña de Usuario**
1. **Hacer clic** en "🔑 Cambiar Contraseña"
2. **Completar formulario**:
   ```
   👤 Usuario: maria.lopez (read-only)
   🔑 Nueva Contraseña: ********
   🔄 Confirmar: ********
   ```
3. **Guardar**: Password se actualiza inmediatamente

#### **Cambiar Rol de Usuario**
1. **Hacer clic** en "🔄 Cambiar Rol"
2. **Seleccionar nuevo rol**:
   ```
   👤 Usuario: maria.lopez
   🛡️ Rol Actual: Analista
   🔄 Nuevo Rol: [Administrador ▼]
   ```
3. **Confirmar**: Cambio toma efecto en próximo login

#### **Eliminar Usuario**
1. **Hacer clic** en "🗑️ Eliminar"
2. **Confirmar en modal**:
   ```
   ⚠️ ¿ELIMINAR USUARIO?
   ────────────────────
   Usuario: maria.lopez
   Rol: Analista
   
   Esta acción no se puede deshacer.
   [Cancelar] [🗑️ Eliminar]
   ```
3. **Validaciones**:
   - No puede eliminar su propio usuario
   - Confirma eliminación definitiva

### Diferencias entre Roles

#### **👑 Administrador**
```
✅ PERMISOS COMPLETOS
─────────────────────
• Gestión de usuarios (CRUD completo)
• Gestión de clientes
• Análisis de sitios web  
• Revisión de vulnerabilidades
• Catálogo global de librerías
• Estadísticas y reportes
• Exportación de datos
• Configuración del sistema
```

#### **👤 Analista**
```
✅ PERMISOS DE ANÁLISIS
──────────────────────
• Gestión de clientes
• Análisis de sitios web
• Revisión de vulnerabilidades  
• Catálogo global de librerías
• Estadísticas y reportes
• Exportación de datos

❌ RESTRICCIONES
───────────────
• NO puede gestionar usuarios
• NO puede cambiar roles
• NO puede eliminar usuarios
```

### Navegación Adaptiva

#### **Menú para Administradores**
```
🏠 Panel de Control
📊 Estadísticas  
🏢 Clientes
📚 Librerías Globales
👥 Usuarios          ← Solo administradores
```

#### **Menú para Analistas**
```
🏠 Panel de Control
📊 Estadísticas
🏢 Clientes  
📚 Librerías Globales
```

### Seguridad y Validaciones

#### **Validaciones de Username**
- ✅ **Único**: No puede repetirse
- ✅ **Caracteres válidos**: Solo letras, números, puntos, guiones
- ✅ **Longitud**: 3-50 caracteres

#### **Validaciones de Contraseña**
- ✅ **Longitud mínima**: 6 caracteres
- ✅ **Confirmación**: Debe coincidir
- ✅ **Hash seguro**: Werkzeug PBKDF2

#### **Protecciones del Sistema**
- ✅ **Auto-eliminación**: Usuario no puede eliminarse a sí mismo
- ✅ **Sesiones**: Login requerido para todas las operaciones
- ✅ **CSRF**: Tokens en todos los formularios

---

## 🔄 Flujos de Trabajo Típicos {#flujos}

### Flujo 1: Análisis Inicial de Cliente Nuevo

#### **Escenario**
Nueva empresa solicita auditoría de seguridad de sus sitios web.

#### **Pasos**
1. **Crear Cliente** (`/clients`):
   ```
   🏢 Nombre: TechCorp S.A.
   📧 Email: seguridad@techcorp.com
   📞 Teléfono: +56 9 1234 5678
   🌐 Sitio: https://techcorp.com
   ```

2. **Análisis Masivo** (`/`):
   ```
   📝 URLs:
   https://techcorp.com
   https://app.techcorp.com
   https://blog.techcorp.com
   https://store.techcorp.com
   
   🏢 Cliente: TechCorp S.A.
   ⏱️ Delay: 3 segundos
   ```

3. **Revisión de Resultados**:
   ```
   📊 Dashboard → Filtrar por "TechCorp"
   📋 4 escaneos realizados
   ⚠️ 15 vulnerabilidades encontradas
   🕐 Todos pendientes de revisión
   ```

4. **Análisis Detallado**:
   ```
   Para cada escaneo:
   • 👁️ Ver detalles
   • 📚 Revisar librerías vulnerables
   • 📄 Documentar findings críticos
   • ✅ Marcar como revisado
   ```

5. **Reporte Final**:
   ```
   📊 Estadísticas → Filtrar "techcorp"
   📄 Exportar PDF ejecutivo
   📈 Exportar Excel detallado
   📧 Enviar a cliente
   ```

**Tiempo estimado:** 2-3 horas

---

### Flujo 2: Monitoreo Continuo de Vulnerabilidades

#### **Escenario**
Revisión semanal de nuevas vulnerabilidades en sitios monitoreados.

#### **Pasos**
1. **Revisión de Estadísticas** (`/statistics`):
   ```
   📊 23 escaneos con vulnerabilidades
   🔍 Buscar por cliente específico si es necesario
   📈 Identificar tendencias
   ```

2. **Priorización**:
   ```
   🚨 ALTA PRIORIDAD (5+ vulnerabilidades):
   • https://portal-bancario.com → 8 vulns
   • https://ecommerce-cliente.com → 6 vulns
   
   🟡 MEDIA PRIORIDAD (2-4 vulnerabilidades):
   • https://blog-empresa.com → 3 vulns
   
   🟢 BAJA PRIORIDAD (1 vulnerabilidad):
   • https://sitio-simple.com → 1 vuln
   ```

3. **Análisis por Prioridad**:
   ```
   Para sitios alta prioridad:
   🛡️ Clic en "Vulns" → Ir directo a vulnerabilidades
   📋 Evaluar cada librería vulnerable:
     • ¿Es crítica la funcionalidad?
     • ¿Hay exploits públicos?
     • ¿Qué datos maneja el sitio?
   📝 Documentar recomendaciones
   📞 Contactar cliente si es crítico
   ✅ Marcar como revisado
   ```

4. **Seguimiento**:
   ```
   📅 Programar re-análisis en 1 semana
   📊 Documentar métricas de mejora
   📈 Reportar a management
   ```

**Frecuencia:** Semanal
**Tiempo por ciclo:** 1-2 horas

---

### Flujo 3: Auditoría de Cumplimiento Regulatorio

#### **Escenario**
Cliente del sector financiero necesita cumplir regulaciones de ciberseguridad.

#### **Pasos**
1. **Análisis Comprehensivo**:
   ```
   🏦 Cliente: Banco Regional
   🌐 Sitios críticos:
   • https://bancoonline.com (portal transaccional)
   • https://admin.bancoonline.com (panel admin)
   • https://api.bancoonline.com (API backend)
   ```

2. **Evaluación de Headers de Seguridad**:
   ```
   Para cada sitio, revisar:
   ✅ HSTS: Strict-Transport-Security
   ✅ CSP: Content-Security-Policy  
   ✅ X-Frame-Options: DENY/SAMEORIGIN
   ✅ X-Content-Type-Options: nosniff
   ❌ Permissions-Policy: (implementar)
   ❌ Referrer-Policy: (implementar)
   
   📊 Puntuación objetivo: >90%
   ```

3. **Inventario de Librerías**:
   ```
   📚 Catálogo completo:
   • JavaScript: 23 librerías detectadas
   • CSS: 8 frameworks identificados
   • ⚠️ Vulnerabilidades críticas: 3
   • 🟡 Vulnerabilidades moderadas: 7
   ```

4. **Reporte de Cumplimiento**:
   ```
   📄 Generar PDF formal con:
   • Resumen ejecutivo
   • Matriz de riesgos
   • Plan de remediación
   • Timeline de implementación
   • Recomendaciones técnicas
   ```

5. **Plan de Remediación**:
   ```
   📋 ACCIONES INMEDIATAS (0-7 días):
   • Actualizar jQuery 2.1.0 → 3.6.0
   • Implementar CSP headers
   
   📋 ACCIONES MEDIANO PLAZO (1-4 semanas):
   • Actualizar Bootstrap 3.3.7 → 5.3.0  
   • Implementar Permissions-Policy
   
   📋 ACCIONES LARGO PLAZO (1-3 meses):
   • Migrar a Angular versión LTS
   • Implementar monitoring continuo
   ```

**Entregables:**
- 📄 Reporte ejecutivo (PDF)
- 📊 Datos técnicos (Excel)
- 📋 Plan de acción (Excel)
- 🔄 Cronograma de seguimiento

---

### Flujo 4: Onboarding de Nuevo Analista

#### **Escenario**
Incorporar nuevo miembro al equipo de ciberseguridad.

#### **Pasos**
1. **Creación de Usuario** (Admin):
   ```
   👤 Username: nuevo.analista
   🔑 Contraseña: temp123456
   🛡️ Rol: Analista
   📧 Notificar credenciales por canal seguro
   ```

2. **Primer Login**:
   ```
   🔑 Login con credenciales temporales
   🔄 Cambiar contraseña obligatoriamente:
     • Contraseña actual: temp123456
     • Nueva contraseña: [segura]
     • Confirmar nueva contraseña
   ```

3. **Capacitación Guiada**:
   ```
   📚 Revisión de documentación:
   • Leer ayuda.md completa
   • Familiarizarse con interface
   
   🎯 Ejercicio práctico:
   • Analizar 3 sitios de prueba
   • Identificar vulnerabilidades
   • Practicar exportación de reportes
   
   📋 Casos reales supervisados:
   • Revisar escaneos pendientes
   • Generar primer reporte
   • Presentar findings al equipo
   ```

4. **Asignación de Responsabilidades**:
   ```
   📊 Clientes asignados: 2-3 clientes menores
   📅 Frecuencia: Revisión semanal
   📈 Objetivos: 95% escaneos revisados en 48h
   ```

**Timeline de onboarding:** 1 semana

---

### Flujo 5: Gestión de Incidente de Seguridad

#### **Escenario**
Se descubre nueva vulnerabilidad crítica en jQuery que afecta múltiples clientes.

#### **Pasos**
1. **Identificación Rápida** (`/statistics`):
   ```
   🔍 Buscar: "jquery"
   📊 Resultados: 45 sitios afectados
   🚨 Filtrar por versiones < 3.4.0
   ```

2. **Clasificación por Criticidad**:
   ```
   🚨 CRÍTICO (sitios transaccionales):
   • banco-online.com → jQuery 2.1.0
   • ecommerce-major.com → jQuery 1.12.4
   
   🟡 ALTO (sitios públicos con forms):
   • contacto-empresa.com → jQuery 2.2.0
   • portal-gobierno.com → jQuery 3.1.0
   
   🟢 MEDIO (sitios informativos):
   • blog-personal.com → jQuery 3.2.0
   ```

3. **Notificación Urgente**:
   ```
   📧 Email automático a clientes críticos:
   
   ASUNTO: [URGENTE] Vulnerabilidad crítica jQuery
   
   Estimado cliente,
   
   Hemos identificado una vulnerabilidad crítica en su sitio:
   • Sitio: https://banco-online.com
   • Librería: jQuery 2.1.0  
   • Riesgo: Cross-Site Scripting (XSS)
   • Acción requerida: Actualizar a jQuery 3.6.0+
   • Plazo: 24-48 horas
   
   Adjunto reporte técnico detallado.
   ```

4. **Seguimiento**:
   ```
   📋 Tracking de remediación:
   • Crear ticket por cada sitio crítico
   • Seguimiento diario de actualizaciones
   • Re-análisis post-fix
   • Confirmación de remediación
   ```

5. **Documentación**:
   ```
   📄 Reporte de incidente:
   • Timeline de descubrimiento
   • Sitios afectados
   • Acciones tomadas
   • Lecciones aprendidas
   • Mejoras de proceso
   ```

**SLA de respuesta:**
- 🚨 Crítico: 4 horas
- 🟡 Alto: 24 horas  
- 🟢 Medio: 72 horas

---

## ❗ Solución de Problemas {#problemas}

### Problemas de Autenticación

#### **Error: "Credenciales inválidas"**
```
🚫 SÍNTOMA: No puede hacer login
🔍 CAUSAS POSIBLES:
• Username incorrecto
• Contraseña incorrecta  
• Usuario fue eliminado
• Base de datos corrupta

✅ SOLUCIONES:
1. Verificar credenciales por defecto:
   Usuario: gabo
   Contraseña: admin123

2. Resetear contraseña (como admin):
   • Login con otro usuario admin
   • Ir a /users
   • Cambiar contraseña del usuario

3. Crear usuario de emergencia:
   python -c "
   from dashboard import create_emergency_user
   create_emergency_user('admin', 'password123')
   "
```

#### **Error: "Sesión expirada"**
```
🚫 SÍNTOMA: Redirige constantemente al login
🔍 CAUSA: Problemas con cookies/sesiones

✅ SOLUCIÓN:
• Limpiar cookies del navegador
• Cerrar y abrir navegador
• Verificar FLASK_SECRET_KEY
```

---

### Problemas de Análisis

#### **Error: "Timeout al analizar URL"**
```
🚫 SÍNTOMA: Análisis falla con timeout
🔍 CAUSAS POSIBLES:
• Sitio web muy lento
• Sitio requiere autenticación
• Problemas de red
• Anti-bot protection

✅ SOLUCIONES:
1. Verificar URL manualmente en navegador
2. Intentar con diferentes URLs del mismo sitio
3. Aumentar timeout en código (para desarrolladores)
4. Usar herramientas alternativas para sitios complejos
```

#### **Error: "No se detectan librerías"**
```
🚫 SÍNTOMA: Escaneo completo pero 0 librerías
🔍 CAUSAS POSIBLES:
• Sitio usa only JavaScript dinámico
• Librerías cargadas por CDN no reconocido
• Sitio SPA (Single Page Application)

✅ SOLUCIONES:
1. Revisar pestaña "Archivos JS/CSS":
   • Si hay archivos → Agregar librerías manualmente
   • Si no hay archivos → Sitio puede usar JS dinámico

2. Agregar librerías manualmente:
   • Ir a detalles del escaneo
   • Pestaña "Librerías"
   • "➕ Agregar Librería Manual"
   • Completar información conocida
```

#### **Error: "Muchos errores 404 en archivos"**
```
🚫 SÍNTOMA: Lista de archivos con errores 404
🔍 CAUSA: URLs relativas mal resueltas

✅ SOLUCIÓN:
• Normal en muchos sitios
• Revisar archivos que SÍ cargaron (status 200)
• Agregar librerías manualmente si es necesario
```

---

### Problemas de Base de Datos

#### **Error: "Database is locked"**
```
🚫 SÍNTOMA: Error al guardar datos
🔍 CAUSA: Múltiples procesos accediendo SQLite

✅ SOLUCIONES:
1. Cerrar todas las instancias de la aplicación
2. Reiniciar aplicación
3. Si persiste:
   rm analysis.db.lock  # Si existe
   python dashboard.py
```

#### **Error: "No such column"**
```
🚫 SÍNTOMA: Error SQL sobre columna faltante
🔍 CAUSA: Esquema de BD desactualizado

✅ SOLUCIÓN:
• La migración debería ser automática
• Si falla, resetear BD:
  rm analysis.db
  python dashboard.py
```

#### **Error: "Duplicate entry"**
```
🚫 SÍNTOMA: Error al crear cliente/usuario
🔍 CAUSA: Nombre ya existe

✅ SOLUCIÓN:
• Usar nombre único
• Verificar en lista existente
• Agregar sufijo numérico si es necesario
```

---

### Problemas de Rendimiento

#### **Lentitud en Dashboard con muchos escaneos**
```
🐌 SÍNTOMA: Dashboard carga muy lento
🔍 CAUSA: Muchos escaneos en BD (>1000)

✅ SOLUCIONES:
1. Usar filtros para reducir resultados:
   • Filtrar por cliente específico
   • Usar búsqueda para limitar scope

2. Limpiar escaneos antiguos:
   • Eliminar escaneos obsoletos
   • Mantener solo últimos 6 meses

3. Reset completo si es necesario:
   • Exportar datos importantes
   • Reset BD desde dashboard
```

#### **Análisis masivo muy lento**
```
🐌 SÍNTOMA: Análisis masivo toma horas
🔍 CAUSA: Delay muy alto o muchas URLs

✅ SOLUCIONES:
• Reducir delay entre requests (mínimo 1 segundo)
• Dividir listas grandes en lotes de 10-20 URLs
• Ejecutar en horarios de menor carga de red
```

---

### Problemas de Exportación

#### **Error: "No module named 'reportlab'"**
```
🚫 SÍNTOMA: Falla exportación PDF
🔍 CAUSA: Dependencia faltante

✅ SOLUCIÓN:
pip install reportlab
# Reiniciar aplicación
```

#### **PDF/Excel vacío o malformado**
```
🚫 SÍNTOMA: Archivo se genera pero sin contenido
🔍 CAUSA: Datos faltantes en escaneo

✅ SOLUCIONES:
1. Verificar que escaneo tiene datos:
   • Ir a detalles del escaneo
   • Verificar que hay librerías/archivos

2. Re-analizar si está vacío:
   • Botón "🔄 Re-escanear"
   • Esperar a que complete
   • Intentar exportar nuevamente
```

---

### Contacto y Soporte

#### **Canales de Soporte**
```
📧 Email técnico: soporte@empresa.com
📞 Teléfono: +56 2 1234 5678
💬 Slack: #ciberseguridad
🎫 Tickets: sistema-tickets.empresa.com
```

#### **Información para Reportar Problemas**
```
📋 INCLUIR EN REPORTE:
• URL donde ocurre el problema
• Usuario afectado
• Pasos para reproducir
• Mensaje de error completo
• Captura de pantalla
• Navegador y versión
• Hora aproximada del incidente
```

#### **Escalación**
```
🟢 BAJO: Reportar por email (respuesta 24-48h)
🟡 MEDIO: Reportar por Slack (respuesta 4-8h)  
🔴 ALTO: Llamar teléfono + Slack (respuesta 1-2h)
🚨 CRÍTICO: Llamar + escalar a manager (respuesta inmediata)
```

---

## 📞 Información de Contacto

**Sistema:** Analizador de Librerías JS/CSS v2.0  
**Documentación:** `/ayuda.md`  
**Última actualización:** Agosto 2025  
**Soporte técnico:** Equipo de Ciberseguridad

---

*Este documento se actualiza regularmente. Para sugerencias de mejora, contactar al equipo de desarrollo.*