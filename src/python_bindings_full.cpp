// Python bindings for FluidX3D using pybind11
// Phase 3: Call WinMain() directly to get full graphics support!
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>
#include <thread>
#include "utilities.hpp"

#if defined(_WIN32)
#include <windows.h>
// Declare WinMain so we can call it
extern "C" INT WINAPI WinMain(_In_ HINSTANCE hInstance, _In_opt_ HINSTANCE hPrevInstance, _In_ PSTR lpCmdLine, _In_ INT nCmdShow);
#endif

namespace py = pybind11;

// External variables that are defined in other FluidX3D source files
extern uint velocity_set, dimensions, transfers;  // Defined in lbm.cpp
extern bool key_P, key_O;  // Defined in graphics.cpp
extern vector<string> main_arguments;  // Defined in graphics.cpp
extern cxxopts::ParseResult g_args;  // Defined in main.cpp
extern int fpxxsize;  // Defined in main.cpp
extern string EXPORT_PATH;  // Defined in main.cpp

// Define the global variables that we need to provide (only those NOT in main.cpp)
bool running = true;

// Forward declare main_setup - this is defined in setup.cpp
void main_setup();

// NOTE: main_label, main_graphics, main_physics are now defined in main.cpp

// FluidX3D argument parser and configuration
class FluidX3DConfig {
private:
    cxxopts::ParseResult args;
    bool parsed = false;
    
public:
    FluidX3DConfig() {}
    
    // Parse arguments using the full FluidX3D argument structure
    void parse_args(const std::vector<std::string>& arg_list) {
        // Convert vector<string> to argc/argv format
        std::vector<std::string> args_copy = arg_list;
        std::vector<char*> argv_vec;
        argv_vec.push_back(const_cast<char*>("fluidx3d"));  // Program name
        
        for (auto& arg : args_copy) {
            argv_vec.push_back(const_cast<char*>(arg.c_str()));
        }
        
        int argc = static_cast<int>(argv_vec.size());
        char** argv = argv_vec.data();
        
        // Create cxxopts with all FluidX3D arguments
        cxxopts::Options options(argv[0], "Lattice Boltzmann CFD software by Dr. Moritz Lehmann");
        
        // Add all the options (matching utilities.hpp)
        options.add_options()
            ("h,help", "Print help")
            ("f,file", "input .stl mesh Filename", cxxopts::value<std::string>()->default_value("input.stl"))
            ("rotx", "X deg rotation of input mesh", cxxopts::value<float>()->default_value("0.0"))
            ("roty", "Y deg rotation of input mesh", cxxopts::value<float>()->default_value("0.0"))
            ("rotz", "Z deg rotation of input mesh", cxxopts::value<float>()->default_value("0.0"))
            ("trx", "X translate input mesh", cxxopts::value<float>()->default_value("0.0"))
            ("try", "Y translate input mesh", cxxopts::value<float>()->default_value("0.0"))
            ("trz", "Z translate input mesh", cxxopts::value<float>()->default_value("0.0"))
            ("x,width", "X width of sim box", cxxopts::value<float>()->default_value("1.0"))
            ("y,length", "Y length of sim box", cxxopts::value<float>()->default_value("1.0"))
            ("z,height", "Z height of sim box", cxxopts::value<float>()->default_value("1.0"))
            ("r,resolution", "Resolution", cxxopts::value<unsigned int>()->default_value("4096"))
            ("re", "Reynolds number", cxxopts::value<float>()->default_value("100000.0"))
            ("rho", "Density kg/m^3", cxxopts::value<float>()->default_value("1.2226"))
            ("u", "Velocity in m/s", cxxopts::value<float>()->default_value("5.0"))
            ("c,cord", "Cord (length of STL) in meters", cxxopts::value<float>()->default_value("1.0"))
            ("t,time", "Time", cxxopts::value<unsigned int>()->default_value("10000"))
            ("s,secs", "Seconds", cxxopts::value<float>()->default_value("10.0"))
            ("scale", "Scale", cxxopts::value<float>()->default_value("0.9"))
            ("a,aoa", "Angle of attack degrees (- to climb)", cxxopts::value<float>()->default_value("0.0"))
            ("camx", "Camera X", cxxopts::value<float>()->default_value("19.0"))
            ("camy", "Camera Y", cxxopts::value<float>()->default_value("19.1"))
            ("camz", "Camera Z", cxxopts::value<float>()->default_value("19.2"))
            ("camzoom", "Camera Zoom", cxxopts::value<float>()->default_value("1.0"))
            ("camrx", "Camera Rotation X", cxxopts::value<float>()->default_value("33.0"))
            ("camry", "Camera Rotation Y", cxxopts::value<float>()->default_value("42.0"))
            ("camfov", "Camera Field of View", cxxopts::value<float>()->default_value("68.0"))
            ("w,window", "Enable window instead of fullscreen mode", cxxopts::value<bool>()->default_value("false"))
            ("wait", "Wait for keypress before ending", cxxopts::value<bool>()->default_value("false"))
            ("pause", "Do not auto-start the simulation", cxxopts::value<bool>()->default_value("false"))
            ("fps", "Frames per Second for video output", cxxopts::value<float>()->default_value("25.0"))
            ("realtime", "Save every frame to video output", cxxopts::value<bool>()->default_value("false"))
            ("slomo", "What speed the video plays at 1=realtime 10=10x slower", cxxopts::value<float>()->default_value("1.0"))
            ("export", "Folder name to save images and data into", cxxopts::value<std::string>()->default_value("export/"))
            ("SUBGRID", "Use SUBGRID", cxxopts::value<bool>()->default_value("false"))
            ("VOLUME_FORCE", "Use VOLUME_FORCE", cxxopts::value<bool>()->default_value("false"))
            ("FORCE_FIELD", "Use FORCE_FIELD", cxxopts::value<bool>()->default_value("false"))
            ("PARTICLES", "Use PARTICLES", cxxopts::value<bool>()->default_value("false"))
            ("TEMPERATURE", "Use TEMPERATURE", cxxopts::value<bool>()->default_value("false"))
            ("UPDATE_FIELDS", "Use UPDATE_FIELDS", cxxopts::value<bool>()->default_value("false"))
            ("MOVING_BOUNDARIES", "Use MOVING_BOUNDARIES", cxxopts::value<bool>()->default_value("false"))
            ("EQUILIBRIUM_BOUNDARIES", "Use EQUILIBRIUM_BOUNDARIES", cxxopts::value<bool>()->default_value("false"))
            ("SURFACE", "Use SURFACE", cxxopts::value<bool>()->default_value("false"))
            ("FP16S", "Use FP16S", cxxopts::value<bool>()->default_value("false"))
            ("FP16C", "Use FP16C", cxxopts::value<bool>()->default_value("false"))
            ("BENCHMARK", "Run GPU Benchmark", cxxopts::value<bool>()->default_value("false"))
            ("GRAPHICS", "Use interactive graphics", cxxopts::value<bool>()->default_value("false"))
            ("GRAPHICS_ASCII", "Use interactive console graphics", cxxopts::value<bool>()->default_value("false"))
            ("FRAME_WIDTH", "Screen or Window resolution width", cxxopts::value<int>()->default_value("1920"))
            ("FRAME_HEIGHT", "Screen or Window resolution height", cxxopts::value<int>()->default_value("1080"))
            ("BACKGROUND_COLOR", "Screen background color", cxxopts::value<int>()->default_value("0x000000"))
            ("STREAMLINE_SPARSE", "Streamlines spacing", cxxopts::value<int>()->default_value("8"))
            ("STREAMLINE_LENGTH", "Streamline length", cxxopts::value<int>()->default_value("128"))
            ("TRANSPARENCY", "Transparency", cxxopts::value<bool>()->default_value("0"))
            ("D2Q9", "Use D2Q9", cxxopts::value<bool>()->default_value("false"))
            ("D3Q15", "Use D3Q15", cxxopts::value<bool>()->default_value("false"))
            ("D3Q19", "Use D3Q19", cxxopts::value<bool>()->default_value("false"))
            ("D3Q27", "Use D3Q27", cxxopts::value<bool>()->default_value("false"))
            ("SRT", "Use SRT", cxxopts::value<bool>()->default_value("false"))
            ("TRT", "Use TRT", cxxopts::value<bool>()->default_value("false"))
            ("floor", "Insert a solid floor", cxxopts::value<bool>()->default_value("false"))
            ("allowsleep", "Do not prevent PC from sleeping", cxxopts::value<bool>()->default_value("false"))
            ("d,display", "Display", cxxopts::value<std::string>()->default_value("0,1"));
        
        // Parse the arguments
        args = options.parse(argc, argv);
        
        // Validate velocity set selection
        int count = (args["D2Q9"].as<bool>() ? 1 : 0) + 
                    (args["D3Q15"].as<bool>() ? 1 : 0) +
                    (args["D3Q19"].as<bool>() ? 1 : 0) + 
                    (args["D3Q27"].as<bool>() ? 1 : 0);
        
        if (count == 0) {
            throw std::runtime_error("Must pick one of --D3Q15 --D3Q19 --D3Q27 or --D2Q9");
        } else if (count > 1) {
            throw std::runtime_error("Can only pick one velocity set (--D3Q15, --D3Q19, --D3Q27, or --D2Q9)");
        }
        
        parsed = true;
    }
    
    // Get string parameter
    std::string get_string(const std::string& key) const {
        if (!parsed) throw std::runtime_error("Arguments not parsed yet. Call parse_args() first.");
        return args[key].as<std::string>();
    }
    
    // Get float parameter
    float get_float(const std::string& key) const {
        if (!parsed) throw std::runtime_error("Arguments not parsed yet. Call parse_args() first.");
        return args[key].as<float>();
    }
    
    // Get int parameter
    int get_int(const std::string& key) const {
        if (!parsed) throw std::runtime_error("Arguments not parsed yet. Call parse_args() first.");
        return args[key].as<int>();
    }
    
    // Get uint parameter
    unsigned int get_uint(const std::string& key) const {
        if (!parsed) throw std::runtime_error("Arguments not parsed yet. Call parse_args() first.");
        return args[key].as<unsigned int>();
    }
    
    // Get bool parameter
    bool get_bool(const std::string& key) const {
        if (!parsed) throw std::runtime_error("Arguments not parsed yet. Call parse_args() first.");
        return args[key].as<bool>();
    }
    
    // Get velocity set name
    std::string get_velocity_set() const {
        if (!parsed) throw std::runtime_error("Arguments not parsed yet. Call parse_args() first.");
        if (args["D2Q9"].as<bool>()) return "D2Q9";
        if (args["D3Q15"].as<bool>()) return "D3Q15";
        if (args["D3Q19"].as<bool>()) return "D3Q19";
        if (args["D3Q27"].as<bool>()) return "D3Q27";
        return "NONE";
    }
    
    // Get all parameters as a Python dict
    py::dict to_dict() const {
        if (!parsed) throw std::runtime_error("Arguments not parsed yet. Call parse_args() first.");
        
        py::dict result;
        result["file"] = args["file"].as<std::string>();
        result["rotx"] = args["rotx"].as<float>();
        result["roty"] = args["roty"].as<float>();
        result["rotz"] = args["rotz"].as<float>();
        result["resolution"] = args["resolution"].as<unsigned int>();
        result["reynolds"] = args["re"].as<float>();
        result["velocity"] = args["u"].as<float>();
        result["secs"] = args["secs"].as<float>();
        result["velocity_set"] = get_velocity_set();
        result["SUBGRID"] = args["SUBGRID"].as<bool>();
        result["FP16S"] = args["FP16S"].as<bool>();
        result["EQUILIBRIUM_BOUNDARIES"] = args["EQUILIBRIUM_BOUNDARIES"].as<bool>();
        // Add more as needed
        
        return result;
    }
    
    std::string get_version() const {
        return "2.16.0-python-phase3";
    }
    
    // Run the simulation by calling WinMain() directly - just like the .exe does!
    void run_simulation() {
        if (!parsed) {
            throw std::runtime_error("Arguments not parsed yet. Call parse_args() first.");
        }
        
        // Set the global g_args that the simulation will read from
        g_args = args;
        
        // Set main_arguments (some code paths check this)
        main_arguments = std::vector<std::string>();  // Empty for Python
        
        // Set global variables based on parsed arguments
        if (args["FP16S"].as<bool>() || args["FP16C"].as<bool>()) {
            fpxxsize = 16;
        } else {
            fpxxsize = 32;
        }
        
        if (args["D2Q9"].as<bool>()) {
            velocity_set = 9u;
            dimensions = 2u;
            transfers = 3u;
        } else if (args["D3Q15"].as<bool>()) {
            velocity_set = 15u;
            dimensions = 3u;
            transfers = 5u;
        } else if (args["D3Q19"].as<bool>()) {
            velocity_set = 19u;
            dimensions = 3u;
            transfers = 5u;
        } else if (args["D3Q27"].as<bool>()) {
            velocity_set = 27u;
            dimensions = 3u;
            transfers = 9u;
        }
        
        EXPORT_PATH = args["export"].as<std::string>();
        key_P = !args["pause"].as<bool>();  // key_P=true means not paused
        
        // Call WinMain() directly - this creates the window and runs everything!
        // This is EXACTLY what the .exe does when you run it!
#if defined(_WIN32)
        HINSTANCE hInstance = GetModuleHandle(NULL);  // Get our module handle
        
        // Release Python GIL so the Windows message pump can run
        py::gil_scoped_release release;
        WinMain(hInstance, NULL, NULL, SW_SHOW);  // Call WinMain directly!
        py::gil_scoped_acquire acquire;
#else
        throw std::runtime_error("Interactive graphics only supported on Windows!");
#endif
    }
};

// Python module definition
PYBIND11_MODULE(fluidx3d, m) {
    m.doc() = "FluidX3D - Lattice Boltzmann CFD Python module (Phase 2: Full argument parsing)";
    
    py::class_<FluidX3DConfig>(m, "Config")
        .def(py::init<>())
        .def("parse_args", &FluidX3DConfig::parse_args,
             "Parse FluidX3D command-line arguments",
             py::arg("args"))
        .def("get_string", &FluidX3DConfig::get_string,
             "Get string parameter",
             py::arg("key"))
        .def("get_float", &FluidX3DConfig::get_float,
             "Get float parameter",
             py::arg("key"))
        .def("get_int", &FluidX3DConfig::get_int,
             "Get int parameter",
             py::arg("key"))
        .def("get_uint", &FluidX3DConfig::get_uint,
             "Get unsigned int parameter",
             py::arg("key"))
        .def("get_bool", &FluidX3DConfig::get_bool,
             "Get bool parameter",
             py::arg("key"))
        .def("get_velocity_set", &FluidX3DConfig::get_velocity_set,
             "Get selected velocity set name")
        .def("to_dict", &FluidX3DConfig::to_dict,
             "Get all parameters as a Python dictionary")
        .def("get_version", &FluidX3DConfig::get_version,
             "Get module version")
        .def("run_simulation", &FluidX3DConfig::run_simulation,
             "Run the FluidX3D simulation (calls main_setup())");
    
    // Module-level version info
    m.attr("__version__") = "2.16.0-python-phase3";
    m.attr("__author__") = "Dr. Moritz Lehmann (original), cnd (Python bindings)";
}

