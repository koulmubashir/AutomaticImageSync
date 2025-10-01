from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="automatic-image-sync",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A powerful GUI application for automatically organizing and synchronizing images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/automatic-image-sync",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: System :: Archiving",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "image-sync=main:main",
            "image-sync-cli=cli:main",
            "image-sync-gui=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.bat", "*.sh"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/automatic-image-sync/issues",
        "Source": "https://github.com/yourusername/automatic-image-sync",
        "Documentation": "https://github.com/yourusername/automatic-image-sync#readme",
    },
    keywords="image organization, duplicate detection, image sync, GUI, automation",
)
