#!/usr/bin/env python3
"""
Simple build script for py_gauge module
"""
import os
import sys
import subprocess

# Get paths
core_dir = os.path.join(os.path.dirname(__file__), '..', 'core')
pybind11_dir = subprocess.check_output([sys.executable, "-c", "import pybind11; print(pybind11.get_include())"], text=True).strip()
python_inc = subprocess.check_output([sys.executable, "-c", "import sysconfig; print(sysconfig.get_path('include'))"], text=True).strip()

# Build command
compile_cmd = [
    "g++", "-O3", "-march=native", "-fPIC", "-std=c++17", "-shared",
    "-I" + core_dir,
    "-I" + pybind11_dir,
    "-I" + python_inc,
    "-o", "py_gauge.so",
    "py_gauge.cpp",
    os.path.join(core_dir, "gauge_node.cpp"),
]

print("Building py_gauge module...")
print(" ".join(compile_cmd))

result = subprocess.run(compile_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("STDERR:", result.stderr)
    print("STDOUT:", result.stdout)
    sys.exit(1)

print("✓ Build successful: py_gauge.so")
