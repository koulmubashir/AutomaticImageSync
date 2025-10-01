# Contributing to Automatic Image Sync

Thank you for your interest in contributing to Automatic Image Sync! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

- **🐛 Bug Reports**: Found a bug? Please report it!
- **✨ Feature Requests**: Have an idea for a new feature?
- **📝 Documentation**: Help improve our docs
- **🔧 Code Contributions**: Submit bug fixes or new features
- **🧪 Testing**: Help test new features and releases

### Getting Started

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   git clone https://github.com/yourusername/automatic-image-sync.git
   cd automatic-image-sync
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv dev_env
   source dev_env/bin/activate  # On Windows: dev_env\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r dev-requirements.txt
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🐛 Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the bug
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, package versions
- **Screenshots**: If applicable
- **Sample Data**: Test images that trigger the bug (if safe to share)

### Bug Report Template

```markdown
**Bug Description**
A clear and concise description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment**
- OS: [e.g. macOS 12.0, Windows 11, Ubuntu 20.04]
- Python Version: [e.g. 3.9.7]
- Package Version: [e.g. 1.0.0]

**Additional Context**
Add any other context about the problem here.
```

## ✨ Feature Requests

When suggesting new features:

- **Use Case**: Explain why this feature would be useful
- **Description**: Detailed description of the proposed feature
- **Implementation Ideas**: If you have thoughts on how to implement it
- **Alternatives**: Any alternative solutions you've considered

## 🔧 Code Contributions

### Development Guidelines

1. **Code Style**
   - Follow PEP 8 style guidelines
   - Use meaningful variable and function names
   - Add docstrings to functions and classes
   - Keep lines under 100 characters

2. **Testing**
   - Add tests for new features
   - Ensure existing tests pass
   - Test on multiple platforms if possible

3. **Documentation**
   - Update documentation for new features
   - Add comments for complex logic
   - Update README if needed

### Code Structure

```
automatic-image-sync/
├── main.py              # GUI application
├── cli.py               # Command-line interface
├── image_processor.py   # Core image processing logic
├── config.py           # Configuration settings
├── tests/              # Test files
│   ├── test_processor.py
│   └── test_cli.py
├── docs/               # Documentation
└── examples/           # Example scripts
```

### Pull Request Process

1. **Before submitting**:
   - Ensure your code follows the style guidelines
   - Run tests and ensure they pass
   - Update documentation if needed
   - Test on your local environment

2. **Pull Request Description**:
   - Clearly describe what your PR does
   - Reference any related issues
   - Include screenshots for UI changes
   - List any breaking changes

3. **Review Process**:
   - Maintainers will review your PR
   - Address any feedback or requested changes
   - Once approved, your PR will be merged

### Pull Request Template

```markdown
**Description**
Brief description of changes made.

**Type of Change**
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

**Testing**
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

**Checklist**
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings

**Related Issues**
Fixes #(issue number)
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_processor.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Test both success and failure cases
- Include edge cases

Example test:
```python
def test_image_similarity_detection():
    """Test that similar images are correctly identified"""
    # Create test images
    img1 = create_test_image(color=(255, 0, 0))
    img2 = create_test_image(color=(255, 10, 10))  # Similar red
    
    # Process images
    processor = ImageProcessor()
    hash1 = processor.get_image_hashes(img1)
    hash2 = processor.get_image_hashes(img2)
    
    # Assert similarity
    assert processor.are_images_similar(hash1, hash2, threshold=0.8)
```

## 📝 Documentation

### Documentation Guidelines

- Use clear, concise language
- Include code examples where helpful
- Update documentation when making changes
- Use proper Markdown formatting

### Types of Documentation

- **User Documentation**: How to use the application
- **Developer Documentation**: How the code works
- **API Documentation**: Function and class references
- **Tutorials**: Step-by-step guides

## 🔄 Development Workflow

### Typical Workflow

1. **Check existing issues** - Avoid duplicate work
2. **Create/comment on issue** - Discuss your plans
3. **Fork and clone** - Get a local copy
4. **Create feature branch** - Keep changes isolated
5. **Make changes** - Implement your feature/fix
6. **Test thoroughly** - Ensure everything works
7. **Update documentation** - Keep docs current
8. **Submit pull request** - Get your changes reviewed
9. **Address feedback** - Make requested changes
10. **Merge!** - Your contribution is now part of the project

### Git Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add support for WebP image format"
git commit -m "Fix memory leak in image processing"
git commit -m "Update installation instructions for macOS"

# Less good
git commit -m "Fix bug"
git commit -m "Update stuff"
git commit -m "WIP"
```

## 🎯 Priority Areas

We especially welcome contributions in these areas:

- **Performance Optimization**: Make image processing faster
- **New Image Formats**: Add support for more formats
- **UI/UX Improvements**: Make the interface more user-friendly
- **Cross-Platform Testing**: Ensure compatibility
- **Documentation**: Improve guides and examples
- **Accessibility**: Make the app more accessible
- **Internationalization**: Add support for multiple languages

## 📞 Getting Help

If you need help with contributing:

- **GitHub Discussions**: Ask questions and discuss ideas
- **GitHub Issues**: Report bugs or request features
- **Email**: Contact maintainers directly

## 🏆 Recognition

Contributors are recognized in:

- **README**: Listed in acknowledgments
- **Releases**: Mentioned in release notes
- **Contributors Page**: GitHub contributors list

## 📋 Development Environment

### Recommended Tools

- **IDE**: VS Code, PyCharm, or your preferred editor
- **Git Client**: Command line or GUI client
- **Python Version Manager**: pyenv or conda
- **Testing**: pytest
- **Linting**: flake8, black
- **Documentation**: Sphinx (for API docs)

### Environment Setup Script

```bash
#!/bin/bash
# setup_dev.sh - Quick development setup

echo "Setting up Automatic Image Sync development environment..."

# Create virtual environment
python -m venv dev_env
source dev_env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 sphinx

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install

echo "Development environment ready!"
echo "Activate with: source dev_env/bin/activate"
```

## 🚀 Release Process

For maintainers:

1. **Update version** in `__init__.py` and `setup_package.py`
2. **Update CHANGELOG** with new features and fixes
3. **Create release tag**: `git tag v1.x.x`
4. **Push tag**: `git push origin v1.x.x`
5. **GitHub Actions** will automatically build and release

Thank you for contributing to Automatic Image Sync! 🎉
