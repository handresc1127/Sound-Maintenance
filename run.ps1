# Soundlab - La Casa del DJ
# Script de inicialización para Windows
# Ejecutar: .\run.ps1 -UseWaitress

param(
    [switch]$UseWaitress = $false,
    [switch]$InitDB = $false,
    [string]$Host = "127.0.0.1",
    [int]$Port = 5000
)

Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  Soundlab - La Casa del DJ" -ForegroundColor Magenta
Write-Host "  Sound-Maintenance System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Magenta

# Verificar si Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python no encontrado. Por favor instalar Python 3.8+" -ForegroundColor Red
    exit 1
}

# Verificar si existe el entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Error al crear entorno virtual" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✓ Entorno virtual activado" -ForegroundColor Green
}
catch {
    Write-Host "✗ Error al activar entorno virtual" -ForegroundColor Red
    exit 1
}

# Instalar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencias instaladas" -ForegroundColor Green

# Crear directorio instance si no existe
if (-not (Test-Path "instance")) {
    New-Item -ItemType Directory -Path "instance" | Out-Null
    Write-Host "✓ Directorio instance creado" -ForegroundColor Green
}

# Inicializar base de datos si se solicita
if ($InitDB) {
    Write-Host "Inicializando base de datos..." -ForegroundColor Yellow
    python -c 'from app import app, init_db; app.app_context().push(); init_db()'
    Write-Host "✓ Base de datos inicializada" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuración del Sistema" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Host: $Host" -ForegroundColor White
Write-Host "Puerto: $Port" -ForegroundColor White
Write-Host "Modo: $(if ($UseWaitress) { 'Producción (Waitress)' } else { 'Desarrollo (Flask)' })" -ForegroundColor White
Write-Host ""

Write-Host "Credenciales por defecto:" -ForegroundColor Yellow
Write-Host "  Usuario: admin" -ForegroundColor White
Write-Host "  Contraseña: admin123" -ForegroundColor White
Write-Host ""

Write-Host "URL de acceso:" -ForegroundColor Green
Write-Host "  http://${Host}:${Port}" -ForegroundColor Cyan
Write-Host ""

# Ejecutar aplicación
if ($UseWaitress) {
    Write-Host "Iniciando servidor Waitress (Producción)..." -ForegroundColor Green
    Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
    Write-Host ""
    waitress-serve --host=$Host --port=$Port app:app
} else {
    Write-Host "Iniciando servidor Flask (Desarrollo)..." -ForegroundColor Green
    Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
    Write-Host ""
    $env:FLASK_APP = "app.py"
    $env:FLASK_ENV = "development"
    $env:FLASK_DEBUG = "1"
    python -m flask run --host=$Host --port=$Port
}