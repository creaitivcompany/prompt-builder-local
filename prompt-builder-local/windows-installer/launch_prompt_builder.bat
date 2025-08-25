@echo off
REM Prompt Builder Launcher for Windows
REM This script launches the Prompt Builder application

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if Python dependencies are installed
echo Checking dependencies...
python -c "import PyQt6, torch, transformers, PIL, requests" 2>nul
if errorlevel 1 (
    echo Dependencies not found. Installing...
    pip install -r requirements_local_only.txt --user
    if errorlevel 1 (
        echo Failed to install dependencies. Please install manually:
        echo pip install -r requirements_local_only.txt --user
        pause
        exit /b 1
    )
)

REM Launch the application
echo Starting Prompt Builder...
python prompt_builder_qt_local_only.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred. Check the error message above.
    echo Press any key to close...
    pause >nul
)