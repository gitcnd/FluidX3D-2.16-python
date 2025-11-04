"""Quick test to see if graphics window appears"""
import fluidx3d

print("Testing graphics window with minimal simulation...")
print("A window should appear!")
print()

config = fluidx3d.Config()
config.parse_args([
    '-f', 'LZ_129_Hindenburg.stl',
    '--D3Q27', '--SRT', '--FP16S',
    '--SUBGRID', '--EQUILIBRIUM_BOUNDARIES',
    '--GRAPHICS',      # Graphics enabled!
    '--window',        # Windowed mode
    '-r', '500',       # Very low resolution for speed
    '--secs', '1.0',   # Just 1 second
    '-u', '5',
    '--re', '100000',
    '--scale', '0.9',
    '-c', '0.7',
])

print(f"Resolution: {config.get_uint('resolution')} (very low for testing)")
print(f"Time: {config.get_float('secs')} seconds")
print()
print("Starting... window should appear NOW!")

config.run_simulation()

print()
print("✅ Done! Did you see the window?")

