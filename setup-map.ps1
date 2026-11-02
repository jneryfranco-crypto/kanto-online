$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
git submodule update --init --recursive
$Link = Join-Path $Root 'engine\decomp'
if (-not (Test-Path $Link)) {
    New-Item -ItemType Junction -Path $Link -Target (Resolve-Path (Join-Path $Root 'decomp')) | Out-Null
}
Set-Location (Join-Path $Root 'engine')
npm install
python -m pip install -r scripts/requirements.txt
npm run extract
npm test
npm run typecheck
Write-Host "Preparação concluída. Para iniciar: cd engine; npm run dev"
