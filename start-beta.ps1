$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Engine = Join-Path $Root 'engine'
if (-not (Test-Path (Join-Path $Engine 'node_modules'))) {
    throw "Dependências não instaladas. Execute primeiro: .\setup-map.ps1"
}
if (-not (Test-Path (Join-Path $Engine 'public\data\overworld.json'))) {
    throw "Mapas ainda não extraídos. Execute primeiro: .\setup-map.ps1"
}
Set-Location $Engine
Write-Host "Kanto Online Beta local: http://127.0.0.1:3000"
Write-Host "Mantenha esta janela aberta enquanto joga. Ctrl+C encerra o servidor."
npm run dev -- --host 127.0.0.1
