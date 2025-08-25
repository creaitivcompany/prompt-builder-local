#!/bin/bash

# Prompt Builder Local-Only Installer
# This script installs the Prompt Builder application with all dependencies

set -e  # Exit on any error

echo "🚀 Prompt Builder Local-Only Installer"
echo "======================================"

# Function to print colored output (compatible with older bash)
print_status() {
    echo "[INFO] \$1"
}

print_success() {
    echo "[SUCCESS] \$1"
}

print_warning() {
    echo "[WARNING] \$1"
}

print_error() {
    echo "[ERROR] \$1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This installer is designed for macOS only."
    exit 1
fi

# Set installation directory
INSTALL_DIR="$HOME/Applications/PromptBuilder"
MODELS_DIR="$INSTALL_DIR/models"

print_status "Installation directory: $INSTALL_DIR"

# Create installation directory
print_status "Creating installation directory..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$MODELS_DIR"

# Check if required files exist
print_status "Checking required files..."
REQUIRED_FILES=(
    "prompt_builder_qt_local_only.py"
    "layout_local_only.ui"
    "ai_generators.py"
    "generate_prompts_from_image.py"
    "blip1_m1_optimized.py"
    "requirements_local_only.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Required file missing: $file"
        print_error "Please make sure all files are in the installer directory."
        exit 1
    fi
done

print_success "All required files found."

# Copy application files
print_status "Copying application files..."
cp prompt_builder_qt_local_only.py "$INSTALL_DIR/"
cp layout_local_only.ui "$INSTALL_DIR/"
cp ai_generators.py "$INSTALL_DIR/"
cp generate_prompts_from_image.py "$INSTALL_DIR/"
cp blip1_m1_optimized.py "$INSTALL_DIR/"
cp requirements_local_only.txt "$INSTALL_DIR/"

# Copy logo if it exists
if [ -f "PromptGen.png" ]; then
    cp PromptGen.png "$INSTALL_DIR/"
    print_status "Logo copied."
fi

print_success "Application files copied."

# Check Python installation
print_status "Checking Python installation..."
if ! command -v python3 >/dev/null 2>&1; then
    print_error "Python 3 is not installed."
    print_error "Please install Python 3.8 or later from python.org"
    print_error "Download: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))' 2>/dev/null || echo "unknown")
print_success "Python $PYTHON_VERSION found"

# Check if pip is available
if ! command -v pip3 >/dev/null 2>&1; then
    print_error "pip3 is not available. Please install pip."
    exit 1
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
print_status "This may take several minutes..."

if pip3 install -r "$INSTALL_DIR/requirements_local_only.txt" --user --quiet; then
    print_success "Python dependencies installed successfully."
else
    print_warning "Some dependencies may have failed to install."
    print_warning "You can try installing them manually later."
fi

# Create launcher script
print_status "Creating launcher script..."
cat > "$INSTALL_DIR/launch_prompt_builder.sh" << 'EOF'
#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the application directory
cd "$SCRIPT_DIR"

# Check if Python dependencies are installed
python3 -c "import PyQt6, torch, transformers, PIL, requests" 2>/dev/null || {
    echo "Dependencies not found. Installing..."
    pip3 install -r requirements_local_only.txt --user
}

# Launch the application
echo "Starting Prompt Builder..."
python3 prompt_builder_qt_local_only.py
EOF

chmod +x "$INSTALL_DIR/launch_prompt_builder.sh"
print_success "Launcher script created."

# Create desktop shortcut
print_status "Creating desktop shortcut..."
DESKTOP_FILE="$HOME/Desktop/Prompt Builder.command"
cat > "$DESKTOP_FILE" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
./launch_prompt_builder.sh
EOF
chmod +x "$DESKTOP_FILE"

# Create Applications folder shortcut
APPS_SHORTCUT="$HOME/Applications/Prompt Builder.command"
cp "$DESKTOP_FILE" "$APPS_SHORTCUT"

print_success "Desktop shortcuts created."

# Download model (optional)
echo ""
print_status "Model Setup"
print_status "==========="
echo "The application requires a local LLM model for the prompt refiner feature."
echo "You can download a recommended model or use your own."
echo ""
echo "Recommended model: Phi-3 Mini 4K Instruct (Q4, ~2.4GB)"
echo "Download URL: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
echo ""
echo "Would you like to download the recommended model now? (y/n)"
read -r REPLY
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Downloading model... (this may take a while)"
    MODEL_URL="https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
    MODEL_FILE="$MODELS_DIR/phi-3-mini-4k-instruct-q4.gguf"
    
    if command -v curl >/dev/null 2>&1; then
        if curl -L -o "$MODEL_FILE" "$MODEL_URL"; then
            print_success "Model downloaded successfully!"
        else
            print_error "Model download failed. You can download it manually later."
        fi
    elif command -v wget >/dev/null 2>&1; then
        if wget -O "$MODEL_FILE" "$MODEL_URL"; then
            print_success "Model downloaded successfully!"
        else
            print_error "Model download failed. You can download it manually later."
        fi
    else
        print_error "Neither curl nor wget found. Please download the model manually."
        print_status "Download URL: $MODEL_URL"
        print_status "Save to: $MODEL_FILE"
    fi
    
    if [ -f "$MODEL_FILE" ]; then
        # Update the model path in the Python file (compatible with older sed)
        if sed -i.bak "s|LOCAL_MODEL_PATH = \".*\"|LOCAL_MODEL_PATH = \"$MODEL_FILE\"|" "$INSTALL_DIR/prompt_builder_qt_local_only.py"; then
            print_success "Model path updated in application."
            rm "$INSTALL_DIR/prompt_builder_qt_local_only.py.bak" 2>/dev/null || true
        else
            print_warning "Could not automatically update model path."
            print_warning "Please manually edit prompt_builder_qt_local_only.py"
            print_warning "Set LOCAL_MODEL_PATH to: $MODEL_FILE"
        fi
    fi
else
    print_warning "Model not downloaded. You'll need to:"
    print_warning "1. Download a GGUF model file"
    print_warning "2. Update LOCAL_MODEL_PATH in prompt_builder_qt_local_only.py"
fi

# Final instructions
echo ""
print_success "Installation completed!"
echo ""
echo "📱 How to run the application:"
echo "   • Double-click 'Prompt Builder.command' on your Desktop"
echo "   • Or run: $INSTALL_DIR/launch_prompt_builder.sh"
echo ""
echo "📁 Installation location: $INSTALL_DIR"
echo ""
echo "🔧 To uninstall:"
echo "   • Delete the folder: $INSTALL_DIR"
echo "   • Delete the shortcuts from Desktop and Applications"
echo ""

if [ ! -f "$MODELS_DIR/phi-3-mini-4k-instruct-q4.gguf" ]; then
    print_warning "Remember to download and configure a model for the prompt refiner!"
fi

print_success "Enjoy using Prompt Builder! 🎉"

echo ""
echo "If you encounter any issues, check the README_INSTALLER.txt file"
echo "or try running the app from Terminal to see error messages."