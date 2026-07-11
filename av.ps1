$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$activate = Join-Path $root 'venv\Scripts\Activate.ps1'

if (Test-Path $activate) {
    & $activate
} else {
    Write-Host "Virtual environment not found at $root\\venv. Creating it now..."
    & (Join-Path $root 'venv.bat')
    if (Test-Path $activate) {
        & $activate
    } else {
        Write-Host 'Failed to activate the virtual environment.'
    }
}
