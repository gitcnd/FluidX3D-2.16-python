"""
File: ragtag/tools/fluidx3d.py
Project: Aura Friday MCP-Link Server
Component: FluidX3D CFD Simulation Tool
Author: Christopher Nathan Drake (cnd)

Tool implementation for running GPU-accelerated Computational Fluid Dynamics simulations
using FluidX3D via Python. Supports interactive graphics, parameter configuration, and
real-time CFD visualization.

Copyright: © 2025 Christopher Nathan Drake. All rights reserved.
SPDX-License-Identifier: Proprietary
"""

import json
import os
import sys
from easy_mcp.server import MCPLogger, get_tool_token
from typing import Dict, List, Optional, Union, Tuple
import threading
import time

# Constants
TOOL_LOG_NAME = "FLUIDX3D"

# Module-level token generated once at import time
TOOL_UNLOCK_TOKEN = get_tool_token(__file__)

# Try to import fluidx3d module
try:
    import fluidx3d as fx3d
    FLUIDX3D_AVAILABLE = True
except ImportError:
    FLUIDX3D_AVAILABLE = False
    MCPLogger.log(TOOL_LOG_NAME, "Warning: fluidx3d module not available. Install with: pip install fluidx3d")

# Tool definitions
TOOLS = [
    {
        "name": "fluidx3d",
        "description": """Run GPU-accelerated Computational Fluid Dynamics (CFD) simulations using FluidX3D.
- Use this tool when you need to perform real-time interactive CFD simulations with GPU acceleration
- Supports loading 3D models (.stl files), configuring simulation parameters, and interactive visualization
""",
        "parameters": {
            "properties": {
                "input": {
                    "type": "object",
                    "description": "All tool parameters are passed in this single dict. Use {\"input\":{\"operation\":\"readme\"}} to get full documentation, parameters, and an unlock token."
                }
            },
            "required": [],
            "type": "object"
        },
        "real_parameters": {
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["readme", "run_simulation", "get_version", "validate_config", "list_devices"],
                    "description": "Operation to perform"
                },
                "config": {
                    "type": "object",
                    "description": "Simulation configuration parameters (required for run_simulation and validate_config operations)",
                    "properties": {
                        "stl_file": {"type": "string", "description": "Path to .stl mesh file"},
                        "velocity_set": {"type": "string", "enum": ["D2Q9", "D3Q15", "D3Q19", "D3Q27"], "description": "Lattice Boltzmann velocity set"},
                        "collision_operator": {"type": "string", "enum": ["SRT", "TRT"], "description": "LBM collision operator"},
                        "resolution": {"type": "integer", "description": "Grid resolution"},
                        "reynolds": {"type": "number", "description": "Reynolds number"},
                        "velocity": {"type": "number", "description": "Flow velocity in m/s"},
                        "density": {"type": "number", "description": "Fluid density (rho) in kg/m³"},
                        "chord_length": {"type": "number", "description": "Cord length of STL in meters"},
                        "simulation_time": {"type": "number", "description": "Simulation time in seconds"},
                        "time_steps": {"type": "integer", "description": "Number of time steps"},
                        "scale": {"type": "number", "description": "Scale factor for mesh"},
                        "angle_of_attack": {"type": "number", "description": "Angle of attack in degrees"},
                        "rotation_x": {"type": "number", "description": "X-axis rotation in degrees"},
                        "rotation_y": {"type": "number", "description": "Y-axis rotation in degrees"},
                        "rotation_z": {"type": "number", "description": "Z-axis rotation in degrees"},
                        "translate_x": {"type": "number", "description": "X-axis translation"},
                        "translate_y": {"type": "number", "description": "Y-axis translation"},
                        "translate_z": {"type": "number", "description": "Z-axis translation"},
                        "box_width": {"type": "number", "description": "X width of sim box"},
                        "box_length": {"type": "number", "description": "Y length of sim box"},
                        "box_height": {"type": "number", "description": "Z height of sim box"},
                        "camera_x": {"type": "number", "description": "Camera X position"},
                        "camera_y": {"type": "number", "description": "Camera Y position"},
                        "camera_z": {"type": "number", "description": "Camera Z position"},
                        "camera_zoom": {"type": "number", "description": "Camera zoom level"},
                        "camera_rotation_x": {"type": "number", "description": "Camera rotation X"},
                        "camera_rotation_y": {"type": "number", "description": "Camera rotation Y"},
                        "camera_fov": {"type": "number", "description": "Camera field of view"},
                        "window_mode": {"type": "boolean", "description": "Use windowed mode instead of fullscreen"},
                        "wait_on_exit": {"type": "boolean", "description": "Wait for keypress before ending"},
                        "pause_on_start": {"type": "boolean", "description": "Do not auto-start the simulation"},
                        "fps": {"type": "number", "description": "Frames per second for video output"},
                        "realtime_export": {"type": "boolean", "description": "Save every frame to video output"},
                        "slomo": {"type": "number", "description": "Slow motion factor (1=realtime, 10=10x slower)"},
                        "export_path": {"type": "string", "description": "Folder name to save images and data"},
                        "frame_width": {"type": "integer", "description": "Screen or window resolution width"},
                        "frame_height": {"type": "integer", "description": "Screen or window resolution height"},
                        "background_color": {"type": "integer", "description": "Screen background color (hex)"},
                        "streamline_sparse": {"type": "integer", "description": "Streamlines spacing"},
                        "streamline_length": {"type": "integer", "description": "Streamline length"},
                        "transparency": {"type": "boolean", "description": "Enable transparency"},
                        "display": {"type": "string", "description": "Display device selection"},
                        "enable_graphics": {"type": "boolean", "description": "Enable interactive 3D graphics"},
                        "enable_graphics_ascii": {"type": "boolean", "description": "Enable console ASCII graphics"},
                        "enable_subgrid": {"type": "boolean", "description": "Enable SUBGRID model"},
                        "enable_volume_force": {"type": "boolean", "description": "Enable VOLUME_FORCE"},
                        "enable_force_field": {"type": "boolean", "description": "Enable FORCE_FIELD"},
                        "enable_particles": {"type": "boolean", "description": "Enable PARTICLES"},
                        "enable_temperature": {"type": "boolean", "description": "Enable TEMPERATURE"},
                        "enable_update_fields": {"type": "boolean", "description": "Enable UPDATE_FIELDS"},
                        "enable_moving_boundaries": {"type": "boolean", "description": "Enable MOVING_BOUNDARIES"},
                        "enable_equilibrium_boundaries": {"type": "boolean", "description": "Enable EQUILIBRIUM_BOUNDARIES"},
                        "enable_surface": {"type": "boolean", "description": "Enable SURFACE"},
                        "enable_fp16s": {"type": "boolean", "description": "Use FP16S half precision"},
                        "enable_fp16c": {"type": "boolean", "description": "Use FP16C half precision"},
                        "enable_benchmark": {"type": "boolean", "description": "Run GPU benchmark"},
                        "enable_floor": {"type": "boolean", "description": "Insert a solid floor"},
                        "allow_sleep": {"type": "boolean", "description": "Do not prevent PC from sleeping"}
                    }
                },
                "tool_unlock_token": {
                    "type": "string",
                    "description": "Security token obtained from readme operation: " + TOOL_UNLOCK_TOKEN
                }
            },
            "required": ["operation", "tool_unlock_token"],
            "type": "object"
        },
        "readme": f"""
FluidX3D - GPU-Accelerated Computational Fluid Dynamics

Real-time interactive Lattice Boltzmann CFD simulations with full GPU acceleration.
This tool wraps the FluidX3D v2.16 Python module for programmatic access to CFD simulations.

## Requirements
- OpenCL-capable GPU (NVIDIA, AMD, or Intel)
- OpenCL runtime (GPU drivers or Intel CPU Runtime)
- fluidx3d Python module (pip install fluidx3d)

## Usage-Safety Token System
Your tool_unlock_token for this installation is: {TOOL_UNLOCK_TOKEN}

You MUST include tool_unlock_token in the input dict for all operations.

## Operations

### 1. Get Documentation (readme)
{{
  "input": {{
    "operation": "readme"
  }}
}}

### 2. Get Version Info
{{
  "input": {{
    "operation": "get_version",
    "tool_unlock_token": "{TOOL_UNLOCK_TOKEN}"
  }}
}}

### 3. List Available OpenCL Devices
{{
  "input": {{
    "operation": "list_devices",
    "tool_unlock_token": "{TOOL_UNLOCK_TOKEN}"
  }}
}}

### 4. Validate Configuration (without running)
{{
  "input": {{
    "operation": "validate_config",
    "config": {{
      "stl_file": "LZ_129_Hindenburg.stl",
      "velocity_set": "D3Q27",
      "resolution": 15400,
      "velocity": 7.0,
      "reynolds": 535000000,
      "simulation_time": 5.0
    }},
    "tool_unlock_token": "{TOOL_UNLOCK_TOKEN}"
  }}
}}

### 5. Run Simulation
{{
  "input": {{
    "operation": "run_simulation",
    "config": {{
      "stl_file": "LZ_129_Hindenburg.stl",
      "velocity_set": "D3Q27",
      "resolution": 15400,
      "velocity": 7.0,
      "reynolds": 535000000,
      "simulation_time": 10.0,
      "enable_graphics": true,
      "window_mode": true,
      "enable_subgrid": true,
      "enable_fp16s": true,
      "collision_operator": "SRT",
      "export_path": "output/",
      "angle_of_attack": 0.0
    }},
    "tool_unlock_token": "{TOOL_UNLOCK_TOKEN}"
  }}
}}

## Configuration Parameters

### Required Parameters
- **stl_file**: Path to 3D mesh file (must exist)
- **velocity_set**: D2Q9, D3Q15, D3Q19, or D3Q27 (D3Q27 recommended)
- **resolution**: Grid resolution (higher = more detail, more GPU memory)
- **velocity**: Flow velocity in m/s
- **reynolds**: Reynolds number (Re = velocity × length / kinematic_viscosity)
- **simulation_time**: How long to run simulation in seconds
- **collision_operator**: SRT (standard) or TRT (two-relaxation-time)

### Optional Parameters
- **enable_graphics**: Show interactive 3D visualization (default: false)
- **window_mode**: Use window instead of fullscreen (default: false)
- **enable_subgrid**: Better turbulence modeling (default: false)
- **enable_fp16s**: Use half-precision for memory efficiency (default: false)
- **export_path**: Directory to save results (default: "export/")
- **camera_x/y/z**: Camera position (defaults: 19.0, 19.1, 19.2)
- **angle_of_attack**: Rotation angle in degrees (default: 0.0)

## Examples

### Example 1: Simple Wing Simulation
{{
  "input": {{
    "operation": "run_simulation",
    "config": {{
      "stl_file": "wing.stl",
      "velocity_set": "D3Q19",
      "resolution": 4096,
      "velocity": 25.0,
      "reynolds": 1000000,
      "simulation_time": 5.0,
      "collision_operator": "SRT",
      "enable_graphics": false
    }},
    "tool_unlock_token": "{TOOL_UNLOCK_TOKEN}"
  }}
}}

### Example 2: Hindenburg Airship with Interactive Graphics
{{
  "input": {{
    "operation": "run_simulation",
    "config": {{
      "stl_file": "LZ_129_Hindenburg.stl",
      "velocity_set": "D3Q27",
      "resolution": 15400,
      "velocity": 7.0,
      "reynolds": 535000000,
      "simulation_time": 10.0,
      "enable_graphics": true,
      "window_mode": true,
      "enable_subgrid": true,
      "enable_fp16s": true,
      "collision_operator": "SRT",
      "angle_of_attack": 0.0
    }},
    "tool_unlock_token": "{TOOL_UNLOCK_TOKEN}"
  }}
}}

### Example 3: Quick Benchmark Test
{{
  "input": {{
    "operation": "run_simulation",
    "config": {{
      "stl_file": "sphere.stl",
      "velocity_set": "D3Q19",
      "resolution": 256,
      "velocity": 1.0,
      "reynolds": 100,
      "simulation_time": 1.0,
      "collision_operator": "SRT",
      "enable_graphics": false
    }},
    "tool_unlock_token": "{TOOL_UNLOCK_TOKEN}"
  }}
}}

## Interactive Controls (when graphics enabled)
- **Mouse**: Rotate view
- **WASD**: Move camera
- **Q/E**: Move up/down
- **Space**: Pause/resume simulation
- **R**: Reset camera
- **F1-F12**: Toggle visualization modes
- **ESC**: Exit simulation

## Notes
1. STL files must exist in the current directory or provide full path
2. Higher resolution requires more GPU memory (D3Q27 @ 15400³ needs ~16GB VRAM)
3. Simulation runs in real-time and blocks until completed
4. Results are automatically exported to export_path if specified
5. FluidX3D module must be installed: `pip install fluidx3d`
6. Requires OpenCL runtime (GPU drivers or Intel CPU Runtime)
7. **Known limitation**: Closing the graphics window calls exit() in C++, which may terminate the server process. This is a limitation of the current C++ implementation.

## Velocity Set Comparison
- **D2Q9**: 2D simulations only
- **D3Q15**: Fast, less accurate, low memory
- **D3Q19**: Good balance (standard)
- **D3Q27**: Most accurate, highest memory usage (recommended for research)

## Typical Reynolds Numbers
- **Sphere/cylinder**: 100-1000 (laminar), 10000+ (turbulent)
- **Aircraft/vehicles**: 1,000,000 - 100,000,000
- **Large airships**: 100,000,000 - 1,000,000,000
"""
    }
]

def validate_parameters(input_param: Dict) -> Tuple[Optional[str], Dict]:
    """Validate input parameters against the real_parameters schema."""
    real_params_schema = TOOLS[0]["real_parameters"]
    properties = real_params_schema["properties"]
    required = real_params_schema.get("required", [])
    
    # For readme operation, don't require token
    operation = input_param.get("operation")
    if operation == "readme":
        required = ["operation"]
    
    # Check for unexpected parameters (at top level only)
    expected_params = set(properties.keys())
    provided_params = set(input_param.keys())
    unexpected_params = provided_params - expected_params
    
    if unexpected_params:
        return f"Unexpected parameters provided: {', '.join(sorted(unexpected_params))}. Expected parameters are: {', '.join(sorted(expected_params))}. Please consult the readme.", {}
    
    # Check for missing required parameters
    missing_required = set(required) - provided_params
    if missing_required:
        return f"Missing required parameters: {', '.join(sorted(missing_required))}. Required parameters are: {', '.join(sorted(required))}", {}
    
    # Validate types
    validated = {}
    for param_name, param_schema in properties.items():
        if param_name in input_param:
            value = input_param[param_name]
            expected_type = param_schema.get("type")
            
            # Type validation
            if expected_type == "string" and not isinstance(value, str):
                return f"Parameter '{param_name}' must be a string, got {type(value).__name__}", {}
            elif expected_type == "object" and not isinstance(value, dict):
                return f"Parameter '{param_name}' must be an object/dictionary, got {type(value).__name__}", {}
            elif expected_type == "integer" and not isinstance(value, int):
                return f"Parameter '{param_name}' must be an integer, got {type(value).__name__}", {}
            elif expected_type == "boolean" and not isinstance(value, bool):
                return f"Parameter '{param_name}' must be a boolean, got {type(value).__name__}", {}
            elif expected_type == "number" and not isinstance(value, (int, float)):
                return f"Parameter '{param_name}' must be a number, got {type(value).__name__}", {}
            
            # Enum validation
            if "enum" in param_schema:
                allowed_values = param_schema["enum"]
                if value not in allowed_values:
                    return f"Parameter '{param_name}' must be one of {allowed_values}, got '{value}'", {}
            
            validated[param_name] = value
        elif param_name in required:
            return f"Required parameter '{param_name}' is missing", {}
        else:
            # Use default value if specified
            default_value = param_schema.get("default")
            if default_value is not None:
                validated[param_name] = default_value
    
    return None, validated

def readme(with_readme: bool = True) -> str:
    """Return tool documentation."""
    try:
        if not with_readme:
            return ''
            
        MCPLogger.log(TOOL_LOG_NAME, "Processing readme request")
        return "\n\n" + json.dumps({
            "description": TOOLS[0]["readme"],
            "parameters": TOOLS[0]["real_parameters"]
        }, indent=2)
    except Exception as e:
        MCPLogger.log(TOOL_LOG_NAME, f"Error processing readme request: {str(e)}")
        return ''

def create_error_response(error_msg: str, with_readme: bool = True) -> Dict:
    """Log and create an error response that optionally includes the tool documentation."""
    MCPLogger.log(TOOL_LOG_NAME, f"Error: {error_msg}")
    return {"content": [{"type": "text", "text": f"{error_msg}{readme(with_readme)}"}], "isError": True}

def handle_get_version(params: Dict) -> Dict:
    """Get FluidX3D version information."""
    try:
        if not FLUIDX3D_AVAILABLE:
            return create_error_response("FluidX3D module not available. Install with: pip install fluidx3d", with_readme=False)
        
        config = fx3d.Config()
        version = config.get_version()
        
        MCPLogger.log(TOOL_LOG_NAME, f"FluidX3D version: {version}")
        
        result = {
            "version": version,
            "module_available": True,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
        
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
            "isError": False
        }
        
    except Exception as e:
        return create_error_response(f"Error getting version: {str(e)}", with_readme=False)

def handle_list_devices(params: Dict) -> Dict:
    """List available OpenCL devices."""
    try:
        if not FLUIDX3D_AVAILABLE:
            return create_error_response("FluidX3D module not available. Install with: pip install fluidx3d", with_readme=False)
        
        MCPLogger.log(TOOL_LOG_NAME, "Listing OpenCL devices")
        
        # This would require additional OpenCL introspection
        # For now, return a placeholder
        result = {
            "message": "Device detection not yet implemented. Run a simulation to see detected devices in output.",
            "note": "FluidX3D will automatically detect and use the best available OpenCL device"
        }
        
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
            "isError": False
        }
        
    except Exception as e:
        return create_error_response(f"Error listing devices: {str(e)}", with_readme=False)

def handle_validate_config(params: Dict) -> Dict:
    """Validate simulation configuration without running."""
    try:
        if not FLUIDX3D_AVAILABLE:
            return create_error_response("FluidX3D module not available. Install with: pip install fluidx3d", with_readme=False)
        
        config_params = params.get("config")
        if not config_params:
            return create_error_response("Missing 'config' parameter", with_readme=True)
        
        # Validate required config parameters
        required_config = ["stl_file", "velocity_set", "resolution", "velocity", "reynolds", "simulation_time", "collision_operator"]
        missing = [p for p in required_config if p not in config_params]
        if missing:
            return create_error_response(f"Missing required config parameters: {', '.join(missing)}", with_readme=True)
        
        # Check if STL file exists
        stl_file = config_params["stl_file"]
        if not os.path.exists(stl_file):
            return create_error_response(f"STL file not found: {stl_file}", with_readme=False)
        
        # Validate velocity set
        valid_vsets = ["D2Q9", "D3Q15", "D3Q19", "D3Q27"]
        if config_params["velocity_set"] not in valid_vsets:
            return create_error_response(f"Invalid velocity_set. Must be one of: {', '.join(valid_vsets)}", with_readme=False)
        
        # Validate collision operator
        valid_ops = ["SRT", "TRT"]
        if config_params["collision_operator"] not in valid_ops:
            return create_error_response(f"Invalid collision_operator. Must be one of: {', '.join(valid_ops)}", with_readme=False)
        
        MCPLogger.log(TOOL_LOG_NAME, "Configuration validated successfully")
        
        result = {
            "valid": True,
            "config": config_params,
            "warnings": []
        }
        
        # Add warnings for high memory usage
        if config_params["resolution"] > 10000:
            result["warnings"].append("High resolution may require significant GPU memory (>8GB)")
        
        if config_params["velocity_set"] == "D3Q27" and config_params["resolution"] > 10000:
            result["warnings"].append("D3Q27 with high resolution may require >16GB GPU memory")
        
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
            "isError": False
        }
        
    except Exception as e:
        return create_error_response(f"Error validating configuration: {str(e)}", with_readme=False)

def handle_run_simulation(params: Dict) -> Dict:
    """Run a CFD simulation."""
    try:
        if not FLUIDX3D_AVAILABLE:
            return create_error_response("FluidX3D module not available. Install with: pip install fluidx3d", with_readme=False)
        
        config_params = params.get("config")
        if not config_params:
            return create_error_response("Missing 'config' parameter", with_readme=True)
        
        # Validate required config parameters
        required_config = ["stl_file", "velocity_set", "resolution", "velocity", "reynolds", "simulation_time", "collision_operator"]
        missing = [p for p in required_config if p not in config_params]
        if missing:
            return create_error_response(f"Missing required config parameters: {', '.join(missing)}", with_readme=True)
        
        # Check if STL file exists
        stl_file = config_params["stl_file"]
        if not os.path.exists(stl_file):
            return create_error_response(f"STL file not found: {stl_file}. Please provide full path or ensure file is in current directory.", with_readme=False)
        
        MCPLogger.log(TOOL_LOG_NAME, f"Starting simulation: {stl_file}")
        
        # Build argument list for FluidX3D
        args = [
            f'--{config_params["velocity_set"]}',
            f'--{config_params["collision_operator"]}',
            '-f', stl_file,
            '-r', str(config_params["resolution"]),
            '-u', str(config_params["velocity"]),
            '--re', str(config_params["reynolds"]),
        ]
        
        # Add simulation time (either secs or time steps)
        if "simulation_time" in config_params:
            args.extend(['--secs', str(config_params["simulation_time"])])
        elif "time_steps" in config_params:
            args.extend(['-t', str(config_params["time_steps"])])
        
        # Mesh transformations
        if "rotation_x" in config_params:
            args.extend(['--rotx', str(config_params["rotation_x"])])
        if "rotation_y" in config_params:
            args.extend(['--roty', str(config_params["rotation_y"])])
        if "rotation_z" in config_params:
            args.extend(['--rotz', str(config_params["rotation_z"])])
        if "translate_x" in config_params:
            args.extend(['--trx', str(config_params["translate_x"])])
        if "translate_y" in config_params:
            args.extend(['--try', str(config_params["translate_y"])])
        if "translate_z" in config_params:
            args.extend(['--trz', str(config_params["translate_z"])])
        if "scale" in config_params:
            args.extend(['--scale', str(config_params["scale"])])
        if "angle_of_attack" in config_params:
            args.extend(['--aoa', str(config_params["angle_of_attack"])])
        
        # Simulation box
        if "box_width" in config_params:
            args.extend(['-x', str(config_params["box_width"])])
        if "box_length" in config_params:
            args.extend(['-y', str(config_params["box_length"])])
        if "box_height" in config_params:
            args.extend(['-z', str(config_params["box_height"])])
        
        # Physical parameters
        if "density" in config_params:
            args.extend(['--rho', str(config_params["density"])])
        if "chord_length" in config_params:
            args.extend(['-c', str(config_params["chord_length"])])
        
        # Camera settings
        if "camera_x" in config_params:
            args.extend(['--camx', str(config_params["camera_x"])])
        if "camera_y" in config_params:
            args.extend(['--camy', str(config_params["camera_y"])])
        if "camera_z" in config_params:
            args.extend(['--camz', str(config_params["camera_z"])])
        if "camera_zoom" in config_params:
            args.extend(['--camzoom', str(config_params["camera_zoom"])])
        if "camera_rotation_x" in config_params:
            args.extend(['--camrx', str(config_params["camera_rotation_x"])])
        if "camera_rotation_y" in config_params:
            args.extend(['--camry', str(config_params["camera_rotation_y"])])
        if "camera_fov" in config_params:
            args.extend(['--camfov', str(config_params["camera_fov"])])
        
        # Graphics settings
        if "export_path" in config_params:
            args.extend(['--export', config_params["export_path"]])
        if "fps" in config_params:
            args.extend(['--fps', str(config_params["fps"])])
        if "slomo" in config_params:
            args.extend(['--slomo', str(config_params["slomo"])])
        if "frame_width" in config_params:
            args.extend(['--FRAME_WIDTH', str(config_params["frame_width"])])
        if "frame_height" in config_params:
            args.extend(['--FRAME_HEIGHT', str(config_params["frame_height"])])
        if "background_color" in config_params:
            args.extend(['--BACKGROUND_COLOR', str(config_params["background_color"])])
        if "streamline_sparse" in config_params:
            args.extend(['--STREAMLINE_SPARSE', str(config_params["streamline_sparse"])])
        if "streamline_length" in config_params:
            args.extend(['--STREAMLINE_LENGTH', str(config_params["streamline_length"])])
        if "display" in config_params:
            args.extend(['-d', config_params["display"]])
        
        # Boolean flags
        if config_params.get("window_mode"):
            args.append('--window')
        if config_params.get("wait_on_exit"):
            args.append('--wait')
        if config_params.get("pause_on_start"):
            args.append('--pause')
        if config_params.get("realtime_export"):
            args.append('--realtime')
        if config_params.get("transparency"):
            args.append('--TRANSPARENCY')
        if config_params.get("enable_graphics"):
            args.append('--GRAPHICS')
        if config_params.get("enable_graphics_ascii"):
            args.append('--GRAPHICS_ASCII')
        if config_params.get("enable_subgrid"):
            args.append('--SUBGRID')
        if config_params.get("enable_volume_force"):
            args.append('--VOLUME_FORCE')
        if config_params.get("enable_force_field"):
            args.append('--FORCE_FIELD')
        if config_params.get("enable_particles"):
            args.append('--PARTICLES')
        if config_params.get("enable_temperature"):
            args.append('--TEMPERATURE')
        if config_params.get("enable_update_fields"):
            args.append('--UPDATE_FIELDS')
        if config_params.get("enable_moving_boundaries"):
            args.append('--MOVING_BOUNDARIES')
        if config_params.get("enable_equilibrium_boundaries"):
            args.append('--EQUILIBRIUM_BOUNDARIES')
        if config_params.get("enable_surface"):
            args.append('--SURFACE')
        if config_params.get("enable_fp16s"):
            args.append('--FP16S')
        if config_params.get("enable_fp16c"):
            args.append('--FP16C')
        if config_params.get("enable_benchmark"):
            args.append('--BENCHMARK')
        if config_params.get("enable_floor"):
            args.append('--floor')
        if config_params.get("allow_sleep"):
            args.append('--allowsleep')
        
        # Create config and parse arguments
        config = fx3d.Config()
        config.parse_args(args)
        
        MCPLogger.log(TOOL_LOG_NAME, f"Running simulation with args: {' '.join(args)}")
        
        # Run simulation (blocks until complete)
        # Note: If the user closes the graphics window, C++ may call exit() which terminates the process
        # This is a limitation of the current C++ implementation
        start_time = time.time()
        
        try:
            config.run_simulation()
        except SystemExit as se:
            # Catch exit() calls from C++ code
            elapsed = time.time() - start_time
            MCPLogger.log(TOOL_LOG_NAME, f"Simulation exited (possibly user closed window) after {elapsed:.1f}s")
            result = {
                "status": "exited",
                "elapsed_time": round(elapsed, 2),
                "config": config_params,
                "message": f"Simulation exited after {elapsed:.1f} seconds (exit code: {se.code})",
                "note": "User may have closed the graphics window"
            }
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False
            }
        
        elapsed = time.time() - start_time
        MCPLogger.log(TOOL_LOG_NAME, f"Simulation completed in {elapsed:.1f}s")
        
        result = {
            "status": "completed",
            "elapsed_time": round(elapsed, 2),
            "config": config_params,
            "message": f"Simulation completed successfully in {elapsed:.1f} seconds"
        }
        
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
            "isError": False
        }
        
    except SystemExit as se:
        # Catch any other exit() calls
        MCPLogger.log(TOOL_LOG_NAME, f"Caught SystemExit: {se.code}")
        result = {
            "status": "exited",
            "message": f"Process attempted to exit with code {se.code}",
            "note": "This is likely from closing the graphics window"
        }
        return {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
            "isError": False
        }
    except Exception as e:
        return create_error_response(f"Error running simulation: {str(e)}", with_readme=False)

def handle_fluidx3d(input_param: Dict) -> Dict:
    """Handle FluidX3D tool operations via MCP interface."""
    try:
        # Pop off synthetic handler_info parameter early
        handler_info = input_param.pop('handler_info', None)
        
        if isinstance(input_param, dict) and "input" in input_param:
            input_param = input_param["input"]

        # Handle readme operation first (before token validation)
        if isinstance(input_param, dict) and input_param.get("operation") == "readme":
            return {
                "content": [{"type": "text", "text": readme(True)}],
                "isError": False
            }
            
        # Validate input structure
        if not isinstance(input_param, dict):
            return create_error_response("Invalid input format. Expected dictionary with tool parameters.", with_readme=True)
            
        # Check for token
        provided_token = input_param.get("tool_unlock_token")
        if provided_token != TOOL_UNLOCK_TOKEN:
            return create_error_response("Invalid or missing tool_unlock_token. Please call readme operation first to get the token:", with_readme=True)

        # Validate all parameters using schema
        error_msg, validated_params = validate_parameters(input_param)
        if error_msg:
            return create_error_response(error_msg, with_readme=True)

        # Extract validated parameters
        operation = validated_params.get("operation")
        
        # Handle operations
        if operation == "get_version":
            return handle_get_version(validated_params)
        elif operation == "list_devices":
            return handle_list_devices(validated_params)
        elif operation == "validate_config":
            return handle_validate_config(validated_params)
        elif operation == "run_simulation":
            return handle_run_simulation(validated_params)
        elif operation == "readme":
            return {
                "content": [{"type": "text", "text": readme(True)}],
                "isError": False
            }
        else:
            valid_operations = TOOLS[0]["real_parameters"]["properties"]["operation"]["enum"]
            return create_error_response(f"Unknown operation: '{operation}'. Available operations: {', '.join(valid_operations)}", with_readme=True)
            
    except Exception as e:
        return create_error_response(f"Error in fluidx3d operation: {str(e)}", with_readme=True)

# Map of tool names to their handlers
HANDLERS = {
    "fluidx3d": handle_fluidx3d
}
