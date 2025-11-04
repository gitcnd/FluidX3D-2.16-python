"""
Test script for FluidX3D Python Module - Phase 3
Simple simulation test (BENCHMARK mode)
"""
import sys
import io
import fluidx3d

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("FluidX3D Python Module - Phase 3 Test")
print("Running actual simulation!")
print("=" * 70)
print(f"Version: {fluidx3d.__version__}")
print()

# Test 1: Run benchmark simulation
print("Test 1: Run BENCHMARK simulation...")
print("This will initialize OpenCL, run on your GPU, and test performance!")
print()

try:
    config = fluidx3d.Config()
    
    # Configure for benchmark mode
    args = [
        '--BENCHMARK',  # Run benchmark
        '--D3Q19',      # Velocity set
        '--FP16S',      # Use FP16 for speed
        '--SRT',        # Collision operator (required!)
    ]
    
    print("Parsing arguments...")
    config.parse_args(args)
    print(f"  ✅ Velocity set: {config.get_velocity_set()}")
    print(f"  ✅ FP16S: {config.get_bool('FP16S')}")
    print(f"  ✅ BENCHMARK: {config.get_bool('BENCHMARK')}")
    print()
    
    print("Starting simulation...")
    print("(This will take a few seconds - FluidX3D is running on your GPU!)")
    print()
    
    config.run_simulation()
    
    print()
    print("  ✅ SUCCESS: Simulation completed!")
    
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("Phase 3 Test Complete!")
print("=" * 70)

