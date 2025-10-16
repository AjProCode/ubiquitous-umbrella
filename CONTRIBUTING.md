# Contributing to MediScan

Thank you for your interest in contributing to MediScan! This document provides guidelines and information for contributors.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Project Structure](#project-structure)
5. [Coding Standards](#coding-standards)
6. [Making Changes](#making-changes)
7. [Testing](#testing)
8. [Submitting Changes](#submitting-changes)
9. [Feature Requests](#feature-requests)
10. [Bug Reports](#bug-reports)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what is best for the project
- Show empathy towards other contributors

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of Python and object-oriented programming
- Familiarity with barcode systems (helpful but not required)

### First Steps
1. Fork the repository
2. Clone your fork locally
3. Set up your development environment
4. Read the documentation (README.md, ARCHITECTURE.md, USAGE_EXAMPLES.md)
5. Look for issues labeled "good first issue"

## Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ubiquitous-umbrella.git
cd ubiquitous-umbrella
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Core dependencies
pip install -r requirements.txt

# Optional dependencies (for full functionality)
pip install opencv-python pyzbar python-barcode pillow openai

# Development dependencies
pip install pytest black pylint mypy
```

### 4. Set Up Configuration
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Initialize Sample Data
```bash
python app.py init
```

### 6. Verify Installation
```bash
python app.py dashboard
python -m pytest tests/  # If tests exist
```

## Project Structure

```
ubiquitous-umbrella/
├── app.py                 # Main application
├── src/
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   ├── ai/              # AI features
│   └── utils/           # Utilities
├── data/                # Data storage
├── tests/               # Test files
└── docs/                # Documentation
```

See ARCHITECTURE.md for detailed structure information.

## Coding Standards

### Python Style Guide
We follow PEP 8 with some modifications:

- **Line Length**: Maximum 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Use single quotes for strings, except docstrings
- **Naming**:
  - Classes: `PascalCase`
  - Functions/Methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: Prefix with underscore `_private_method`

### Documentation Standards

#### Docstrings
Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this is raised
    """
    pass
```

#### Comments
- Use comments sparingly
- Explain "why", not "what"
- Keep comments up-to-date with code changes

### Type Hints
Use type hints for all function signatures:

```python
from typing import List, Optional, Dict

def process_products(
    products: List[Product],
    filter_expired: bool = False
) -> Dict[str, Any]:
    pass
```

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately
- Don't catch exceptions silently

```python
try:
    product = self.get_product(barcode)
except KeyError:
    raise ProductNotFoundError(f"Product with barcode {barcode} not found")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

## Making Changes

### Branch Naming
Use descriptive branch names:
- `feature/add-batch-scanning`
- `bugfix/fix-expiry-calculation`
- `docs/update-readme`
- `refactor/improve-verification`

### Commit Messages
Follow conventional commits format:

```
type(scope): brief description

Longer description if needed.

- Bullet points for multiple changes
- Another change

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(barcode): add QR code support

fix(expiry): correct calculation for leap years

docs(readme): add installation troubleshooting section
```

### Development Workflow

1. **Create a Branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make Changes**
- Write code
- Add/update tests
- Update documentation

3. **Format Code**
```bash
black src/
```

4. **Lint Code**
```bash
pylint src/
```

5. **Run Tests**
```bash
pytest tests/
```

6. **Commit Changes**
```bash
git add .
git commit -m "feat: add new feature"
```

7. **Push to Your Fork**
```bash
git push origin feature/your-feature-name
```

8. **Create Pull Request**
- Go to GitHub
- Click "New Pull Request"
- Fill out the template
- Link relevant issues

## Testing

### Writing Tests
Place tests in the `tests/` directory with the same structure as `src/`:

```python
# tests/services/test_product_service.py
import pytest
from src.services.product_service import ProductService

def test_add_product():
    """Test adding a product"""
    service = ProductService()
    product = create_test_product()
    
    result = service.add_product(product)
    
    assert result is True
    assert service.get_product(product.barcode) is not None
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/services/test_product_service.py

# Run specific test
pytest tests/services/test_product_service.py::test_add_product
```

### Test Coverage
Aim for at least 80% code coverage for new features.

## Submitting Changes

### Pull Request Checklist
Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Branch is up-to-date with main

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated

## Related Issues
Fixes #123
```

### Review Process
1. Maintainer reviews PR
2. Feedback provided (if needed)
3. Make requested changes
4. Re-review
5. Merge when approved

## Feature Requests

### Submitting Feature Requests
Use GitHub Issues with the "enhancement" label:

1. **Title**: Clear, concise feature description
2. **Problem**: What problem does this solve?
3. **Solution**: Proposed solution
4. **Alternatives**: Other solutions considered
5. **Additional Context**: Screenshots, examples, etc.

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Additional context**
Any other context, screenshots, or examples.
```

## Bug Reports

### Submitting Bug Reports
Use GitHub Issues with the "bug" label:

1. **Title**: Brief bug description
2. **Description**: Detailed explanation
3. **Steps to Reproduce**: Exact steps
4. **Expected Behavior**: What should happen
5. **Actual Behavior**: What actually happens
6. **Environment**: OS, Python version, etc.
7. **Screenshots**: If applicable

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g., Windows 10]
 - Python Version: [e.g., 3.9.5]
 - MediScan Version: [e.g., 1.0.0]

**Additional context**
Any other context about the problem.
```

## Areas for Contribution

### High Priority
- [ ] Add comprehensive test coverage
- [ ] Implement database backend (SQLite)
- [ ] Add web API (Flask/FastAPI)
- [ ] Mobile app integration
- [ ] OCR for label scanning
- [ ] Multi-language support

### Medium Priority
- [ ] Improved AI models
- [ ] Batch operations
- [ ] Export/import functionality
- [ ] Advanced search
- [ ] Reporting features
- [ ] Cloud sync

### Low Priority
- [ ] UI themes
- [ ] Plugin system
- [ ] Additional barcode formats
- [ ] Integration with pharmacy systems
- [ ] Nutrition tracking
- [ ] Shopping list generation

## Communication

### Channels
- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Pull Requests**: Code review, implementation discussion

### Response Times
We aim to:
- Acknowledge issues within 48 hours
- Review PRs within 1 week
- Release updates monthly (or as needed for critical bugs)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Given appropriate GitHub badges
- Thanked in announcements

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Questions?

If you have questions:
1. Check existing documentation
2. Search closed issues
3. Ask in GitHub Discussions
4. Open a new issue with the "question" label

## Thank You!

Your contributions make MediScan better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🎉**
