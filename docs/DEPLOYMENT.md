# 🚀 Guía de Despliegue - NTG JS Analyzer

## Instrucciones completas para desplegar desde GitHub usando Podman

> **⚠️ NOTA**: Esta guía ha sido actualizada para reflejar la estructura actual del proyecto

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

### Linux (RHEL/Fedora/CentOS)
```bash
# RHEL 8+/CentOS Stream
sudo dnf install -y podman podman-compose

# Fedora
sudo dnf install -y podman podman-compose

# Verificar instalación
podman --version
```

### macOS
```bash
# Instalar Homebrew si no está disponible
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Podman
brew install podman

# Inicializar máquina virtual
podman machine init
podman machine start

# Verificar instalación
podman --version
```

### Windows
```powershell
# Opción 1: Podman Desktop (Recomendado)
# Descargar desde: https://podman-desktop.io/downloads

# Opción 2: WSL2 + Podman
# Instalar WSL2 primero, luego seguir instrucciones de Linux
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

# === Configuración de base de datos ===
DB_PATH=/app/data/analysis.db

# === Configuración de análisis ===
HTTP_TIMEOUT=30
MAX_FILES_PER_SITE=10
BATCH_DELAY=2.0

# === Configuración de logging ===
LOG_LEVEL=INFO
LOG_MAX_SIZE=10m
LOG_MAX_FILES=3

# === Configuración de seguridad ===
SECURITY_HEADERS=true
CSRF_PROTECTION=true
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

#### 1. Construir y ejecutar con compose (Modernizado)
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

#### 1. Construir imagen (Modernizada)
```bash
# Construir imagen
podman build -t ntg-js-analyzer:latest -f Dockerfile .

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