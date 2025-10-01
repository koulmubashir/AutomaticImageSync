#!/usr/bin/env python3
"""
Quick launcher for Automatic Image Sync
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['PIL', 'imagehash', 'cv2', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def main():
    """Main launcher function"""
    print("🖼️  Automatic Image Sync Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found in current directory")
        print("Please run this script from the AutomaticImageSync directory")
        sys.exit(1)
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"📦 Missing dependencies detected: {', '.join(missing)}")
        print("🔧 Running setup to install dependencies...")
        
        try:
            subprocess.check_call([sys.executable, "setup.py"])
        except subprocess.CalledProcessError:
            print("❌ Setup failed. Please install dependencies manually:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("✅ All dependencies are installed")
    
    # Launch the application
    print("🚀 Starting Automatic Image Sync...")
    try:
        subprocess.call([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

if __name__ == "__main__":
    main()
