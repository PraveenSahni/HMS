# Sync IST Health design system assets into the React frontend.
# Run from repo root: .\frontend\scripts\sync-design.ps1

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$design = Join-Path $root 'design\styles'
$assets = Join-Path $root 'assets'
$legal = Join-Path $root 'legal'
$frontend = Join-Path $root 'frontend'
$publicStyles = Join-Path $frontend 'public\styles'

New-Item -ItemType Directory -Path $publicStyles -Force | Out-Null
Copy-Item (Join-Path $design '*') (Join-Path $frontend 'src\styles\') -Force
Copy-Item (Join-Path $design '*') $publicStyles -Force
Copy-Item (Join-Path $assets 'logo-full.svg') (Join-Path $frontend 'public\assets\logo-full.svg') -Force
Copy-Item (Join-Path $assets 'logo-symbol.svg') (Join-Path $frontend 'public\assets\logo-symbol.svg') -Force
Copy-Item (Join-Path $legal 'privacy.html') (Join-Path $frontend 'public\legal\privacy.html') -Force
Copy-Item (Join-Path $legal 'terms.html') (Join-Path $frontend 'public\legal\terms.html') -Force

# Ensure legal pages reference served CSS path
$legalFiles = @('privacy.html', 'terms.html')
foreach ($file in $legalFiles) {
    $path = Join-Path $frontend "public\legal\$file"
    (Get-Content $path -Raw) -replace '\.\./design/styles/ist-health\.css', '/styles/ist-health.css' |
        Set-Content $path -NoNewline
}

Write-Host 'Design sync complete: src/styles, public/styles, logos, legal pages.'
