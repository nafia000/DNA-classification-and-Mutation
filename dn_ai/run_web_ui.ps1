# DN-AI Web UI Launcher (PowerShell)
# This script starts the Streamlit web interface

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   DN-AI Web Interface Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script location
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if we're in the right directory
if (-not (Test-Path "$scriptPath\src\main.py")) {
    Write-Host "ERROR: Please run this script from the DN-AI project directory" -ForegroundColor Red
    Write-Host "Expected location: c:\Users\nafia\main project\dn_ai" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dataset exists
if (-not (Test-Path "$scriptPath\..\synthetic_dna_dataset.csv")) {
    Write-Host "WARNING: synthetic_dna_dataset.csv not found in parent directory" -ForegroundColor Yellow
    Write-Host "The application may not work correctly without the dataset" -ForegroundColor Yellow
    Write-Host ""
}

# Change to project directory
Set-Location $scriptPath

Write-Host "Installing/updating Streamlit..." -ForegroundColor Green
pip install streamlit -q

Write-Host ""
Write-Host "Starting DN-AI Web Interface..." -ForegroundColor Green
Write-Host "Opening browser at http://localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m streamlit run app.py

Read-Host "Press Enter to exit"
