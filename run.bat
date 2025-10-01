@echo off
echo Automatic Image Sync - Windows Launcher
echo =======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found in current directory
    echo Please run this script from the AutomaticImageSync directory
    pause
    exit /b 1
)

REM Try to launch the application
echo Starting Automatic Image Sync...
python main.py

REM If there are errors, try running setup first
if errorlevel 1 (
    echo.
    echo There was an error starting the application.
    echo Attempting to install dependencies...
    python setup.py
    echo.
    echo Please try running the application again.
    pause
)
