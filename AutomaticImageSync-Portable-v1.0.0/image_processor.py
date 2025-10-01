import os
import hashlib
import shutil
from pathlib import Path
from PIL import Image
import imagehash
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Set
import threading


class ImageProcessor:
    """Fast image processing and comparison utilities"""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp'}
    HASH_SIZE = 16  # Increased for better accuracy
    
    @staticmethod
    def is_image_file(file_path: Path) -> bool:
        """Check if file is a supported image format"""
        return file_path.suffix.lower() in ImageProcessor.SUPPORTED_FORMATS
    
    @staticmethod
    def get_file_hash(file_path: Path) -> str:
        """Get MD5 hash of file for exact duplicate detection"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    @staticmethod
    def get_image_hashes(file_path: Path) -> Dict[str, str]:
        """Get multiple perceptual hashes for robust comparison"""
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                return {
                    'ahash': str(imagehash.average_hash(img, hash_size=ImageProcessor.HASH_SIZE)),
                    'phash': str(imagehash.phash(img, hash_size=ImageProcessor.HASH_SIZE)),
                    'dhash': str(imagehash.dhash(img, hash_size=ImageProcessor.HASH_SIZE)),
                    'whash': str(imagehash.whash(img, hash_size=ImageProcessor.HASH_SIZE))
                }
        except Exception:
            return {}
    
    @staticmethod
    def calculate_hash_similarity(hash1: str, hash2: str) -> float:
        """Calculate similarity between two hashes (0-1, where 1 is identical)"""
        try:
            # Convert hex strings to binary and calculate Hamming distance
            bin1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
            bin2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
            
            if len(bin1) != len(bin2):
                return 0.0
            
            differences = sum(c1 != c2 for c1, c2 in zip(bin1, bin2))
            similarity = 1.0 - (differences / len(bin1))
            return similarity
        except Exception:
            return 0.0
    
    @staticmethod
    def are_images_similar(hashes1: Dict[str, str], hashes2: Dict[str, str], threshold: float = 0.85) -> bool:
        """Compare two sets of image hashes to determine similarity"""
        if not hashes1 or not hashes2:
            return False
        
        similarities = []
        for hash_type in ['ahash', 'phash', 'dhash', 'whash']:
            if hash_type in hashes1 and hash_type in hashes2:
                sim = ImageProcessor.calculate_hash_similarity(hashes1[hash_type], hashes2[hash_type])
                similarities.append(sim)
        
        if not similarities:
            return False
        
        # Images are similar if average similarity exceeds threshold
        avg_similarity = sum(similarities) / len(similarities)
        return avg_similarity >= threshold
    
    @staticmethod
    def extract_image_context(file_path: Path) -> str:
        """Extract context from image for folder naming"""
        try:
            # Use file name as base context
            name = file_path.stem
            
            # Clean up the name for folder creation
            context = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            
            # If name is too generic or empty, use parent directory name
            if not context or len(context) < 3 or context.lower() in ['img', 'image', 'photo', 'pic']:
                context = file_path.parent.name
            
            return context[:50]  # Limit length for folder names
        except Exception:
            return "unknown"


class ImageData:
    """Container for image file information"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_hash = ""
        self.image_hashes = {}
        self.context = ""
        self.processed = False
    
    def process(self):
        """Process image to extract hashes and context"""
        if self.processed:
            return
        
        self.file_hash = ImageProcessor.get_file_hash(self.file_path)
        self.image_hashes = ImageProcessor.get_image_hashes(self.file_path)
        self.context = ImageProcessor.extract_image_context(self.file_path)
        self.processed = True


class ImageSynchronizer:
    """Main class for image synchronization and organization"""
    
    def __init__(self, progress_callback=None, status_callback=None):
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.stop_processing = threading.Event()
    
    def update_progress(self, value: float, message: str = ""):
        """Update progress callback"""
        if self.progress_callback:
            self.progress_callback(value, message)
    
    def update_status(self, message: str):
        """Update status callback"""
        if self.status_callback:
            self.status_callback(message)
    
    def stop(self):
        """Stop the synchronization process"""
        self.stop_processing.set()
    
    def collect_images(self, folder_path: Path) -> List[ImageData]:
        """Collect all image files from folder"""
        images = []
        if not folder_path.exists():
            return images
        
        for file_path in folder_path.rglob("*"):
            if self.stop_processing.is_set():
                break
            
            if file_path.is_file() and ImageProcessor.is_image_file(file_path):
                images.append(ImageData(file_path))
        
        return images
    
    def process_images_parallel(self, images: List[ImageData], max_workers: int = 4):
        """Process images in parallel for better performance"""
        total = len(images)
        processed = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_image = {executor.submit(img.process): img for img in images}
            
            for future in as_completed(future_to_image):
                if self.stop_processing.is_set():
                    break
                
                try:
                    future.result()
                    processed += 1
                    self.update_progress(processed / total * 50, f"Processing images... {processed}/{total}")
                except Exception as e:
                    print(f"Error processing image: {e}")
    
    def find_similar_groups(self, images1: List[ImageData], images2: List[ImageData]) -> Dict[str, List[ImageData]]:
        """Find groups of similar images"""
        self.update_status("Finding similar images...")
        
        all_images = images1 + images2
        groups = {}
        processed = 0
        total_comparisons = len(all_images) * (len(all_images) - 1) // 2
        
        for i, img1 in enumerate(all_images):
            if self.stop_processing.is_set():
                break
            
            for j, img2 in enumerate(all_images[i + 1:], i + 1):
                if self.stop_processing.is_set():
                    break
                
                # Check for exact duplicates first (much faster)
                if img1.file_hash and img2.file_hash and img1.file_hash == img2.file_hash:
                    similarity = True
                else:
                    # Check perceptual similarity
                    similarity = ImageProcessor.are_images_similar(img1.image_hashes, img2.image_hashes)
                
                if similarity:
                    # Find existing group or create new one
                    group_key = None
                    for key, group in groups.items():
                        if img1 in group or img2 in group:
                            group_key = key
                            break
                    
                    if group_key is None:
                        # Create new group using the first image's context
                        group_key = img1.context or img2.context or f"group_{len(groups) + 1}"
                        groups[group_key] = []
                    
                    # Add both images to group
                    if img1 not in groups[group_key]:
                        groups[group_key].append(img1)
                    if img2 not in groups[group_key]:
                        groups[group_key].append(img2)
                
                processed += 1
                if processed % 100 == 0:
                    progress = 50 + (processed / total_comparisons * 30)
                    self.update_progress(progress, f"Comparing images... {processed}/{total_comparisons}")
        
        return groups
    
    def organize_images(self, folder1: Path, folder2: Path, output_folder: Path) -> Dict[str, int]:
        """Main method to organize images"""
        self.update_status("Starting image organization...")
        
        # Create output folder
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Collect images
        self.update_status("Collecting images from folder 1...")
        images1 = self.collect_images(folder1)
        
        self.update_status("Collecting images from folder 2...")
        images2 = self.collect_images(folder2)
        
        if not images1 and not images2:
            return {"error": 1, "message": "No images found in either folder"}
        
        # Process images
        all_images = images1 + images2
        self.process_images_parallel(all_images)
        
        if self.stop_processing.is_set():
            return {"cancelled": 1}
        
        # Find similar groups
        similar_groups = self.find_similar_groups(images1, images2)
        
        # Track statistics
        stats = {
            "similar_groups": 0,
            "unique_images": 0,
            "total_processed": 0,
            "errors": 0
        }
        
        # Process similar groups
        grouped_images = set()
        for group_name, group_images in similar_groups.items():
            if self.stop_processing.is_set():
                break
            
            self.update_status(f"Creating folder for similar images: {group_name}")
            
            # Create folder for similar images
            safe_name = "".join(c for c in group_name if c.isalnum() or c in (' ', '-', '_')).strip()
            group_folder = output_folder / f"similar_{safe_name}"
            group_folder.mkdir(parents=True, exist_ok=True)
            
            # Move images to group folder
            for img in group_images:
                try:
                    dest_path = group_folder / img.file_path.name
                    # Handle name conflicts
                    counter = 1
                    while dest_path.exists():
                        stem = img.file_path.stem
                        suffix = img.file_path.suffix
                        dest_path = group_folder / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(img.file_path), str(dest_path))
                    grouped_images.add(img)
                    stats["total_processed"] += 1
                except Exception as e:
                    print(f"Error moving {img.file_path}: {e}")
                    stats["errors"] += 1
            
            stats["similar_groups"] += 1
        
        # Process unique images
        unique_images = [img for img in all_images if img not in grouped_images]
        
        if unique_images and not self.stop_processing.is_set():
            self.update_status("Moving unique images...")
            unique_folder = output_folder / "unique_images"
            unique_folder.mkdir(parents=True, exist_ok=True)
            
            for img in unique_images:
                try:
                    dest_path = unique_folder / img.file_path.name
                    # Handle name conflicts
                    counter = 1
                    while dest_path.exists():
                        stem = img.file_path.stem
                        suffix = img.file_path.suffix
                        dest_path = unique_folder / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(img.file_path), str(dest_path))
                    stats["unique_images"] += 1
                    stats["total_processed"] += 1
                except Exception as e:
                    print(f"Error moving {img.file_path}: {e}")
                    stats["errors"] += 1
        
        self.update_progress(100, "Organization complete!")
        self.update_status("Image organization completed successfully!")
        
        return stats
