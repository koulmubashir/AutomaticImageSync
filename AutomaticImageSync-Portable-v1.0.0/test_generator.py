#!/usr/bin/env python3
"""
Test script for Automatic Image Sync
Creates sample images for testing the application
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def create_test_image(path, size=(800, 600), color=None, text=""):
    """Create a test image with specified properties"""
    if color is None:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Create image
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # Add some patterns
    for i in range(0, size[0], 50):
        draw.line([(i, 0), (i, size[1])], fill=(255, 255, 255), width=1)
    
    for i in range(0, size[1], 50):
        draw.line([(0, i), (size[0], i)], fill=(255, 255, 255), width=1)
    
    # Add text if provided
    if text:
        try:
            font_size = min(size) // 10
            # Try to use a default font
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position (center)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            
            # Add text with background
            draw.rectangle([x-10, y-10, x+text_width+10, y+text_height+10], 
                         fill=(0, 0, 0, 128))
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
        except Exception as e:
            print(f"Could not add text to image: {e}")
    
    # Save image
    img.save(path, 'JPEG', quality=95)

def create_test_folders():
    """Create test folders with sample images"""
    base_path = Path("test_data")
    
    # Remove existing test data
    if base_path.exists():
        shutil.rmtree(base_path)
    
    # Create folder structure
    folder1 = base_path / "folder1"
    folder2 = base_path / "folder2"
    output = base_path / "output"
    
    folder1.mkdir(parents=True, exist_ok=True)
    folder2.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    
    print("Creating test images...")
    
    # Create similar images (should be grouped together)
    # Group 1: Nature photos
    colors = [(34, 139, 34), (0, 128, 0), (50, 205, 50)]  # Green variations
    for i, color in enumerate(colors, 1):
        create_test_image(folder1 / f"nature_{i}.jpg", 
                         size=(800, 600), color=color, text=f"Nature {i}")
        # Create similar version in folder2
        create_test_image(folder2 / f"forest_{i}.jpg", 
                         size=(800, 600), color=color, text=f"Forest {i}")
    
    # Group 2: Sky photos  
    colors = [(135, 206, 235), (0, 191, 255), (30, 144, 255)]  # Blue variations
    for i, color in enumerate(colors, 1):
        create_test_image(folder1 / f"sky_{i}.jpg", 
                         size=(800, 600), color=color, text=f"Sky {i}")
        create_test_image(folder2 / f"cloud_{i}.jpg", 
                         size=(800, 600), color=color, text=f"Cloud {i}")
    
    # Create unique images (should go to unique folder)
    # Unique in folder1
    create_test_image(folder1 / "sunset.jpg", 
                     size=(800, 600), color=(255, 165, 0), text="Sunset")
    create_test_image(folder1 / "ocean.jpg", 
                     size=(800, 600), color=(0, 100, 200), text="Ocean")
    
    # Unique in folder2
    create_test_image(folder2 / "mountain.jpg", 
                     size=(800, 600), color=(139, 69, 19), text="Mountain")
    create_test_image(folder2 / "city.jpg", 
                     size=(800, 600), color=(128, 128, 128), text="City")
    
    # Create exact duplicates (should be detected as identical)
    duplicate_img = folder1 / "duplicate_original.jpg"
    create_test_image(duplicate_img, size=(800, 600), color=(255, 0, 0), text="Duplicate")
    shutil.copy2(duplicate_img, folder2 / "duplicate_copy.jpg")
    
    print(f"✅ Test data created successfully!")
    print(f"📁 Folder 1: {folder1.absolute()} ({len(list(folder1.glob('*.jpg')))} images)")
    print(f"📁 Folder 2: {folder2.absolute()} ({len(list(folder2.glob('*.jpg')))} images)")
    print(f"📁 Output folder: {output.absolute()}")
    print("\nTest images include:")
    print("  • Similar nature/forest images (should be grouped)")
    print("  • Similar sky/cloud images (should be grouped)")
    print("  • Unique images (should go to unique folder)")
    print("  • Exact duplicate (should be detected)")
    print("\nYou can now use these folders to test the application!")

def cleanup_test_data():
    """Remove test data"""
    base_path = Path("test_data")
    if base_path.exists():
        shutil.rmtree(base_path)
        print("Test data cleaned up successfully!")
    else:
        print("No test data found to clean up.")

def main():
    """Main function"""
    print("🧪 Automatic Image Sync - Test Data Generator")
    print("=" * 50)
    
    try:
        choice = input("Choose an option:\n1. Create test data\n2. Clean up test data\nEnter choice (1-2): ").strip()
        
        if choice == "1":
            create_test_folders()
        elif choice == "2":
            cleanup_test_data()
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
