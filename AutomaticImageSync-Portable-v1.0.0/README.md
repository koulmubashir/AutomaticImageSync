# Automatic Image Sync

A powerful GUI application for automatically organizing and synchronizing images from two folders. The application uses advanced image processing algorithms to detect similar images, create organized folders based on image content, and efficiently manage duplicate and unique images.

## Features

### 🚀 Fast Performance
- **Parallel Processing**: Multi-threaded image processing for maximum speed
- **Optimized Algorithms**: Uses efficient hashing algorithms for quick image comparison
- **Memory Efficient**: Processes images without loading entire datasets into memory

### 🔍 Smart Image Detection
- **Multiple Hash Algorithms**: Uses Average Hash, Perceptual Hash, Difference Hash, and Wavelet Hash
- **Exact Duplicate Detection**: Fast MD5 hash comparison for identical files
- **Similarity Threshold**: Adjustable threshold for fine-tuning similarity detection (default: 85%)
- **Robust Comparison**: Handles different formats, sizes, and minor variations

### 📁 Intelligent Organization
- **Context-Based Folders**: Creates folders based on image content and metadata
- **Similar Image Grouping**: Groups similar images into organized folders
- **Unique Image Handling**: Separates unique images into dedicated folder
- **Conflict Resolution**: Automatically handles filename conflicts

### 🖥️ User-Friendly GUI
- **Intuitive Interface**: Clean, modern GUI built with tkinter
- **Real-Time Progress**: Live progress bars and status updates
- **Detailed Results**: Comprehensive summary of operations performed
- **Error Handling**: Graceful error handling with user-friendly messages

### 🛡️ Safe Operations
- **Non-Destructive**: Moves files safely with backup considerations
- **Validation**: Comprehensive input validation before processing
- **Stop Functionality**: Ability to cancel operations mid-process
- **Error Recovery**: Continues processing even if individual files fail

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- GIF (.gif)
- WebP (.webp)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Setup
1. Clone or download this repository
2. Run the setup script:
   ```bash
   python setup.py
   ```

### Manual Installation
If you prefer to install dependencies manually:

```bash
pip install Pillow>=10.0.0
pip install imagehash>=4.3.1
pip install opencv-python>=4.8.0
pip install numpy>=1.24.0
```

## Usage

### Starting the Application
```bash
python main.py
```

### Step-by-Step Guide

1. **Select Input Folders**
   - Click "Browse" next to "Folder 1" to select your first image folder
   - Click "Browse" next to "Folder 2" to select your second image folder

2. **Choose Output Location**
   - Click "Browse" next to "Output Folder" to select where organized images will be saved
   - Note: Output folder must be different from input folders

3. **Adjust Settings (Optional)**
   - **Similarity Threshold**: Adjust the slider to control how similar images need to be to be grouped together
     - Lower values (0.5-0.7): More permissive, groups more images together
     - Higher values (0.8-0.99): More strict, only groups very similar images
     - Recommended: 0.85 for balanced results

4. **Start Processing**
   - Click "Start Synchronization" to begin
   - Monitor progress in real-time
   - Use "Stop" button to cancel if needed

### Output Structure

After processing, your output folder will contain:

```
Output Folder/
├── similar_[context1]/          # Group of similar images
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.png
├── similar_[context2]/          # Another group of similar images
│   ├── photo1.jpg
│   └── photo2.jpg
└── unique_images/               # Images with no similar matches
    ├── unique1.jpg
    ├── unique2.png
    └── unique3.jpg
```

## How It Works

### 1. Image Collection
- Recursively scans both input folders for supported image files
- Creates an inventory of all images to process

### 2. Hash Generation
The application generates multiple types of hashes for each image:
- **Average Hash**: Compares average pixel values
- **Perceptual Hash**: Uses DCT for perceptual similarity
- **Difference Hash**: Compares adjacent pixel differences  
- **Wavelet Hash**: Uses wavelet transform for robust comparison

### 3. Similarity Detection
- First checks for exact duplicates using MD5 file hashes (fastest)
- Then compares perceptual hashes for similar images
- Calculates similarity scores and groups images above threshold

### 4. Smart Grouping
- Creates groups of similar images
- Uses image metadata and filenames to generate meaningful folder names
- Handles edge cases like generic names or missing metadata

### 5. Safe File Operations
- Moves images to organized folders
- Handles filename conflicts automatically
- Preserves original file integrity

## Algorithm Details

### Similarity Calculation
The application uses a multi-hash approach for robust similarity detection:

1. **Exact Match**: MD5 hash comparison (100% accuracy for identical files)
2. **Perceptual Similarity**: Combines 4 different hash algorithms
3. **Threshold-Based Grouping**: Configurable similarity threshold
4. **Hamming Distance**: Measures bit differences between hashes

### Performance Optimizations
- **Parallel Processing**: Uses ThreadPoolExecutor for concurrent image processing
- **Early Termination**: Stops processing on exact hash matches
- **Memory Management**: Processes images individually to minimize memory usage
- **Progress Tracking**: Real-time progress updates without blocking UI

## Troubleshooting

### Common Issues

**"Import PIL could not be resolved"**
- Solution: Install Pillow: `pip install Pillow`

**"No images found in either folder"**
- Check that folders contain supported image formats
- Verify folder paths are correct
- Ensure you have read permissions for the folders

**"Error during synchronization"**
- Check available disk space in output folder
- Verify write permissions for output folder
- Ensure output folder is not the same as input folders

**Slow processing with large image collections**
- Processing time depends on number of images and their sizes
- Consider using a smaller subset for testing
- Ensure sufficient RAM is available

### Performance Tips

1. **Optimal Folder Structure**: Avoid deeply nested folders for better performance
2. **Disk Space**: Ensure output drive has sufficient space (same as combined input folders)
3. **RAM Usage**: Application uses approximately 100-200MB per 1000 images
4. **Threshold Tuning**: Higher thresholds (0.9+) process faster but may miss similar images

## Technical Specifications

### Dependencies
- **tkinter**: GUI framework (included with Python)
- **Pillow (PIL)**: Image processing library
- **imagehash**: Perceptual image hashing
- **opencv-python**: Computer vision library
- **numpy**: Numerical computing
- **pathlib**: Modern path handling
- **threading**: Concurrent processing
- **hashlib**: File hashing utilities

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum, 8GB recommended for large collections
- **Storage**: Free space equal to size of image collections being processed

## Contributing

### Development Setup
1. Fork the repository
2. Install development dependencies
3. Make your changes
4. Test thoroughly with different image types and sizes
5. Submit a pull request

### Code Structure
- `main.py`: GUI application and user interface
- `image_processor.py`: Core image processing and synchronization logic
- `setup.py`: Installation and setup script
- `requirements.txt`: Python package dependencies

## License

This project is released under the MIT License. See LICENSE file for details.

## Support

For issues, feature requests, or questions:
1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information about your problem

## Changelog

### Version 1.0
- Initial release
- Multi-threaded image processing
- GUI interface with progress tracking
- Support for multiple image formats
- Intelligent folder organization
- Configurable similarity threshold
