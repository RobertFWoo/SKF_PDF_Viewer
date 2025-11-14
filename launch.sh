#!/bin/bash
# SKF PDF Viewer Launcher Script

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
fi

# Launch the PDF viewer
echo "Starting SKF PDF Viewer..."
python3 pdf_viewer.py "$@"
