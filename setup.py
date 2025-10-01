#!/usr/bin/env python3
"""
Setup script for Automatic Image Sync
Installs required dependencies and runs the application
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    
    packages = [
        "Pillow>=10.0.0",
        "imagehash>=4.3.1", 
        "opencv-python>=4.8.0",
        "numpy>=1.24.0"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            return False
    
    print("All packages installed successfully!")
    return True

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        return False
    return True

def main():
    """Main setup function"""
    print("="*50)
    print("Automatic Image Sync - Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print(f"Python {sys.version} detected - OK")
    
    # Install requirements
    if not install_requirements():
        print("Setup failed due to package installation errors")
        sys.exit(1)
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    print("python main.py")
    
    # Ask if user wants to run the application now
    try:
        response = input("\nWould you like to run the application now? (y/n): ").lower()
        if response in ['y', 'yes']:
            print("\nStarting Automatic Image Sync...")
            subprocess.call([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nSetup completed. Run 'python main.py' to start the application.")

if __name__ == "__main__":
    main()
