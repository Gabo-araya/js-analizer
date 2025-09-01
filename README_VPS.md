# 🚀 Despliegue VPS Hostinger - JS Analyzer

## Guía Rápida para `analizador.do-ob.cl`

### 📋 Pre-requisitos
- Hostinger VPS con Ubuntu
- Dominio `analizador.do-ob.cl` configurado
- Acceso SSH al VPS

---

## 🔧 Instalación (15 minutos)

### 1. Conectar al VPS y Preparar
```bash
# Conectar via SSH
ssh root@tu_vps_ip

ssh do-ob-server

# Actualizar sistema e instalar Podman
sudo apt update
sudo apt install -y podman git
```

### 2. Clonar y Configurar Proyecto
```bash
# Clonar repositorio
git clone https://github.com/Gabo-araya/js-analizer.git
cd js-analizer

# Generar clave secreta segura
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Crear archivo de configuración
echo "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" > .env
echo "FLASK_ENV=production" >> .env
echo "FLASK_DEBUG=0" >> .env
echo "TZ=America/Santiago" >> .env

# Crear base de datos
touch analysis.db
chmod 666 analysis.db
```

### 3. Construir y Ejecutar
```bash
# Opción A: Con Podman Compose (Recomendado)
podman-compose up -d

# Opción B: Manual
podman build -t js-analyzer .
podman run -d \
  --name js-analyzer \
  -p 127.0.0.1:5000:5000 \
  -v $(pwd)/analysis.db:/app/analysis.db:Z \
  --env-file .env \
  --restart unless-stopped \
  js-analyzer
```

### 4. Configurar Nginx de Hostinger
```bash
# Añadir al archivo de configuración de Nginx de Hostinger
# para el dominio analizador.do-ob.cl:

location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## ✅ Verificación

```bash
# 1. Verificar contenedor ejecutándose
podman ps

# 2. Verificar aplicación local
curl http://localhost:5000

# 3. Verificar acceso web
curl https://analizador.do-ob.cl
```

**¡Listo! 🎉** Tu aplicación debería estar funcionando en: **https://analizador.do-ob.cl**

---

## 🔄 Comandos de Mantenimiento

```bash
# Ver estado
podman ps

# Ver logs
podman logs js-analyzer

# Reiniciar
podman restart js-analyzer

# Actualizar desde GitHub
git pull origin main
podman-compose up --build -d

# Backup de base de datos
cp analysis.db backup_$(date +%Y%m%d).db
```

---

## 📂 Estructura de Archivos

```
js-analizer/
├── analysis.db          ← Base de datos persistente (TUS DATOS)
├── .env                 ← Configuración (NO subir a Git)
├── Dockerfile           ← Imagen simplificada
├── podman-compose.yml   ← Configuración de contenedor
└── README_VPS.md        ← Esta guía
```

---

## 🆘 Troubleshooting

### Problema: No funciona el puerto 5000
```bash
# Verificar qué usa el puerto
sudo lsof -i :5000

# Cambiar puerto en podman-compose.yml si es necesario
# Cambiar "127.0.0.1:5000:5000" por "127.0.0.1:5001:5000"
```

### Problema: Datos no persisten
```bash
# Verificar que analysis.db existe
ls -la analysis.db

# Verificar volumen del contenedor
podman inspect js-analyzer | grep -A5 "Mounts"
```

### Problema: No carga la web
```bash
# Verificar logs de la aplicación
podman logs js-analyzer

# Verificar configuración de Nginx en Hostinger
# Asegurarse que el proxy_pass apunte a 127.0.0.1:5000
```


### Solucionar el conflicto de puertos:

```bash
# 1. Verificar qué está usando el puerto 5000:

podman ps

# 2. Detener y remover el contenedor anterior del analizador:

podman stop js-analyzer
podman rm js-analyzer

# 3. Ejecutar el nuevo contenedor en puerto 5050:

podman run -d \
  --name js-analyzer \
  -p 127.0.0.1:5050:5000 \
  -v $(pwd)/analysis.db:/app/analysis.db:Z \
  --env-file .env \
  --restart unless-stopped \
  js-analyzer

# 4. Verificar que esté funcionando:

podman ps
curl http://localhost:5050

# 5. Actualizar la configuración de Nginx en Hostinger:

# Necesitarás cambiar el proxy_pass en la configuración de nginx para analizador.do-ob.cl de:
proxy_pass http://127.0.0.1:5000;

# a:
proxy_pass http://127.0.0.1:5050;

```

### Revisar configuración de nginx

En un VPS de Hostinger, puedes revisar la configuración de nginx de estas maneras:

```bash
# 1. Buscar archivos de configuración de nginx:

sudo find /etc/nginx -name "*analizador*" -type f
sudo find /etc/nginx -name "*do-ob*" -type f

# 2. Revisar archivos de configuración comunes:

# Archivo principal de nginx
sudo cat /etc/nginx/nginx.conf

# Sitios disponibles
ls -la /etc/nginx/sites-available/
ls -la /etc/nginx/sites-enabled/

# Buscar configuraciones que mencionen tu dominio
sudo grep -r "analizador.do-ob.cl" /etc/nginx/

# 3. Revisar configuraciones de virtual hosts:

# Ver todos los archivos de configuración de sitios
sudo ls -la /etc/nginx/sites-available/
sudo ls -la /etc/nginx/sites-enabled/

# Ver contenido de archivos específicos (reemplaza "default" por el nombre real)
sudo cat /etc/nginx/sites-available/default
sudo cat /etc/nginx/sites-enabled/default

# 4. Si Hostinger usa un panel específico, revisar:

# Buscar en directorios comunes de paneles de hosting
sudo find /usr/local -name "*nginx*" -type d 2>/dev/null
sudo find /opt -name "*nginx*" -type d 2>/dev/null

# 5. Verificar el estado y configuración actual:

sudo nginx -t
sudo systemctl status nginx

```




---

## 🔒 Notas de Seguridad

- ✅ Solo puerto 127.0.0.1:5000 (no público directo)
- ✅ Nginx de Hostinger maneja SSL
- ✅ FLASK_SECRET_KEY único generado
- ✅ FLASK_DEBUG=0 en producción

**Contacto**: gabo@do-ob.cl
**Repositorio**: https://github.com/Gabo-araya/js-analizer
