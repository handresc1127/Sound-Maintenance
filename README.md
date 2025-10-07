# Sound-Maintenance - Soundlab la Casa del DJ

Sistema completo de gestión para servicios de mantenimiento y reparación de equipos de DJ desarrollado para **Soundlab**. El sistema maneja inventario de repuestos, registro de clientes y seguimiento completo de servicios de reparación para equipos como consolas DJ, controladores, luces, equipos de sonido, máquinas de humo y todo lo relacionado con el mundo del espectáculo.

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

## 📦 Módulos del Sistema

### 🔧 **Módulo de Servicios** (Principal)
- Registro de órdenes de trabajo
- Seguimiento de estado de reparaciones
- Diagnósticos y trabajos realizados
- Evidencias fotográficas (antes/durante/después)
- Control de costos estimados y finales
- Gestión de partes utilizadas

### 👥 **Módulo de Clientes**
- Registro completo de clientes
- Historial de servicios por cliente
- Información de contacto y notas
- Gestión de equipos por cliente

### 📦 **Módulo de Inventario**
- Control de stock de repuestos y accesorios
- Alertas de stock mínimo
- Categorización por tipo de producto
- Movimientos de entrada/salida
- Integración con servicios

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- PowerShell (Windows)

### Instalación Rápida

1. **Clonar el repositorio**
```bash
git clone https://github.com/handresc1127/Sound-Maintenance.git
cd Sound-Maintenance
```

2. **Ejecutar script de inicialización**
```powershell
# Desarrollo
.\run.ps1

# Producción con Waitress
.\run.ps1 -UseWaitress

# Inicializar base de datos
.\run.ps1 -InitDB
```

3. **Acceder al sistema**
- URL: http://127.0.0.1:5000
- Usuario: `admin`
- Contraseña: `admin123`

### Instalación Manual

1. **Crear entorno virtual**
```bash
python -m venv venv
```

2. **Activar entorno virtual**
```powershell
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Inicializar base de datos**
```python
python -c "from app import app, init_db; app.app_context().push(); init_db()"
```

5. **Ejecutar aplicación**
```bash
# Desarrollo
python app.py

# Producción
waitress-serve --host=127.0.0.1 --port=5000 app:app
```

## 📁 Estructura del Proyecto

```
Sound-Maintenance/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── run.ps1               # Script de inicialización Windows
├── models/
│   └── models.py         # Modelos SQLAlchemy
├── templates/            # Plantillas Jinja2
│   ├── layout.html       # Plantilla base
│   ├── dashboard.html    # Dashboard principal
│   ├── auth/
│   ├── customers/
│   ├── services/
│   └── inventory/
├── static/              # Archivos estáticos
│   ├── css/
│   │   └── soundlab.css # Estilos personalizados
│   └── js/
│       └── soundlab.js  # JavaScript personalizado
└── instance/
    └── soundlab.db      # Base de datos SQLite
```

## 🎯 Características Principales

### 🔐 **Sistema de Autenticación**
- Login seguro con roles (admin/técnico)
- Gestión de sesiones con Flask-Login
- Protección de rutas sensibles

### 📊 **Dashboard Inteligente**
- Estadísticas en tiempo real
- Alertas de stock bajo
- Servicios activos
- Accesos rápidos

### 🛠️ **Gestión de Servicios**
- Estados: Recibido → En Proceso → Completado → Entregado
- Seguimiento de tiempos y costos
- Evidencias fotográficas
- Reportes técnicos

### 📱 **Diseño Responsivo**
- Interfaz adaptada para móviles y tablets
- Tema personalizado con colores de marca
- Iconografía específica para equipos DJ

## 🔧 Tipos de Equipos Soportados

| Categoría | Ejemplos | Icono |
|-----------|----------|-------|
| **Consolas DJ** | Pioneer, Denon, Numark | 🎵 |
| **Controladores** | Traktor, Serato, VirtualDJ | 🎛️ |
| **Iluminación** | LED, Moving Heads, Strobes | 💡 |
| **Sonido** | Monitores, Amplificadores | 🔊 |
| **Efectos** | Máquinas de humo, Láser | ☁️ |
| **Accesorios** | Cables, Conectores, Cases | 🔧 |

## 📈 API Endpoints

### Autenticación
- `POST /login` - Iniciar sesión
- `GET /logout` - Cerrar sesión

### Clientes
- `GET /customers` - Listar clientes
- `POST /customers/create` - Crear cliente
- `GET /customers/<id>` - Ver cliente
- `POST /customers/<id>/update` - Actualizar cliente

### Servicios
- `GET /services` - Listar servicios
- `POST /services/create` - Crear servicio
- `GET /services/<id>` - Ver servicio
- `POST /services/<id>/update` - Actualizar servicio

### Inventario
- `GET /inventory` - Listar inventario
- `POST /inventory/create` - Agregar item
- `POST /inventory/<id>/movement` - Registrar movimiento

## 🛡️ Seguridad

- Contraseñas hasheadas con Werkzeug
- Protección CSRF en formularios
- Validación de entrada en frontend y backend
- Sanitización de archivos subidos
- Sesiones seguras con Flask-Login

## 🔄 Workflow de Servicios

1. **Recepción del Equipo**
   - Registro del cliente y equipo
   - Descripción del problema
   - Fotos del estado inicial

2. **Diagnóstico**
   - Evaluación técnica
   - Estimación de costo
   - Identificación de repuestos

3. **Reparación**
   - Trabajo técnico
   - Documentación del proceso
   - Fotos del progreso

4. **Entrega**
   - Pruebas finales
   - Documentación completa
   - Facturación y entrega

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# .env file
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///instance/soundlab.db
FLASK_ENV=development
```

### Base de Datos
```python
# Migración a PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/soundlab'
```

### Backup Automático
```powershell
# Script de backup
copy instance\soundlab.db "backups\soundlab_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
```

## 📞 Soporte y Contribución

- **Issues**: Reportar bugs en GitHub Issues
- **Features**: Solicitar nuevas características
- **Contribuir**: Fork → Branch → Pull Request

## 📝 Licencia

Este proyecto está desarrollado específicamente para **Soundlab - La Casa del DJ**.

---

**Soundlab** - Especializados en equipos de DJ y espectáculos 🎵