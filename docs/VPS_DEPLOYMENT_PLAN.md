# 🚀 Plan de Implementación VPS Hostinger - Analizador.do-ob.cl

## 📋 Resumen Ejecutivo

**Objetivo**: Desplegar la aplicación JS Analyzer en Hostinger VPS utilizando contenedores Podman bajo el subdominio `analizador.do-ob.cl`.

**Repositorio GitHub**: https://github.com/Gabo-araya/js-analizer

**Tecnologías**:
- **Contenedores**: Podman + Podman Compose
- **Proxy Reverso**: Nginx existente de Hostinger
- **SSL**: Configurado por Hostinger
- **Dominio**: analizador.do-ob.cl
- **Base de Datos**: SQLite simple (solo analysis.db)

---

## 🎯 Objetivos del Despliegue

### Funcionalidades Requeridas
- ✅ **Acceso público via HTTPS**: https://analizador.do-ob.cl
- ✅ **Persistencia de datos**: Solo analysis.db
- ✅ **Configuración simple**: Mínima complejidad
- ✅ **Integración con Hostinger**: Usar infraestructura existente

### Beneficios Esperados
- **Accesibilidad**: Disponible 24/7 desde cualquier ubicación
- **Simplicidad**: Configuración mínima y mantenible
- **Confiabilidad**: Aprovecha infraestructura de Hostinger

---

## 🏗️ Arquitectura de Despliegue

### Diagrama de Arquitectura
```
Internet → Hostinger Nginx → Podman Container → Flask App
                ↓
         [analizador.do-ob.cl:443]
                ↓
         [localhost:5000] → analysis.db
```

### Componentes del Sistema
1. **Hostinger VPS** (configurado)
2. **Nginx**: Proxy reverso existente de Hostinger
3. **Podman**: Gestión de contenedores simple
4. **SSL**: Manejado por Hostinger
5. **analysis.db**: Base de datos SQLite única

---

## 📦 Modificaciones Requeridas

### 1. Dockerfile Simple

**Archivo**: `/Dockerfile`

```dockerfile
FROM python:3.11-alpine3.19

WORKDIR /app

# Dependencias mínimas del sistema
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    rm -rf /var/cache/apk/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de aplicación
COPY . .

# Crear base de datos
RUN touch analysis.db && chmod 666 analysis.db

# Variables de entorno
ENV FLASK_ENV=production \
    FLASK_DEBUG=0 \
    PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "dashboard.py"]
```

### 2. Podman Compose Simple

**Archivo**: `/podman-compose.yml`

```yaml
version: '3.8'

services:
  js-analyzer:
    build: .
    container_name: js-analyzer
    ports:
      - "127.0.0.1:5000:5000"
    volumes:
      - ./analysis.db:/app/analysis.db:Z
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY:-default_key_change_this}
      - TZ=America/Santiago
    restart: unless-stopped
```

### 3. Configuración de Nginx (para añadir al Nginx de Hostinger)

**Añadir a la configuración existente de Hostinger:**

```nginx
# Agregar location para el analizador
location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```


---

## 🔄 Procedimiento de Despliegue Simple

### Paso 1: Instalación de Podman

```bash
# En Hostinger VPS (Ubuntu)
sudo apt update
sudo apt install -y podman git
```

### Paso 2: Clonar y Configurar

```bash
# 1. Clonar repositorio
git clone https://github.com/Gabo-araya/js-analizer.git
cd js-analizer

# 2. Generar clave secreta
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
echo "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" > .env

# 3. Crear base de datos
touch analysis.db
chmod 666 analysis.db
```

### Paso 3: Construir y Ejecutar

```bash
# Construir imagen
podman build -t js-analyzer .

# Ejecutar contenedor
podman run -d \
  --name js-analyzer \
  -p 127.0.0.1:5000:5000 \
  -v $(pwd)/analysis.db:/app/analysis.db:Z \
  --env-file .env \
  --restart unless-stopped \
  js-analyzer

# O usar podman-compose (recomendado)
podman-compose up -d
```

### Paso 4: Configurar Proxy Nginx

```bash
# Añadir al archivo de configuración de nginx de Hostinger
# para el dominio analizador.do-ob.cl la configuración de proxy
# mostrada en la sección anterior
```

---

## 📊 Comandos Básicos de Mantenimiento

```bash
# Ver estado del contenedor
podman ps

# Ver logs de la aplicación
podman logs js-analyzer

# Reiniciar el contenedor
podman restart js-analyzer

# Actualizar desde GitHub
git pull origin main
podman-compose up --build -d

# Backup manual de la base de datos
cp analysis.db analysis_backup_$(date +%Y%m%d).db
```

---

## ✅ Checklist Simple de Implementación

### Pre-requisitos
- [ ] Hostinger VPS funcionando
- [ ] Dominio `analizador.do-ob.cl` configurado en DNS
- [ ] Acceso SSH al VPS

### Implementación
- [ ] Podman instalado en el VPS
- [ ] Repositorio clonado desde GitHub
- [ ] Clave secreta FLASK_SECRET_KEY generada
- [ ] Base de datos analysis.db creada
- [ ] Contenedor construido y ejecutándose

### Configuración Final
- [ ] Nginx proxy configurado para el puerto 5000
- [ ] SSL configurado por Hostinger
- [ ] Aplicación accesible via https://analizador.do-ob.cl
- [ ] Credenciales administrativas cambiadas

---

## 🎯 Resultado Final

**URL de Acceso**: https://analizador.do-ob.cl  
**Repositorio**: https://github.com/Gabo-araya/js-analizer  
**Base de Datos**: Solo analysis.db (SQLite)  
**Mantenimiento**: Manual según necesidad  

**⏱️ Tiempo estimado**: 1-2 horas de implementación