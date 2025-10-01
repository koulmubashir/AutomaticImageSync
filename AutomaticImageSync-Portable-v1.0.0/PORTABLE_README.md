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
