## Guía de Usuario: Herramienta de Análisis de Seguridad de Librerías

### Introducción
Bienvenido a la herramienta de análisis de seguridad de librerías JS/CSS. Esta aplicación te permite escanear sitios web para identificar las librerías que utilizan, detectar vulnerabilidades conocidas y gestionar los resultados de forma centralizada.

### Escanear URLs
- **Análisis Individual:** Ingresa una URL en el campo principal del dashboard y haz clic en "Analizar".
- **Análisis en Lote:** Haz clic en "Análisis en Lote", pega una lista de URLs (una por línea) y haz clic en "Iniciar Análisis".

### Reportes y Detalles
Cada escaneo genera un reporte detallado que incluye:
- **Librerías Detectadas:** Lista de librerías JS y CSS encontradas, con su versión.
- **Cadenas de Versión:** Líneas de código específicas donde se encontró la palabra "version", útil para investigación manual.
- **Archivos Encontrados:** Todas las URLs de archivos JS/CSS vinculados en la página.
- **Análisis de Cabeceras:** Revisión de las cabeceras de seguridad HTTP.

Puedes exportar los reportes en formato PDF, CSV y Excel.

### Gestión de Clientes
La sección "Clientes" te permite agrupar escaneos por cliente. Puedes crear, editar y asignar escaneos a clientes específicos para una mejor organización.

### Bibliotecas Globales
El catálogo de bibliotecas globales es una base de datos centralizada de librerías conocidas. Aquí puedes:
- Definir la **última versión segura** y la **última versión disponible** de una librería.
- Esta información se usa en los reportes para determinar si una librería detectada es vulnerable.
- Puedes importar y exportar este catálogo en formato CSV o JSON.

### Historial de Acciones
El sistema registra acciones importantes como inicios de sesión, escaneos, y modificaciones de datos. Puedes consultar este historial para auditoría y seguimiento.

---

## Preguntas Frecuentes (FAQ)

### ¿Cómo funciona la relación entre las bibliotecas de un escaneo y las bibliotecas globales?

**Respuesta corta: Mediante una asociación opcional.**

-   **Asociación:** Al añadir o editar una biblioteca manual en un escaneo, puedes **asociarla opcionalmente** a una biblioteca del Catálogo Global.
-   **Vista de Detalle del Escaneo:**
    -   Si una biblioteca está asociada, la tabla mostrará las versiones ("Segura" y "Última") de la biblioteca global junto a las versiones detectadas en el escaneo.
    -   Aparecerá un icono de enlace <i class="bi bi-link-45deg"></i> junto al nombre de la biblioteca para indicar que está asociada.
    -   Se mostrará un checkmark verde (✅) si la versión segura o la última versión de la biblioteca del escaneo coincide con la versión correspondiente de la biblioteca global.
-   **Independencia de los datos:** Aunque estén asociadas, los datos de la biblioteca del escaneo (versión, versión segura, etc.) siguen siendo independientes. Cambiar la biblioteca global **no** alterará los datos ya guardados en escaneos anteriores. La asociación simplemente permite visualizar y comparar los datos globales en la vista de detalle.

### Si cambio la versión en una biblioteca global, ¿cambia en las bibliotecas de un escaneo existente?

**Respuesta corta: No.**

Los datos de las bibliotecas dentro de un escaneo (tanto las detectadas automáticamente como las manuales) son **independientes** del catálogo global una vez que se han guardado.

Si actualizas la "última versión" o la "última versión segura" en el catálogo global, estos cambios **no se propagarán** a las bibliotecas que ya existen en los resultados de escaneos anteriores. Sin embargo, gracias a la nueva funcionalidad de asociación, podrás ver la nueva información global directamente en la tabla de detalles del escaneo para una comparación más fácil.
