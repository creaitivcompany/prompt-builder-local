===============================================================================
                    PROMPT BUILDER LOCAL-ONLY - INSTALLATION GUIDE
===============================================================================

🚀 QUICK INSTALL
================

1. Download the installer package and extract it
2. Open Terminal and navigate to the extracted folder
3. Run the installer:
   
   chmod +x install_prompt_builder.sh
   ./install_prompt_builder.sh

4. Follow the prompts - the installer will:
   • Install all Python dependencies
   • Set up the application in ~/Applications/PromptBuilder/
   • Create desktop shortcuts
   • Optionally download the AI model

📦 WHAT GETS INSTALLED
======================

• Application files in ~/Applications/PromptBuilder/
• Python dependencies (PyQt6, PyTorch, Transformers, etc.)
• Desktop shortcut for easy access
• AI model (optional, ~2.4GB)

🎯 RUNNING THE APP
==================

After installation, you can run the app by:
• Double-clicking "Prompt Builder.command" on your Desktop
• Or from Applications folder
• Or running: ~/Applications/PromptBuilder/launch_prompt_builder.sh

💻 SYSTEM REQUIREMENTS
======================

• macOS (tested on macOS 10.15+)
• Python 3.8+ (install from python.org if needed)
• 4GB+ RAM (8GB recommended for AI model)
• 5GB free disk space (for app + model)

✨ FEATURES
===========

• Image Analysis - Upload images and generate descriptive prompts
• AI Generator Support - Format prompts for Midjourney, DALL-E, Stable Diffusion, etc.
• Local Prompt Refiner - Improve prompts using local AI (no internet required)
• No API Keys - Everything runs locally on your Mac

🔧 TROUBLESHOOTING
==================

Python Issues:
--------------
If you get Python errors:

# Install Python 3 from python.org, then:
pip3 install --upgrade pip
pip3 install -r ~/Applications/PromptBuilder/requirements_local_only.txt --user

Model Issues:
-------------
If the prompt refiner doesn't work:
1. Check that the model file exists in ~/Applications/PromptBuilder/models/
2. Update the model path in prompt_builder_qt_local_only.py
3. Make sure you have enough RAM (4GB+ free)

Permission Issues:
------------------
If you get permission errors:

chmod +x ~/Applications/PromptBuilder/launch_prompt_builder.sh

App Won't Start:
----------------
1. Make sure Python 3.8+ is installed
2. Check that all files are in the same directory
3. Try running from Terminal to see error messages:
   cd ~/Applications/PromptBuilder
   python3 prompt_builder_qt_local_only.py

🗑️ UNINSTALLING
================

To remove the application:
1. Delete ~/Applications/PromptBuilder/ folder
2. Delete shortcuts from Desktop and Applications folder
3. Optionally remove Python packages:
   pip3 uninstall PyQt6 torch transformers

📋 INSTALLATION CHECKLIST
==========================

Before installing:
□ macOS 10.15 or later
□ At least 5GB free disk space
□ Python 3.8+ installed (check with: python3 --version)

After installing:
□ Desktop shortcut created
□ App launches without errors
□ Image upload works
□ Prompt generation works
□ Model downloaded (if selected)

🆘 SUPPORT
==========

For issues or questions:
• Check the troubleshooting section above
• Ensure all files are in the same directory
• Verify Python 3.8+ is installed
• Make sure you have sufficient disk space and RAM

Common Solutions:
• Restart Terminal after Python installation
• Use "python3" instead of "python" command
• Install Xcode Command Line Tools if prompted
• Check file permissions with "ls -la"

📁 FILE STRUCTURE AFTER INSTALLATION
====================================

~/Applications/PromptBuilder/
├── prompt_builder_qt_local_only.py    (Main application)
├── layout_local_only.ui               (User interface)
├── ai_generators.py                   (AI generator configs)
├── generate_prompts_from_image.py     (Image analysis)
├── blip1_m1_optimized.py             (BLIP model)
├── requirements_local_only.txt        (Dependencies)
├── launch_prompt_builder.sh           (Launcher script)
├── PromptGen.png                      (Logo, if included)
└── models/
    └── phi-3-mini-4k-instruct-q4.gguf (AI model, if downloaded)

Desktop:
└── Prompt Builder.command             (Desktop shortcut)

===============================================================================
                        Enjoy creating amazing prompts! 🎨
===============================================================================

Version: Local-Only Edition
Last Updated: August 2025