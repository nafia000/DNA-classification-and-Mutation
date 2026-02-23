@echo off
REM DN-AI Web UI Launcher
REM This script starts the Streamlit web interface

echo.
echo ========================================
echo    DN-AI Web Interface Launcher
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "src\main.py" (
    echo ERROR: Please run this script from the DN-AI project directory
    echo Expected location: c:\Users\nafia\main project\dn_ai
    pause
    exit /b 1
)

REM Check if synthetic_dna_dataset.csv exists
if not exist "..\synthetic_dna_dataset.csv" (
    echo WARNING: synthetic_dna_dataset.csv not found in parent directory
    echo The application may not work correctly without the dataset
    echo.
)

echo Installing/updating Streamlit...
pip install streamlit -q

echo.
echo Starting DN-AI Web Interface...
echo Opening browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run app.py

pause
