#!/bin/bash

# Build Standalone Executable for Automatic Image Sync
# This creates a single executable file that can be shared

echo "🔨 Building Standalone Executable for Automatic Image Sync"
echo "=========================================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from project directory."
    exit 1
fi

# Create virtual environment for building
echo "📦 Setting up build environment..."
python3 -m venv build_env
source build_env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Test that everything works
echo "🧪 Testing imports..."
python -c "from image_processor import ImageSynchronizer; print('✅ Core module works')"

# Build GUI executable
echo "🔨 Building GUI executable..."
pyinstaller --clean \
    --onefile \
    --windowed \
    --name "AutomaticImageSync" \
    --add-data "README.md:." \
    --add-data "QUICKSTART.md:." \
    --hidden-import "PIL._tkinter_finder" \
    --collect-all "cv2" \
    --collect-all "PIL" \
    --collect-all "imagehash" \
    main.py

# Build CLI executable
echo "🔨 Building CLI executable..."
pyinstaller --clean \
    --onefile \
    --name "AutomaticImageSyncCLI" \
    --add-data "README.md:." \
    --collect-all "cv2" \
    --collect-all "PIL" \
    --collect-all "imagehash" \
    cli.py

# Create distribution folder
echo "📁 Creating distribution package..."
mkdir -p release
cp dist/AutomaticImageSync release/
cp dist/AutomaticImageSyncCLI release/
cp README.md release/
cp QUICKSTART.md release/
cp requirements.txt release/

# Create test data for distribution
echo "🧪 Creating sample test data..."
source ../build_env/bin/activate
python test_generator.py << 'EOF'
1
EOF

# Copy test data to release
cp -r test_data release/sample_images

# Create usage instructions
cat > release/USAGE.txt << 'EOF'
Automatic Image Sync - Distribution Package
==========================================

This package contains:
- AutomaticImageSync: GUI application
- AutomaticImageSyncCLI: Command-line version
- sample_images/: Test data for trying the application
- Documentation files

Quick Start:
1. Double-click AutomaticImageSync to run the GUI
2. Or use command line: ./AutomaticImageSyncCLI folder1 folder2 output

Test with included sample data:
./AutomaticImageSyncCLI sample_images/folder1 sample_images/folder2 output

For detailed instructions, see README.md and QUICKSTART.md
EOF

# Create version info
echo "1.0.0" > release/VERSION
echo "$(date)" > release/BUILD_DATE

# Calculate sizes
echo "📊 Package Information:"
echo "  GUI Executable: $(du -h release/AutomaticImageSync | cut -f1)"
echo "  CLI Executable: $(du -h release/AutomaticImageSyncCLI | cut -f1)"
echo "  Total Package: $(du -sh release | cut -f1)"

# Cleanup
deactivate
rm -rf build_env build *.spec

echo ""
echo "✅ Build completed successfully!"
echo "📁 Distribution files are in: ./release/"
echo ""
echo "To test the executable:"
echo "  cd release"
echo "  ./AutomaticImageSync"
echo "  ./AutomaticImageSyncCLI sample_images/folder1 sample_images/folder2 test_output"
echo ""
echo "To create a ZIP for sharing:"
echo "  zip -r AutomaticImageSync-v1.0.0.zip release/"
