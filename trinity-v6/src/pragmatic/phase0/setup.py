#!/usr/bin/env python3
"""
Setup script for py_gauge module - Phase 0 Proof of Concept
Build with: python3 setup.py build_ext --inplace
"""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import pybind11
from setuptools import setup, Extension
import sys
import os

# Get the directory containing this setup.py
this_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(this_dir, '..', 'core')

ext_modules = [
    Extension(
        "py_gauge",
        sources=[
            "py_gauge.cpp",
            os.path.join(core_dir, "gauge_node.cpp"),
        ],
        include_dirs=[
            core_dir,
            pybind11.get_include(),
        ],
        language='c++',
        extra_compile_args=['-O3', '-march=native', '-fPIC', '-std=c++17'],
    ),
]

setup(
    name="py_gauge",
    version="0.1.0",
    author="Pragmatic Geometric AI Team",
    description="Pybind11 bindings for GaugeNode128",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
)
