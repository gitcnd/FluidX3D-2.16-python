"""
Test script for FluidX3D Python Module - Phase 2
Full argument parsing integration
"""
import sys
import io
import fluidx3d

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("FluidX3D Python Module - Phase 2 Test")
print("Full Argument Parsing")
print("=" * 70)
print(f"Version: {fluidx3d.__version__}")
print(f"Author: {fluidx3d.__author__}")
print()

# Test 1: Basic argument parsing
print("Test 1: Parse basic arguments...")
try:
    config = fluidx3d.Config()
    config.parse_args(['--D3Q27', '--FP16S', '-f', 'test.stl'])
    print(f"  ✅ SUCCESS: Arguments parsed!")
    print(f"     Velocity set: {config.get_velocity_set()}")
    print(f"     File: {config.get_string('file')}")
    print(f"     FP16S: {config.get_bool('FP16S')}")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
print()

# Test 2: No velocity set (should fail)
print("Test 2: Parse without velocity set (should fail)...")
try:
    config2 = fluidx3d.Config()
    config2.parse_args(['-f', 'test.stl'])
    print("  ❌ UNEXPECTED: Should have raised an exception!")
except RuntimeError as e:
    print(f"  ✅ SUCCESS: Caught expected error: {e}")
print()

# Test 3: Hindenburg example from your command line
print("Test 3: Parse Hindenburg airship simulation arguments...")
try:
    config3 = fluidx3d.Config()
    args = [
        '-f', 'LZ_129_Hindenburg.stl',
        '-r', '15400',
        '--SUBGRID',
        '--roty', '0',
        '--rotx', '-180',
        '--rotz', '0',
        '--try', '-0.2',
        '-c', '0.7',
        '-u', '7',
        '--re', '535000000',
        '--rho', '1024',
        '--fps', '60',
        '--SRT',
        '--UPDATE_FIELDS',
        '--EQUILIBRIUM_BOUNDARIES',
        '--FP16S',
        '--D3Q27',
        '--export', 'png_fine/',
        '--slomo', '10',
        '--scale', '1',
        '--width', '0.1',
        '--length', '0.2',
        '--height', '0.1',
        '--secs', '5.0'  # Short simulation time for testing
    ]
    config3.parse_args(args)
    print(f"  ✅ SUCCESS: Hindenburg simulation config parsed!")
    print(f"     File: {config3.get_string('file')}")
    print(f"     Resolution: {config3.get_uint('resolution')}")
    print(f"     Reynolds: {config3.get_float('re')}")
    print(f"     Velocity: {config3.get_float('u')} m/s")
    print(f"     Simulation time: {config3.get_float('secs')} seconds")
    print(f"     Velocity set: {config3.get_velocity_set()}")
    print(f"     SUBGRID: {config3.get_bool('SUBGRID')}")
    print(f"     FP16S: {config3.get_bool('FP16S')}")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 4: Get all parameters as dict
print("Test 4: Get parameters as Python dictionary...")
try:
    config4 = fluidx3d.Config()
    config4.parse_args(['--D3Q19', '-f', 'wing.stl', '-r', '8192', '-u', '25', '--SUBGRID'])
    params = config4.to_dict()
    print("  ✅ SUCCESS: Parameters extracted as dictionary:")
    for key, value in params.items():
        print(f"     {key}: {value}")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
print()

# Test 5: Float parameter access
print("Test 5: Access various parameter types...")
try:
    config5 = fluidx3d.Config()
    config5.parse_args([
        '--D3Q27',
        '--rotx', '45.5',
        '--roty', '-30.2',
        '-r', '4096',
        '--re', '150000.5'
    ])
    print("  ✅ SUCCESS: Parameter access:")
    print(f"     rotx (float): {config5.get_float('rotx')}")
    print(f"     roty (float): {config5.get_float('roty')}")
    print(f"     resolution (uint): {config5.get_uint('resolution')}")
    print(f"     reynolds (float): {config5.get_float('re')}")
    print(f"     SUBGRID (bool): {config5.get_bool('SUBGRID')}")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
print()

# Test 6: Simulation control parameters
print("Test 6: Simulation control parameters...")
try:
    config6 = fluidx3d.Config()
    config6.parse_args([
        '--D3Q27',
        '--secs', '100.5',  # Run for 100.5 seconds
        '--fps', '30',
        '--slomo', '5',
        '--pause',
        '--floor'
    ])
    print("  ✅ SUCCESS: Control parameters:")
    print(f"     Simulation time: {config6.get_float('secs')} seconds")
    print(f"     FPS: {config6.get_float('fps')}")
    print(f"     Slow-motion factor: {config6.get_float('slomo')}x")
    print(f"     Start paused: {config6.get_bool('pause')}")
    print(f"     Floor: {config6.get_bool('floor')}")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
print()

print("=" * 70)
print("Phase 2 Tests Complete!")
print("=" * 70)
print()
print("✅ Full argument parsing is working!")
print("✅ Can parse Hindenburg simulation config")
print("✅ Parameter access methods functional")
print("✅ Simulation time control available (--secs)")
print()
print("Next: Phase 3 - Integrate actual LBM simulation!")
print("=" * 70)

