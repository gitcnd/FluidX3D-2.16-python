"""
Test script for the FluidX3D Python module
"""
import sys
import io
import fluidx3d

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("FluidX3D Python Module Test")
print("=" * 60)
print(f"Version: {fluidx3d.__version__}")
print(f"Author: {fluidx3d.__author__}")
print()

# Test 1: No arguments (should fail)
print("Test 1: Validating with no arguments...")
try:
    fluidx3d.validate_args([])
    print("  ❌ UNEXPECTED: Should have raised an exception!")
except RuntimeError as e:
    print(f"  ✅ SUCCESS: Caught expected error: {e}")
print()

# Test 2: Valid arguments
print("Test 2: Validating with valid arguments (--D3Q27)...")
try:
    result = fluidx3d.validate_args(['--D3Q27'])
    print(f"  ✅ SUCCESS: {result}")
except RuntimeError as e:
    print(f"  ❌ UNEXPECTED: {e}")
print()

# Test 3: Multiple velocity sets (should fail)
print("Test 3: Validating with multiple velocity sets...")
try:
    fluidx3d.validate_args(['--D3Q27', '--D3Q19'])
    print("  ❌ UNEXPECTED: Should have raised an exception!")
except RuntimeError as e:
    print(f"  ✅ SUCCESS: Caught expected error: {e}")
print()

# Test 4: Using the class interface
print("Test 4: Using ArgumentValidator class...")
validator = fluidx3d.ArgumentValidator()
print(f"  Version from validator: {validator.get_version()}")
try:
    validator.validate_args(['--D3Q19'])
    print("  ✅ SUCCESS: Arguments validated!")
except RuntimeError as e:
    print(f"  ❌ UNEXPECTED: {e}")
print()

print("=" * 60)
print("All tests completed!")
print("=" * 60)

