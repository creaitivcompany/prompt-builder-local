Prompt Builder Local-Only Edition

A powerful, privacy-focused AI prompt builder that runs entirely on your local machine. Generate, analyze, and refine prompts for various AI image generators without sending any data to external APIs.





✨ Features
🖼️ Image Analysis

Upload images and generate detailed descriptive prompts

Powered by BLIP (Bootstrapping Language-Image Pre-training)

Extract visual elements, colors, composition, and style details

Perfect for reverse-engineering prompts from existing images


🎨 AI Generator Support

Midjourney - Optimized prompt formatting with parameters

DALL-E - Clean, descriptive prompt structure

Stable Diffusion - Technical prompt optimization

Leonardo AI - Creative prompt enhancement

Firefly - Adobe-specific formatting

And more - Easily extensible for new generators


🧠 Local LLM Integration

Refine and improve prompts using local language models

No internet connection required after setup

Supports GGUF model format (Phi-3, Llama, etc.)

Complete privacy - your prompts never leave your machine


🔒 Privacy First

100% Local Processing - No data sent to external servers

No API Keys Required - No subscriptions or usage limits

Offline Capable - Works without internet connection

Your Data Stays Yours - Complete control over your creative process


🚀 Quick Start

macOS Installation

Download PromptBuilder-Installer-Mac.zip

Extract and open Terminal in the folder

Run the installer:

chmod +x install_prompt_builder.sh
./install_prompt_builder.sh

Launch from Desktop shortcut or Applications folder


Windows Installation

Download PromptBuilder-Installer-Win.zip

Extract and open Command Prompt in the folder

Run the installer:

install_prompt_builder.bat

Launch from Desktop shortcut or Start Menu

💻 System Requirements
Minimum Requirements

macOS: 10.15+ or Windows: 10+

Python: 3.8 or later

RAM: 4GB (8GB recommended for LLM features)

Storage: 5GB free space (including AI model)

Internet: Required for initial setup only

Recommended Setup

RAM: 8GB+ for smooth LLM operation

Storage: SSD for faster model loading

CPU: Multi-core processor for better performance

📦 What's Included
Core Application

Prompt Builder GUI - Intuitive PyQt6 interface

Image Analysis Engine - BLIP model integration

AI Generator Configs - Pre-configured prompt templates

Local LLM Support - Offline prompt refinement

Installation Package

Automated Installer - One-click setup for both platforms

Dependency Management - Automatic Python package installation

Desktop Integration - Shortcuts and file associations

Comprehensive Documentation - Setup guides and troubleshooting

🎯 How It Works
Upload an Image (optional)

Drag and drop any image file

AI analyzes and describes the visual content

Generates base prompt from image analysis

Choose Your AI Generator

Select from supported platforms (Midjourney, DALL-E, etc.)

Prompt gets formatted for optimal results

Platform-specific parameters added automatically

Refine with Local LLM (optional)

Enhance prompt creativity and detail

Add artistic styles and technical parameters

All processing happens locally on your machine

Copy and Use

Get perfectly formatted prompts

Copy to clipboard with one click

Use in your favorite AI image generator

🛠️ Technical Details
Built With

Python 3.8+ - Core application language

PyQt6 - Modern cross-platform GUI framework

PyTorch - Deep learning framework for AI models

Transformers - Hugging Face model integration

Pillow - Image processing and manipulation

AI Models

BLIP-1 - Image captioning and analysis

Phi-3 Mini - Local language model (recommended)

Custom GGUF Models - Support for various local LLMs

Extensible Architecture - Easy to add new models

Architecture

Modular Design - Separate components for different functions

Plugin System - Easy to add new AI generators

Local Processing - No external API dependencies

Cross-Platform - Consistent experience on macOS and Windows

📁 Project Structure
prompt-builder-local/
├── mac-installer/              # macOS installation package
│   ├── install_prompt_builder.sh
│   ├── launch_prompt_builder.sh
│   └── README_INSTALLER.txt
├── windows-installer/          # Windows installation package
│   ├── install_prompt_builder.bat
│   ├── launch_prompt_builder.bat
│   └── README_INSTALLER_WINDOWS.txt
├── src/                       # Source code (shared between platforms)
│   ├── prompt_builder_qt_local_only.py
│   ├── layout_local_only.ui
│   ├── ai_generators.py
│   ├── generate_prompts_from_image.py
│   ├── blip1_m1_optimized.py
│   └── requirements_local_only.txt
└── docs/                      # Documentation and guides

🔧 Troubleshooting
Common Issues

Python Not Found

Install Python 3.8+ from python.org

Make sure "Add to PATH" is checked during installation

Dependencies Failed to Install

Run installer as Administrator (Windows) or with sudo (macOS)

Install manually: pip install -r requirements_local_only.txt --user

App Won't Start

Check all files are in the same directory

Run from terminal/command prompt to see error messages

Verify Python version: python --version

Model Issues

Ensure sufficient RAM (4GB+ free)

Download model manually if automatic download fails

Update model path in configuration file

Getting Help

Check the platform-specific README files in installer folders

Run the application from terminal to see detailed error messages

Ensure all dependencies are properly installed

🤝 Contributing

We welcome contributions! Here's how you can help:

Ways to Contribute

Bug Reports - Found an issue? Let us know!

Feature Requests - Ideas for new AI generators or features

Code Contributions - Submit pull requests for improvements

Documentation - Help improve guides and tutorials

Testing - Test on different systems and configurations

Development Setup

Clone the repository

Install development dependencies

Make your changes

Test on both macOS and Windows if possible

Submit a pull request

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

Hugging Face - For the Transformers library and model hosting

PyQt - For the excellent cross-platform GUI framework

BLIP Team - For the image captioning model

Microsoft - For the Phi-3 language model

Open Source Community - For the countless libraries that make this possible

📊 Roadmap
Version 1.1 (Planned)

Additional AI generator support (Flux, Ideogram)

Batch image processing

Prompt history and favorites

Custom prompt templates

Version 1.2 (Future)

Plugin system for custom generators

Advanced image analysis options

Prompt variation generation

Export/import functionality

📞 Support

Issues: GitHub Issues

Discussions: GitHub Discussions

Documentation: Check the installer README files for detailed setup instructions

Made with ❤️ for the AI art community

Keep your creative process private and powerful with local AI processing.
