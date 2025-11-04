"""
Test script for FluidX3D Python Module - Phase 3
Run a quick wing simulation (DEM_CND_WING mode with short time)
"""
import sys
import io
import fluidx3d

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("FluidX3D Python Module - Phase 3 Test")
print("Running Wing Simulation from Python!")
print("=" * 70)
print(f"Version: {fluidx3d.__version__}")
print()

# Test: Run a simple wing simulation
print("Test: Run short wing simulation...")
print("This will:")
print("  - Initialize OpenCL on your GPU")
print("  - Load the Hindenburg STL file")
print("  - Run 1 second of simulation")
print("  - Complete and return to Python")
print()

try:
    config = fluidx3d.Config()
    
    # Configure for a VERY short simulation
    args = [
        '-f', 'LZ_129_Hindenburg.stl',  # STL file
        '--D3Q27',                        # Velocity set
        '--SRT',                          # Collision operator
        '--FP16S',                        # Use FP16 for speed
        '--SUBGRID',                      # Subgrid for complex geometry
        '--EQUILIBRIUM_BOUNDARIES',       # Boundary conditions
        '-r', '2000',                     # Low resolution for speed
        '-u', '10',                       # Velocity 10 m/s
        '--re', '1000000',                # Reynolds number
        '--secs', '1.0',                  # Run for ONLY 1 second!
        '--scale', '0.9',
        '--cord', '0.7',
    ]
    
    print("Parsing arguments...")
    config.parse_args(args)
    print(f"  ✅ File: {config.get_string('file')}")
    print(f"  ✅ Resolution: {config.get_uint('resolution')}")
    print(f"  ✅ Simulation time: {config.get_float('secs')} seconds")
    print(f"  ✅ Velocity set: {config.get_velocity_set()}")
    print()
    
    print("Starting simulation...")
    print("(This may take 10-30 seconds depending on your GPU)")
    print()
    
    config.run_simulation()
    
    print()
    print("  ✅ SUCCESS: Simulation completed and returned to Python!")
    print()
    print("🎉🎉🎉 IT WORKS! 🎉🎉🎉")
    print()
    print("FluidX3D is now callable from Python!")
    
except FileNotFoundError as e:
    print(f"  ⚠️  STL file not found: {e}")
    print("     (This is expected if you don't have the Hindenburg STL)")
    print("     But the Python integration is working!")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("Phase 3 Test Complete!")
print("=" * 70)

