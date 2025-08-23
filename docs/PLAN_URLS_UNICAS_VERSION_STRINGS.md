# Plan de Implementación: URLs Únicas en Cadenas de Versión

## Problema Identificado

En la pestaña "Cadenas de Versión" de la vista de detalles de escaneo (`/scan/<id>`), aparecen URLs duplicadas cuando el mismo archivo JavaScript contiene múltiples líneas con palabras clave de versión (como `version`, `ver`, etc.). Esto genera ruido visual y dificulta la comprensión de los resultados.

## Análisis del Problema

### Estado Actual
```sql
-- Consulta actual en dashboard.py línea 1230-1235
SELECT id, file_url, file_type, line_number, line_content, version_keyword
FROM version_strings
WHERE scan_id = ? AND file_type = 'js'
ORDER BY file_url, line_number
```

### Ejemplo del Problema
Un archivo `jquery.min.js` puede tener:
- Línea 1: `/*! jQuery v3.6.0 | (c) OpenJS Foundation */`
- Línea 25: `version: "3.6.0"`
- Línea 140: `jQuery.fn.jquery = "3.6.0"`

**Resultado actual**: 3 filas con la misma URL `jquery.min.js` aparecen en la tabla.

**Resultado deseado**: 1 fila agrupada que muestre todas las líneas de versión encontradas en ese archivo.

## Solución Propuesta

### Opción 1: Agrupación por URL (Recomendada)
Agrupar las cadenas de versión por `file_url` y mostrar:
- Una fila por archivo único
- Múltiples líneas de versión agrupadas dentro de la misma fila
- Contador de líneas encontradas

### Opción 2: Vista Expandible
- Mostrar una fila colapsada por archivo
- Click para expandir y ver todas las líneas individuales

## Plan de Implementación

### Fase 1: Modificación de Consulta en dashboard.py
**Archivo**: `dashboard.py` (líneas 1230-1235)
**Duración**: 20 minutos

#### Opción 1A: Agrupación Completa con Concatenación
```sql
SELECT 
    MIN(id) as id,
    file_url,
    file_type,
    GROUP_CONCAT(line_number ORDER BY line_number) as line_numbers,
    GROUP_CONCAT(line_content ORDER BY line_number SEPARATOR '\n---\n') as line_contents,
    GROUP_CONCAT(DISTINCT version_keyword ORDER BY version_keyword) as version_keywords,
    COUNT(*) as lines_count
FROM version_strings
WHERE scan_id = ? AND file_type = 'js'
GROUP BY file_url, file_type
ORDER BY file_url
```

#### Opción 1B: Procesamiento en Python (Más flexible)
```python
# Mantener consulta actual pero procesar en Python
version_strings_raw = conn.execute('''
    SELECT id, file_url, file_type, line_number, line_content, version_keyword
    FROM version_strings
    WHERE scan_id = ? AND file_type = 'js'
    ORDER BY file_url, line_number
''', (scan_id,)).fetchall()

# Agrupar en Python
version_strings_grouped = {}
for vs in version_strings_raw:
    file_url = vs['file_url']
    if file_url not in version_strings_grouped:
        version_strings_grouped[file_url] = {
            'id': vs['id'],
            'file_url': file_url,
            'file_type': vs['file_type'],
            'lines': [],
            'version_keywords': set(),
            'lines_count': 0
        }
    
    version_strings_grouped[file_url]['lines'].append({
        'line_number': vs['line_number'],
        'line_content': vs['line_content'],
        'version_keyword': vs['version_keyword']
    })
    version_strings_grouped[file_url]['version_keywords'].add(vs['version_keyword'])
    version_strings_grouped[file_url]['lines_count'] += 1

version_strings = list(version_strings_grouped.values())
```

### Fase 2: Actualización del Template
**Archivo**: `templates/scan_detail.html` (líneas 858-890)
**Duración**: 30 minutos

#### Cambios Requeridos:

```html
<!-- ANTES (líneas 858-890) -->
{% for vs in version_strings %}
<tr>
    <td>
        <input type="checkbox" ... value="{{ vs.id }}" ... />
    </td>
    <td>
        <a href="{{ vs.file_url|e }}" target="_blank">
            {{ vs.file_url|e | truncate_left(40) }}
        </a>
    </td>
    <td>{{ vs.line_number }}</td>
    <td>{{ vs.line_content|e | truncate(80) }}</td>
    <td>
        <button ... data-vs-id="{{ vs.id }}">
            <i class="bi bi-trash"></i>
        </button>
    </td>
</tr>
{% endfor %}

<!-- DESPUÉS -->
{% for vs in version_strings %}
<tr>
    <td>
        <input type="checkbox" ... value="{{ vs.id }}" ... />
    </td>
    <td>
        <a href="{{ vs.file_url|e }}" target="_blank">
            {{ vs.file_url|e | truncate_left(40) }}
        </a>
        {% if vs.lines_count > 1 %}
        <span class="badge bg-info ms-2">{{ vs.lines_count }} líneas</span>
        {% endif %}
    </td>
    <td>
        {% if vs.lines|length == 1 %}
            {{ vs.lines[0].line_number }}
        {% else %}
            <div class="version-lines-container">
                <button class="btn btn-link btn-sm p-0" type="button" 
                        data-bs-toggle="collapse" data-bs-target="#lines-{{ vs.id }}">
                    Ver {{ vs.lines|length }} líneas
                    <i class="bi bi-chevron-down"></i>
                </button>
                <div id="lines-{{ vs.id }}" class="collapse mt-2">
                    {% for line in vs.lines %}
                    <div class="small text-muted">Línea {{ line.line_number }}</div>
                    {% endfor %}
                </div>
            </div>
        {% endif %}
    </td>
    <td>
        {% if vs.lines|length == 1 %}
            <code class="small">{{ vs.lines[0].line_content|e | truncate(80) }}</code>
        {% else %}
            <div class="version-content-container">
                <button class="btn btn-link btn-sm p-0" type="button" 
                        data-bs-toggle="collapse" data-bs-target="#content-{{ vs.id }}">
                    Ver contenido <i class="bi bi-chevron-down"></i>
                </button>
                <div id="content-{{ vs.id }}" class="collapse mt-2">
                    {% for line in vs.lines %}
                    <div class="mb-1">
                        <small class="text-muted">L{{ line.line_number }}:</small>
                        <code class="small d-block">{{ line.line_content|e | truncate(100) }}</code>
                    </div>
                    {% endfor %}
                </div>
            </div>
        {% endif %}
    </td>
    <td>
        <button type="button" class="btn btn-outline-danger btn-sm"
                data-bs-toggle="modal" data-bs-target="#deleteIndividualVersionStringModal"
                data-vs-id="{{ vs.id }}" data-vs-file="{{ vs.file_url|e }}"
                data-vs-lines="{{ vs.lines_count }}">
            <i class="bi bi-trash"></i>
        </button>
    </td>
</tr>
{% endfor %}
```

### Fase 3: Actualización de Funcionalidad JavaScript
**Archivo**: `static/js/scan_detail.js` (si existe)
**Duración**: 15 minutos

#### Cambios Necesarios:
1. **Contadores actualizados**: Actualizar lógica de conteo de elementos seleccionados
2. **Modales de confirmación**: Actualizar modales para mostrar "X líneas de versión" en lugar de "1 cadena"
3. **Eliminación en lote**: Ajustar para manejar grupos de líneas

### Fase 4: Actualización de Rutas de API y Exportación
**Duración**: 20 minutos

#### Archivos Afectados:
- `dashboard.py` - Ruta `/api/version-strings` (líneas 1335-1342)
- `dashboard.py` - Función `get_scan_export_data()` (líneas 2405-2411)

#### Cambios:
```python
# API version-strings - mantener compatibilidad
@app.route('/api/version-strings')
@login_required
def api_version_strings():
    conn = get_db_connection()
    # Opción: mantener formato actual para APIs externas
    # O implementar parámetro ?grouped=true para nueva funcionalidad
```

## Opciones de Implementación

### Opción Recomendada: Híbrida
1. **Backend**: Usar Opción 1B (procesamiento en Python) para máxima flexibilidad
2. **Frontend**: Implementar vista colapsable/expandible
3. **Compatibilidad**: Mantener APIs existentes sin cambios

### Beneficios de la Opción Recomendada:
- ✅ **Flexibilidad**: Fácil de ajustar lógica de agrupación
- ✅ **Compatibilidad**: No rompe APIs existentes
- ✅ **UX mejorada**: Reduce ruido visual manteniendo acceso a detalles
- ✅ **Rendimiento**: Menos filas en tabla = mejor rendimiento de renderizado

## Consideraciones Técnicas

### Impacto en Base de Datos
- **Positivo**: Consultas más simples, menos transferencia de datos
- **Neutral**: No requiere cambios de schema

### Impacto en Funcionalidades Existentes
- **Eliminación individual**: Debe eliminar todas las líneas del archivo
- **Eliminación masiva**: Lógica similar
- **Exportaciones**: Pueden mantener formato actual o adaptarse

### Testing
1. **Casos de prueba**:
   - Archivo con 1 línea de versión → comportamiento normal
   - Archivo con múltiples líneas → agrupación correcta
   - Eliminación de grupos → todas las líneas se eliminan
2. **Pruebas de regresión**:
   - Exportaciones PDF/CSV/Excel
   - APIs públicas
   - Operaciones masivas

## Cronograma de Implementación

| Fase | Tarea | Duración | Dependencias |
|------|--------|----------|--------------|
| 1 | Modificar consulta en dashboard.py | 20 min | - |
| 2 | Actualizar template scan_detail.html | 30 min | Fase 1 |
| 3 | Actualizar JavaScript (si necesario) | 15 min | Fase 2 |
| 4 | Ajustar APIs y exportaciones | 20 min | Fase 1-3 |
| 5 | Testing y validación | 25 min | Todas |
| **Total** | **110 min** | **~2 horas** | - |

## Criterios de Éxito

### Funcionales
- [ ] Un archivo aparece una sola vez en la tabla de Cadenas de Versión
- [ ] Se muestran todas las líneas encontradas para cada archivo
- [ ] La eliminación funciona correctamente (individual y masiva)
- [ ] Las exportaciones incluyen toda la información

### No Funcionales
- [ ] Tiempo de carga similar o mejorado
- [ ] Interfaz más limpia y menos confusa
- [ ] Compatibilidad hacia atrás mantenida

## Post-Implementación

### Posibles Mejoras Futuras
1. **Filtrado por palabra clave**: Permitir filtrar por `version_keyword`
2. **Resaltado de patrones**: Highlight de términos de versión en el contenido
3. **Estadísticas mejoradas**: Mostrar "X archivos con Y líneas de versión"
4. **Búsqueda**: Búsqueda dentro del contenido de las líneas

### Monitoreo
- Verificar que la funcionalidad no afecte el rendimiento
- Validar que usuarios encuentren la nueva interfaz más intuitiva
- Confirmar que las exportaciones mantengan la información completa