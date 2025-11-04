# FluidX3D Python Module

**Real-time interactive GPU-accelerated Computational Fluid Dynamics (CFD) with Python!**

This is a Python wrapper for [FluidX3D v2.16](https://github.com/ProjectPhysX/FluidX3D), the fastest and most memory efficient Lattice Boltzmann CFD software, capable of running simulations with up to 10 billion cells in VRAM.

![FluidX3D Demo](https://raw.githubusercontent.com/ProjectPhysX/FluidX3D/master/img/fluidx3d.png)

## Features

- 🚀 **Full GPU Acceleration** - Utilizes OpenCL for massive parallel computation
- 🎮 **Interactive Graphics** - Real-time 3D visualization with interactive controls
- 🔧 **Runtime Configuration** - All simulation parameters configurable via Python API
- 📊 **High Performance** - Processes millions of lattice cells per second
- 🎯 **Easy to Use** - Simple Python interface to powerful CFD engine
- 🪟 **Windows Graphics** - Native window support with keyboard/mouse controls

## Requirements

- **Windows** (required for interactive graphics)
- **Python 3.11+**
- **OpenCL-capable GPU** (NVIDIA, AMD, or Intel)
- **Visual C++ Redistributables** (usually already installed)

## Installation

```bash
pip install fluidx3d
```

## Quick Start

```python
import fluidx3d

# Configure simulation
config = fluidx3d.Config()
config.parse_args([
    '--D3Q27',              # Use D3Q27 velocity set
    '--FP16S',              # Use FP16 precision
    '--SUBGRID',            # Enable subgrid model
    '--SRT',                # Use SRT collision operator
    '--GRAPHICS',           # Enable graphics
    '--window',             # Use windowed mode (not fullscreen)
    '-f', 'your_model.stl', # Input STL file
    '-r', '15400',          # Resolution (VRAM in MB)
    '-u', '7.0',            # Velocity (m/s)
    '--re', '535000000',    # Reynolds number
    '--secs', '10.0',       # Simulation time (seconds)
])

# Run simulation (opens interactive window!)
config.run_simulation()
```

## Interactive Controls

When the graphics window opens:

- **P** - Pause/resume simulation
- **O** - Save frames to disk
- **H** - Show/hide help overlay
- **1-7** - Toggle visualization modes
- **Mouse** - Rotate camera
- **W/A/S/D** - Move camera (in free camera mode)
- **F** - Toggle free camera mode
- **Esc** - Quit

## Example: Airship Simulation

```python
import fluidx3d

config = fluidx3d.Config()
config.parse_args([
    '--D3Q27', '--FP16S', '--SUBGRID',
    '--SRT', '--UPDATE_FIELDS', '--GRAPHICS',
    '--EQUILIBRIUM_BOUNDARIES',
    '-f', 'LZ_129_Hindenburg.stl',
    '-r', '15400',  # ~15GB VRAM
    '-u', '7',      # 7 m/s velocity
    '--re', '535000000',  # Reynolds number
    '--rho', '1024',      # Density
    '--secs', '30.0',     # 30 seconds simulation
    '--fps', '60',
    '--slomo', '10',
])

# Access parameters
print(f"Velocity: {config.get_float('u')} m/s")
print(f"Reynolds: {config.get_float('re')}")

# Get all parameters as dict
params = config.to_dict()

# Run simulation
config.run_simulation()
```

## Available Arguments

### Velocity Sets
- `--D2Q9` - 2D 9-velocity
- `--D3Q15` - 3D 15-velocity  
- `--D3Q19` - 3D 19-velocity
- `--D3Q27` - 3D 27-velocity (recommended)

### Precision & Performance
- `--FP16S` - Half precision (recommended, 2x faster)
- `--FP16C` - Half precision compression
- `--SUBGRID` - Subgrid turbulence model

### Collision Operators
- `--SRT` - Single Relaxation Time
- `--TRT` - Two Relaxation Time

### Features
- `--GRAPHICS` - Enable interactive graphics
- `--window` - Windowed mode (not fullscreen)
- `--UPDATE_FIELDS` - Update velocity/density fields
- `--EQUILIBRIUM_BOUNDARIES` - Equilibrium boundaries
- `--MOVING_BOUNDARIES` - Moving solid boundaries
- `--SURFACE` - Free surface flow
- `--TEMPERATURE` - Temperature simulation
- `--PARTICLES` - Particle tracking

### Simulation Parameters
- `-f FILE` - Input STL file
- `-r RES` - Resolution (VRAM usage in MB)
- `-u VEL` - Velocity (m/s)
- `-c CHORD` - Characteristic length (m)
- `--re RE` - Reynolds number
- `--rho RHO` - Density (kg/m³)
- `--secs TIME` - Simulation duration (seconds)
- `--fps FPS` - Video framerate
- `--slomo FACTOR` - Slow motion factor
- `--export PATH` - Export directory

### Geometry Transform
- `--rotx DEG` - Rotate around X axis
- `--roty DEG` - Rotate around Y axis  
- `--rotz DEG` - Rotate around Z axis
- `--scale FACTOR` - Scale factor
- `--aoa DEG` - Angle of attack

## Performance Tips

1. **Use `--FP16S`** - Doubles performance on most GPUs
2. **Use `--D3Q27`** - Best accuracy for complex flows
3. **Adjust resolution** - Use `-r` to balance quality vs speed
4. **Monitor VRAM** - Shown in console output at startup

## Hardware Requirements

### Minimum
- NVIDIA GTX 1060 / AMD RX 580 / Intel Arc A380 (4GB VRAM)
- 8GB system RAM
- Windows 10/11

### Recommended  
- NVIDIA RTX 3060 or better (12GB+ VRAM)
- 16GB+ system RAM
- Windows 11

## Credits

- **Original FluidX3D**: Dr. Moritz Lehmann - https://github.com/ProjectPhysX/FluidX3D
- **Python Bindings**: AuraFriday (cnd) - https://github.com/gitcnd/FluidX3D-2.16-python

## License

GNU General Public License v3.0 - See LICENSE.md

## Links

- **GitHub**: https://github.com/gitcnd/FluidX3D-2.16-python
- **Original FluidX3D**: https://github.com/ProjectPhysX/FluidX3D
- **Issues**: https://github.com/gitcnd/FluidX3D-2.16-python/issues

