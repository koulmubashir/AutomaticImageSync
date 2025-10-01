#!/usr/bin/env python3
"""
Command-line version of Automatic Image Sync
For systems where GUI is not available
"""

import sys
import argparse
from pathlib import Path
from image_processor import ImageSynchronizer


def progress_callback(value, message=""):
    """Progress callback for command line"""
    bar_length = 40
    filled = int(bar_length * value / 100)
    bar = '█' * filled + '▒' * (bar_length - filled)
    print(f"\r[{bar}] {value:.1f}% - {message}", end='', flush=True)


def status_callback(message):
    """Status callback for command line"""
    print(f"\n📍 {message}")


def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(description='Automatic Image Synchronizer - Command Line')
    parser.add_argument('folder1', help='First image folder path')
    parser.add_argument('folder2', help='Second image folder path')
    parser.add_argument('output', help='Output folder path')
    parser.add_argument('--threshold', type=float, default=0.85,
                       help='Similarity threshold (0.0-1.0, default: 0.85)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    print("🖼️  Automatic Image Sync - Command Line")
    print("=" * 50)
    
    # Validate paths
    folder1 = Path(args.folder1)
    folder2 = Path(args.folder2)
    output = Path(args.output)
    
    if not folder1.exists():
        print(f"❌ Error: Folder 1 does not exist: {folder1}")
        sys.exit(1)
    
    if not folder2.exists():
        print(f"❌ Error: Folder 2 does not exist: {folder2}")
        sys.exit(1)
    
    if output == folder1 or output == folder2:
        print("❌ Error: Output folder must be different from input folders")
        sys.exit(1)
    
    print(f"📁 Folder 1: {folder1.absolute()}")
    print(f"📁 Folder 2: {folder2.absolute()}")
    print(f"📁 Output: {output.absolute()}")
    print(f"🎯 Similarity threshold: {args.threshold}")
    print()
    
    # Create synchronizer
    synchronizer = ImageSynchronizer(
        progress_callback=progress_callback,
        status_callback=status_callback
    )
    
    try:
        # Run synchronization
        print("🚀 Starting image synchronization...")
        stats = synchronizer.organize_images(folder1, folder2, output)
        
        print("\n" + "=" * 50)
        print("✅ SYNCHRONIZATION COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
        if "error" in stats:
            print(f"❌ Error: {stats.get('message', 'Unknown error')}")
            sys.exit(1)
        
        if "cancelled" in stats:
            print("⚠️  Synchronization was cancelled")
            sys.exit(0)
        
        # Display results
        print(f"\n📊 Results Summary:")
        print(f"  • Similar image groups created: {stats.get('similar_groups', 0)}")
        print(f"  • Unique images moved: {stats.get('unique_images', 0)}")
        print(f"  • Total images processed: {stats.get('total_processed', 0)}")
        print(f"  • Errors encountered: {stats.get('errors', 0)}")
        
        print(f"\n📁 Output structure:")
        print(f"  • Similar images: folders named 'similar_[context]'")
        print(f"  • Unique images: 'unique_images' folder")
        
        if stats.get('errors', 0) > 0:
            print(f"\n⚠️  {stats['errors']} errors occurred during processing")
        
        print(f"\n🎉 Image organization completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
