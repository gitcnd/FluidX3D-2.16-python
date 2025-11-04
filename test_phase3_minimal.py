"""
Test script for FluidX3D Python Module - Phase 3
Minimal test - very short simulation, no graphics
"""
import sys
import io
import time
import fluidx3d

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("FluidX3D Python Module - Phase 3 Minimal Test")
print("=" * 70)
print(f"Version: {fluidx3d.__version__}")
print()

print("Test: Run VERY short simulation (0.01 seconds of sim time)")
print("This should:")
print("  - Initialize OpenCL")
print("  - Load STL")
print("  - Run briefly")
print("  - STOP after 0.01 seconds")
print("  - Return to Python")
print()

try:
    config = fluidx3d.Config()
    
    # Configure for MINIMAL simulation
    args = [
        '-f', 'LZ_129_Hindenburg.stl',
        '--D3Q27',
        '--SRT',
        '--FP16S',
        '--SUBGRID',
        '--EQUILIBRIUM_BOUNDARIES',
        '-r', '1000',          # Very low resolution
        '-u', '5',
        '--re', '100000',
        '--secs', '0.01',      # Only 0.01 seconds!
        '--scale', '0.9',
        '--cord', '0.7',
    ]
    
    print("Parsing arguments...")
    config.parse_args(args)
    print(f"  ✅ Simulation time: {config.get_float('secs')} seconds")
    print()
    
    print("Starting simulation...")
    start_time = time.time()
    
    config.run_simulation()
    
    elapsed = time.time() - start_time
    print()
    print(f"  ✅ SUCCESS! Simulation completed in {elapsed:.2f} seconds")
    print()
    print("🎉🎉🎉 FluidX3D ran from Python and STOPPED correctly! 🎉🎉🎉")
    
except FileNotFoundError as e:
    print(f"  ⚠️  STL file not found: {e}")
except KeyboardInterrupt:
    print("\n  ⚠️  Interrupted by user (Ctrl+C)")
    print("     The simulation was running but didn't stop on its own.")
    print("     We need to fix the stopping mechanism!")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)

