# Configuración de NTG JS Analyzer con Podman

Esta guía proporciona instrucciones detalladas para configurar y ejecutar la aplicación NTG JS Analyzer utilizando Podman como alternativa a Docker.

## 🚀 Inicio Rápido

```bash
# 1. Instalar podman-compose
pip3 install podman-compose

# 2. Crear directorios y base de datos persistente
mkdir -p data logs
touch analysis.db && chmod 666 analysis.db

# 3. Configurar variable de entorno
export FLASK_SECRET_KEY="mi_clave_secreta_muy_segura_$(date +%s)"

# 4. Construir y ejecutar
podman-compose -f podman-compose.yml build --no-cache
podman-compose -f podman-compose.yml up -d

# 5. Ver credenciales generadas
podman logs ntg-js-analyzer | grep -A5 "IMPORTANT"

# 6. Verificar estado y persistencia
podman ps
ls -la analysis.db  # Verificar base de datos persistente

# 7. Acceder a la aplicación
# http://localhost:5000
```

**🎉 Ejemplo de salida exitosa:**
```
Successfully tagged localhost/ntg-js-analyzer_ntg-analyzer:latest
🔐 IMPORTANT: Save these credentials securely!
Username: admin
Password: [contraseña-generada-automáticamente]

Credentials also saved to 'admin_credentials.txt'
🔒 Running in PRODUCTION mode
* Running on http://127.0.0.1:5000
```

## Prerrequisitos

- Podman instalado en el sistema
- podman-compose instalado (opcional, para usar docker-compose syntax)

### Instalación de Podman en sistemas Linux

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y podman

# CentOS/RHEL/Fedora
sudo dnf install -y podman

# Verificar instalación
podman --version
```

### Instalación de podman-compose (opcional)

```bash
pip3 install podman-compose
```

## Métodos de Despliegue

### Método 1: Usando podman-compose (Recomendado)

#### Paso 1: Preparar el entorno

```bash
# Crear directorios necesarios y base de datos persistente
mkdir -p data logs
touch analysis.db && chmod 666 analysis.db

# Configurar variable de entorno para clave secreta
export FLASK_SECRET_KEY="tu_clave_secreta_muy_segura_aqui_cambiar_en_produccion"
```

#### Paso 2: Construir y ejecutar con podman-compose

```bash
# Construir la imagen sin cache (recomendado para primera vez)
podman-compose -f podman-compose.yml build --no-cache

# Ejecutar la aplicación
podman-compose -f podman-compose.yml up -d

# Ver logs
podman-compose -f podman-compose.yml logs -f

# Detener la aplicación
podman-compose -f podman-compose.yml down
```

**⚠️ Solución de problemas comunes:**

Si obtienes error de contenedor duplicado:
```bash
# Eliminar contenedor existente
podman stop ntg-js-analyzer && podman rm ntg-js-analyzer
```

Si hay problemas con la base de datos:
```bash
# Crear archivo de base de datos persistente
touch analysis.db && chmod 666 analysis.db

# Verificar que el archivo existe y tiene permisos
ls -la analysis.db
```

### Método 2: Usando comandos Podman directos

#### Paso 1: Construir la imagen

```bash
# Navegar al directorio del proyecto
cd /ruta/al/proyecto/ntg-js-analyzer

# Crear directorios necesarios y base de datos persistente
mkdir -p data logs
touch analysis.db && chmod 666 analysis.db

# Construir la imagen
podman build -t ntg-js-analyzer:latest .
```

#### Paso 2: Crear red de Podman

```bash
# Crear red personalizada (opcional pero recomendado)
podman network create ntg-analyzer-network
```

#### Paso 3: Ejecutar el contenedor

```bash
# Ejecutar el contenedor con todas las configuraciones necesarias
podman run -d \
  --name ntg-js-analyzer \
  -p 5000:5000 \
  -v "$(pwd)/data:/app/data:Z" \
  -v "$(pwd)/logs:/app/logs:Z" \
  -v "$(pwd)/analysis.db:/app/analysis.db:Z" \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  -e FLASK_SECRET_KEY="tu_clave_secreta_muy_segura_aqui" \
  -e TZ=America/Santiago \
  --network ntg-analyzer-network \
  ntg-js-analyzer:latest
```

**Nota**: La base de datos SQLite `analysis.db` se monta como volumen para mantener persistencia entre reinicios del contenedor.

**Explicación de parámetros:**
- `-d`: Ejecuta en modo detached (segundo plano)
- `--name`: Asigna nombre al contenedor
- `-p 5000:5000`: Mapea puerto 5000 del host al contenedor
- `-v`: Monta volúmenes con etiqueta `:Z` para SELinux
- `-e`: Variables de entorno
- `--network`: Conecta a red personalizada

## Gestión del Contenedor

### Verificar estado

```bash
# Listar contenedores en ejecución
podman ps

# Ver todos los contenedores (incluidos detenidos)
podman ps -a

# Ver logs del contenedor
podman logs ntg-js-analyzer

# Ver logs en tiempo real
podman logs -f ntg-js-analyzer
```

**✅ Ejemplo de contenedor funcionando correctamente:**
```
CONTAINER ID  IMAGE                                          COMMAND               CREATED        STATUS            PORTS                   NAMES
e17dcd4a6400  localhost/ntg-js-analyzer_ntg-analyzer:latest  python dashboard....  3 minutes ago  Up 3 minutes ago  0.0.0.0:5000->5000/tcp  ntg-js-analyzer
```

**Indicadores de funcionamiento correcto:**
- STATUS: `Up X minutes ago`
- PORTS: `0.0.0.0:5000->5000/tcp` (puerto mapeado correctamente)
- La aplicación responde en `http://localhost:5000`

### Operaciones básicas

```bash
# Con podman-compose (recomendado)
podman-compose -f podman-compose.yml down      # Detener
podman-compose -f podman-compose.yml up -d     # Iniciar
podman-compose -f podman-compose.yml restart   # Reiniciar

# Comandos directos de podman
podman stop ntg-js-analyzer         # Detener el contenedor
podman start ntg-js-analyzer        # Iniciar el contenedor detenido
podman restart ntg-js-analyzer      # Reiniciar el contenedor
podman rm ntg-js-analyzer           # Eliminar el contenedor
podman rmi ntg-js-analyzer:latest   # Eliminar la imagen
```

### Acceso al contenedor

```bash
# Ejecutar comando dentro del contenedor
podman exec -it ntg-js-analyzer bash

# Ver procesos en el contenedor
podman top ntg-js-analyzer

# Inspeccionar configuración del contenedor
podman inspect ntg-js-analyzer
```

## Configuraciones Avanzadas

### Configuración de SELinux

Si tienes SELinux habilitado, asegúrate de usar la etiqueta `:Z` en los volúmenes:

```bash
# Verificar estado de SELinux
getenforce

# Si está habilitado, usar :Z en volúmenes
-v "$(pwd)/data:/app/data:Z"
```

### Configuración de memoria y CPU

```bash
# Limitar recursos del contenedor
podman run -d \
  --name ntg-js-analyzer \
  --memory=1g \
  --cpus=1.0 \
  # ... resto de parámetros
```

### Persistencia de Datos

La aplicación mantiene persistencia de datos a través de volúmenes montados:

```bash
# Archivos persistentes en el host:
./data/          # Archivos de datos y exports
./logs/          # Logs de la aplicación
./analysis.db    # Base de datos SQLite (IMPORTANTE)

# Verificar persistencia
ls -la analysis.db data/ logs/
```

### Backup de datos

```bash
# Backup de la base de datos (RECOMENDADO)
cp analysis.db backup_analysis_$(date +%Y%m%d_%H%M%S).db

# Backup desde contenedor ejecutándose
podman exec ntg-js-analyzer cp /app/analysis.db /app/data/backup_$(date +%Y%m%d_%H%M%S).db

# Backup completo del directorio data
tar -czf backup_completo_$(date +%Y%m%d_%H%M%S).tar.gz data/ logs/ analysis.db

# Restaurar backup
cp backup_analysis_YYYYMMDD_HHMMSS.db analysis.db
```

### Variables de entorno disponibles

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `FLASK_ENV` | Entorno de Flask | `production` |
| `FLASK_DEBUG` | Modo debug | `0` |
| `FLASK_SECRET_KEY` | Clave secreta (REQUERIDA) | - |
| `TZ` | Zona horaria | `America/Santiago` |

## Solución de Problemas

### Error de contenedor duplicado

```bash
# Error: "container name is already in use"
# Solución: Eliminar contenedor existente
podman stop ntg-js-analyzer && podman rm ntg-js-analyzer

# Luego ejecutar nuevamente el comando de creación
```

### Error de base de datos

```bash
# Error: "unable to open database file"
# Solución: Crear directorios y archivo base
mkdir -p data logs
touch analysis.db && chmod 666 analysis.db

# Reconstruir imagen sin cache
podman-compose -f podman-compose.yml build --no-cache
```

### Warning de CNI/Network

```bash
# Warning: "Error validating CNI config file"
# Este warning es normal en Podman y no afecta el funcionamiento
# No requiere acción, es informativo únicamente

# Ejemplo real del warning (NORMAL):
WARN[0000] Error validating CNI config file /home/user/.config/cni/net.d/ntg-js-analyzer_ntg-analyzer-network.conflist: [plugin firewall does not support config version "1.0.0"]
```

**Nota**: Este warning aparece en cada comando de Podman pero NO impide que la aplicación funcione correctamente.

### Error de permisos

```bash
# Si hay problemas de permisos, ejecutar:
sudo chown -R $(id -u):$(id -g) data logs
chmod -R 755 data logs
```

### Error de puerto ocupado

```bash
# Verificar qué proceso usa el puerto 5000
sudo netstat -tlnp | grep :5000

# Usar puerto diferente
podman run -p 5001:5000 # ... resto de parámetros
```

### Limpiar recursos de Podman

```bash
# Eliminar contenedores detenidos
podman container prune

# Eliminar imágenes no utilizadas
podman image prune

# Eliminar volúmenes no utilizados
podman volume prune

# Limpieza completa del sistema
podman system prune -a
```

## Acceso a la Aplicación

Una vez iniciado el contenedor, la aplicación estará disponible en:

```
http://localhost:5000
```

### Credenciales por defecto

La aplicación crea automáticamente un usuario administrador al iniciar por primera vez:

- **Usuario**: `admin`
- **Contraseña**: Se genera automáticamente y se muestra en los logs

Para ver las credenciales generadas:
```bash
# Ver logs del contenedor para encontrar las credenciales
podman-compose -f podman-compose.yml logs | grep -A5 "IMPORTANT"

# O usar comando directo
podman logs ntg-js-analyzer | grep -A5 "IMPORTANT"
```

**⚠️ Importante**: Guarda las credenciales de forma segura y elimina el archivo `admin_credentials.txt` después de copiar la contraseña.

## Monitoreo y Logs

### Ver logs en tiempo real

```bash
# Con podman-compose
podman-compose -f podman-compose.yml logs -f

# Comando directo de podman
podman logs -f ntg-js-analyzer

# Logs con timestamp
podman logs -f -t ntg-js-analyzer

# Últimas 100 líneas
podman logs --tail 100 ntg-js-analyzer

# Buscar información específica
podman logs ntg-js-analyzer | grep "IMPORTANT"  # Ver credenciales
podman logs ntg-js-analyzer | grep "ERROR"      # Ver errores
```

### Métricas del contenedor

```bash
# Uso de recursos en tiempo real
podman stats ntg-js-analyzer

# Información detallada del contenedor
podman inspect ntg-js-analyzer | jq '.[]'
```

## Automatización

### Systemd service (opcional)

Para ejecutar como servicio del sistema:

```bash
# Generar archivo de servicio
podman generate systemd --new --name ntg-js-analyzer

# Habilitar y iniciar servicio
systemctl --user enable container-ntg-js-analyzer.service
systemctl --user start container-ntg-js-analyzer.service
```

## Consideraciones de Seguridad

1. **Cambiar la clave secreta**: Siempre configura `FLASK_SECRET_KEY` con un valor único y seguro
2. **Actualizar regularmente**: Mantén Podman y las imágenes actualizadas
3. **Firewall**: Configura adecuadamente el firewall para el puerto 5000
4. **Backup**: Realiza backups regulares de la base de datos y configuraciones

## Diferencias con Docker

- Podman no requiere daemon corriendo como root
- Los contenedores corren con permisos de usuario
- La sintaxis es prácticamente idéntica a Docker
- Mejor integración con systemd
- Soporte nativo para pods (grupos de contenedores)


----


● 🔐 Credenciales de acceso:

Usuario: adminContraseña: RiohnTRhU5iZp0PdSlzlkA

📝 Formas de obtener las credenciales:

Método 1: Archivo de credenciales (actual)

cat admin_credentials.txt

Método 2: Logs del contenedor (cuando se crean nuevas)

podman logs ntg-js-analyzer | grep -A5 "IMPORTANT"

Método 3: Si quieres resetear las credenciales

# Eliminar base de datos existente
rm analysis.db

# Reiniciar contenedor (generará nuevas credenciales)
podman-compose -f podman-compose.yml down
podman-compose -f podman-compose.yml up -d

# Ver nuevas credenciales
podman logs ntg-js-analyzer | grep -A5 "IMPORTANT"

🌐 Acceso a la aplicación:

1. URL: http://localhost:5000
2. Usuario: admin
3. Contraseña: RiohnTRhU5iZp0PdSlzlkA

💡 Consejo: Una vez que hayas guardado las credenciales de forma segura, puedes eliminar el
archivo temporal:
rm admin_credentials.txt
