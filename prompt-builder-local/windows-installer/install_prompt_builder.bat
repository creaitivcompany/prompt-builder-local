@echo off
setlocal enabledelayedexpansion

REM Prompt Builder Local-Only Installer for Windows
REM This script installs the Prompt Builder application with all dependencies

echo.
echo 🚀 Prompt Builder Local-Only Installer for Windows
echo ===================================================
echo.

REM Set installation directory
set "INSTALL_DIR=%USERPROFILE%\AppData\Local\PromptBuilder"
set "MODELS_DIR=%INSTALL_DIR%\models"

echo [INFO] Installation directory: %INSTALL_DIR%
echo.

REM Create installation directory
echo [INFO] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%MODELS_DIR%" mkdir "%MODELS_DIR%"

REM Check if required files exist
echo [INFO] Checking required files...
set "MISSING_FILES="

if not exist "prompt_builder_qt_local_only.py" set "MISSING_FILES=!MISSING_FILES! prompt_builder_qt_local_only.py"
if not exist "layout_local_only.ui" set "MISSING_FILES=!MISSING_FILES! layout_local_only.ui"
if not exist "ai_generators.py" set "MISSING_FILES=!MISSING_FILES! ai_generators.py"
if not exist "generate_prompts_from_image.py" set "MISSING_FILES=!MISSING_FILES! generate_prompts_from_image.py"
if not exist "blip1_m1_optimized.py" set "MISSING_FILES=!MISSING_FILES! blip1_m1_optimized.py"
if not exist "requirements_local_only.txt" set "MISSING_FILES=!MISSING_FILES! requirements_local_only.txt"

if not "!MISSING_FILES!"=="" (
    echo [ERROR] Required files missing:!MISSING_FILES!
    echo [ERROR] Please make sure all files are in the installer directory.
    pause
    exit /b 1
)

echo [SUCCESS] All required files found.
echo.

REM Copy application files
echo [INFO] Copying application files...
copy "prompt_builder_qt_local_only.py" "%INSTALL_DIR%\" >nul
copy "layout_local_only.ui" "%INSTALL_DIR%\" >nul
copy "ai_generators.py" "%INSTALL_DIR%\" >nul
copy "generate_prompts_from_image.py" "%INSTALL_DIR%\" >nul
copy "blip1_m1_optimized.py" "%INSTALL_DIR%\" >nul
copy "requirements_local_only.txt" "%INSTALL_DIR%\" >nul

REM Copy logo if it exists
if exist "PromptGen.png" (
    copy "PromptGen.png" "%INSTALL_DIR%\" >nul
    echo [INFO] Logo copied.
)

echo [SUCCESS] Application files copied.
echo.

REM Check Python installation
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo [ERROR] Please install Python 3.8 or later from python.org
    echo [ERROR] Download: https://www.python.org/downloads/
    echo [ERROR] Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo [SUCCESS] Python %PYTHON_VERSION% found
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available. Please reinstall Python with pip.
    pause
    exit /b 1
)

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
echo [INFO] This may take several minutes...
echo.

pip install -r "%INSTALL_DIR%\requirements_local_only.txt" --user --quiet
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install.
    echo [WARNING] You can try installing them manually later.
) else (
    echo [SUCCESS] Python dependencies installed successfully.
)
echo.

REM Create launcher batch file
echo [INFO] Creating launcher script...
(
echo @echo off
echo REM Prompt Builder Launcher
echo cd /d "%%~dp0"
echo.
echo REM Check if Python dependencies are installed
echo python -c "import PyQt6, torch, transformers, PIL, requests" 2^>nul
echo if errorlevel 1 ^(
echo     echo Dependencies not found. Installing...
echo     pip install -r requirements_local_only.txt --user
echo ^)
echo.
echo REM Launch the application
echo echo Starting Prompt Builder...
echo python prompt_builder_qt_local_only.py
echo.
echo REM Keep window open if there's an error
echo if errorlevel 1 ^(
echo     echo.
echo     echo Press any key to close...
echo     pause ^>nul
echo ^)
) > "%INSTALL_DIR%\launch_prompt_builder.bat"

echo [SUCCESS] Launcher script created.
echo.

REM Create desktop shortcut
echo [INFO] Creating desktop shortcut...
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\Prompt Builder.bat"
(
echo @echo off
echo cd /d "%INSTALL_DIR%"
echo call launch_prompt_builder.bat
) > "%DESKTOP_SHORTCUT%"

REM Create Start Menu shortcut
set "STARTMENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%STARTMENU_DIR%" mkdir "%STARTMENU_DIR%"
set "STARTMENU_SHORTCUT=%STARTMENU_DIR%\Prompt Builder.bat"
copy "%DESKTOP_SHORTCUT%" "%STARTMENU_SHORTCUT%" >nul

echo [SUCCESS] Desktop and Start Menu shortcuts created.
echo.

REM Download model (optional)
echo [INFO] Model Setup
echo [INFO] ===========
echo The application requires a local LLM model for the prompt refiner feature.
echo You can download a recommended model or use your own.
echo.
echo Recommended model: Phi-3 Mini 4K Instruct (Q4, ~2.4GB)
echo.
set /p "DOWNLOAD_MODEL=Would you like to download the recommended model now? (y/n): "
if /i "!DOWNLOAD_MODEL!"=="y" (
    echo [INFO] Downloading model... (this may take a while)
    set "MODEL_URL=https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
    set "MODEL_FILE=%MODELS_DIR%\phi-3-mini-4k-instruct-q4.gguf"
    
    REM Try to download with PowerShell
    powershell -Command "try { Invoke-WebRequest -Uri '!MODEL_URL!' -OutFile '!MODEL_FILE!' -UseBasicParsing; Write-Host '[SUCCESS] Model downloaded successfully!' } catch { Write-Host '[ERROR] Model download failed. You can download it manually later.' }"
    
    REM Check if model was downloaded
    if exist "!MODEL_FILE!" (
        echo [INFO] Updating model path in application...
        REM Use PowerShell to update the model path (more reliable than batch string replacement)
        powershell -Command "(Get-Content '%INSTALL_DIR%\prompt_builder_qt_local_only.py') -replace 'LOCAL_MODEL_PATH = \".*\"', 'LOCAL_MODEL_PATH = \"!MODEL_FILE!\"' | Set-Content '%INSTALL_DIR%\prompt_builder_qt_local_only.py'"
        echo [SUCCESS] Model path updated in application.
    )
) else (
    echo [WARNING] Model not downloaded. You'll need to:
    echo [WARNING] 1. Download a GGUF model file
    echo [WARNING] 2. Update LOCAL_MODEL_PATH in prompt_builder_qt_local_only.py
)

echo.
echo [SUCCESS] Installation completed!
echo.
echo 📱 How to run the application:
echo    • Double-click 'Prompt Builder.bat' on your Desktop
echo    • Or from Start Menu: Start ^> Prompt Builder
echo    • Or run: %INSTALL_DIR%\launch_prompt_builder.bat
echo.
echo 📁 Installation location: %INSTALL_DIR%
echo.
echo 🔧 To uninstall:
echo    • Delete the folder: %INSTALL_DIR%
echo    • Delete the shortcuts from Desktop and Start Menu
echo.

if not exist "%MODELS_DIR%\phi-3-mini-4k-instruct-q4.gguf" (
    echo [WARNING] Remember to download and configure a model for the prompt refiner!
)

echo [SUCCESS] Enjoy using Prompt Builder! 🎉
echo.
echo If you encounter any issues, check the README_INSTALLER.txt file
echo or try running the app from Command Prompt to see error messages.
echo.
pause