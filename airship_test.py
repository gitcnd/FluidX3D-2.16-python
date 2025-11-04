"""
Python equivalent of your Hindenburg airship simulation!

Original command:
bin\FluidX3D.exe -f LZ_129_Hindenburg.stl -r 12400 --SUBGRID --roty 0 --rotx -180 
--rotz 0 --try -0.2 -c 0.7 -u 7 --re 535000000 --rho 1024 --fps 60 --SRT 
--UPDATE_FIELDS --GRAPHICS --EQUILIBRIUM_BOUNDARIES --FP16S --D3Q27 
--export png_fine/ --slomo 10 --scale 1 --width 0.1 --length 0.2 --height 0.1
"""
import fluidx3d
import time

print("=" * 70)
print("Hindenburg Airship CFD Simulation - Python Edition")
print("=" * 70)
print()

# Configure the simulation
config = fluidx3d.Config()
config.parse_args([
    '-f', 'LZ_129_Hindenburg.stl',
    '-r', '15400',              # High resolution (this will take time!)
    '--D3Q27',                  # Velocity set
    '--FP16S',                  # Half precision for 2x speedup
    '--SUBGRID',                # Subgrid for complex geometry
    '--SRT',                    # Collision operator (required!)
    '--EQUILIBRIUM_BOUNDARIES', # Boundary conditions
    '--UPDATE_FIELDS',          # Update fields for visualization
    '--GRAPHICS',               # Enable graphics! (window will appear)
    '--window',                 # Use windowed mode instead of fullscreen
    '-u', '7',                  # Velocity 7 m/s
    '--re', '535000000',        # Reynolds number
    '--rho', '1024',            # Density
    '--secs', '5.0',            # Run for 5 seconds (change to run longer)
    '--rotx', '-180',           # Rotations to match your original
    '--roty', '0',
    '--rotz', '0',
    '--try', '-0.2',            # Translation
    '-c', '0.7',                # Chord length
    '--scale', '1',
    '--width', '0.1',
    '--length', '0.2',
    '--height', '0.1',
    '--export', 'png_fine/',    # Export frames here
    '--fps', '60',
    '--slomo', '10',
])

# Show configuration
print("Configuration:")
print(f"  File: {config.get_string('file')}")
print(f"  Resolution: {config.get_uint('resolution')}")
print(f"  Velocity: {config.get_float('u')} m/s")
print(f"  Reynolds: {config.get_float('re')}")
print(f"  Simulation time: {config.get_float('secs')} seconds")
print(f"  Velocity set: {config.get_velocity_set()}")
print()

print("✅ Graphics enabled! A window should appear when simulation starts.")
print("   The simulation runs in a separate thread, just like your .exe!")
print()

input("Press Enter to start the simulation...")
print()
print("Starting simulation (this will take several minutes)...")
print("Watch your GPU usage - it should spike to 100%!")
print()

start_time = time.time()

try:
    config.run_simulation()
    
    elapsed = time.time() - start_time
    print()
    print("=" * 70)
    print(f"✅ Simulation completed in {elapsed:.1f} seconds!")
    print("=" * 70)
    print()
    print("Check the png_fine/ folder for exported frames!")
    print("You can use ffmpeg to create a video from the frames.")
    
except FileNotFoundError as e:
    print(f"❌ STL file not found: {e}")
    print("   Make sure LZ_129_Hindenburg.stl is in the current directory")
except KeyboardInterrupt:
    print("\n⚠️  Interrupted by user (Ctrl+C)")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
