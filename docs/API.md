# API Documentation

## Core Classes

### ImageProcessor

Static utility class for image processing operations.

#### Methods

##### `is_image_file(file_path: Path) -> bool`
Check if a file is a supported image format.

**Parameters:**
- `file_path`: Path to the file to check

**Returns:**
- `bool`: True if file is a supported image format

**Example:**
```python
from pathlib import Path
from image_processor import ImageProcessor

if ImageProcessor.is_image_file(Path("photo.jpg")):
    print("This is an image file")
```

##### `get_file_hash(file_path: Path) -> str`
Get MD5 hash of file for exact duplicate detection.

**Parameters:**
- `file_path`: Path to the file

**Returns:**
- `str`: MD5 hash of the file

##### `get_image_hashes(file_path: Path) -> Dict[str, str]`
Get multiple perceptual hashes for robust comparison.

**Parameters:**
- `file_path`: Path to the image file

**Returns:**
- `Dict[str, str]`: Dictionary containing different hash types:
  - `ahash`: Average hash
  - `phash`: Perceptual hash
  - `dhash`: Difference hash
  - `whash`: Wavelet hash

**Example:**
```python
hashes = ImageProcessor.get_image_hashes(Path("image.jpg"))
print(f"Perceptual hash: {hashes['phash']}")
```

##### `are_images_similar(hashes1: Dict[str, str], hashes2: Dict[str, str], threshold: float = 0.85) -> bool`
Compare two sets of image hashes to determine similarity.

**Parameters:**
- `hashes1`: First image's hash dictionary
- `hashes2`: Second image's hash dictionary  
- `threshold`: Similarity threshold (0.0-1.0)

**Returns:**
- `bool`: True if images are similar above threshold

### ImageData

Container class for image file information.

#### Attributes
- `file_path`: Path to the image file
- `file_hash`: MD5 hash of the file
- `image_hashes`: Dictionary of perceptual hashes
- `context`: Extracted context for folder naming
- `processed`: Whether the image has been processed

#### Methods

##### `process()`
Process image to extract hashes and context.

**Example:**
```python
img_data = ImageData(Path("photo.jpg"))
img_data.process()
print(f"Context: {img_data.context}")
```

### ImageSynchronizer

Main class for image synchronization and organization.

#### Constructor

```python
ImageSynchronizer(progress_callback=None, status_callback=None)
```

**Parameters:**
- `progress_callback`: Function called with progress updates (value, message)
- `status_callback`: Function called with status updates (message)

#### Methods

##### `organize_images(folder1: Path, folder2: Path, output_folder: Path) -> Dict[str, int]`
Main method to organize images from two folders.

**Parameters:**
- `folder1`: First image folder
- `folder2`: Second image folder
- `output_folder`: Destination for organized images

**Returns:**
- `Dict[str, int]`: Statistics dictionary with keys:
  - `similar_groups`: Number of similar groups created
  - `unique_images`: Number of unique images moved
  - `total_processed`: Total images processed
  - `errors`: Number of errors encountered

**Example:**
```python
def progress_update(value, message):
    print(f"Progress: {value}% - {message}")

def status_update(message):
    print(f"Status: {message}")

sync = ImageSynchronizer(progress_update, status_update)
stats = sync.organize_images(
    Path("folder1"), 
    Path("folder2"), 
    Path("output")
)
print(f"Created {stats['similar_groups']} groups")
```

##### `stop()`
Stop the synchronization process.

## GUI Classes

### ImageSyncGUI

Main GUI application class built with tkinter.

#### Constructor

```python
ImageSyncGUI()
```

Initializes the GUI application with all necessary components.

#### Methods

##### `run()`
Start the GUI application main loop.

**Example:**
```python
app = ImageSyncGUI()
app.run()
```

## Configuration

### Modifying Settings

Settings can be modified in `config.py`:

```python
from config import IMAGE_PROCESSING

# Modify hash size for better accuracy
IMAGE_PROCESSING['HASH_SIZE'] = 32

# Adjust number of worker threads
IMAGE_PROCESSING['MAX_WORKERS'] = 8
```

### Available Settings

See `config.py` for complete configuration options:

- **IMAGE_PROCESSING**: Core processing settings
- **GUI_SETTINGS**: GUI appearance and behavior
- **FILE_OPERATIONS**: File handling options
- **PERFORMANCE**: Performance optimization settings

## Command Line Interface

### CLI Module

The command line interface is implemented in `cli.py`.

#### Usage

```bash
python cli.py folder1 folder2 output [options]
```

#### Options

- `--threshold FLOAT`: Similarity threshold (default: 0.85)
- `--verbose`: Enable verbose output
- `--help`: Show help message

#### Example

```bash
# Basic usage
python cli.py /path/to/folder1 /path/to/folder2 /path/to/output

# With custom threshold
python cli.py folder1 folder2 output --threshold 0.9 --verbose
```

## Error Handling

### Common Exceptions

The application handles these common exceptions gracefully:

- `FileNotFoundError`: Missing input folders
- `PermissionError`: Insufficient file permissions
- `IOError`: File read/write errors
- `MemoryError`: Insufficient memory for large operations

### Error Recovery

- Failed file operations are logged but don't stop processing
- Memory errors trigger garbage collection and retry
- Network timeouts are handled with retries

## Performance Considerations

### Memory Usage

- Memory usage scales with number of images processed simultaneously
- Configure `MAX_WORKERS` based on available RAM
- Large images (>50MB) use more memory for hash calculation

### Processing Speed

- Multi-threading provides significant speed improvements
- SSD storage is recommended for large collections
- Network drives may be slower due to latency

### Optimization Tips

1. **Adjust worker threads**: More threads for CPU-bound tasks
2. **Increase hash size**: Better accuracy but slower processing
3. **Use SSD storage**: Faster file I/O operations
4. **Sufficient RAM**: Prevents swapping during processing

## Integration Examples

### Using as a Library

```python
from image_processor import ImageSynchronizer
from pathlib import Path

# Create synchronizer
sync = ImageSynchronizer()

# Process images
stats = sync.organize_images(
    Path("input1"),
    Path("input2"), 
    Path("output")
)

print(f"Processed {stats['total_processed']} images")
```

### Custom Progress Tracking

```python
import tkinter as tk
from tkinter import ttk

def create_progress_window():
    root = tk.Tk()
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var)
    progress_bar.pack()
    
    def update_progress(value, message):
        progress_var.set(value)
        root.update_idletasks()
    
    return update_progress, root

progress_callback, window = create_progress_window()
sync = ImageSynchronizer(progress_callback=progress_callback)
```

### Batch Processing

```python
import os
from pathlib import Path

def process_multiple_folders(base_folder, output_base):
    """Process multiple folder pairs"""
    folders = list(Path(base_folder).iterdir())
    
    for i, folder1 in enumerate(folders):
        for folder2 in folders[i+1:]:
            if folder1.is_dir() and folder2.is_dir():
                output = Path(output_base) / f"{folder1.name}_vs_{folder2.name}"
                
                sync = ImageSynchronizer()
                stats = sync.organize_images(folder1, folder2, output)
                
                print(f"Processed {folder1.name} vs {folder2.name}: "
                      f"{stats['similar_groups']} groups")
```
