# DataEng Toolbox - Quick Commands

## Development Commands

### Setup Development Environment
```bash
# Clone and setup (for contributors)
git clone https://github.com/yourusername/dataeng_toolbox.git
cd dataeng_toolbox

# If you have pip available:
pip install -e .[dev]
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_core.py -v
```

### Code Quality
```bash
# Format code (if black is available)
black dataeng_toolbox tests examples

# Lint code (if flake8 is available)
flake8 dataeng_toolbox tests

# Type checking (if mypy is available)
mypy dataeng_toolbox
```

### Building Package
```bash
# Build package using custom script
python build_package.py

# Or if build module is available:
python -m build
```

### Running Examples
```bash
# Run basic usage example
python examples/basic_usage.py
```

### Validation
```bash
# Validate package is ready for publishing
python validate.py
```

## Publishing Commands

### Test PyPI (Recommended First)
```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ dataeng-toolbox
```

### Production PyPI
```bash
# Upload to PyPI
twine upload dist/*

# Test installation
pip install dataeng-toolbox
```

## Usage Commands

### Install Package
```bash
# Install from PyPI (after publishing)
pip install dataeng-toolbox

# Install in development mode (for development)
pip install -e .
```

### Use Package
```python
# In Python script
from dataeng_toolbox import Core

toolbox = Core()
print(toolbox.hello_world())
info = toolbox.get_info()
```

## File Structure Overview
```
dataeng_toolbox/
├── dataeng_toolbox/           # Main package
│   ├── __init__.py           # Package initialization
│   └── core.py               # Core functionality
├── tests/                    # Unit tests
│   ├── __init__.py
│   └── test_core.py
├── examples/                 # Usage examples
│   ├── basic_usage.py
│   └── README.md
├── .github/workflows/        # GitHub Actions
│   └── ci-cd.yml
├── pyproject.toml            # Project configuration
├── README.md                 # Main documentation
├── LICENSE                   # License file
├── PUBLISHING.md             # Publishing guide
├── build_package.py          # Custom build script
└── validate.py               # Validation script
```

## Version Management
When updating versions, change in these files:
1. `pyproject.toml` - version field
2. `dataeng_toolbox/__init__.py` - __version__
3. `dataeng_toolbox/core.py` - self.version

## GitHub Workflow
1. Push changes to repository
2. Create pull request for review
3. Merge to main branch
4. Create release on GitHub (triggers auto-publish)
5. Package is automatically published to PyPI
