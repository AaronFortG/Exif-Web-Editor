# Contributing to EXIF Web Editor

Thank you for your interest in contributing to EXIF Web Editor! This project is designed to be simple and maintainable so anyone can contribute.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, browser)
- Screenshots if applicable

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Why this feature would be useful
- How it might work (optional)

### Code Contributions

1. **Fork the repository**
2. **Create a branch** for your feature or fix
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test your changes** thoroughly
5. **Commit your changes** with clear commit messages
   ```bash
   git commit -m "Add feature: description of what you added"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** with a clear description

## Development Setup

1. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/Exif-Web-Editor.git
   cd Exif-Web-Editor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install exiftool**
   - See the main README for installation instructions

5. **Run the application**
   ```bash
   FLASK_DEBUG=true python app.py
   ```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused
- Write docstrings for functions

Example:
```python
def process_image(filepath):
    """
    Process an image file and extract metadata.
    
    Args:
        filepath (str): Path to the image file
        
    Returns:
        dict: Dictionary containing image metadata
    """
    # Implementation here
```

## Testing

Before submitting a pull request:

1. **Test the application manually**
   - Upload different image formats
   - Edit various EXIF fields
   - Download the modified image
   - Verify EXIF data was updated correctly

2. **Test edge cases**
   - Large files
   - Files without EXIF data
   - Invalid file types
   - Special characters in EXIF fields

3. **Test in different browsers** (if you changed the frontend)
   - Chrome
   - Firefox
   - Safari
   - Edge

## Ideas for Contributions

Here are some areas where contributions would be especially welcome:

### Backend
- [ ] Add batch processing for multiple images
- [ ] Add image format conversion
- [ ] Add GPS coordinate editing with map preview
- [ ] Add more EXIF fields (camera settings, lens info, etc.)
- [ ] Add IPTC and XMP metadata support
- [ ] Add API authentication
- [ ] Add rate limiting
- [ ] Add image preview generation (thumbnails)
- [ ] Add support for RAW image formats
- [ ] Add EXIF template/preset system

### Frontend
- [ ] Improve UI/UX design
- [ ] Add dark mode
- [ ] Add mobile responsiveness improvements
- [ ] Add before/after EXIF comparison view
- [ ] Add history of changes
- [ ] Add keyboard shortcuts
- [ ] Add accessibility improvements
- [ ] Add internationalization (i18n)
- [ ] Add image cropping/rotation
- [ ] Add bulk edit mode

### Documentation
- [ ] Add video tutorials
- [ ] Add more examples
- [ ] Add API documentation
- [ ] Add troubleshooting guide
- [ ] Improve README clarity
- [ ] Add architecture documentation

### DevOps
- [ ] Add Docker Compose setup
- [ ] Add Kubernetes deployment files
- [ ] Add CI/CD pipeline
- [ ] Add automated testing
- [ ] Add code coverage reporting
- [ ] Add performance benchmarks

### Security
- [ ] Add user authentication
- [ ] Add file encryption at rest
- [ ] Add audit logging
- [ ] Add CSP headers
- [ ] Add input validation improvements

## Pull Request Guidelines

### Good Pull Requests

✅ Focus on a single feature or fix
✅ Include clear description of changes
✅ Update documentation if needed
✅ Test thoroughly before submitting
✅ Follow existing code style
✅ Keep changes minimal and focused

### Pull Request Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
How did you test this change?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] My code follows the project's code style
- [ ] I have tested my changes
- [ ] I have updated the documentation
- [ ] My changes don't break existing functionality
```

## Code Review Process

1. A maintainer will review your PR
2. They may request changes or ask questions
3. Make requested changes and push to your branch
4. Once approved, your PR will be merged

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues and discussions
- Review the README and documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Thank You!

Every contribution, no matter how small, is valuable and appreciated. Thank you for helping make EXIF Web Editor better! 🎉
