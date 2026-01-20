@echo off
REM Windows batch script to run the Notes App
REM This script sets up environment and starts the server

cls
echo ================================
echo  AI Enhanced Notes App Launcher
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Python found: 
python --version
echo.

REM Check if dependencies are installed
echo [2/4] Checking dependencies...
pip list | findstr /i "fastapi uvicorn sentence-transformers" >nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed
)
echo.

REM Check if vectors directory exists
echo [3/4] Checking vector store...
if not exist "app\vectors" (
    mkdir app\vectors
    echo Created vectors directory
) else (
    echo Vector store ready
)
echo.

REM Start the server
echo [4/4] Starting server...
echo.
echo ================================
echo  Server starting on:
echo  http://127.0.0.1:8000
echo ================================
echo.
echo Press CTRL+C to stop the server
echo.

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

pause
