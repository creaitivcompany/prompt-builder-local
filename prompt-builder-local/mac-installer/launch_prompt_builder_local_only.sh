#!/bin/bash

# Prompt Builder Local-Only Mac App Launcher Script
# This script sets up the environment and launches the PyQt6 application

# Get the directory where this script is located (inside the app bundle)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APP_DIR="$SCRIPT_DIR"

# Change to the app directory
cd "$APP_DIR"

# Set up Python path to include the app directory
export PYTHONPATH="$APP_DIR:$PYTHONPATH"

# Try to find the correct Python installation
# Check multiple possible Python locations
PYTHON_CANDIDATES=(
    "/usr/bin/python3"
    "/usr/local/bin/python3"
    "/opt/homebrew/bin/python3"
    "$(which python3 2>/dev/null)"
    "$(which python 2>/dev/null)"
)

PYTHON_CMD=""

# Test each Python candidate to see if PyQt6 is available
for candidate in "${PYTHON_CANDIDATES[@]}"; do
    if [[ -n "$candidate" && -x "$candidate" ]]; then
        # Test if this Python has PyQt6
        if "$candidate" -c "import PyQt6" 2>/dev/null; then
            PYTHON_CMD="$candidate"
            echo "Found working Python with PyQt6: $PYTHON_CMD"
            break
        fi
    fi
done

# If no Python with PyQt6 found, try to install it
if [[ -z "$PYTHON_CMD" ]]; then
    # Try to find any working Python3
    for candidate in "${PYTHON_CANDIDATES[@]}"; do
        if [[ -n "$candidate" && -x "$candidate" ]]; then
            PYTHON_CMD="$candidate"
            break
        fi
    done
    
    if [[ -n "$PYTHON_CMD" ]]; then
        # Try to install PyQt6 and other dependencies
        osascript -e 'display dialog "PyQt6 not found. Attempting to install dependencies for local-only version..." buttons {"OK"} default button "OK"'
        
        # Try pip3 first, then pip
        if command -v pip3 &> /dev/null; then
            pip3 install PyQt6 torch torchvision transformers accelerate Pillow sentencepiece protobuf psutil llama-cpp-python
        elif command -v pip &> /dev/null; then
            pip install PyQt6 torch torchvision transformers accelerate Pillow sentencepiece protobuf psutil llama-cpp-python
        else
            osascript -e 'display dialog "pip not found. Please install Python dependencies manually:\n\npip3 install PyQt6 torch torchvision transformers accelerate Pillow sentencepiece protobuf psutil llama-cpp-python" buttons {"OK"} default button "OK"'
            exit 1
        fi
        
        # Test again after installation
        if ! "$PYTHON_CMD" -c "import PyQt6" 2>/dev/null; then
            osascript -e 'display dialog "Failed to install PyQt6. Please run in Terminal:\n\npip3 install PyQt6 torch torchvision transformers accelerate Pillow sentencepiece protobuf psutil llama-cpp-python\n\nThen try launching the app again." buttons {"OK"} default button "OK"'
            exit 1
        fi
    else
        osascript -e 'display dialog "Python 3 is not installed. Please install Python 3 from python.org or using Homebrew." buttons {"OK"} default button "OK"'
        exit 1
    fi
fi

echo "Using Python: $PYTHON_CMD"
echo "Working directory: $APP_DIR"
echo "Python path: $PYTHONPATH"

# Check if required files exist
if [[ ! -f "prompt_builder_qt_local_only.py" ]]; then
    osascript -e 'display dialog "Main application file not found. Please ensure prompt_builder_qt_local_only.py is in the app bundle." buttons {"OK"} default button "OK"'
    exit 1
fi

if [[ ! -f "layout_local_only.ui" ]]; then
    osascript -e 'display dialog "UI layout file not found. Please ensure layout_local_only.ui is in the app bundle." buttons {"OK"} default button "OK"'
    exit 1
fi

# Launch the application
"$PYTHON_CMD" prompt_builder_qt_local_only.py

# If the app exits with an error, show a dialog
if [ $? -ne 0 ]; then
    osascript -e 'display dialog "The application encountered an error. Please check the console for details." buttons {"OK"} default button "OK"'
fi