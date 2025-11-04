# Publishing to PyPI

## Prerequisites

1. Install build tools:
```bash
pip install --upgrade pip setuptools wheel twine build
```

2. Get your PyPI API token from https://pypi.org/manage/account/token/

3. Create/update `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-<your-token-here>
```

## Build the Package

**IMPORTANT**: Build **ONLY wheels** (binary distributions), NOT source distributions!
Users should get pre-compiled binaries and NOT need Visual Studio!

```bash
# Clean previous builds
rm -rf build dist *.egg-info

# Build wheels for each Python version you want to support
py -3.11 -m build --wheel  # Python 3.11
py -3.12 -m build --wheel  # Python 3.12
py -3.13 -m build --wheel  # Python 3.13
py -3.14 -m build --wheel  # Python 3.14

# Or use the automated script:
build_wheels.bat

# This creates ONLY wheels (no .tar.gz!):
# - dist/fluidx3d-2.16.0-cp311-cp311-win_amd64.whl (Python 3.11)
# - dist/fluidx3d-2.16.0-cp312-cp312-win_amd64.whl (Python 3.12)
# - etc.
```

**Why wheels only?**
- ✅ Pre-compiled, ready to install
- ✅ Users don't need Visual Studio
- ✅ Fast installation
- ❌ Source distributions require users to compile (BAD!)

## Test on Test PyPI (Recommended First)

```bash
# Upload to TestPyPI (WHEELS ONLY!)
python -m twine upload --repository testpypi dist/*.whl

# DO NOT upload .tar.gz files! Only .whl files!

# Test install (from another PC or clean venv)
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple fluidx3d

# Test it works
python -c "import fluidx3d; print(fluidx3d.__version__)"
```

## Upload to PyPI

```bash
# Upload to real PyPI (WHEELS ONLY!)
python -m twine upload dist/*.whl

# Install from PyPI
pip install fluidx3d

# If you accidentally uploaded a source distribution too, users might try to compile it!
# Only upload .whl files to prevent this!
```

## Version Updates

To release a new version:

1. Update version in `setup.py`:
```python
version='2.16.1',  # Increment version
```

2. Update version in `src/python_bindings_full.cpp`:
```cpp
return "2.16.1-python";
```

3. Rebuild and upload:
```bash
rm -rf build dist *.egg-info
python -m build
python -m twine upload dist/*
```

## Common Issues

### "File already exists"
- You can't re-upload the same version
- Increment version number and rebuild

### "Invalid username/password"
- Make sure you're using `__token__` as username
- Token must start with `pypi-`

### Missing DLLs
- OpenCL.lib must be in `src/OpenCL/lib/`
- Check MANIFEST.in includes all necessary files

### Platform-specific wheels
- This package only works on Windows (x64)
- Wheel will be: `fluidx3d-2.16.0-cp3XX-cp3XX-win_amd64.whl`

## Notes

- Each Python version needs its own wheel (3.11, 3.12, 3.13, 3.14)
- Build on the target Python version you want to support
- Source distribution (.tar.gz) will require compilation on user's machine
- Wheels (.whl) are pre-compiled and install faster

