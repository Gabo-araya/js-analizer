### Plan de Implementación: Asociación de Bibliotecas Manuales con Globales

El objetivo es crear una asociación opcional entre las bibliotecas añadidas manualmente en un escaneo y las bibliotecas del catálogo global.

#### 1. Modificación de la Base de Datos

-   **Tabla:** `libraries`
-   **Acción:** Añadir una nueva columna para almacenar la referencia a la biblioteca global.
    -   **Nombre de la columna:** `global_library_id`
    -   **Tipo:** `INTEGER`
    -   **Propiedades:**
        -   Debe ser `NULL` (opcional), para no afectar a las bibliotecas existentes.
        -   Debe ser una clave foránea (FOREIGN KEY) que apunte a `global_libraries(id)`.
        -   Se configurará `ON DELETE SET NULL` para que, si se elimina una biblioteca global, la asociación simplemente se anule sin borrar la biblioteca del escaneo.
-   **Implementación:** Se modificará la función `init_database` en `dashboard.py` para añadir esta columna de forma segura en bases de datos existentes (migración).

#### 2. Cambios en el Backend (`dashboard.py`)

1.  **Actualizar Vistas Existentes:**
    -   **`scan_detail()`:** Se modificará para que:
        -   La consulta a la tabla `libraries` incluya el nuevo campo `global_library_id`.
        -   Se obtenga una lista completa de las bibliotecas globales (`id`, `library_name`) y se pase a la plantilla `scan_detail.html`. Esto es necesario para rellenar el nuevo campo de selección en los modales.
    -   **`add_manual_library()` y `edit_library()`:** Se actualizarán para procesar el `global_library_id` que llegará desde el formulario y lo guardarán/actualizarán en la base de datos.

2.  **Crear Nuevo Endpoint y Vista:**
    -   **Ruta:** Se creará una nueva ruta, por ejemplo, `/asociar-bibliotecas`.
    -   **Lógica:** Esta página mostrará una lista de **todas las bibliotecas manuales que aún no tienen una asociación** (`global_library_id IS NULL`). La consulta unirá las tablas `libraries` y `scans` para mostrar información útil como el nombre de la biblioteca, la versión y un enlace al escaneo al que pertenece.
    -   **Funcionalidad:** Cada elemento de la lista tendrá un formulario (probablemente un menú desplegable) para seleccionar una biblioteca global y un botón "Asociar". Este formulario enviará los datos a una función en el backend que creará la asociación.

#### 3. Cambios en el Frontend (Plantillas y JS)

1.  **`templates/scan_detail.html`:**
    -   **Modales de Añadir/Editar:** Se añadirá un nuevo campo de tipo `<select>` (menú desplegable) llamado "Asociar con Biblioteca Global". Este campo se llenará con la lista de bibliotecas globales. Si una biblioteca ya está asociada, esa opción aparecerá preseleccionada.
    -   **Vista de la Tabla:** En la lista de bibliotecas del escaneo, si una de ellas está asociada a una global, se mostrará un pequeño icono de enlace (`<i class="bi bi-link-45deg"></i>`) junto al nombre, que podría enlazar a la entrada correspondiente en el catálogo global.

2.  **`templates/global_libraries.html`:**
    -   Se añadirá un botón bien visible con el texto "Gestionar Asociaciones Manuales", que dirigirá al usuario a la nueva página `/asociar-bibliotecas`.

3.  **`templates/asociar_bibliotecas.html` (Nuevo Archivo):**
    -   Se creará esta nueva plantilla que mostrará la tabla de bibliotecas manuales no asociadas, con sus respectivos menús desplegables para realizar la asociación.

4.  **`static/js/scan_detail.js`:**
    -   Se actualizará el código JavaScript que se encarga de rellenar los datos del modal de edición para que también gestione el nuevo campo `global_library_id` y seleccione la opción correcta en el menú desplegable.
