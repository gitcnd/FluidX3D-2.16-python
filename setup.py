"""
FluidX3D Python Module Setup
Builds the pybind11 extension module for FluidX3D
"""
import sys
import os
from pathlib import Path
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class get_pybind_include:
    """Helper class to determine the pybind11 include path"""
    def __str__(self):
        import pybind11
        return pybind11.get_include()

# Source files from FluidX3D
# Phase 3: Link ALL FluidX3D source files so we can call main_setup()
fluidx3d_sources = [
    'src/graphics.cpp',
    'src/info.cpp',
    'src/kernel.cpp',
    'src/lbm.cpp',
    'src/lodepng.cpp',
    'src/main.cpp',
    'src/setup.cpp',
    'src/shapes.cpp',
    'src/python_bindings_full.cpp',  # Our Python wrapper
]

ext_modules = [
    Extension(
        'fluidx3d',
        sources=fluidx3d_sources,
        include_dirs=[
            get_pybind_include(),
            'src/OpenCL/include',
        ],
        library_dirs=['src/OpenCL/lib'],
        libraries=['OpenCL', 'user32', 'gdi32', 'kernel32'],  # OpenCL + Windows GUI libs
        language='c++',
        extra_compile_args=[
            '/std:c++17',
            '/EHsc',
            '/MD',
            '/O2',
            '/fp:fast'
        ],
    ),
]

setup(
    name='fluidx3d',
    version='2.16.3',
    author='Dr. Moritz Lehmann (original), AuraFriday (Python bindings)',
    author_email='',  # Add your email if you want
    description='Real-time interactive Lattice Boltzmann CFD with full GPU acceleration and graphics',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gitcnd/FluidX3D-2.16-python',
    project_urls={
        'Bug Reports': 'https://github.com/gitcnd/FluidX3D-2.16-python/issues',
        'Source': 'https://github.com/gitcnd/FluidX3D-2.16-python',
        'Original FluidX3D': 'https://github.com/ProjectPhysX/FluidX3D',
    },
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.6.0'],
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: C++',
        'Operating System :: Microsoft :: Windows',
        'Environment :: GPU :: NVIDIA CUDA',
    ],
    keywords='cfd, lattice-boltzmann, fluid-dynamics, gpu, opencl, computational-physics, simulation, interactive',
    zip_safe=False,
)

