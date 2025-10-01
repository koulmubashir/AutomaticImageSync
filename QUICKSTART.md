# Quick Start Guide - Automatic Image Sync

## Installation & Setup

### Option 1: Automatic Setup (Recommended)
```bash
# Download/clone the project
# Navigate to the project folder
cd AutomaticImageSync

# Run the setup script (installs dependencies and launches app)
python setup.py
```

### Option 2: Quick Launch Scripts
```bash
# For Unix/Linux/macOS:
./run.sh

# For Windows:
run.bat

# Cross-platform launcher:
python launch.py
```

### Option 3: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI version
python main.py

# Run command-line version
python cli.py folder1 folder2 output
```

## Basic Usage

### GUI Version (Recommended)
1. Run `python main.py`
2. Click "Browse" to select your two image folders
3. Choose an output folder for organized images
4. Adjust similarity threshold (0.85 recommended)
5. Click "Start Synchronization"
6. Monitor progress and view results

### Command-Line Version
```bash
# Basic usage
python cli.py /path/to/folder1 /path/to/folder2 /path/to/output

# With custom similarity threshold
python cli.py folder1 folder2 output --threshold 0.9

# Show help
python cli.py --help
```

## Testing the Application

### Create Test Data
```bash
# Generate sample images for testing
python test_generator.py
# Choose option 1 to create test data

# Test with command-line version
python cli.py test_data/folder1 test_data/folder2 test_data/output

# Clean up test data
python test_generator.py
# Choose option 2 to clean up
```

## Expected Output Structure

After processing, your output folder will contain:
```
output/
├── similar_nature/       # Similar nature images grouped together
│   ├── forest1.jpg
│   ├── trees2.png
│   └── landscape3.jpg
├── similar_sky/         # Similar sky images grouped together
│   ├── clouds1.jpg
│   └── blue_sky2.jpg
└── unique_images/       # No similar matches found
    ├── car.jpg
    ├── building.png
    └── person.jpg
```

## Troubleshooting

### "tkinter not available" Error
- **Solution**: Use the command-line version: `python cli.py`
- **Or install tkinter**: 
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - macOS: `brew install python-tk`
  - Windows: tkinter is usually included

### "Import PIL could not be resolved"
- **Solution**: Install Pillow: `pip install Pillow`
- **Or run**: `python setup.py`

### Slow Processing
- **Reduce similarity threshold** (0.7-0.8) for faster processing
- **Use smaller test datasets** initially
- **Ensure sufficient RAM** (4GB+ recommended)
- **Close other applications** during processing

### No Similar Images Found
- **Lower the similarity threshold** (try 0.7-0.8)
- **Check image formats** (only standard formats supported)
- **Verify images are actually similar** (test with duplicates first)

## Performance Tips

1. **Optimal Threshold Settings**:
   - 0.95-0.99: Only nearly identical images
   - 0.85-0.90: Similar images (recommended)
   - 0.70-0.80: More permissive grouping
   - 0.50-0.65: Very loose similarity

2. **Large Collections**:
   - Process in batches of 1000-2000 images
   - Ensure 8GB+ RAM for large datasets
   - Use SSD storage for better performance

3. **Quality vs Speed**:
   - Higher thresholds = faster processing
   - Lower thresholds = more thorough detection

## Features Summary

✅ **Smart Image Detection**: Multiple hash algorithms  
✅ **Fast Processing**: Multi-threaded operation  
✅ **Safe Operations**: Non-destructive file moving  
✅ **Flexible Interface**: GUI and command-line options  
✅ **Progress Tracking**: Real-time status updates  
✅ **Error Handling**: Graceful error recovery  
✅ **Test Support**: Built-in test data generator  

## Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)  
- BMP (.bmp)
- TIFF (.tiff, .tif)
- GIF (.gif)
- WebP (.webp)

## Need Help?
- Check the README.md for detailed documentation
- Run `python cli.py --help` for command options
- Use the test data generator to verify installation
- Ensure all dependencies are installed via `python setup.py`
