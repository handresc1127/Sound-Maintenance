# Soundlab - La Casa del DJ
# Script de inicialización simplificado para Windows
param(
    [switch]$UseWaitress = $false,
    [string]$Host = "127.0.0.1",
    [int]$Port = 5000
)

Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  Soundlab - La Casa del DJ" -ForegroundColor Magenta  
Write-Host "  Sound-Maintenance System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Magenta

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python no encontrado. Instalar Python 3.8+" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Entorno virtual activado" -ForegroundColor Green

# Instalar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Dependencias instaladas" -ForegroundColor Green

# Crear directorio instance
if (-not (Test-Path "instance")) {
    New-Item -ItemType Directory -Path "instance" | Out-Null
    Write-Host "✓ Directorio instance creado" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Iniciando Soundlab System" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Host: $Host" -ForegroundColor White
Write-Host "Puerto: $Port" -ForegroundColor White
Write-Host ""
Write-Host "Credenciales:" -ForegroundColor Yellow
Write-Host "  Usuario: admin" -ForegroundColor White
Write-Host "  Contraseña: admin123" -ForegroundColor White
Write-Host ""
Write-Host "URL: http://${Host}:${Port}" -ForegroundColor Cyan
Write-Host ""

# Iniciar servidor
if ($UseWaitress) {
    Write-Host "Iniciando Waitress (Producción)..." -ForegroundColor Green
    waitress-serve --host=$Host --port=$Port app:app
} else {
    Write-Host "Iniciando Flask (Desarrollo)..." -ForegroundColor Green
    $env:FLASK_APP = "app.py"
    $env:FLASK_DEBUG = "1"
    python app.py
}