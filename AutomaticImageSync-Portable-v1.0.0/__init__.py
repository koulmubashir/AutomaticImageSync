"""
Automatic Image Sync Package
A powerful GUI application for automatically organizing and synchronizing images
"""

from .image_processor import ImageProcessor, ImageData, ImageSynchronizer
from .main import ImageSyncGUI

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Make main classes available at package level
__all__ = [
    "ImageProcessor",
    "ImageData", 
    "ImageSynchronizer",
    "ImageSyncGUI",
]
