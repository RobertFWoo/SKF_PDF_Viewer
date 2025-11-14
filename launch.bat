@echo off
REM SKF PDF Viewer Launcher Script for Windows

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import PyQt6" 2>nul
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
)

REM Launch the PDF viewer
echo Starting SKF PDF Viewer...
python pdf_viewer.py %*
