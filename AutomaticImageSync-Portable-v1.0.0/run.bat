@echo off
echo Automatic Image Sync - Portable Edition
echo ========================================

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is required but not found.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Setup virtual environment if needed
if not exist "venv" (
    echo Setting up portable environment...
    python -m venv venv
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Start GUI
echo Starting GUI application...
python main.py

REM If GUI fails, show CLI help
if errorlevel 1 (
    echo.
    echo GUI failed to start. Use run_cli.bat for command line version.
    pause
)
