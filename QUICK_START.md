# FluidX3D Python Module - Quick Start Guide

## Installation (Development Mode)

### Prerequisites
- Python 3.11+ (tested with 3.14.0)
- Visual Studio 2022 (for MSVC compiler)
- pybind11: `pip install pybind11`
- numpy: `pip install numpy`

### Build the Module

```batch
# Navigate to the project directory
cd C:\Users\cnd\Downloads\repos\FluidX3D-3.5\FluidX3D-2.16

# Build the extension
python setup.py build_ext --inplace

# Copy the .pyd file to root (if not already there)
copy src\fluidx3d.cp3XX-win_amd64.pyd fluidx3d.pyd
```

Or simply run:
```batch
.\build_python_module.bat
```

## Basic Usage

### Import and Check Version

```python
import fluidx3d

print(f"FluidX3D Python Module v{fluidx3d.__version__}")
print(f"Author: {fluidx3d.__author__}")
```

### Validate Arguments

```python
import fluidx3d

# This works - valid velocity set
try:
    result = fluidx3d.validate_args(['--D3Q27'])
    print(result)  # "Arguments validated successfully!"
except RuntimeError as e:
    print(f"Error: {e}")

# This fails - no velocity set specified
try:
    fluidx3d.validate_args([])
except RuntimeError as e:
    print(f"Error: {e}")  # "Must pick one of --D3Q15 --D3Q19 --D3Q27 or --D2Q9"

# This fails - multiple velocity sets
try:
    fluidx3d.validate_args(['--D3Q27', '--D3Q19'])
except RuntimeError as e:
    print(f"Error: {e}")  # "Can only pick one velocity set..."
```

### Using the Class Interface

```python
import fluidx3d

# Create a validator
validator = fluidx3d.ArgumentValidator()

# Get version
print(validator.get_version())  # "2.16.0-python"

# Validate arguments
validator.validate_args(['--D3Q19'])  # Success!
```

## Running Tests

```batch
python test_module.py
```

Expected output:
```
============================================================
FluidX3D Python Module Test
============================================================
Version: 2.16.0-python

Test 1: Validating with no arguments...
  ✅ SUCCESS: Caught expected error: Must pick one of --D3Q15 --D3Q19 --D3Q27 or --D2Q9

Test 2: Validating with valid arguments (--D3Q27)...
  ✅ SUCCESS: Arguments validated successfully!

...

All tests completed!
============================================================
```

## Troubleshooting

### Module Not Found

If you get `ModuleNotFoundError: No module named 'fluidx3d'`:

1. Make sure you're in the correct directory
2. Check that `fluidx3d.pyd` exists in the current directory
3. Try: `python -c "import sys; print(sys.path)"`

### Build Failures

If the build fails:

1. Ensure Visual Studio 2022 is installed
2. Run from a "Developer Command Prompt for VS 2022"
3. Check that pybind11 is installed: `pip list | grep pybind11`

### Wrong Python Version

The .pyd file is tied to a specific Python version. If you switch Python versions:

1. Delete the old .pyd file
2. Delete the `build/` directory
3. Rebuild: `python setup.py build_ext --inplace`

## What's Next?

Phase 1 is complete! We've proven that:
- ✅ pybind11 integration works
- ✅ Error handling is robust
- ✅ Build system is functional

**Phase 2** will add:
- Full argument parsing
- LBM simulation functionality
- Data extraction (NumPy arrays)
- OpenCL integration

See `PYTHON_MODULE_STATUS.md` for the full roadmap.

## Python 3.11.14 Compatibility

This module is designed to work with Python 3.11.14+ (your target version). The build system will automatically create the correct .pyd file for your Python version:

- Python 3.11: `fluidx3d.cp311-win_amd64.pyd`
- Python 3.14: `fluidx3d.cp314-win_amd64.pyd`

Simply rename it to `fluidx3d.pyd` for easier importing.

## Support

For issues, refer to:
- `PYTHON_MODULE_STATUS.md` - Detailed status and roadmap
- `test_module.py` - Working examples
- Original FluidX3D: https://github.com/ProjectPhysX/FluidX3D

---

**Good luck and happy computing!** 🚀

