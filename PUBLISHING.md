# Publishing Guide for DataEng Toolbox

This guide walks you through publishing the `dataeng_toolbox` package to PyPI.

## Prerequisites

1. **Python 3.11+** installed
2. **PyPI Account**: Create an account at [pypi.org](https://pypi.org/account/register/)
3. **API Token**: Generate an API token from your PyPI account settings

## Setup for Publishing

### 1. Install Required Tools

If you have pip available:
```bash
pip install build twine
```

If pip is not available, you can use the built-in build script:
```bash
python build_package.py
```

### 2. Configure PyPI Credentials

Create a `.pypirc` file in your home directory:

**Windows**: `C:\Users\YourUsername\.pypirc`
**Linux/Mac**: `~/.pypirc`

```ini
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = pypi-your-api-token-here
```

Or use environment variables:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here
```

## Building the Package

### Option 1: Using build module (if available)
```bash
python -m build
```

### Option 2: Using the custom build script
```bash
python build_package.py
```

This will create:
- `dist/dataeng_toolbox-0.1.0.tar.gz` (source distribution)
- `dist/dataeng_toolbox-0.1.0-py3-none-any.whl` (wheel)

## Publishing Steps

### 1. Test on Test PyPI (Recommended)

First, upload to Test PyPI to verify everything works:

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*
```

Then test the installation:
```bash
pip install --index-url https://test.pypi.org/simple/ dataeng-toolbox
```

### 2. Publish to Production PyPI

Once tested, publish to the main PyPI:

```bash
twine upload dist/*
```

### 3. Verify Installation

Test that users can install your package:
```bash
pip install dataeng-toolbox
```

## Version Management

When releasing new versions:

1. Update the version in `pyproject.toml`
2. Update the version in `dataeng_toolbox/__init__.py`
3. Update the version in `dataeng_toolbox/core.py`
4. Update the CHANGELOG in README.md
5. Create a new git tag:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

## GitHub Actions (Automated Publishing)

The project includes GitHub Actions workflow for automated publishing:

1. **Set up secrets** in your GitHub repository:
   - Go to Settings > Secrets and variables > Actions
   - Add `PYPI_API_TOKEN` with your PyPI API token

2. **Publishing workflow**:
   - Automatic testing on every push/PR
   - Automatic publishing when you create a release on GitHub

To create a release:
1. Go to your GitHub repository
2. Click "Releases" > "Create a new release"
3. Create a new tag (e.g., `v0.1.0`)
4. Add release notes
5. Publish the release

The workflow will automatically build and publish to PyPI.

## Troubleshooting

### Common Issues

1. **Authentication Error**: Check your API token and `.pypirc` configuration
2. **Package Already Exists**: You cannot upload the same version twice. Increment the version number.
3. **Build Errors**: Make sure all dependencies are installed and pyproject.toml is correct

### Manual Upload Command

If twine doesn't work with config files:
```bash
twine upload -u __token__ -p pypi-your-token-here dist/*
```

### Checking Package Before Upload

Validate your package before uploading:
```bash
twine check dist/*
```

## Security Notes

- Never commit API tokens to version control
- Use environment variables or secure config files
- Consider using keyring for credential storage
- Regularly rotate your API tokens

## Success Verification

After publishing, your package should be available at:
- PyPI page: `https://pypi.org/project/dataeng-toolbox/`
- Installation: `pip install dataeng-toolbox`

Users can then use your package:
```python
from dataeng_toolbox import Core
toolbox = Core()
print(toolbox.hello_world())
```
