#!/bin/bash
echo "🖼️  Automatic Image Sync - Portable Edition"
echo "=========================================="

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Setting up portable environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check what to run
if command -v tkinter &> /dev/null || python3 -c "import tkinter" 2>/dev/null; then
    echo "🚀 Starting GUI application..."
    python3 main.py
else
    echo "⚠️  GUI not available, starting CLI help..."
    echo "Usage: ./run_cli.sh folder1 folder2 output"
    python3 cli.py --help
fi
