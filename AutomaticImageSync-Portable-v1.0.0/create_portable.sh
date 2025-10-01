#!/bin/bash

# Create Portable ZIP Package for Automatic Image Sync
# This creates a self-contained package that can run anywhere

echo "📦 Creating Portable Package for Automatic Image Sync"
echo "===================================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from project directory."
    exit 1
fi

# Create portable directory structure
PACKAGE_NAME="AutomaticImageSync-Portable-v1.0.0"
mkdir -p "$PACKAGE_NAME"

# Copy source files
echo "📂 Copying source files..."
cp *.py "$PACKAGE_NAME/"
cp *.md "$PACKAGE_NAME/"
cp *.txt "$PACKAGE_NAME/"
cp *.sh "$PACKAGE_NAME/"
cp *.bat "$PACKAGE_NAME/"

# Create portable launcher scripts
echo "🚀 Creating launcher scripts..."

# Unix launcher
cat > "$PACKAGE_NAME/run.sh" << 'EOF'
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
EOF

# Windows launcher
cat > "$PACKAGE_NAME/run.bat" << 'EOF'
@echo off
echo Automatic Image Sync - Portable Edition
echo ========================================

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is required but not found.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Setup virtual environment if needed
if not exist "venv" (
    echo Setting up portable environment...
    python -m venv venv
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Start GUI
echo Starting GUI application...
python main.py

REM If GUI fails, show CLI help
if errorlevel 1 (
    echo.
    echo GUI failed to start. Use run_cli.bat for command line version.
    pause
)
EOF

# CLI launcher for Unix
cat > "$PACKAGE_NAME/run_cli.sh" << 'EOF'
#!/bin/bash
# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Setting up environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

python3 cli.py "$@"
EOF

# CLI launcher for Windows
cat > "$PACKAGE_NAME/run_cli.bat" << 'EOF'
@echo off
if not exist "venv" (
    echo Setting up environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

python cli.py %*
EOF

# Create test data
echo "🧪 Creating test data..."
cd "$PACKAGE_NAME"
python3 test_generator.py << 'EOF'
1
EOF
cd ..

# Create README for portable package
cat > "$PACKAGE_NAME/PORTABLE_README.md" << 'EOF'
# Automatic Image Sync - Portable Edition

This is a portable, self-contained version of Automatic Image Sync that can run on any system with Python 3.7+.

## Quick Start

### Windows:
1. Double-click `run.bat` to start the GUI
2. Or use `run_cli.bat folder1 folder2 output` for command line

### Mac/Linux:
1. Run `./run.sh` to start the GUI  
2. Or use `./run_cli.sh folder1 folder2 output` for command line

## First Run
The first time you run the application, it will:
1. Create a virtual environment (`venv/` folder)
2. Install required dependencies automatically
3. Launch the application

This may take a few minutes on first run but will be fast afterwards.

## Test with Sample Data
The package includes test images in `test_data/`:
- `test_data/folder1/` - First set of images
- `test_data/folder2/` - Second set of images

Try: `./run_cli.sh test_data/folder1 test_data/folder2 test_output`

## Requirements
- Python 3.7 or higher
- Internet connection (for first-time setup only)

## Sharing
You can share this entire folder with others. They just need Python installed.

## Troubleshooting
- If GUI doesn't work, use the CLI version (`run_cli.sh/bat`)
- Make sure you have Python 3.7+ installed
- On first run, make sure you have internet for package downloads

For detailed documentation, see README.md and QUICKSTART.md
EOF

# Make scripts executable
chmod +x "$PACKAGE_NAME"/*.sh

# Create ZIP package
echo "🗜️  Creating ZIP package..."
zip -r "${PACKAGE_NAME}.zip" "$PACKAGE_NAME/"

# Calculate sizes
FOLDER_SIZE=$(du -sh "$PACKAGE_NAME" | cut -f1)
ZIP_SIZE=$(du -sh "${PACKAGE_NAME}.zip" | cut -f1)

echo ""
echo "✅ Portable package created successfully!"
echo ""
echo "📊 Package Information:"
echo "  Folder size: $FOLDER_SIZE"
echo "  ZIP size: $ZIP_SIZE"
echo "  Contains: GUI + CLI + Documentation + Test Data"
echo ""
echo "📁 Created:"
echo "  📂 $PACKAGE_NAME/ - Portable folder"
echo "  📦 ${PACKAGE_NAME}.zip - Shareable ZIP file"
echo ""
echo "🚀 To test locally:"
echo "  cd $PACKAGE_NAME"
echo "  ./run.sh  (or run.bat on Windows)"
echo ""
echo "📤 To share with others:"
echo "  Send them the ${PACKAGE_NAME}.zip file"
echo "  They extract it and run run.sh/run.bat"
