@echo off
echo ================================
echo   Genome-X ML Integration Setup
echo ================================
echo.

echo Step 1: Installing Frontend Dependencies...
echo.
call npm install
if errorlevel 1 (
    echo Error installing npm dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Installing Backend Dependencies...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing Python dependencies
    pause
    exit /b 1
)

echo.
echo ================================
echo   Setup Complete!
echo ================================
echo.
echo To start the application:
echo.
echo 1. Terminal 1 - Start Backend:
echo    python server.py
echo.
echo 2. Terminal 2 - Start Frontend:
echo    npm run dev
echo.
echo Frontend will be available at: http://localhost:5173
echo Backend API will be available at: http://localhost:8000
echo.
pause
