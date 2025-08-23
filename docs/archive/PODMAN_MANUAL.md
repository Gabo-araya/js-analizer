# Cómo levantar la aplicación con Podman (Manual)

Este documento proporciona instrucciones paso a paso para levantar la aplicación "NTG JS/CSS Analyzer" utilizando comandos directos de Podman, sin depender de los scripts de `docker-compose` o del directorio `docker/`.

## Prerrequisitos

*   Tener Podman instalado en tu sistema.

## Pasos

### 1. Construir la Imagen de Podman

Primero, necesitas construir la imagen de la aplicación a partir del `Dockerfile` presente en la raíz del proyecto.

1.  Abre una terminal y navega al directorio raíz del proyecto `ntg-js-analyzer`.
2.  Ejecuta el siguiente comando para construir la imagen:

    ```bash
    podman build -t ntg-js-analyzer:latest .
    ```

    Esto creará una imagen llamada `ntg-js-analyzer` con la etiqueta `latest`.

### 2. Crear Directorios Necesarios

La aplicación utiliza directorios para almacenar datos y logs. Asegúrate de que existan en la raíz de tu proyecto:

```bash
mkdir -p data logs
```

### 3. Ejecutar el Contenedor de Podman

Ahora, puedes ejecutar el contenedor utilizando la imagen que acabas de construir. Este comando mapeará los puertos, montará los volúmenes necesarios y establecerá las variables de entorno.

1.  **Crea una red de Podman (si no existe):**
    Si aún no tienes una red llamada `ntg-analyzer-network`, puedes crearla:
    ```bash
podman network create ntg-analyzer-network || true
```
    El `|| true` evita que el comando falle si la red ya existe.

2.  **Ejecuta el contenedor:**
    ```bash
podman run -d \
  --name ntg-js-analyzer \
  -p 5000:5000 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  -e FLASK_SECRET_KEY=tu_clave_secreta_aqui \
  -e TZ=America/Santiago \
  --network ntg-analyzer-network \
  ntg-js-analyzer:latest
```

    **Explicación de las opciones:**
    *   `-d`: Ejecuta el contenedor en modo "detached" (en segundo plano).
    *   `--name ntg-js-analyzer`: Asigna un nombre al contenedor para facilitar su gestión.
    *   `-p 5000:5000`: Mapea el puerto 5000 del host al puerto 5000 del contenedor.
    *   `-v "$(pwd)/data:/app/data"`: Monta el directorio `data` de tu proyecto local en `/app/data` dentro del contenedor.
    *   `-v "$(pwd)/logs:/app/logs"`: Monta el directorio `logs` de tu proyecto local en `/app/logs` dentro del contenedor.
    *   `-e FLASK_ENV=production`: Establece la variable de entorno `FLASK_ENV` a `production`.
    *   `-e FLASK_DEBUG=0`: Deshabilita el modo de depuración de Flask.
    *   `-e FLASK_SECRET_KEY=tu_clave_secreta_aqui`: **IMPORTANTE:** Reemplaza `tu_clave_secreta_aqui` con una clave secreta fuerte y única para tu aplicación.
    *   `-e TZ=America/Santiago`: Establece la zona horaria dentro del contenedor.
    *   `--network ntg-analyzer-network`: Conecta el contenedor a la red `ntg-analyzer-network`.
    *   `ntg-js-analyzer:latest`: La imagen de Podman que se utilizará.

### 4. Verificar el Estado del Contenedor

Para asegurarte de que el contenedor se está ejecutando correctamente:

```bash
podman ps
```

Para ver los logs del contenedor:

```bash
podman logs ntg-js-analyzer
```

### 5. Acceder a la Aplicación

Una vez que el contenedor esté en funcionamiento, puedes acceder a la aplicación en tu navegador web:

```
http://localhost:5000
```

### 6. Detener y Eliminar el Contenedor

Cuando hayas terminado de usar la aplicación, puedes detener y eliminar el contenedor:

```bash
podman stop ntg-js-analyzer
podman rm ntg-js-analyzer
```

