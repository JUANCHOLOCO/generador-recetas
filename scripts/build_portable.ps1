<#
Genera la version portable en dist\GeneradorRecetas\ (ver docs\portable.md).
Requiere el entorno virtual activo con: pip install -e ".[dev,build]"
#>
$ErrorActionPreference = "Stop"
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    python scripts\generar_icono.py build\icono.ico
    if ($LASTEXITCODE -ne 0) { throw "No se pudo generar el icono." }

    pyinstaller packaging\recetas.spec --noconfirm --clean
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller termino con errores." }

    New-Item -ItemType Directory -Force dist\GeneradorRecetas\output | Out-Null
    Write-Host "Listo: dist\GeneradorRecetas\GeneradorRecetas.exe" -ForegroundColor Green
}
finally {
    Pop-Location
}