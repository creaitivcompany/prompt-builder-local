import sys
import os
import requests
import json
import re
import concurrent.futures
import traceback
import subprocess
import stat
from functools import partial
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
    QMessageBox, QTextEdit, QComboBox, QLabel,
    QPushButton, QSpinBox, QFrame, QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

# Import your existing modules
from ai_generators import (
    get_generator_names, get_generator_config, supports_negative_prompt,
    has_flags, format_prompt, get_midjourney_options
)
from generate_prompts_from_image import generate_prompts_from_image

# Try to import llama-cpp-python (optional)
try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("llama-cpp-python not installed. Local LLM will not be available.")

# --- Configuration ---
# Local LLM model path - CHANGE THIS to your downloaded model
LOCAL_MODEL_PATH = "/Users/jozefkubica/prompt_builder/models/phi-3-mini-4k-instruct-q4.gguf"

class PromptBuilderQt(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(script_dir, 'layout_local_only.ui')

        # Load the UI file
        uic.loadUi(ui_file_path, self)

        # Get references to widgets by their objectName (set in Qt Designer)
        self.upload_btn = self.findChild(QPushButton, "uploadButton")
        self.image_label = self.findChild(QLabel, "imageFileLabel")
        self.preview = self.findChild(QLabel, "imagePreviewLabel")
        self.generate_btn = self.findChild(QPushButton, "generateButton")
        self.prompt_text = self.findChild(QTextEdit, "promptText")
        self.send_to_refiner_btn = self.findChild(QPushButton, "sendToRefinerButton")

        # AI Generator controls
        self.model_combo = self.findChild(QComboBox, "modelCombo")
        self.mj_controls_frame = self.findChild(QFrame, "mjControlsFrame")
        self.aspect_ratio_combo = self.findChild(QComboBox, "aspectRatioCombo")
        self.version_combo = self.findChild(QComboBox, "versionCombo")
        self.style_combo = self.findChild(QComboBox, "styleCombo")
        self.stylize_spinbox = self.findChild(QSpinBox, "stylizeSpinBox")
        self.convert_btn = self.findChild(QPushButton, "convertButton")
        self.converted_text = self.findChild(QTextEdit, "convertedText")

        # Right column (refiner) controls
        self.refiner_input = self.findChild(QTextEdit, "refinerInput")
        self.refine_btn = self.findChild(QPushButton, "refineButton")
        self.refiner_output = self.findChild(QTextEdit, "refinerOutput")
        self.send_to_ai_btn = self.findChild(QPushButton, "sendToAiButton")
        self.copy_btn = self.findChild(QPushButton, "copyButton")

        # State variables
        self.uploaded_image = None
        self.local_llm = None
        
        # Thread executor for background tasks
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        # Setup UI
        self.setup_ui()
        self.connect_signals()
        self.load_local_llm()

    def setup_ui(self):
        """Initialize UI elements with data"""
        # Populate AI generator dropdown
        self.model_combo.addItems(get_generator_names())
        self.model_combo.setCurrentText("None")

        # Populate Midjourney controls
        self.aspect_ratio_combo.addItems(["1:1", "16:9", "9:16", "4:3", "3:4", "2:3", "3:2"])
        self.aspect_ratio_combo.setCurrentText("16:9")

        self.version_combo.addItems(["6", "5.2", "5.1", "5"])
        self.version_combo.setCurrentText("6")

        self.style_combo.addItems(["raw", "default"])
        self.style_combo.setCurrentText("raw")

        # Initially hide Midjourney controls
        self.mj_controls_frame.setVisible(False)

        # Load logo if it exists
        self.load_logo()

    def load_local_llm(self):
        """Load the local LLM model with verbose diagnostics."""
        print("=== Local LLM diagnostics start ===")
        print("LLAMA_CPP_AVAILABLE:", LLAMA_CPP_AVAILABLE)

        # Try import again and print details
        try:
            from llama_cpp import Llama
            print("Imported llama_cpp (llama-cpp-python) successfully.")
        except Exception as e:
            print("ImportError: failed to import llama_cpp:", repr(e))
            traceback.print_exc()
            self.local_llm = None
            print("=== Local LLM diagnostics end ===")
            return

        model_path = LOCAL_MODEL_PATH
        print("Configured LOCAL_MODEL_PATH:", model_path)

        # File existence & metadata
        try:
            exists = os.path.exists(model_path)
            print("Model exists:", exists)
            if exists:
                st = os.stat(model_path)
                print("Model file size (bytes):", st.st_size)
                print("Model file mode:", oct(st.st_mode))
                print("Model file permissions (rwx for owner):",
                      bool(st.st_mode & stat.S_IRUSR),
                      bool(st.st_mode & stat.S_IWUSR),
                      bool(st.st_mode & stat.S_IXUSR))
                # Run 'file' to see actual file type
                try:
                    file_out = subprocess.run(["file", model_path], capture_output=True, text=True, check=False)
                    print("`file` output:", file_out.stdout.strip())
                except Exception as e:
                    print("Could not run `file` command:", repr(e))
            else:
                print("Model not found at path. Please re-check the path and filename.")
                self.local_llm = None
                print("=== Local LLM diagnostics end ===")
                return
        except Exception as e:
            print("Error checking model file:", repr(e))
            traceback.print_exc()
            self.local_llm = None
            print("=== Local LLM diagnostics end ===")
            return

        # Attempt to instantiate Llama and show full traceback on failure
        try:
            print("Attempting to load model with Llama(...) – this may take a moment.")
            # Use conservative defaults; adjust n_threads as needed
            self.local_llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4, verbose=False)
            print("Local LLM loaded successfully!")
        except Exception as e:
            print("Exception while loading model with Llama():", repr(e))
            traceback.print_exc()
            self.local_llm = None

        print("=== Local LLM diagnostics end ===")

    def load_logo(self):
        """Load logo image if it exists"""
        logo_path = "PromptGen.png"
        if os.path.exists(logo_path):
            logo_label = self.findChild(QLabel, "logoLabel")
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setText("")  # Clear the default "■" text

    def connect_signals(self):
        """Connect UI signals to their respective slots"""
        # Left column signals
        self.upload_btn.clicked.connect(self.upload_image)
        self.generate_btn.clicked.connect(self.generate_prompt)
        self.send_to_refiner_btn.clicked.connect(self.send_to_refiner)

        # AI Generator signals
        self.model_combo.currentTextChanged.connect(self.on_generator_changed)
        self.convert_btn.clicked.connect(self.convert_prompt)

        # Midjourney controls signals
        self.aspect_ratio_combo.currentTextChanged.connect(self.convert_prompt)
        self.version_combo.currentTextChanged.connect(self.convert_prompt)
        self.style_combo.currentTextChanged.connect(self.convert_prompt)
        self.stylize_spinbox.valueChanged.connect(self.convert_prompt)

        # Right column signals
        self.refine_btn.clicked.connect(self.refine_prompt)
        self.send_to_ai_btn.clicked.connect(self.send_to_ai_generator)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

    def upload_image(self):
        """Handle image upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image",
            "",
            "Image files (*.jpg *.jpeg *.png *.bmp *.gif *.tiff)"
        )

        if file_path:
            try:
                # Store the image path
                self.uploaded_image = file_path

                # Update the file label
                self.image_label.setText(f"Selected: {os.path.basename(file_path)}")

                # Load and display preview
                pixmap = QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
                self.preview.setPixmap(scaled_pixmap)
                self.preview.setText("")  # Clear the default text

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def generate_prompt(self):
        """Generate prompt from uploaded image"""
        if not self.uploaded_image:
            QMessageBox.warning(self, "Warning", "Please upload an image first!")
            return

        try:
            display_text = self.analyze_image(self.uploaded_image)
            self.prompt_text.setPlainText(display_text)
            self.convert_prompt()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate prompt: {str(e)}")

    def analyze_image(self, image_path):
        """Analyze image using BLIP model"""
        # Use BLIP-based generator; returns a list of strings
        prompts = generate_prompts_from_image(image_path)
        # Ensure no stray braces or extra spaces (defensive)
        cleaned = [p.strip(" {}[]\"'").strip() for p in prompts if p and p.strip()]
        if not cleaned:
            return ""
        # Build one longer prompt from the list
        base = cleaned[0].rstrip(".")
        extras = cleaned[1:]
        if extras:
            base += ". " + "; ".join(extras)
        return base

    def on_generator_changed(self, text):
        """Handle AI generator selection change"""
        selected_generator = self.model_combo.currentText()

        # Show/hide Midjourney controls
        self.mj_controls_frame.setVisible(selected_generator == "Midjourney")

        # Convert prompt with new generator
        self.convert_prompt()

    def convert_prompt(self):
        """Convert prompt according to selected AI generator and show both positive and negative in converted field"""
        prompt = self.prompt_text.toPlainText().strip()
        if not prompt:
            self.converted_text.setPlainText("")
            return

        selected_generator = self.model_combo.currentText()

        # Prepare kwargs for format_prompt
        kwargs = {}

        # Add Midjourney-specific parameters
        if selected_generator == "Midjourney":
            stylize_value = self.stylize_spinbox.value()
            kwargs.update({
                "aspect_ratio": self.aspect_ratio_combo.currentText(),
                "version": self.version_combo.currentText(),
                "style": self.style_combo.currentText(),
                "stylize": stylize_value if stylize_value != 100 else None
            })

        # Format the prompt using the ai_generators module
        result = format_prompt(selected_generator, prompt, **kwargs)

        # Always show both positive and negative in the converted field
        if supports_negative_prompt(selected_generator) and result.get("negative"):
            # Show positive prompt first, then negative prompt
            display_text = f"Positive:\n{result['positive']}\n\nNegative:\n{result['negative']}"
        else:
            # Show only positive prompt
            display_text = result["positive"]

        self.converted_text.setPlainText(display_text)

    def send_to_refiner(self):
        """Send generated prompt to refiner"""
        prompt = self.prompt_text.toPlainText().strip()
        self.refiner_input.setPlainText(prompt)

    def refine_prompt(self):
        """Refine prompt using local LLM only."""
        prompt = self.refiner_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Warning", "Please enter a prompt to refine!")
            return

        # Check if local LLM is available
        if not self.local_llm:
            QMessageBox.warning(
                self,
                "Warning",
                "Local LLM is not available. Please check the model path and installation."
            )
            return

        # Disable the refine button during processing
        self.refine_btn.setEnabled(False)
        self.refine_btn.setText("Refining...")

        # Use local LLM
        future = self.executor.submit(self.improve_prompt_with_local, prompt)

        # Set up callback for when refinement is done
        future.add_done_callback(lambda f: QTimer.singleShot(0, partial(self._on_refine_done, f)))

    def _on_refine_done(self, future):
        """Handle completion of prompt refinement."""
        try:
            result = future.result()
        except Exception as e:
            result = f"Error during refinement: {str(e)}"

        # Update UI
        self.refiner_output.setPlainText(str(result))

        self.refine_btn.setEnabled(True)
        self.refine_btn.setText("Refine Prompt")

    def improve_prompt_with_local(self, prompt):
        """Improve prompt using local LLM"""
        if not self.local_llm:
            return "Local LLM not available. Please check model path and installation."
        
        instruction = (
            "Improve and expand this image prompt for an image-generation model. "
            "Make it more descriptive and detailed while keeping it concise. "
            "Focus on visual elements, style, lighting, and composition. "
            "Return only the improved prompt without any explanation.\n\n"
            f"Original prompt: {prompt}\n\n"
            "Improved prompt:"
        )
        
        try:
            response = self.local_llm(
                instruction,
                max_tokens=256,
                temperature=0.7,
                top_p=0.9,
                stop=["Original prompt:", "Improved prompt:", "\n\n"],
                echo=False
            )
            
            # Extract the generated text
            generated_text = response.get("choices", [{}])[0].get("text", "").strip()
            
            # Clean up the response
            if generated_text:
                # Remove any remaining instruction text
                lines = generated_text.split('\n')
                cleaned_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith(("Original prompt:", "Improved prompt:", "Here's")):
                        cleaned_lines.append(line)
                
                result = ' '.join(cleaned_lines).strip()
                return result if result else prompt
            else:
                return prompt
            
        except Exception as e:
            return f"Local LLM error: {str(e)}"

    def send_to_ai_generator(self):
        """Send refined prompt back to AI generator"""
        refined = self.refiner_output.toPlainText().strip()
        self.prompt_text.setPlainText(refined)
        self.convert_prompt()

    def copy_to_clipboard(self):
        """Copy refined prompt to clipboard"""
        refined = self.refiner_output.toPlainText().strip()
        if refined:
            clipboard = QApplication.clipboard()
            clipboard.setText(refined)
            QMessageBox.information(self, "Success", "Refined prompt copied to clipboard!")
        else:
            QMessageBox.warning(self, "Warning", "No prompt to copy!")

def main():
    app = QApplication(sys.argv)

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ui_file_path = os.path.join(script_dir, 'layout_local_only.ui')

    # Check if layout_local_only.ui exists
    if not os.path.exists(ui_file_path):
        QMessageBox.critical(None, "Error", "layout_local_only.ui file not found! Please make sure it's in the same directory as this script.")
        sys.exit(1)

    window = PromptBuilderQt()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()