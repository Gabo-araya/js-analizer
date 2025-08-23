### Plan de Implementación: Añadir Columnas de Versión Global

El objetivo es añadir dos nuevas columnas a la tabla de bibliotecas en la página de "Detalles del Escaneo" (`/scan/...`) que muestren la "Versión Segura" y la "Última Versión" directamente desde el catálogo global, para aquellas bibliotecas que tengan una asociación.

#### 1. Cambios en el Backend (`dashboard.py`)

1.  **Función `scan_detail()`:**
    -   **Acción:** Se debe modificar la consulta SQL que obtiene las bibliotecas de un escaneo para que también obtenga los datos de la biblioteca global asociada.
    -   **Implementación:** Se utilizará un `LEFT JOIN` desde la tabla `libraries` hacia la tabla `global_libraries` usando la columna `global_library_id` que ya hemos implementado.
    -   **Detalles de la consulta:**
        -   Se seleccionarán los campos `latest_safe_version` y `latest_version` de la tabla `global_libraries`.
        -   Se usarán alias para estos nuevos campos (por ejemplo, `gl_latest_safe_version` y `gl_latest_version`) para evitar conflictos con los campos que ya existen en la tabla `libraries`.
    -   **Resultado:** La función pasará a la plantilla una lista de bibliotecas donde cada una contendrá, además de sus datos propios, los datos de la versión de su biblioteca global asociada (si existe).

    **Consulta SQL a implementar:**
    ```sql
    SELECT
        l.id, l.library_name, l.version, l.type, l.source_url, l.description,
        l.latest_safe_version, l.latest_version, l.is_manual, l.global_library_id,
        gl.latest_safe_version as gl_latest_safe_version,
        gl.latest_version as gl_latest_version
    FROM libraries l
    LEFT JOIN global_libraries gl ON l.global_library_id = gl.id
    WHERE l.scan_id = ?
    ORDER BY l.type, l.library_name
    ```

#### 2. Cambios en el Frontend (`templates/scan_detail.html`)

1.  **Pestaña "Bibliotecas":**
    -   **Acción:** Se modificará la estructura de la tabla de bibliotecas para añadir las dos nuevas columnas.
    -   **Implementación:**
        1.  **Cabecera de la tabla (`<thead>`):**
            -   Se añadirá un `<th>` para "Versión Segura Global" justo después de la columna "Versión Segura".
            -   Se añadirá un `<th>` para "Última Versión Global" justo después de la columna "Última Versión".
        2.  **Cuerpo de la tabla (`<tbody>`):**
            -   Por cada fila (biblioteca), se añadirán dos nuevas celdas (`<td>`).
            -   La primera celda mostrará el valor de `library.gl_latest_safe_version`. Si el valor existe, se mostrará dentro de un `badge` de color (ej. verde). Si no, se mostrará un guion (`-`).
            -   La segunda celda mostrará el valor de `library.gl_latest_version`. Si el valor existe, se mostrará dentro de un `badge` de otro color (ej. azul). Si no, se mostrará un guion (`-`).

Este plan no requiere cambios en la base de datos ni en los archivos JavaScript, ya que se apoya en la estructura existente.
