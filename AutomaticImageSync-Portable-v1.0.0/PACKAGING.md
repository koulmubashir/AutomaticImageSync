# Packaging for Distribution

## Option 1: Python Package (PyPI)

### Build and Upload to PyPI
```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI (requires account)
python -m twine upload dist/*
```

### Install from PyPI
```bash
pip install automatic-image-sync
```

## Option 2: Standalone Executable (PyInstaller)

### Install PyInstaller
```bash
pip install pyinstaller
```

### Create Standalone Executable
```bash
# GUI version
pyinstaller --onefile --windowed --name "AutomaticImageSync" main.py

# CLI version  
pyinstaller --onefile --name "AutomaticImageSyncCLI" cli.py
```

### Create Cross-Platform Executables
```bash
# For current platform
./build_executable.sh

# The executable will be in dist/ folder
```

## Option 3: Docker Container

### Build Docker Image
```bash
docker build -t automatic-image-sync .
```

### Run with Docker
```bash
docker run -v /path/to/images:/app/images automatic-image-sync
```

## Option 4: Portable ZIP Package

### Create Portable Package
```bash
./create_portable.sh
```

This creates a self-contained ZIP file that can be extracted and run anywhere.

## Option 5: macOS App Bundle

### Create macOS .app
```bash
./build_macos_app.sh
```

Creates a native macOS application bundle.

## Option 6: Windows Installer

### Create Windows .msi Installer
```bash
# Requires WiX Toolset on Windows
./build_windows_installer.bat
```

## Recommended Distribution Methods

### For End Users:
1. **Standalone Executable** - Easiest for non-technical users
2. **Portable ZIP** - No installation required
3. **Platform-specific installers** - Native feel

### For Developers:
1. **PyPI Package** - Easy pip install
2. **GitHub Releases** - Source code + binaries
3. **Docker** - Consistent environment

### For Enterprise:
1. **Docker containers** - Scalable deployment
2. **MSI/DEB/RPM packages** - System integration
