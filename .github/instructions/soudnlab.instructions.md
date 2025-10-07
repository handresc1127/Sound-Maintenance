# Sound-Maintenance - Soundlab la Casa del DJ

## 📋 Descripción General
Sound-Maintenance es un sistema completo de gestión para servicios de mantenimiento y reparación de equipos de DJ desarrollado para Soundlab. El sistema maneja inventario de repuestos, registro de clientes y seguimiento completo de servicios de reparación para equipos como consolas DJ, controladores, luces, equipos de sonido, máquinas de humo y todo lo relacionado con el mundo del espectáculo.

## 🎨 Identidad de Marca
- **Colores**: Negro, Morado y Fucsia
- **Enfoque**: Equipos de DJ y espectáculos
- **Servicios**: Mantenimiento, reparación y venta de repuestos

## 🏗️ Stack Tecnológico Principal
- **Backend**: Flask 2.3.3 + SQLAlchemy + Flask-Login
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript + jQuery  
- **Base de Datos**: SQLite (con soporte para PostgreSQL/MySQL)
- **Servidor**: Waitress (recomendado para Windows)
- **Reportes**: ReportLab para PDFs
- **Zona Horaria**: America/Bogota (CO_TZ)

## 📁 Módulos del Sistema
- **Inventario**: Gestión de stock de repuestos y accesorios
- **Clientes**: Registro e ingreso de clientes
- **Servicios**: Mantenimiento y reparación de equipos (módulo principal)
  - Reportes de estado
  - Evidencias fotográficas
  - Seguimiento de reparaciones

## 📁 Estructura de Archivos Clave
- `app.py`: Aplicación principal Flask con todas las rutas
- `models/models.py`: Modelos SQLAlchemy (User, Customer, Equipment, Service, Inventory, etc.)
- `templates/`: Plantillas Jinja2 organizadas por funcionalidad
- `static/`: CSS, JavaScript y archivos estáticos
- `instance/app.db`: Base de datos SQLite
- `requirements.txt`: Dependencias Python

## 🎯 Estándares de Desarrollo

### Principios Generales de Código
- Usar type hints cuando el lenguaje lo permita
- Seguir convenciones estándar del lenguaje (PEP 8 para Python, PSR para PHP, etc.)
- Documentación clara para funciones públicas
- Manejo apropiado de excepciones
- Validar entrada tanto en backend como frontend
- Usar estándares de fecha/hora apropiados para el contexto

### Filosofía de Desarrollo y Debugging
**CRÍTICO - Ciclo de Desarrollo con Limpieza:**
1. **Durante Desarrollo**: Crear logs extensivos, comentarios de debug, prints temporales, tests de validación
2. **Durante Testing**: Mantener todos los elementos de debugging para identificar problemas
3. **Antes de Producción**: ELIMINAR completamente todo código de debugging
   - Remover todos los `print()`, `console.log()` temporales
   - Eliminar comentarios de debug (`# TODO`, `# DEBUG`, `# TEMP`)
   - Limpiar logs no esenciales (solo mantener logs críticos de seguridad/errores)
   - Remover tests temporales y código experimental
   - Eliminar variables no utilizadas y imports innecesarios

**Regla de Oro**: El código productivo debe ser limpio, sin rastros de debugging temporal

**OBLIGATORIO - Marcado de Código Temporal:**
- **SIEMPRE** marcar elementos temporales con comentarios identificables:
  ```python
  # DEBUG: imprimir valores para troubleshooting
  print(f"Debug: usuario = {user}")
  
  # TODO: optimizar esta query
  debug_var = "temporal"  # TEMP: variable de prueba
  
  # FIXME: revisar lógica de validación
  import pdb; pdb.set_trace()  # DEBUG: breakpoint temporal
  ```
  
  ```javascript
  // DEBUG: verificar valores del formulario
  console.log("Debug info:", data);
  
  // TODO: implementar validación real
  // TEMP: función de prueba para testing
  function debugFunction() { alert("Test"); }  // DEBUG
  ```

**Marcadores Estándar para Limpieza:**
- `# DEBUG:` / `// DEBUG:` - Código de debugging temporal
- `# TODO:` / `// TODO:` - Tareas pendientes de implementar
- `# TEMP:` / `// TEMP:` - Código experimental temporal
- `# FIXME:` / `// FIXME:` - Código que necesita corrección
- `# TEST:` / `// TEST:` - Funciones/variables solo para testing

### Desarrollo Frontend
- Implementar diseño responsivo
- Incluir navegación clara (breadcrumbs cuando sea apropiado)
- Usar componentes modales para formularios secundarios
- Implementar notificaciones para feedback al usuario
- Código JavaScript organizado y modular
- Validación del lado cliente complementaria a la del servidor
- Implementar búsquedas y autocompletado cuando sea necesario

## 🔧 Patrones de Arquitectura

### Estructuras de Rutas Estándar
```
# Patrón CRUD estándar para entidades
/entity             # Listar
/entity/new         # Formulario crear  
/entity/create      # Procesar creación
/entity/<id>        # Ver detalle
/entity/<id>/edit   # Formulario editar
/entity/<id>/update # Procesar actualización
/entity/<id>/delete # Eliminar
```

### Modelos de Base de Datos (cuando aplique)
- Implementar patrones de timestamp consistentes (`created_at`, `updated_at`)
- Usar relaciones apropiadas del ORM
- Implementar métodos de serialización para APIs
- Validaciones en el modelo cuando sea apropiado

### Autenticación y Seguridad
- Implementar sistema de roles apropiado
- Usar decoradores de autorización
- Hashear contraseñas correctamente
- Implementar protección CSRF
- Sanitizar archivos subidos y entrada de usuarios

## � Mejores Prácticas

### Base de Datos
- Usar transacciones para operaciones críticas
- Manejar concurrencia apropiadamente
- Implementar backup automático para producción
- Migraciones deben ser backward compatible cuando sea posible

### Rendimiento
- Implementar paginación para listas largas
- Crear índices en campos de búsqueda frecuente
- Optimizar carga de datos relacionados
- Evitar consultas N+1

### Zona Horaria y Timestamps
- **CRÍTICO**: Siempre usar `datetime.now(CO_TZ)` para Colombia
- Mostrar fechas en formato local en templates
- Almacenar UTC en base de datos cuando sea posible
- Zona horaria: America/Bogota (CO_TZ)

## 🎨 Convenciones UI/UX

### Componentes de Interfaz
- Usar framework CSS consistentemente
- Cards/tarjetas para contenido agrupado
- Tablas responsivas para listas
- Modals para formularios rápidos
- Navegación clara y consistente

### Iconografía y Diseño
- Usar librería de iconos consistente
- Mantener consistencia en iconos por acción
- Usar colores semánticos (éxito, advertencia, error)
- Asegurar accesibilidad y contraste

### Formularios
- Validación tanto JavaScript como backend
- Campos requeridos marcados claramente
- Autocompletado donde sea apropiado
- Mensajes de error claros y útiles

## 📋 APIs y Estructura

### APIs y Endpoints
- Seguir convenciones RESTful
- Implementar versionado apropiado  
- Documentar endpoints claramente
- Manejar errores de forma consistente

### Organización de Archivos
- Estructura de carpetas lógica y consistente
- Separación clara de responsabilidades
- Archivos de configuración organizados
- Documentación actualizada

## 🔄 Workflow de Desarrollo

### Testing
- Implementar tests unitarios y de integración
- Testing manual para funcionalidades críticas
- Verificar flujos de usuario completos
- Asegurar cobertura de casos edge

### Debugging y Logs
- Logs estructurados para acciones críticas
- Manejo de errores con try/catch apropiado
- Mensajes de feedback claros para usuarios
- Logs de debugging solo durante desarrollo

### Proceso de Limpieza Pre-Producción
**OBLIGATORIO antes de deploy:**
1. **Revisar y limpiar logs temporales**:
   ```python
   # ELIMINAR antes de producción
   print(f"Debug: usuario = {user}")
   app.logger.debug("Temporal debugging info")
   ```

2. **Eliminar comentarios de debugging**:
   ```python
   # TODO: revisar esta lógica
   # DEBUG: imprimir valores aquí
   # TEMP: código experimental
   # FIXME: corregir validación
   # TEST: función solo para pruebas
   ```

3. **Limpiar imports y variables no usadas**:
   ```python
   import pdb  # DEBUG: breakpoint library
   debug_var = "test"  # TEMP: variable de prueba
   test_data = []  # TEST: datos de prueba
   ```

4. **Remover código comentado**:
   ```python
   # old_function()  # TODO: eliminar función deprecated
   # if debug_mode:   # DEBUG: lógica de debugging
   ```

5. **Limpiar JavaScript temporal**:
   ```javascript
   console.log("Debug info");  // DEBUG: log temporal
   // alert("Test");           // TEST: alerta de prueba
   // TODO: implementar validación real
   debugVar = "test";         // TEMP: variable temporal
   ```

**Comandos de Búsqueda para Limpieza:**
```bash
# Buscar elementos temporales en código
grep -rn "# DEBUG\|# TODO\|# TEMP\|# FIXME\|# TEST" --include="*.py" .
grep -rn "// DEBUG\|// TODO\|// TEMP\|// FIXME\|// TEST" --include="*.js" --include="*.html" .

# Buscar elementos de debugging temporales
grep -rn "print(" --include="*.py" .
grep -rn "console\.log\|console\.debug" --include="*.js" .
```

## 🚀 Deployment y Configuración

### Desarrollo Local
- Configurar entorno de desarrollo apropiado
- Variables de entorno para configuración
- Scripts de inicio automatizados
- Documentación de setup clara

### Producción
- Usar servidores apropiados para el stack tecnológico
- Variables de entorno en archivos de configuración seguros
- Configurar servicios del sistema cuando sea necesario
- Implementar backup automático de datos críticos

## ✅ Checklist de Limpieza Pre-Producción

### OBLIGATORIO - Limpieza de Código de Debugging
**Antes de cada deploy, verificar que se han eliminado:**

**Python/Backend:**
- [ ] Todos los `print()` temporales de debugging (buscar `# DEBUG:`)
- [ ] `app.logger.debug()` no esenciales (buscar `# DEBUG:`)
- [ ] Comentarios `# TODO`, `# DEBUG`, `# TEMP`, `# FIXME`, `# TEST`
- [ ] Imports no utilizados (`import pdb`, `from pprint import pprint`) con marcadores
- [ ] Variables de debugging (`debug_var`, `test_data`, etc.) marcadas como `# TEMP:`
- [ ] Código comentado experimental marcado como `# TODO:` o `# FIXME:`
- [ ] Funciones de test temporales marcadas como `# TEST:`

**Frontend/JavaScript:**
- [ ] `console.log()`, `console.debug()`, `console.warn()` marcados como `// DEBUG:`
- [ ] `alert()` de testing marcados como `// TEST:`
- [ ] Comentarios `// TODO`, `// DEBUG`, `// FIXME`, `// TEMP`, `// TEST`
- [ ] Variables JS no utilizadas marcadas como `// TEMP:`
- [ ] Código CSS/HTML comentado con marcadores temporales
- [ ] Funciones de test en JavaScript marcadas como `// TEST:`

**Comandos de Búsqueda para Limpieza:**
```bash
# Buscar elementos temporales Python
grep -rn "# DEBUG\|# TODO\|# TEMP\|# FIXME\|# TEST" --include="*.py" .

# Buscar elementos temporales JavaScript/HTML
grep -rn "// DEBUG\|// TODO\|// TEMP\|// FIXME\|// TEST" --include="*.js" --include="*.html" .

# Buscar prints temporales
grep -rn "print(" --include="*.py" .

# Buscar console.log temporales
grep -rn "console\.log\|console\.debug" --include="*.js" .
```

**Templates/HTML:**
- [ ] Comentarios HTML de debugging
- [ ] Elementos ocultos para testing
- [ ] Código experimental comentado

**Configuración:**
- [ ] Configuraciones de desarrollo en archivos de producción
- [ ] URLs de testing hardcodeadas
- [ ] Claves API de desarrollo

**Logs Permitidos en Producción:**
**SOLO mantener logs de:**
- Errores críticos del sistema
- Acciones de seguridad (intentos de login, denegaciones de permisos)
- Transacciones importantes específicas del negocio
- Métricas de performance críticas

---

**Nota**: Este archivo proporciona estándares técnicos generales que se pueden adaptar a diferentes tipos de proyectos y stacks tecnológicos.