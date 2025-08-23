# 🚀 Guía de Despliegue - NTG JS Analyzer

## Instrucciones completas para desplegar desde GitHub usando Podman

### 📋 Prerrequisitos

#### Sistema Operativo
- **Linux** (Ubuntu 20.04+, RHEL 8+, Fedora 34+)
- **macOS** (con Homebrew)
- **Windows** (con WSL2 o Podman Desktop)

#### Software Requerido
- **Podman 4.0+** o **Podman Desktop**
- **Git 2.30+**
- **Python 3.8+** (para desarrollo local opcional)
- **OpenSSL** (para generar claves seguras)

---

## 🛠️ Instalación de Podman

### Linux (Ubuntu/Debian)
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Podman
sudo apt install -y podman podman-compose

# Verificar instalación
podman --version
podman-compose --version
```


---

## 📥 Clonado del Repositorio

### 1. Clonar desde GitHub
```bash
# Usar HTTPS (recomendado para la mayoría de usuarios)
git clone https://github.com/gabo-ntg/ntg-js-analyzer.git
cd ntg-js-analyzer

# O usar SSH (si tienes llaves configuradas)
git clone git@github.com:gabo-ntg/ntg-js-analyzer.git
cd ntg-js-analyzer
```

### 2. Verificar archivos descargados
```bash
ls -la
# Debe mostrar: Dockerfile, podman-compose.yml, dashboard.py, etc.
```

---

## 🔐 Configuración de Seguridad

### 1. Generar clave secreta segura
```bash
# Generar clave fuerte de 32 bytes
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Mostrar la clave generada (guardar en lugar seguro)
echo "Tu clave secreta: $FLASK_SECRET_KEY"
```

### 2. Crear archivo de entorno (recomendado)
```bash
# Crear archivo .env para variables de entorno
cat > .env << EOF
# === Configuración de Seguridad ===
FLASK_ENV=production
FLASK_DEBUG=0
FLASK_SECRET_KEY=$FLASK_SECRET_KEY

# === Configuración de la aplicación ===
FLASK_PORT=5000
TZ=America/Santiago

# === Configuración de red ===
HOST_PORT=5000

# === Configuración de recursos ===
MEMORY_LIMIT=1GB
CPU_LIMIT=0.5

# === Configuración de logging ===
LOG_LEVEL=INFO
EOF

echo "✅ Archivo .env creado con configuración segura"
```

### 3. Verificar configuración de seguridad
```bash
# El archivo .env debe contener una clave secreta fuerte
grep "FLASK_SECRET_KEY" .env
```

---

## 🐳 Construcción y Despliegue con Podman

### Método 1: Usando Podman Compose (Recomendado)

#### 1. Construir y ejecutar con compose
```bash
# Construir imagen y levantar servicios
podman-compose up --build -d

# Verificar que el contenedor está corriendo
podman-compose ps
```

#### 2. Ver logs de la aplicación
```bash
# Ver logs en tiempo real
podman-compose logs -f ntg-analyzer

# Ver logs específicos
podman logs ntg-js-analyzer
```

#### 3. Comandos de gestión
```bash
# Detener servicio
podman-compose down

# Reiniciar servicio
podman-compose restart

# Ver estado
podman-compose ps

# Eliminar todo (incluyendo volúmenes)
podman-compose down -v
```

### Método 2: Construcción Manual

#### 1. Construir imagen
```bash
# Construir imagen desde Dockerfile
podman build -t ntg-js-analyzer:latest .

# Verificar imagen creada
podman images | grep ntg-js-analyzer
```

#### 2. Crear directorios de datos
```bash
# Crear directorios para persistencia
mkdir -p ./data ./logs
chmod 755 ./data ./logs
```

#### 3. Ejecutar contenedor
```bash
# Ejecutar con todas las configuraciones
podman run -d \
  --name ntg-js-analyzer \
  --env-file .env \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data:Z \
  -v $(pwd)/logs:/app/logs:Z \
  -v $(pwd)/analysis.db:/app/analysis.db:Z \
  --restart unless-stopped \
  ntg-js-analyzer:latest
```

#### 4. Verificar despliegue
```bash
# Verificar que el contenedor está corriendo
podman ps | grep ntg-js-analyzer

# Ver logs
podman logs ntg-js-analyzer

# Verificar conectividad
curl -I http://localhost:5000
```

---

## 🌐 Acceso a la Aplicación

### 1. Abrir en navegador
```bash
# La aplicación estará disponible en:
echo "🌐 Acceder a: http://localhost:5000"

# O en la IP del servidor:
echo "🌐 Acceder a: http://$(hostname -I | awk '{print $1}'):5000"
```

### 2. Credenciales iniciales
```bash
# Las credenciales se generan automáticamente al primer inicio
# Revisar logs para ver las credenciales:
podman logs ntg-js-analyzer | grep -A 3 "IMPORTANT: Save these credentials"
```

⚠️ **IMPORTANTE**: Cambiar las credenciales por defecto inmediatamente después del primer acceso.

---

## 📁 Gestión de Datos Persistentes

### Estructura de directorios
```
proyecto/
├── data/                    # Base de datos y archivos de aplicación
│   └── analysis.db         # Base de datos SQLite principal
├── logs/                    # Logs de la aplicación
│   └── application.log      # Log principal
├── .env                     # Variables de entorno (NO subir a Git)
└── analysis.db             # Archivo de BD local (bind mount)
```

### Backup de datos
```bash
# Crear backup de la base de datos
podman exec ntg-js-analyzer cp /app/analysis.db /app/data/analysis-backup-$(date +%Y%m%d).db

# Copiar backup al host
podman cp ntg-js-analyzer:/app/data/ ./backup/

# O usando el volumen montado
cp ./data/analysis.db ./backup/analysis-backup-$(date +%Y%m%d).db
```

### Restaurar datos
```bash
# Detener contenedor
podman-compose down

# Restaurar base de datos
cp ./backup/analysis-backup-YYYYMMDD.db ./analysis.db

# Reiniciar contenedor
podman-compose up -d
```

---

## 🔧 Configuración Avanzada

### 1. Variables de entorno disponibles
```bash
# Seguridad
FLASK_ENV=production              # production/development
FLASK_DEBUG=0                     # 0/1
FLASK_SECRET_KEY=                 # Clave secreta (32+ caracteres)

# Red
FLASK_HOST=0.0.0.0               # Host binding
FLASK_PORT=5000                   # Puerto interno

# Aplicación
TZ=America/Santiago               # Zona horaria
HTTP_TIMEOUT=30                   # Timeout para requests
MAX_FILES_PER_SITE=10            # Límite de archivos por análisis
BATCH_DELAY=2                     # Delay entre requests batch

# Recursos
MEMORY_LIMIT=1GB                  # Límite de memoria
CPU_LIMIT=0.5                     # Límite de CPU
```

### 2. Configurar proxy reverso (Nginx)
```nginx
# /etc/nginx/sites-available/ntg-analyzer
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Configurar HTTPS (Let's Encrypt)
```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com

# Verificar renovación automática
sudo certbot renew --dry-run
```

---

## 🔍 Monitoreo y Troubleshooting

### 1. Verificar estado del servicio
```bash
# Estado del contenedor
podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Uso de recursos
podman stats ntg-js-analyzer

# Inspeccionar configuración
podman inspect ntg-js-analyzer
```

### 2. Revisar logs
```bash
# Logs de aplicación
podman logs --tail 50 -f ntg-js-analyzer

# Logs del sistema Podman
journalctl -u podman-compose@ntg-analyzer -f

# Logs específicos por fecha
podman logs --since 2024-01-01 ntg-js-analyzer
```

### 3. Problemas comunes y soluciones

#### Puerto ocupado
```bash
# Verificar qué está usando el puerto
sudo lsof -i :5000

# Cambiar puerto en podman-compose.yml
sed -i 's/5000:5000/5001:5000/' podman-compose.yml
podman-compose up -d
```

#### Problemas de permisos
```bash
# Ajustar permisos de volúmenes
sudo chown -R 1000:1000 ./data ./logs
sudo chmod 755 ./data ./logs
```

#### Contenedor no inicia
```bash
# Ver logs detallados del error
podman logs ntg-js-analyzer

# Inspeccionar configuración
podman inspect ntg-js-analyzer | grep -A 10 "Config"

# Verificar imagen
podman images | grep ntg-js-analyzer
```

#### Base de datos corrupta
```bash
# Backup de la BD actual
cp analysis.db analysis.db.backup

# Eliminar BD corrupta y reiniciar
rm analysis.db
podman-compose restart
```

---

## 🔄 Actualizaciones

### 1. Actualizar desde GitHub
```bash
# Detener servicios
podman-compose down

# Obtener últimos cambios
git pull origin main

# Reconstruir y reiniciar
podman-compose up --build -d
```

### 2. Actualizar solo la imagen
```bash
# Reconstruir imagen sin cache
podman build --no-cache -t ntg-js-analyzer:latest .

# Recrear contenedor
podman-compose up -d --force-recreate
```

---

## 📊 Configuración de Producción

### 1. Optimizaciones de rendimiento
```bash
# En .env, ajustar límites de recursos
MEMORY_LIMIT=2GB
CPU_LIMIT=1.0
MAX_FILES_PER_SITE=20
BATCH_DELAY=1
```

### 2. Configuración de seguridad adicional
```bash
# Configurar firewall
sudo ufw allow 5000/tcp
sudo ufw enable

# Configurar fail2ban (opcional)
sudo apt install fail2ban
```

### 3. Backup automatizado
```bash
# Crear script de backup
cat > backup-ntg.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
podman exec ntg-js-analyzer cp /app/analysis.db /app/data/analysis-backup-$DATE.db
cp ./data/analysis-backup-$DATE.db $BACKUP_DIR/
echo "Backup created: $BACKUP_DIR/analysis-backup-$DATE.db"
EOF

chmod +x backup-ntg.sh

# Configurar cron para backup diario
echo "0 2 * * * $(pwd)/backup-ntg.sh" | crontab -
```

---

## 🆘 Soporte y Ayuda

### 1. Recursos útiles
- **Documentación técnica**: `CLAUDE.md`
- **README principal**: `README.md`
- **Issues GitHub**: https://github.com/gabo-ntg/ntg-js-analyzer/issues

### 2. Comandos de diagnóstico
```bash
# Información del sistema
podman info | head -20

# Versión de Podman
podman --version

# Verificar conectividad
curl -v http://localhost:5000/api/stats
```

### 3. Logs para reportar problemas
```bash
# Generar reporte completo
echo "=== SISTEMA ===" > debug-report.txt
uname -a >> debug-report.txt
echo -e "\n=== PODMAN ===" >> debug-report.txt
podman --version >> debug-report.txt
echo -e "\n=== CONTENEDOR ===" >> debug-report.txt
podman ps >> debug-report.txt
echo -e "\n=== LOGS ===" >> debug-report.txt
podman logs --tail 100 ntg-js-analyzer >> debug-report.txt

echo "Reporte generado en: debug-report.txt"
```

---

## 🏢 Despliegue en VPS Ubuntu Server con Podman

Esta sección contiene instrucciones específicas para desplegar el proyecto en un servidor VPS Ubuntu usando contenedores Podman con persistencia de base de datos y respaldo automático.

### 📋 Prerrequisitos VPS Ubuntu Server

#### Especificaciones mínimas del servidor
- **RAM**: 2GB mínimo, 4GB recomendado
- **CPU**: 1 vCPU mínimo, 2 vCPU recomendado
- **Almacenamiento**: 20GB mínimo, 50GB recomendado
- **SO**: Ubuntu Server 20.04 LTS o superior
- **Red**: Conexión estable a internet

#### Acceso al servidor
```bash
# Conectar al VPS via SSH
ssh usuario@ip-del-servidor

# O usando llave privada
ssh -i ~/.ssh/mi-llave.pem usuario@ip-del-servidor
```

### 🛠️ Preparación del Servidor Ubuntu

#### 1. Actualización inicial del sistema
```bash
# Actualizar repositorios y paquetes
sudo apt update && sudo apt upgrade -y

# Instalar paquetes básicos
sudo apt install -y \
    curl \
    wget \
    git \
    htop \
    nano \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release
```

#### 2. Configurar firewall UFW
```bash
# Habilitar firewall
sudo ufw enable

# Permitir SSH (importante antes de habilitar UFW)
sudo ufw allow ssh
sudo ufw allow 22/tcp

# Permitir puerto de la aplicación
sudo ufw allow 5000/tcp

# Permitir HTTP/HTTPS si usas proxy reverso
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Verificar reglas
sudo ufw status verbose
```

#### 3. Crear usuario para la aplicación
```bash
# Crear usuario dedicado para la aplicación
sudo adduser ntgapp
sudo usermod -aG sudo ntgapp

# Cambiar a usuario ntgapp
sudo su - ntgapp
cd ~
```

### 📦 Instalación de Podman en Ubuntu Server

#### 1. Instalar Podman desde repositorios oficiales
```bash
# Agregar repositorio de Podman
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/unstable/xUbuntu_$(lsb_release -rs)/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:unstable.list

# Agregar llave GPG
curl -fsSL https://download.opensuse.org/repositories/devel:kubic:libcontainers:unstable/xUbuntu_$(lsb_release -rs)/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/kubic-libcontainers-unstable.gpg > /dev/null

# Actualizar repositorios
sudo apt update

# Instalar Podman y compose
sudo apt install -y podman podman-compose

# Verificar instalación
podman --version
podman-compose --version
```

#### 2. Configurar Podman para usuario sin root
```bash
# Configurar registries sin root
echo 'unqualified-search-registries = ["registry.fedoraproject.org", "registry.access.redhat.com", "docker.io", "quay.io"]' | sudo tee /etc/containers/registries.conf

# Crear directorios de configuración
mkdir -p ~/.config/containers

# Habilitar servicios de usuario
systemctl --user enable podman.socket
systemctl --user start podman.socket

# Verificar socket
systemctl --user status podman.socket
```

### 🔧 Despliegue de la Aplicación

#### 1. Clonar repositorio del proyecto
```bash
# Navegar al directorio home del usuario
cd ~

# Clonar proyecto desde GitHub
git clone https://github.com/usuario/ntg-js-analyzer.git
cd ntg-js-analyzer

# Verificar contenido
ls -la
```

#### 2. Configurar estructura de directorios persistentes
```bash
# Crear directorios para datos persistentes
mkdir -p ~/ntg-js-analyzer/data
mkdir -p ~/ntg-js-analyzer/logs
mkdir -p ~/ntg-js-analyzer/backups

# Configurar permisos apropiados
chmod 755 ~/ntg-js-analyzer/data
chmod 755 ~/ntg-js-analyzer/logs
chmod 755 ~/ntg-js-analyzer/backups

# Crear archivo de base de datos SQLite si no existe
touch ~/ntg-js-analyzer/analysis.db
chmod 644 ~/ntg-js-analyzer/analysis.db
```

#### 3. Configurar variables de entorno de producción
```bash
# Generar clave secreta fuerte
FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Crear archivo de configuración del servidor
cat > ~/ntg-js-analyzer/.env << EOF
# === Configuración de Seguridad ===
FLASK_ENV=production
FLASK_DEBUG=0
FLASK_SECRET_KEY=$FLASK_SECRET_KEY

# === Configuración del servidor ===
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
TZ=America/Santiago

# === Configuración de red ===
HOST_PORT=5000

# === Configuración de recursos del servidor ===
MEMORY_LIMIT=1.5GB
CPU_LIMIT=1.0

# === Configuración de logging ===
LOG_LEVEL=INFO

# === Configuración de aplicación ===
HTTP_TIMEOUT=30
MAX_FILES_PER_SITE=15
BATCH_DELAY=1

# === Configuración de base de datos ===
DB_PATH=/app/analysis.db
DB_BACKUP_RETENTION_DAYS=30
EOF

echo "✅ Archivo .env creado para servidor VPS"
echo "🔑 Clave secreta: $FLASK_SECRET_KEY"
echo "⚠️ IMPORTANTE: Guarda la clave secreta en un lugar seguro"
```

#### 4. Configurar Podman Compose para servidor
```bash
# Crear archivo podman-compose.yml optimizado para servidor
cat > ~/ntg-js-analyzer/podman-compose.yml << 'EOF'
version: '3.8'

services:
  ntg-analyzer:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ntg-js-analyzer-server
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    env_file:
      - .env
    volumes:
      # Persistencia de base de datos principal
      - ./analysis.db:/app/analysis.db:Z
      # Directorio de datos adicionales
      - ./data:/app/data:Z
      # Logs de aplicación
      - ./logs:/app/logs:Z
      # Templates personalizados (si existen)
      - ./templates:/app/templates:Z
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/stats"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID
    read_only: false
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m
EOF
```

#### 5. Construir y desplegar contenedor
```bash
# Cambiar al directorio del proyecto
cd ~/ntg-js-analyzer

# Construir imagen optimizada para servidor
podman-compose build --no-cache

# Verificar imagen construida
podman images | grep ntg-js-analyzer

# Levantar servicios en modo daemon
podman-compose up -d

# Verificar estado del contenedor
podman-compose ps
podman-compose logs -f ntg-analyzer
```

#### 6. Verificar despliegue exitoso
```bash
# Verificar que el contenedor está corriendo
podman ps | grep ntg-js-analyzer

# Probar conectividad local
curl -I http://localhost:5000

# Verificar desde IP externa (desde otra máquina)
curl -I http://IP-DEL-SERVIDOR:5000

# Revisar logs para credenciales iniciales
podman logs ntg-js-analyzer-server | grep -A 5 "IMPORTANT: Save these credentials"
```

### 🗄️ Configuración de Persistencia de Base de Datos SQLite

#### 1. Estructura de persistencia
```bash
# La base de datos SQLite se monta como volumen persistente
# Ubicación en host: ~/ntg-js-analyzer/analysis.db
# Ubicación en contenedor: /app/analysis.db

# Verificar montaje de volumen
podman inspect ntg-js-analyzer-server | grep -A 10 '"Mounts"'

# Verificar que la base de datos persiste
ls -la ~/ntg-js-analyzer/analysis.db
```

#### 2. Configurar respaldos automáticos de base de datos
```bash
# Crear script de respaldo automatizado
cat > ~/ntg-js-analyzer/backup-database.sh << 'EOF'
#!/bin/bash

# Configuración
BACKUP_DIR="$HOME/ntg-js-analyzer/backups"
DB_FILE="$HOME/ntg-js-analyzer/analysis.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="analysis_backup_${TIMESTAMP}.db"
RETENTION_DAYS=30

# Crear directorio de backup si no existe
mkdir -p "$BACKUP_DIR"

# Verificar que la base de datos existe
if [ ! -f "$DB_FILE" ]; then
    echo "❌ Error: Base de datos no encontrada en $DB_FILE"
    exit 1
fi

# Crear backup usando SQLite
echo "📊 Creando backup de base de datos..."
if command -v sqlite3 >/dev/null 2>&1; then
    # Usar sqlite3 para backup consistente
    sqlite3 "$DB_FILE" ".backup '$BACKUP_DIR/$BACKUP_FILE'"
else
    # Fallback: copia simple
    cp "$DB_FILE" "$BACKUP_DIR/$BACKUP_FILE"
fi

# Verificar que el backup se creó
if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    echo "✅ Backup creado exitosamente: $BACKUP_FILE (${BACKUP_SIZE})"
else
    echo "❌ Error: No se pudo crear el backup"
    exit 1
fi

# Limpiar backups antiguos
echo "🧹 Limpiando backups antiguos (>${RETENTION_DAYS} días)..."
find "$BACKUP_DIR" -name "analysis_backup_*.db" -type f -mtime +${RETENTION_DAYS} -delete

# Mostrar estadísticas de backups
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/analysis_backup_*.db 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
echo "📈 Total de backups: $BACKUP_COUNT archivos (${TOTAL_SIZE})"

# Log del backup
echo "$(date '+%Y-%m-%d %H:%M:%S') - Backup creado: $BACKUP_FILE" >> "$BACKUP_DIR/backup.log"
EOF

# Hacer ejecutable el script
chmod +x ~/ntg-js-analyzer/backup-database.sh

# Probar el script
~/ntg-js-analyzer/backup-database.sh
```

#### 3. Configurar cron para respaldos automáticos
```bash
# Instalar sqlite3 para backups consistentes
sudo apt install -y sqlite3

# Agregar tarea cron para backup diario a las 2:00 AM
(crontab -l 2>/dev/null; echo "0 2 * * * $HOME/ntg-js-analyzer/backup-database.sh >> $HOME/ntg-js-analyzer/backups/cron.log 2>&1") | crontab -

# Agregar tarea cron para backup semanal adicional (domingos a las 3:00 AM)
(crontab -l 2>/dev/null; echo "0 3 * * 0 cp $HOME/ntg-js-analyzer/analysis.db $HOME/ntg-js-analyzer/backups/weekly_backup_\$(date +\%Y\%m\%d).db") | crontab -

# Verificar tareas cron configuradas
crontab -l

echo "✅ Backups automáticos configurados:"
echo "   - Diario: 2:00 AM"
echo "   - Semanal: Domingos 3:00 AM"
```

### 🔄 Configurar Respaldos en GitHub desde el Servidor

#### 1. Configurar Git y SSH para respaldos automáticos
```bash
# Configurar Git globalmente
git config --global user.name "NTG Server"
git config --global user.email "servidor@tu-dominio.com"

# Generar llave SSH para GitHub
ssh-keygen -t ed25519 -C "ntg-server-backup" -f ~/.ssh/github_backup_key

# Mostrar llave pública para agregar a GitHub
echo "🔑 Agrega esta llave pública a tu cuenta de GitHub:"
echo "https://github.com/settings/ssh/new"
echo ""
cat ~/.ssh/github_backup_key.pub
echo ""
echo "⏳ Presiona Enter después de agregar la llave a GitHub..."
read -p ""

# Configurar SSH para usar la llave específica
cat >> ~/.ssh/config << EOF

# Configuración para respaldos GitHub NTG
Host github-backup
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_backup_key
    IdentitiesOnly yes
EOF

# Configurar permisos SSH
chmod 600 ~/.ssh/github_backup_key
chmod 600 ~/.ssh/config

# Probar conexión SSH
ssh -T github-backup
```

#### 2. Crear script de respaldo a GitHub
```bash
# Crear script para respaldar base de datos a GitHub
cat > ~/ntg-js-analyzer/backup-to-github.sh << 'EOF'
#!/bin/bash

# Configuración
PROJECT_DIR="$HOME/ntg-js-analyzer"
BACKUP_DIR="$PROJECT_DIR/backups"
DB_FILE="$PROJECT_DIR/analysis.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_BRANCH="database-backups"

cd "$PROJECT_DIR"

echo "🔄 Iniciando respaldo a GitHub..."

# Verificar que estamos en un repo Git
if [ ! -d ".git" ]; then
    echo "❌ Error: No es un repositorio Git"
    exit 1
fi

# Crear backup de la base de datos
echo "📊 Creando backup de base de datos..."
cp "$DB_FILE" "$BACKUP_DIR/analysis_github_backup_${TIMESTAMP}.db"

# Verificar si existe la rama de backup
git fetch origin
if git show-ref --quiet refs/remotes/origin/$BACKUP_BRANCH; then
    echo "📥 Cambiando a rama de backup existente..."
    git checkout $BACKUP_BRANCH
    git pull origin $BACKUP_BRANCH
else
    echo "🌟 Creando nueva rama de backup..."
    git checkout -b $BACKUP_BRANCH
fi

# Agregar archivos de backup al Git
git add backups/analysis_github_backup_${TIMESTAMP}.db
git add backups/backup.log

# Crear commit con información del backup
git commit -m "Database backup ${TIMESTAMP}

- Backup automático desde servidor VPS
- Fecha: $(date '+%Y-%m-%d %H:%M:%S')
- Tamaño BD: $(du -h $DB_FILE | cut -f1)
- Servidor: $(hostname)
- IP: $(curl -s ifconfig.me 2>/dev/null || echo 'N/A')
"

# Subir cambios a GitHub
echo "⬆️ Subiendo backup a GitHub..."
if git push github-backup $BACKUP_BRANCH; then
    echo "✅ Backup subido exitosamente a GitHub"

    # Log del backup
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Backup GitHub: analysis_github_backup_${TIMESTAMP}.db" >> "$BACKUP_DIR/github_backup.log"
else
    echo "❌ Error al subir backup a GitHub"
    exit 1
fi

# Volver a rama principal
git checkout main

# Limpiar backups GitHub antiguos (mantener solo los últimos 10)
echo "🧹 Limpiando backups antiguos en directorio local..."
cd "$BACKUP_DIR"
ls -t analysis_github_backup_*.db | tail -n +11 | xargs -r rm

echo "✅ Respaldo a GitHub completado"
EOF

# Hacer ejecutable el script
chmod +x ~/ntg-js-analyzer/backup-to-github.sh

# Probar el script (opcional)
echo "🧪 ¿Quieres probar el script de backup a GitHub ahora? (y/n)"
read -p "Respuesta: " test_backup
if [ "$test_backup" = "y" ]; then
    ~/ntg-js-analyzer/backup-to-github.sh
fi
```

#### 3. Configurar respaldos automáticos a GitHub
```bash
# Agregar tarea cron para backup semanal a GitHub (sábados a las 4:00 AM)
(crontab -l 2>/dev/null; echo "0 4 * * 6 $HOME/ntg-js-analyzer/backup-to-github.sh >> $HOME/ntg-js-analyzer/backups/github_cron.log 2>&1") | crontab -

# Verificar configuración de cron actualizada
crontab -l

echo "✅ Respaldo automático a GitHub configurado:"
echo "   - Frecuencia: Sábados a las 4:00 AM"
echo "   - Rama: database-backups"
echo "   - Logs: ~/ntg-js-analyzer/backups/github_cron.log"
```

### 📊 Comandos de Mantenimiento y Actualización

#### 1. Actualizar aplicación desde GitHub
```bash
# Crear script de actualización
cat > ~/ntg-js-analyzer/update-from-github.sh << 'EOF'
#!/bin/bash

PROJECT_DIR="$HOME/ntg-js-analyzer"
cd "$PROJECT_DIR"

echo "🔄 Actualizando aplicación desde GitHub..."

# Crear backup de la configuración actual
echo "📦 Creando backup de configuración..."
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Detener servicios
echo "⏹️ Deteniendo servicios..."
podman-compose down

# Obtener últimos cambios
echo "📥 Descargando actualizaciones..."
git stash push -m "Auto-stash before update $(date)"
git fetch origin
git pull origin main

# Reconstruir imagen
echo "🔧 Reconstruyendo imagen..."
podman-compose build --no-cache

# Reiniciar servicios
echo "▶️ Reiniciando servicios..."
podman-compose up -d

# Verificar estado
echo "🔍 Verificando estado..."
sleep 10
podman-compose ps

# Probar conectividad
if curl -f http://localhost:5000/api/stats >/dev/null 2>&1; then
    echo "✅ Actualización completada exitosamente"
    echo "🌐 Aplicación disponible en: http://$(hostname -I | awk '{print $1}'):5000"
else
    echo "⚠️ Advertencia: La aplicación puede no estar respondiendo correctamente"
    echo "📋 Revisa los logs: podman-compose logs ntg-analyzer"
fi

# Log de actualización
echo "$(date '+%Y-%m-%d %H:%M:%S') - Actualización desde GitHub completada" >> "$PROJECT_DIR/backups/update.log"
EOF

chmod +x ~/ntg-js-analyzer/update-from-github.sh
```

#### 2. Script de monitoreo y diagnóstico
```bash
# Crear script de estado del sistema
cat > ~/ntg-js-analyzer/status-check.sh << 'EOF'
#!/bin/bash

PROJECT_DIR="$HOME/ntg-js-analyzer"
cd "$PROJECT_DIR"

echo "🔍 === ESTADO DEL SISTEMA NTG JS ANALYZER ==="
echo "📅 Fecha: $(date)"
echo "🖥️ Servidor: $(hostname)"
echo "📍 IP Externa: $(curl -s ifconfig.me 2>/dev/null || echo 'N/A')"
echo ""

echo "🐳 === ESTADO DE CONTENEDORES ==="
podman-compose ps
echo ""

echo "📊 === RECURSOS DEL SISTEMA ==="
echo "💾 Uso de memoria:"
free -h
echo ""
echo "💽 Uso de disco:"
df -h | grep -E "(Filesystem|/dev/)"
echo ""
echo "⚡ Carga del sistema:"
uptime
echo ""

echo "🗄️ === ESTADO DE BASE DE DATOS ==="
if [ -f "$PROJECT_DIR/analysis.db" ]; then
    DB_SIZE=$(du -h "$PROJECT_DIR/analysis.db" | cut -f1)
    echo "✅ Base de datos: $DB_SIZE"

    # Verificar integridad de la BD
    if command -v sqlite3 >/dev/null 2>&1; then
        if sqlite3 "$PROJECT_DIR/analysis.db" "PRAGMA integrity_check;" | grep -q "ok"; then
            echo "✅ Integridad de BD: OK"
        else
            echo "⚠️ Integridad de BD: PROBLEMAS DETECTADOS"
        fi
    fi
else
    echo "❌ Base de datos no encontrada"
fi
echo ""

echo "💾 === BACKUPS RECIENTES ==="
if [ -d "$PROJECT_DIR/backups" ]; then
    echo "📦 Backups locales (últimos 5):"
    ls -lt "$PROJECT_DIR/backups"/analysis_backup_*.db | head -5 | awk '{print $9, $6, $7, $8}'
    echo ""
    BACKUP_COUNT=$(ls -1 "$PROJECT_DIR/backups"/analysis_backup_*.db 2>/dev/null | wc -l)
    BACKUP_SIZE=$(du -sh "$PROJECT_DIR/backups" 2>/dev/null | cut -f1)
    echo "📈 Total backups: $BACKUP_COUNT archivos ($BACKUP_SIZE)"
else
    echo "❌ Directorio de backups no encontrado"
fi
echo ""

echo "🌐 === CONECTIVIDAD ==="
if curl -f http://localhost:5000/api/stats >/dev/null 2>&1; then
    echo "✅ Aplicación web: FUNCIONANDO"
else
    echo "❌ Aplicación web: NO RESPONDE"
fi

# Verificar puertos
if ss -tlnp | grep -q ":5000"; then
    echo "✅ Puerto 5000: ABIERTO"
else
    echo "❌ Puerto 5000: CERRADO"
fi
echo ""

echo "📋 === LOGS RECIENTES (últimas 10 líneas) ==="
podman logs --tail 10 ntg-js-analyzer-server 2>/dev/null || echo "No se pudieron obtener logs"
echo ""

echo "🔚 === FIN DEL REPORTE ==="
EOF

chmod +x ~/ntg-js-analyzer/status-check.sh

# Probar script de estado
~/ntg-js-analyzer/status-check.sh
```

#### 3. Configurar monitoreo con cron
```bash
# Configurar chequeo de estado cada hora
(crontab -l 2>/dev/null; echo "0 * * * * $HOME/ntg-js-analyzer/status-check.sh >> $HOME/ntg-js-analyzer/backups/status.log 2>&1") | crontab -

# Configurar reinicio automático si la aplicación no responde
cat > ~/ntg-js-analyzer/auto-restart.sh << 'EOF'
#!/bin/bash

PROJECT_DIR="$HOME/ntg-js-analyzer"
cd "$PROJECT_DIR"

# Verificar si la aplicación responde
if ! curl -f http://localhost:5000/api/stats >/dev/null 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Aplicación no responde, reiniciando..." >> "$PROJECT_DIR/backups/auto-restart.log"

    # Reiniciar servicios
    podman-compose restart

    # Esperar y verificar
    sleep 30
    if curl -f http://localhost:5000/api/stats >/dev/null 2>&1; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Reinicio exitoso" >> "$PROJECT_DIR/backups/auto-restart.log"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Reinicio falló, requiere intervención manual" >> "$PROJECT_DIR/backups/auto-restart.log"
    fi
fi
EOF

chmod +x ~/ntg-js-analyzer/auto-restart.sh

# Configurar verificación cada 15 minutos
(crontab -l 2>/dev/null; echo "*/15 * * * * $HOME/ntg-js-analyzer/auto-restart.sh") | crontab -

# Mostrar configuración final de cron
echo "✅ Configuración de cron completada:"
crontab -l
```

### 🔒 Configuración de Seguridad Adicional para VPS

#### 1. Configurar fail2ban para protección contra ataques
```bash
# Instalar fail2ban
sudo apt install -y fail2ban

# Configurar regla personalizada para la aplicación
sudo cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3

[ntg-analyzer]
enabled = true
port = 5000
filter = ntg-analyzer
logpath = /home/ntgapp/ntg-js-analyzer/logs/*.log
maxretry = 10
bantime = 7200
EOF

# Crear filtro para la aplicación
sudo cat > /etc/fail2ban/filter.d/ntg-analyzer.conf << 'EOF'
[Definition]
failregex = .*Failed login attempt from <HOST>.*
            .*Invalid access from <HOST>.*
            .*Blocked request from <HOST>.*
ignoreregex =
EOF

# Reiniciar fail2ban
sudo systemctl restart fail2ban
sudo systemctl enable fail2ban

# Verificar estado
sudo fail2ban-client status
```

#### 2. Configurar certificados SSL con Let's Encrypt (opcional)
```bash
# Instalar certbot
sudo apt install -y certbot

# Si tienes un dominio configurado
read -p "¿Tienes un dominio configurado para este servidor? (y/n): " has_domain

if [ "$has_domain" = "y" ]; then
    read -p "Ingresa tu dominio (ej: analyzer.tu-dominio.com): " domain_name

    # Obtener certificado SSL
    sudo certbot certonly --standalone -d $domain_name

    echo "✅ Certificado SSL obtenido para $domain_name"
    echo "📁 Certificados en: /etc/letsencrypt/live/$domain_name/"

    # Configurar renovación automática
    (sudo crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | sudo crontab -
fi
```

### 📈 Resumen de la Configuración VPS

#### Estructura final del proyecto
```
~/ntg-js-analyzer/
├── analysis.db                 # Base de datos SQLite principal
├── .env                       # Variables de entorno
├── podman-compose.yml         # Configuración de contenedor
├── data/                      # Datos adicionales de la aplicación
├── logs/                      # Logs de la aplicación
├── backups/                   # Backups automáticos
│   ├── analysis_backup_*.db   # Backups locales diarios
│   ├── weekly_backup_*.db     # Backups semanales
│   ├── analysis_github_backup_*.db # Backups para GitHub
│   ├── backup.log            # Log de backups locales
│   ├── github_backup.log     # Log de backups GitHub
│   ├── status.log            # Log de monitoreo
│   └── auto-restart.log      # Log de reinicios automáticos
├── backup-database.sh         # Script backup local
├── backup-to-github.sh       # Script backup GitHub
├── update-from-github.sh     # Script de actualización
├── status-check.sh           # Script de monitoreo
└── auto-restart.sh           # Script de reinicio automático
```

#### Tareas programadas (cron)
```bash
# Ver todas las tareas configuradas
crontab -l

# Tareas típicas configuradas:
# 0 2 * * * - Backup diario de BD
# 0 3 * * 0 - Backup semanal adicional
# 0 4 * * 6 - Backup a GitHub
# 0 * * * * - Monitoreo de estado
# */15 * * * * - Verificación y reinicio automático
```

#### Comandos útiles para administración
```bash
# Estado general del sistema
~/ntg-js-analyzer/status-check.sh

# Actualizar desde GitHub
~/ntg-js-analyzer/update-from-github.sh

# Backup manual
~/ntg-js-analyzer/backup-database.sh

# Ver logs de la aplicación
podman-compose logs -f ntg-analyzer

# Reiniciar servicios
cd ~/ntg-js-analyzer && podman-compose restart

# Verificar backups
ls -la ~/ntg-js-analyzer/backups/

# Verificar cron jobs
crontab -l
```

---

## ✅ Checklist de Despliegue

### Pre-despliegue
- [ ] Podman instalado y funcionando
- [ ] Repositorio clonado desde GitHub
- [ ] Clave secreta fuerte generada
- [ ] Archivo .env configurado
- [ ] Directorios de datos creados

### Despliegue
- [ ] Imagen construida exitosamente
- [ ] Contenedor ejecutándose
- [ ] Puerto 5000 accesible
- [ ] Logs sin errores críticos
- [ ] Base de datos inicializada

### Post-despliegue
- [ ] Aplicación accesible via web
- [ ] Credenciales administrativas cambiadas
- [ ] Backup configurado
- [ ] Monitoreo funcionando
- [ ] Proxy reverso configurado (si aplica)

---

**🎉 ¡Despliegue Completo!**

Tu aplicación NTG JS Analyzer debería estar funcionando en: **http://localhost:5000**

Para cualquier problema, revisa los logs con: `podman logs ntg-js-analyzer`
