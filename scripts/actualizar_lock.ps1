<#
Regenera requirements-build.lock con las versiones exactas para construir la portable.
Usarlo solo para actualizar dependencias a proposito (ver docs\portable.md).
#>
$ErrorActionPreference = "Stop"
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    py -3.13 -m venv .venv-lock --clear
    if ($LASTEXITCODE -ne 0) { throw "No se pudo crear el entorno temporal." }
    $python = ".venv-lock\Scripts\python.exe"

    & $python -m pip install --quiet --upgrade pip
    & $python -m pip install --quiet ".[build]"
    if ($LASTEXITCODE -ne 0) { throw "No se pudieron instalar las dependencias." }

    & $python -m pip freeze --exclude generador-recetas |
        Out-File -Encoding ascii requirements-build.lock
    if ($LASTEXITCODE -ne 0) { throw "No se pudo escribir el lock." }

    Write-Host "Listo: requirements-build.lock. Revisa el diff antes de hacer commit." -ForegroundColor Green
}
finally {
    Remove-Item -Recurse -Force .venv-lock -ErrorAction SilentlyContinue
    Pop-Location
}