# 🐳 Manual Completo de Podman - NTG JS Analyzer (v3.0 Modular)

Este documento proporciona instrucciones detalladas para levantar la aplicación "NTG JS Analyzer" utilizando comandos directos de Podman, con la nueva arquitectura modular.

> **🆕 VERSIÓN 3.0**: Manual actualizado para la nueva arquitectura modular con Flask App Factory y CLI moderno.

## 📋 Prerrequisitos

### Software Requerido
- **Podman 4.0+** instalado y funcionando
- **Git 2.30+** para clonar el repositorio
- **OpenSSL** para generar claves seguras
- Al menos **2GB RAM** y **1GB espacio libre**

### Verificar Instalación de Podman
```bash
podman --version
podman info | grep -A 5 "Version"
```

---

## 🚀 Método 1: Usando Podman Compose (Recomendado)

### 1. Preparación del Entorno
```bash
# Clonar repositorio
git clone https://github.com/gabo-ntg/ntg-js-analyzer.git
cd ntg-js-analyzer

# Generar clave secreta fuerte
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
echo "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" >> .env

# Configurar variables de entorno
cat >> .env << 'EOF'
# === Configuración de Producción ===
FLASK_ENV=production
FLASK_DEBUG=0
TZ=America/Santiago

# === Configuración de Red ===
HOST_PORT=5000

# === Configuración de Historial (BD Separada) ===
ENABLE_ACTION_LOGGING=true
HISTORY_RETENTION_DAYS=365

# === Configuración de Análisis ===
ANALYSIS_TIMEOUT=10
MAX_FILES_PER_SCAN=10
BATCH_DELAY=1.0

# === Configuración de Recursos ===
MEMORY_LIMIT=1GB
CPU_LIMIT=0.5

# === Configuración de Logging ===
LOG_LEVEL=INFO
EOF
```

### 2. Crear Directorios Necesarios
```bash
# Crear estructura de directorios con permisos correctos
mkdir -p {data,logs}
chmod 755 {data,logs}

# Verificar estructura
ls -la data logs
```

### 3. Construcción y Despliegue
```bash
# 🆕 Construir y levantar con la nueva arquitectura modular
podman-compose up --build -d

# Verificar estado del contenedor
podman-compose ps

# Ver logs en tiempo real
podman-compose logs -f ntg-analyzer
```

### 4. Verificar Despliegue
```bash
# Estado del servicio
podman-compose ps

# Salud del contenedor
podman exec ntg-js-analyzer curl -f http://localhost:5000/api/stats

# Acceso desde el host
curl -I http://localhost:5000
```

---

## 🛠️ Método 2: Construcción Manual con Podman

### 1. Construcción de la Imagen
```bash
# 🆕 Construir imagen con nueva estructura modular
podman build -t ntg-js-analyzer:3.0 -f docker/Dockerfile .

# Verificar imagen creada
podman images | grep ntg-js-analyzer

# Inspeccionar detalles de la imagen
podman inspect ntg-js-analyzer:3.0 | grep -A 5 "Config"
```

### 2. Crear Red de Podman
```bash
# Crear red dedicada (si no existe)
podman network create ntg-analyzer-network --driver bridge || true

# Verificar red creada
podman network ls | grep ntg-analyzer
```

### 3. Preparar Directorios de Datos
```bash
# Crear directorios con permisos apropiados
mkdir -p {data,logs,backups}
chmod 755 {data,logs,backups}

# Configurar SELinux labels si es necesario (RHEL/Fedora)
if command -v selinuxenabled &> /dev/null && selinuxenabled; then
    chcon -R -t container_file_t {data,logs}
fi
```

### 4. Ejecutar Contenedor Manual
```bash
# 🆕 Ejecutar con nueva configuración modular y CLI
podman run -d \
  --name ntg-js-analyzer \
  -p 5000:5000 \
  -v "$(pwd)/data:/app/data:Z" \
  -v "$(pwd)/logs:/app/logs:Z" \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  -e FLASK_SECRET_KEY="$FLASK_SECRET_KEY" \
  -e TZ=America/Santiago \
  -e DATABASE_PATH=/app/data/analysis.db \
  -e HISTORY_DATABASE_PATH=/app/data/history.db \
  -e ENABLE_ACTION_LOGGING=true \
  -e LOG_LEVEL=INFO \
  -e ANALYSIS_TIMEOUT=10 \
  -e MAX_FILES_PER_SCAN=10 \
  -e BATCH_DELAY=1.0 \
  -e HISTORY_RETENTION_DAYS=365 \
  --network ntg-analyzer-network \
  --restart unless-stopped \
  --health-cmd="curl -f http://localhost:5000/api/stats || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  --health-start-period=40s \
  ntg-js-analyzer:3.0
```

### Explicación de Parámetros Clave
| Parámetro | Descripción |
|-----------|-------------|
| `-d` | Ejecutar en segundo plano (detached) |
| `-p 5000:5000` | Mapear puerto host:contenedor |
| `-v data:/app/data:Z` | Montar volumen con label SELinux |
| `-e FLASK_SECRET_KEY` | **CRÍTICO**: Clave secreta fuerte |
| `--network` | Red aislada para el contenedor |
| `--restart unless-stopped` | Reinicio automático |
| `--health-*` | Monitoreo de salud del contenedor |

---

## 🔍 Monitoreo y Verificación

### 1. Estado del Contenedor
```bash
# Estado general
podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}"

# Uso de recursos
podman stats ntg-js-analyzer --no-stream

# Información detallada
podman inspect ntg-js-analyzer | jq '.[] | {State, Config, Mounts}'
```

### 2. Revisión de Logs
```bash
# Logs de la aplicación (últimas 50 líneas)
podman logs --tail 50 ntg-js-analyzer

# Seguimiento en tiempo real
podman logs -f ntg-js-analyzer

# Logs con timestamp
podman logs -t ntg-js-analyzer

# Logs filtrados por fecha
podman logs --since "2025-01-01" ntg-js-analyzer
```

### 3. Pruebas de Conectividad
```bash
# Test de salud interno
podman exec ntg-js-analyzer curl -f http://localhost:5000/api/stats

# Test desde el host
curl -v http://localhost:5000

# Test de endpoints críticos
curl -s http://localhost:5000/login | grep -i "login"
curl -s http://localhost:5000/api/stats | jq '.'
```

---

## 📊 Gestión de Datos y Backup

### 1. Estructura de Datos
```bash
# Verificar estructura de datos
podman exec ntg-js-analyzer find /app/data -type f -name "*.db" -ls
podman exec ntg-js-analyzer ls -la /app/data/

# Tamaño de bases de datos
podman exec ntg-js-analyzer du -h /app/data/*.db
```

### 2. Backup de Bases de Datos
```bash
# Crear backup con timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
podman exec ntg-js-analyzer cp /app/data/analysis.db /app/data/analysis_backup_$TIMESTAMP.db
podman exec ntg-js-analyzer cp /app/data/history.db /app/data/history_backup_$TIMESTAMP.db

# Copiar backups al host
podman cp ntg-js-analyzer:/app/data/analysis_backup_$TIMESTAMP.db ./backups/
podman cp ntg-js-analyzer:/app/data/history_backup_$TIMESTAMP.db ./backups/

# Script de backup automatizado
cat > backup-databases.sh << 'EOF'
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

echo "Creando backup de bases de datos..."
podman exec ntg-js-analyzer cp /app/data/analysis.db /app/data/analysis_backup_$TIMESTAMP.db
podman exec ntg-js-analyzer cp /app/data/history.db /app/data/history_backup_$TIMESTAMP.db

podman cp ntg-js-analyzer:/app/data/analysis_backup_$TIMESTAMP.db $BACKUP_DIR/
podman cp ntg-js-analyzer:/app/data/history_backup_$TIMESTAMP.db $BACKUP_DIR/

echo "Backup completado: $BACKUP_DIR/"
ls -la $BACKUP_DIR/*$TIMESTAMP*
EOF

chmod +x backup-databases.sh
```

### 3. Restaurar Bases de Datos
```bash
# Detener contenedor
podman stop ntg-js-analyzer

# Restaurar desde backup
cp ./backups/analysis_backup_YYYYMMDD_HHMMSS.db ./data/analysis.db
cp ./backups/history_backup_YYYYMMDD_HHMMSS.db ./data/history.db

# Reiniciar contenedor
podman start ntg-js-analyzer
```

---

## 🔧 Comandos de Gestión

### 1. Ciclo de Vida del Contenedor
```bash
# Iniciar contenedor
podman start ntg-js-analyzer

# Detener contenedor suavemente
podman stop ntg-js-analyzer

# Reiniciar contenedor
podman restart ntg-js-analyzer

# Forzar detención
podman kill ntg-js-analyzer

# Eliminar contenedor (datos persisten en volúmenes)
podman rm ntg-js-analyzer

# Recrear contenedor con nueva configuración
podman stop ntg-js-analyzer && podman rm ntg-js-analyzer
# Ejecutar comando "podman run" nuevamente
```

### 2. Gestión de Recursos
```bash
# Limitar recursos en ejecución
podman update --memory=2GB --cpus=1.0 ntg-js-analyzer

# Reiniciar con nuevos límites
podman stop ntg-js-analyzer
podman start ntg-js-analyzer
```

### 3. Acceso al Contenedor
```bash
# Shell interactivo
podman exec -it ntg-js-analyzer /bin/sh

# Ejecutar comandos específicos
podman exec ntg-js-analyzer python cli.py --help
podman exec ntg-js-analyzer ls -la /app/data/

# Ver procesos internos
podman exec ntg-js-analyzer ps aux
```

---

## 🚨 Troubleshooting

### Problemas Comunes y Soluciones

#### 1. Contenedor no inicia
```bash
# Verificar logs detallados
podman logs ntg-js-analyzer

# Problemas comunes:
# - Puerto ocupado: cambiar HOST_PORT en .env
# - Permisos: ajustar ownership de directorios
# - Memoria: verificar recursos disponibles

# Soluciones:
sudo lsof -i :5000  # Ver qué usa el puerto
sudo chown -R 1000:1000 data logs  # Arreglar permisos
free -h  # Verificar memoria disponible
```

#### 2. Base de datos bloqueada
```bash
# Verificar procesos que usan BD
podman exec ntg-js-analyzer fuser /app/data/analysis.db

# Reiniciar contenedor si es necesario
podman restart ntg-js-analyzer

# En casos extremos, restaurar desde backup
cp ./backups/latest_backup.db ./data/analysis.db
```

#### 3. Problemas de red
```bash
# Verificar configuración de red
podman network inspect ntg-analyzer-network

# Recrear red si es necesario
podman network rm ntg-analyzer-network
podman network create ntg-analyzer-network --driver bridge

# Verificar puertos
podman port ntg-js-analyzer
```

#### 4. Problemas de permisos (SELinux)
```bash
# Verificar contexto SELinux
ls -Z data/ logs/

# Ajustar contexto si es necesario
chcon -R -t container_file_t data/ logs/

# Deshabilitar SELinux temporalmente (no recomendado)
sudo setenforce 0
```

### Comandos de Diagnóstico
```bash
# Información del sistema
podman system info | head -20

# Estado de recursos
podman system df

# Verificar salud del contenedor
podman healthcheck run ntg-js-analyzer

# Generar reporte completo
cat > diagnostic-report.sh << 'EOF'
#!/bin/bash
echo "=== DIAGNÓSTICO NTG JS ANALYZER ===" > diagnostic.log
echo "Fecha: $(date)" >> diagnostic.log
echo -e "\n=== SISTEMA ===" >> diagnostic.log
uname -a >> diagnostic.log
echo -e "\n=== PODMAN ===" >> diagnostic.log
podman --version >> diagnostic.log
echo -e "\n=== CONTENEDOR ===" >> diagnostic.log
podman ps -a | grep ntg >> diagnostic.log
echo -e "\n=== RECURSOS ===" >> diagnostic.log
podman stats --no-stream ntg-js-analyzer >> diagnostic.log
echo -e "\n=== LOGS (últimas 50 líneas) ===" >> diagnostic.log
podman logs --tail 50 ntg-js-analyzer >> diagnostic.log
echo "Reporte generado: diagnostic.log"
EOF

chmod +x diagnostic-report.sh
./diagnostic-report.sh
```

---

## 🔄 Actualizaciones y Mantenimiento

### 1. Actualizar Aplicación
```bash
# Obtener últimos cambios
git pull origin main

# Hacer backup antes de actualizar
./backup-databases.sh

# Reconstruir imagen
podman build --no-cache -t ntg-js-analyzer:3.0 -f docker/Dockerfile .

# Recrear contenedor
podman stop ntg-js-analyzer
podman rm ntg-js-analyzer
# Ejecutar comando "podman run" con nueva imagen
```

### 2. Limpieza de Sistema
```bash
# Limpiar imágenes no utilizadas
podman image prune -a

# Limpiar volúmenes huérfanos
podman volume prune

# Limpiar sistema completo
podman system prune -a --volumes
```

---

## ✅ Checklist de Verificación

### Pre-despliegue
- [ ] Podman instalado y funcionando
- [ ] Clave secreta fuerte generada (`FLASK_SECRET_KEY`)
- [ ] Directorios `data/` y `logs/` creados con permisos 755
- [ ] Variables de entorno configuradas en `.env`
- [ ] Red de Podman creada

### Despliegue
- [ ] Imagen construida exitosamente
- [ ] Contenedor ejecutándose (`podman ps`)
- [ ] Health check funcionando
- [ ] Puerto 5000 accesible
- [ ] Logs sin errores críticos

### Post-despliegue
- [ ] Aplicación accesible en http://localhost:5000
- [ ] Login funcional con credenciales administrativas
- [ ] Bases de datos inicializadas (analysis.db y history.db)
- [ ] Sistema de historial habilitado
- [ ] Backup configurado
- [ ] Monitoreo funcionando

---

## 📞 Soporte y Recursos

### Enlaces Útiles
- **Documentación Principal**: `CLAUDE.md`
- **Guía de Despliegue**: `DEPLOYMENT.md`
- **Issues GitHub**: https://github.com/gabo-ntg/ntg-js-analyzer/issues

### Comandos de Ayuda
```bash
# Ayuda de la aplicación
podman exec ntg-js-analyzer python cli.py --help

# Información de configuración
podman exec ntg-js-analyzer python -c "from config.config import Config; print(vars(Config))"

# Estado de las bases de datos
podman exec ntg-js-analyzer python -c "from app.models.history_manager import history_manager; print(history_manager.get_database_stats())"
```

---

**🎉 ¡Despliegue con Podman Completado!**

Tu aplicación NTG JS Analyzer (v3.0 Modular) está funcionando en: **http://localhost:5000**

Para soporte adicional, revisa los logs: `podman logs ntg-js-analyzer`