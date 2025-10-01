#!/bin/bash

# Automatic Image Sync - Unix Launcher
echo "🖼️  Automatic Image Sync - Unix Launcher"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found in current directory"
    echo "Please run this script from the AutomaticImageSync directory"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $python_version detected, but Python $required_version or higher is required"
    exit 1
fi

echo "✅ Python $python_version detected"

# Try to launch the application
echo "🚀 Starting Automatic Image Sync..."
python3 main.py

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  There was an error starting the application."
    echo "🔧 Attempting to install dependencies..."
    python3 setup.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Dependencies installed. Please try running the application again:"
        echo "   ./run.sh  or  python3 main.py"
    else
        echo "❌ Failed to install dependencies. Please install manually:"
        echo "   pip3 install -r requirements.txt"
    fi
fi
