#!/bin/bash

# GitHub Setup Script for Automatic Image Sync
# This script helps you push your project to GitHub

echo "🚀 GitHub Setup for Automatic Image Sync"
echo "========================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   Download from: https://git-scm.com/"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from project directory."
    exit 1
fi

echo "✅ Found project files"

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📁 Adding files to Git..."
git add .

# Create initial commit if no commits exist
if ! git log --oneline -1 &>/dev/null; then
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit: Automatic Image Sync v1.0.0

Features:
- GUI and CLI interfaces
- Multi-threaded image processing
- Smart similarity detection using multiple hash algorithms
- Intelligent folder organization
- Cross-platform support (Windows, macOS, Linux)
- Portable package distribution
- Complete documentation and tests"
    echo "✅ Initial commit created"
else
    echo "✅ Repository already has commits"
fi

# Check for GitHub CLI
if command -v gh &> /dev/null; then
    echo ""
    echo "🌟 GitHub CLI detected! Would you like to create a repository automatically?"
    read -p "Enter repository name (or press Enter for 'automatic-image-sync'): " repo_name
    
    if [ -z "$repo_name" ]; then
        repo_name="automatic-image-sync"
    fi
    
    echo "📡 Creating GitHub repository: $repo_name"
    
    # Create repository
    gh repo create "$repo_name" --public --description "A powerful GUI application for automatically organizing and synchronizing images" --clone=false
    
    # Add remote
    git remote add origin "https://github.com/$(gh api user --jq .login)/$repo_name.git"
    
    # Push to GitHub
    echo "🚀 Pushing to GitHub..."
    git branch -M main
    git push -u origin main
    
    echo ""
    echo "🎉 SUCCESS! Your repository is now on GitHub!"
    echo "🔗 Repository URL: https://github.com/$(gh api user --jq .login)/$repo_name"
    echo ""
    
else
    echo ""
    echo "📝 Manual GitHub Setup Instructions"
    echo "=================================="
    echo ""
    echo "1. Go to GitHub.com and create a new repository"
    echo "   - Repository name: automatic-image-sync (or your preferred name)"
    echo "   - Description: A powerful GUI application for automatically organizing and synchronizing images"
    echo "   - Make it Public (recommended for open source)"
    echo "   - Don't initialize with README (we already have one)"
    echo ""
    echo "2. After creating the repository, run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOURUSERNAME/YOURREPOSITORY.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "3. Replace YOURUSERNAME and YOURREPOSITORY with your actual values"
    echo ""
fi

# Show status
echo ""
echo "📊 Repository Status:"
echo "===================="
git status --short
echo ""
echo "📈 Commit History:"
git log --oneline -5

echo ""
echo "📋 Next Steps:"
echo "=============="
echo "1. ✅ Code is ready for GitHub"
echo "2. 🔗 Push to your GitHub repository (see instructions above)"
echo "3. 🏷️  Create your first release:"
echo "   - Go to your repository on GitHub"
echo "   - Click 'Releases' → 'Create a new release'"
echo "   - Tag: v1.0.0"
echo "   - Title: Automatic Image Sync v1.0.0"
echo "   - Upload: AutomaticImageSync-Portable-v1.0.0.zip"
echo "4. 📝 Update README_GITHUB.md with your actual repository URLs"
echo "5. 🌟 Share your project with the world!"

echo ""
echo "💡 Pro Tips:"
echo "- Add screenshots to docs/images/ folder"
echo "- Update README_GITHUB.md with your GitHub username"
echo "- Consider adding GitHub Pages for documentation"
echo "- Enable GitHub Actions for automatic builds"

echo ""
echo "🎯 Files ready for GitHub:"
echo "========================="
echo "✅ Source code (main.py, cli.py, image_processor.py, etc.)"
echo "✅ Documentation (README.md, QUICKSTART.md, CONTRIBUTING.md)"
echo "✅ Distribution (portable ZIP package)"
echo "✅ Configuration (.gitignore, GitHub Actions)"
echo "✅ Legal (LICENSE)"

if [ -f "AutomaticImageSync-Portable-v1.0.0.zip" ]; then
    echo "✅ Portable package ready for release upload"
fi

echo ""
echo "🚀 Your project is ready for GitHub! Good luck! 🌟"
