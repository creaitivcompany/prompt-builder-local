===============================================================================
                PROMPT BUILDER LOCAL-ONLY - WINDOWS INSTALLATION GUIDE
===============================================================================

🚀 QUICK INSTALL
================

1. Download the installer package and extract it to a folder
2. Open Command Prompt as Administrator (recommended)
3. Navigate to the extracted folder
4. Run the installer:
   
   install_prompt_builder.bat

5. Follow the prompts - the installer will:
   • Install all Python dependencies
   • Set up the application in %USERPROFILE%\AppData\Local\PromptBuilder\
   • Create desktop and Start Menu shortcuts
   • Optionally download the AI model

📦 WHAT GETS INSTALLED
======================

• Application files in %USERPROFILE%\AppData\Local\PromptBuilder\
• Python dependencies (PyQt6, PyTorch, Transformers, etc.)
• Desktop shortcut: "Prompt Builder.bat"
• Start Menu shortcut: Start > Prompt Builder
• AI model (optional, ~2.4GB)

🎯 RUNNING THE APP
==================

After installation, you can run the app by:
• Double-clicking "Prompt Builder.bat" on your Desktop
• From Start Menu: Start > Prompt Builder
• Or running: %USERPROFILE%\AppData\Local\PromptBuilder\launch_prompt_builder.bat

💻 SYSTEM REQUIREMENTS
======================

• Windows 10 or later (tested on Windows 10/11)
• Python 3.8+ (install from python.org if needed)
• 4GB+ RAM (8GB recommended for AI model)
• 5GB free disk space (for app + model)
• Internet connection for initial setup

✨ FEATURES
===========

• Image Analysis - Upload images and generate descriptive prompts
• AI Generator Support - Format prompts for Midjourney, DALL-E, Stable Diffusion, etc.
• Local Prompt Refiner - Improve prompts using local AI (no internet required)
• No API Keys - Everything runs locally on your PC

🔧 TROUBLESHOOTING
==================

Python Issues:
--------------
If you get "Python is not recognized" error:

1. Install Python from python.org
2. During installation, CHECK "Add Python to PATH"
3. Restart Command Prompt
4. Test with: python --version

If you get dependency errors:
pip install PyQt6 torch transformers pillow requests --user

Permission Issues:
------------------
If you get permission errors:
1. Run Command Prompt as Administrator
2. Or install to a different location with write permissions

Model Issues:
-------------
If the prompt refiner doesn't work:
1. Check that the model file exists in the models folder
2. Make sure you have enough RAM (4GB+ free)
3. Update the model path in prompt_builder_qt_local_only.py

App Won't Start:
----------------
1. Make sure Python 3.8+ is installed and in PATH
2. Check that all files are in the same directory
3. Try running from Command Prompt to see error messages:
   cd %USERPROFILE%\AppData\Local\PromptBuilder
   python prompt_builder_qt_local_only.py

Antivirus Issues:
-----------------
Some antivirus software may flag the .bat files:
1. Add the installation folder to antivirus exceptions
2. Or run the Python file directly instead of the batch file

🗑️ UNINSTALLING
================

To remove the application:
1. Delete folder: %USERPROFILE%\AppData\Local\PromptBuilder
2. Delete shortcuts from Desktop and Start Menu
3. Optionally remove Python packages:
   pip uninstall PyQt6 torch transformers pillow requests

📋 INSTALLATION CHECKLIST
==========================

Before installing:
□ Windows 10 or later
□ At least 5GB free disk space
□ Python 3.8+ installed with PATH enabled
□ Internet connection for downloads

After installing:
□ Desktop shortcut created
□ Start Menu shortcut created
□ App launches without errors
□ Image upload works
□ Prompt generation works
□ Model downloaded (if selected)

🆘 SUPPORT
==========

For issues or questions:
• Check the troubleshooting section above
• Ensure Python is properly installed and in PATH
• Run Command Prompt as Administrator
• Check Windows Defender/antivirus settings

Common Solutions:
• Restart Command Prompt after Python installation
• Use "python" instead of "python3" on Windows
• Install Visual C++ Redistributable if PyTorch fails
• Disable antivirus temporarily during installation

📁 FILE STRUCTURE AFTER INSTALLATION
====================================

%USERPROFILE%\AppData\Local\PromptBuilder\
├── prompt_builder_qt_local_only.py    (Main application)
├── layout_local_only.ui               (User interface)
├── ai_generators.py                   (AI generator configs)
├── generate_prompts_from_image.py     (Image analysis)
├── blip1_m1_optimized.py             (BLIP model)
├── requirements_local_only.txt        (Dependencies)
├── launch_prompt_builder.bat          (Launcher script)
├── PromptGen.png                      (Logo, if included)
└── models\
    └── phi-3-mini-4k-instruct-q4.gguf (AI model, if downloaded)

Desktop:
└── Prompt Builder.bat                 (Desktop shortcut)

Start Menu:
└── Prompt Builder.bat                 (Start Menu shortcut)

🔍 WINDOWS-SPECIFIC NOTES
==========================

• Uses Windows batch files (.bat) instead of shell scripts
• Installs to %USERPROFILE%\AppData\Local\ (user-specific)
• Creates both Desktop and Start Menu shortcuts
• Uses PowerShell for model downloads
• Compatible with Windows Defender
• Works with both Command Prompt and PowerShell

===============================================================================
                        Enjoy creating amazing prompts! 🎨
===============================================================================

Version: Local-Only Edition (Windows)
Last Updated: August 2025