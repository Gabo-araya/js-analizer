# Metodología de Detección de Versiones de Bibliotecas

Este documento detalla la metodología utilizada en el proyecto para identificar bibliotecas de JavaScript y CSS, así como sus respectivas versiones, a partir del análisis de URLs.

## 1. Componentes Principales

El sistema de detección se basa en tres archivos clave que trabajan en conjunto:

-   `js_analyzer.py`: El orquestador principal. Se encarga de recibir una URL, descargar su contenido HTML, e iniciar el proceso de análisis para encontrar archivos JS y CSS.
-   `library_detector.py`: Contiene la lógica para una detección "avanzada". Utiliza patrones de expresiones regulares (RegEx) para identificar bibliotecas basándose en el nombre del archivo y su contenido.
-   `library_signatures.py`: Define un sistema de "firmas" más profundo y específico para cada biblioteca. En lugar de solo buscar en nombres de archivo, analiza el contenido real del código en busca de patrones únicos, como definiciones de variables, funciones o comentarios de cabecera, para una identificación más precisa.

## 2. Flujo General de Detección

El proceso de análisis para una URL determinada sigue estos pasos:

1.  **Análisis Inicial (Orquestado por `js_analyzer.py`)**:
    *   Se descarga el contenido HTML de la URL.
    *   Se utiliza `BeautifulSoup` para parsear el HTML y extraer todas las etiquetas `<script src="...">` (JavaScript) y `<link rel="stylesheet" href="...">` (CSS).
    *   Para cada archivo JS/CSS encontrado, se inicia un análisis más profundo.

2.  **Detección Avanzada por Nombre de Archivo (`library_detector.py`)**:
    *   La URL de cada archivo JS/CSS se pasa al `LibraryDetector`.
    *   Este componente intenta identificar la biblioteca y su versión aplicando una serie de patrones de expresiones regulares sobre el **nombre del archivo**.
    *   Por ejemplo, un archivo llamado `jquery-3.6.0.min.js` coincidirá con el patrón `jquery[-.]?(\d+\.\d+\.\d+)` y extraerá "jQuery" como nombre y "3.6.0" as como la versión.
    *   Este método es rápido pero depende de que el nombre del archivo sea descriptivo.

3.  **Análisis de Contenido y Firmas (`library_signatures.py`)**:
    *   Si la detección por nombre de archivo no es suficiente o para confirmarla, se descarga el contenido del archivo JS/CSS.
    *   El `LibraryDetectionEngine` procesa este contenido y lo compara con una base de datos de "firmas".
    *   Cada firma define patrones específicos que son únicos para una biblioteca. Estos patrones incluyen:
        *   **Patrones de contenido**: Buscan cadenas exactas que definen la versión, como `jQuery.fn.jquery = "3.6.0"`.
        *   **Patrones en comentarios**: Buscan en los comentarios de cabecera, como `/*! jQuery v3.6.0 | (c) OpenJS Foundation */`.
        *   **Patrones de variables y funciones**: Verifican la existencia de variables o funciones globales características, como `window.jQuery` o `React.createElement`.
    *   Una detección se considera positiva si coinciden múltiples patrones, lo que aumenta la confianza en el resultado.

4.  **Escaneo de Cadenas de Versión Genéricas (`js_analyzer.py`)**:
    *   De forma paralela, el sistema busca en cada línea de los archivos JS/CSS cualquier cadena que se parezca a un número de versión.
    *   Utiliza una lista extensa de expresiones regulares para encontrar patrones como:
        *   `version: '1.2.3'`
        *   `@version 1.2.3`
        *   `v1.2.3`
        *   Cualquier secuencia numérica con el formato `X.Y.Z`.
    *   Cuando se encuentra una de estas cadenas, se guarda junto con el contenido de la línea y el número de línea para una revisión manual posterior. Este método ayuda a encontrar versiones en bibliotecas que no son conocidas por el sistema.

## 3. Mecanismos de Identificación de Versiones

La extracción de la versión se realiza a través de los siguientes mecanismos, ordenados de mayor a menor precisión:

1.  **Firmas de Contenido (`library_signatures.py`)**: Es el método más fiable. Busca la declaración explícita de la versión dentro del código fuente de la biblioteca.
    *   Ejemplo: `React.version = "18.2.0"`

2.  **Patrones en Comentarios y Cabeceras (`library_signatures.py` y `library_detector.py`)**: Muy fiable. Las bibliotecas suelen incluir su nombre y versión en los comentarios de cabecera del archivo.
    *   Ejemplo: `/* Bootstrap v5.3.0 */`

3.  **Patrones en Nombres de Archivo (`library_detector.py`)**: Fiable si se sigue una convención de nomenclatura estándar.
    *   Ejemplo: `angular-1.8.2.min.js`

4.  **Búsqueda Genérica de Patrones de Versión (`js_analyzer.py`)**: Es el método menos preciso y sirve como último recurso. Captura cualquier cadena que parezca una versión, pero no puede asociarla directamente a una biblioteca específica sin contexto adicional.
    *   Ejemplo: Encuentra la cadena `"2.5.1"` en una línea de código, pero no sabe si pertenece a una biblioteca o es un valor arbitrario.

## 4. Patrones de Identificación Específicos por Biblioteca

A continuación se detallan los patrones específicos utilizados para la identificación de las bibliotecas más comunes, combinando la detección por nombre de archivo (`library_detector.py`) y por firma de contenido (`library_signatures.py`).

### jQuery

-   **Detección por Nombre de Archivo:**
    -   `jquery[-.]?(\d+\.\d+\.\d+)`: Busca "jquery-" o "jquery." seguido de una versión completa (e.g., `jquery-3.6.0.js`).
    -   `jquery[-.]?v?(\d+\.\d+)`: Busca versiones más cortas, con una "v" opcional (e.g., `jquery-3.6.js` o `jquery.v3.6.min.js`).
    -   `jquery[.-]min\.js`, `jquery[.-]slim[.-]min\.js`: Identifica archivos de jQuery aunque no tengan la versión en el nombre.

-   **Detección por Firma de Contenido:**
    -   **Comentario:** `jQuery\s+JavaScript\s+Library\s+v(\d+\.\d+\.\d+)`
        -   *Ejemplo:* `/*! jQuery JavaScript Library v3.6.0 */`
    -   **Código Fuente (Content Pattern):** `jQuery\.fn\.jquery\s*=\s*["']([^"']+)["']`
        -   *Ejemplo:* `jQuery.fn.jquery = "3.6.0";`
    -   **Variable Característica:** `jQuery\.fn\.jquery`
    -   **Función Característica:** `jQuery\s*=\s*function`

### React

-   **Detección por Nombre de Archivo:**
    -   `react[-.]?(\d+\.\d+\.\d+)`: Busca `react-` seguido de la versión (e.g., `react-18.2.0.js`).
    -   `react[.-]dom[.-]min\.js`, `react[.-]min\.js`: Identifica los archivos principales de React y ReactDOM.

-   **Detección por Firma de Contenido:**
    -   **Cabecera (Header):** `React\s+v(\d+\.\d+\.\d+)`
        -   *Ejemplo:* `// React v18.2.0`
    -   **Código Fuente (Content Pattern):** `React\.version\s*=\s*["']([^"']+)["']`
        -   *Ejemplo:* `React.version = "18.2.0";`
    -   **Variable Característica:** `React\.createElement`, `ReactDOM\.render`

### Vue.js

-   **Detección por Nombre de Archivo:**
    -   `vue[-.]?(\d+\.\d+\.\d+)`: Busca `vue-` o `vue.` con la versión (e.g., `vue.2.6.14.js`).
    -   `vue[.-]min\.js`: Identifica el archivo minificado de Vue.

-   **Detección por Firma de Contenido:**
    -   **Comentario:** `Vue\.js\s+v(\d+\.\d+\.\d+)`
        -   *Ejemplo:* `/*! Vue.js v2.6.14 */`
    -   **Código Fuente (Content Pattern):** `Vue\.version\s*=\s*["']([^"']+)["']`
        -   *Ejemplo:* `Vue.version = '2.6.14'`
    -   **Variable Característica:** `Vue\.prototype`, `Vue\.component`

### Bootstrap (JS y CSS)

-   **Detección por Nombre de Archivo:**
    -   `bootstrap[-.]?(\d+\.\d+\.\d+)`: Busca `bootstrap-` con la versión (e.g., `bootstrap-5.3.0.bundle.js`).
    -   `bootstrap[.-]min\.(js|css)`: Identifica archivos minificados de JS o CSS.

-   **Detección por Firma de Contenido (CSS):**
    -   **Comentario:** `Bootstrap\s+v(\d+\.\d+\.\d+)`
        -   *Ejemplo:* `/*! Bootstrap v5.3.0 | MIT License | https://getbootstrap.com */`
    -   **Código Fuente (Content Pattern):** `\.container\s*\{[^\}]*max-width` (Busca reglas CSS icónicas de Bootstrap).

-   **Detección por Firma de Contenido (JS):**
    -   **Comentario:** `Bootstrap\s+v(\d+\.\d+\.\d+)`
    -   **Variable Característica:** `\$\.fn\.modal`, `\$\.fn\.dropdown` (Verifica si los plugins de jQuery de Bootstrap están presentes).

### Font Awesome

-   **Detección por Nombre de Archivo (CSS):**
    -   `font-?awesome[-.]?(\d+\.\d+\.\d+)`: Busca `font-awesome-` o `fontawesome.` con la versión.
    -   `all[.-]min\.css`: Identifica el archivo principal de Font Awesome 5+.

-   **Detección por Firma de Contenido (CSS):**
    -   **Comentario:** `Font\s+Awesome\s+(\d+\.\d+\.\d+)`
        -   *Ejemplo:* `/*! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com */`
    -   **Código Fuente (Content Pattern):** `\.fa-[a-z-]+:before\s*\{` (Busca la definición de clases de íconos).
    -   **Código Fuente (Content Pattern):** `@font-face.*FontAwesome` (Busca la declaración de la fuente).

## Conclusión

La metodología combina un enfoque de "caja negra" (analizando nombres de archivo desde el exterior) con un enfoque de "caja blanca" (analizando el contenido del código fuente). Este sistema multicapa permite una alta probabilidad de detección, comenzando por los métodos más rápidos y avanzando hacia los más profundos y precisos, asegurando así un equilibrio entre rendimiento y exactitud.