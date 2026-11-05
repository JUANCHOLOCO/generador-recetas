<#
Genera la version portable en dist\ (ver docs\portable.md).
Crea un entorno limpio (.venv-build) con las versiones exactas de requirements-build.lock,
revisa vulnerabilidades conocidas y empaqueta con PyInstaller.
Requiere Python 3.13 (py -3.13) y el entorno de desarrollo activo (para pip-audit).
#>
param([switch]$SinAuditoria)
$ErrorActionPreference = "Stop"

function Invocar([string]$paso, [scriptblock]$comando) {
    Write-Host "== $paso" -ForegroundColor Cyan
    & $comando
    if ($LASTEXITCODE -ne 0) { throw "Fallo: $paso" }
}

function Comprimir([string]$carpeta, [string]$zip) {
    # .NET y no Compress-Archive: comparte la lectura con el antivirus, que suele estar
    # revisando los archivos recien creados, e incluye las carpetas vacias (output\).
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    for ($intento = 1; $intento -le 3; $intento++) {
        try {
            if (Test-Path $zip) { Remove-Item $zip -Force }
            [IO.Compression.ZipFile]::CreateFromDirectory(
                $carpeta, $zip, [IO.Compression.CompressionLevel]::Optimal, $true)
            return
        } catch {
            if ($intento -eq 3) { throw }
            Write-Warning "Archivo en uso (antivirus?). Reintento en 5 segundos..."
            Start-Sleep -Seconds 5
        }
    }
}

Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    if ($SinAuditoria) {
        Write-Warning "Sin auditoria de vulnerabilidades: repetirla antes de entregar."
    } else {
        Invocar "Auditar dependencias" {
            pip-audit --requirement requirements-build.lock --no-deps --disable-pip
        }
    }

    $python = ".venv-build\Scripts\python.exe"
    Invocar "Crear entorno limpio" { py -3.13 -m venv .venv-build --clear }
    Invocar "Instalar dependencias" {
        & $python -m pip install --quiet -r requirements-build.lock
    }
    Invocar "Instalar la app" { & $python -m pip install --quiet --no-deps . }
    Invocar "Generar icono" { & $python scripts\generar_icono.py build\icono.ico }
    Invocar "Empaquetar" {
        & $python -m PyInstaller packaging\recetas.spec --noconfirm --clean
    }

    $version = & $python -c "import recetas; print(recetas.__version__)"
    New-Item -ItemType Directory -Force dist\GeneradorRecetas\output | Out-Null
    $origen = (Resolve-Path dist\GeneradorRecetas).Path
    $zip = Join-Path (Resolve-Path dist).Path "GeneradorRecetas_$version.zip"
    Invocar "Comprimir" { Comprimir $origen $zip }
    Write-Host "Listo: dist\GeneradorRecetas\ y $zip" -ForegroundColor Green
}
finally {
    Pop-Location
}