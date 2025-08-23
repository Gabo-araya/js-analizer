# 🚀 Inicio Rápido - NTG JS Analyzer

Guía simple para ejecutar el proyecto desde la consola en menos de 5 minutos.

## ⚡ Método Rápido (Recomendado)

### 1. Preparar entorno
```bash
# Clonar repositorio (si no lo tienes)
git clone https://github.com/gabo-ntg/ntg-js-analyzer.git
cd ntg-js-analyzer

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar seguridad
```bash
# Generar clave secreta
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Habilitar historial (opcional pero recomendado)
source logging_config.sh
```

### 3. Ejecutar aplicación
```bash
# 🆕 Usar CLI moderno
python cli.py run --port 5000

# O método tradicional
python dashboard.py
```

### 4. Acceder
Abrir navegador en: **http://localhost:5000**

---

## 🐳 Con Contenedores (Más Simple)

### Usando Podman/Docker Compose
```bash
# Configurar variables
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
echo "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" > .env

# Ejecutar (elige uno)
podman-compose up --build -d  # Podman
docker-compose up --build -d  # Docker

# Acceder en: http://localhost:5000
```

---

## 🔧 Comandos Útiles

### Desarrollo
```bash
# Modo desarrollo con debug
python cli.py run --port 5000 --debug

# Ver ayuda del CLI
python cli.py --help

# Análisis por línea de comandos
python cli.py analyze --urls-file urls.txt
```

### Gestión de datos
```bash
# Resetear base de datos
rm analysis.db  # Se recrea automáticamente

# Migrar historial (solo si tienes datos existentes)
python cli.py migrate-history
# O alternativamente: python scripts/migrate_history.py

# Ver estadísticas del sistema
python cli.py stats
```

---

## 🚨 Solución de Problemas

| Problema | Solución |
|----------|----------|
| Error de dependencias | `pip install -r requirements.txt` |
| Puerto ocupado | Cambiar puerto: `python cli.py run --port 5001` |
| Base de datos bloqueada | Eliminar `analysis.db`, se recrea automáticamente |
| Error de permisos | `chmod 755 data/ logs/` |

---

## 📝 Primeros Pasos

1. **Login**: Usuario `admin`, contraseña se genera automáticamente (revisar consola)
2. **Analizar URL**: Ir a "Nuevo Análisis" y ingresar una URL
3. **Ver Resultados**: Los análisis aparecen en el dashboard principal
4. **Exportar**: Usar botones PDF/Excel/CSV para reportes

---

## ⚙️ Variables de Entorno (Opcional)

```bash
# Configuración básica
export FLASK_ENV=production        # production/development
export FLASK_DEBUG=0              # 0/1
export LOG_LEVEL=INFO             # DEBUG/INFO/WARNING/ERROR

# Análisis
export MAX_FILES_PER_SCAN=10      # Límite de archivos por sitio
export BATCH_DELAY=1.0            # Delay entre requests (segundos)
export ANALYSIS_TIMEOUT=10        # Timeout por request (segundos)
```

---

**✅ ¡Listo!** El proyecto está funcionando en http://localhost:5000
