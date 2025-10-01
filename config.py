"""
Configuration file for Automatic Image Sync
Modify these settings to customize the application behavior
"""

# Image Processing Settings
IMAGE_PROCESSING = {
    # Hash size for perceptual hashing (higher = more accurate but slower)
    'HASH_SIZE': 16,
    
    # Maximum number of worker threads for parallel processing
    'MAX_WORKERS': 4,
    
    # Default similarity threshold (0.0 - 1.0)
    'DEFAULT_SIMILARITY_THRESHOLD': 0.85,
    
    # Supported image file extensions
    'SUPPORTED_FORMATS': {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp'},
    
    # Maximum file size to process (in MB, 0 = no limit)
    'MAX_FILE_SIZE_MB': 0,
}

# GUI Settings
GUI_SETTINGS = {
    # Window dimensions
    'WINDOW_WIDTH': 800,
    'WINDOW_HEIGHT': 600,
    
    # Enable/disable window resizing
    'RESIZABLE': True,
    
    # Progress update frequency (lower = more frequent updates)
    'PROGRESS_UPDATE_FREQUENCY': 100,
    
    # Theme settings (if available)
    'THEME': 'light',  # 'light', 'dark', or 'auto'
}

# File Operation Settings
FILE_OPERATIONS = {
    # How to handle filename conflicts
    'CONFLICT_RESOLUTION': 'append_number',  # 'append_number', 'skip', 'overwrite'
    
    # Create backup before moving files
    'CREATE_BACKUP': False,
    
    # Preserve original file timestamps
    'PRESERVE_TIMESTAMPS': True,
    
    # Verify file integrity after move
    'VERIFY_AFTER_MOVE': True,
}

# Logging Settings
LOGGING = {
    # Enable debug logging
    'DEBUG_MODE': False,
    
    # Log file location (None = no file logging)
    'LOG_FILE': None,  # e.g., 'image_sync.log'
    
    # Log level: 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    'LOG_LEVEL': 'INFO',
}

# Performance Settings
PERFORMANCE = {
    # Cache hash calculations to speed up repeated operations
    'ENABLE_HASH_CACHE': True,
    
    # Maximum memory usage for image processing (MB)
    'MAX_MEMORY_MB': 1024,
    
    # Batch size for processing large image collections
    'BATCH_SIZE': 100,
    
    # Enable memory optimization for large collections
    'MEMORY_OPTIMIZATION': True,
}

# Advanced Algorithm Settings
ALGORITHM_SETTINGS = {
    # Weight for different hash types in similarity calculation
    'HASH_WEIGHTS': {
        'ahash': 0.25,  # Average hash
        'phash': 0.30,  # Perceptual hash
        'dhash': 0.25,  # Difference hash
        'whash': 0.20,  # Wavelet hash
    },
    
    # Minimum number of hash matches required for similarity
    'MIN_HASH_MATCHES': 2,
    
    # Use exact file hash comparison first (much faster)
    'USE_EXACT_HASH_FIRST': True,
    
    # Enable enhanced similarity detection for rotated/flipped images
    'DETECT_TRANSFORMATIONS': False,
}

# Folder Organization Settings
ORGANIZATION = {
    # Maximum length for auto-generated folder names
    'MAX_FOLDER_NAME_LENGTH': 50,
    
    # Fallback folder name for images with no context
    'FALLBACK_FOLDER_NAME': 'unknown_context',
    
    # Prefix for similar image folders
    'SIMILAR_FOLDER_PREFIX': 'similar_',
    
    # Name for unique images folder
    'UNIQUE_FOLDER_NAME': 'unique_images',
    
    # Clean up folder names (remove special characters)
    'CLEAN_FOLDER_NAMES': True,
}
