cmake_minimum_required(VERSION 3.22.1)
project("glyf-cathedral")

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find packages
find_package(game-activity REQUIRED CONFIG)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Native library for wgpu rendering
add_library(
    glyf-native
    SHARED
    native-renderer.cpp
)

# Link libraries
target_link_libraries(
    glyf-native
    game-activity::game-activity
    android
    log
    EGL
    GLESv3
)

# Compiler flags for performance
target_compile_options(
    glyf-native
    PRIVATE
    -O3
    -DNDEBUG
    -ffast-math
    -funroll-loops
)
