cmake_minimum_required(VERSION 3.14)
project(looman VERSION 0.1.0 LANGUAGES C CXX)

# C++17 required
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# C11 required
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Options
option(LLAMA_CUDA "Enable CUDA support" OFF)
option(LLAMA_METAL "Enable Metal support (macOS)" OFF)

# Find packages
find_package(Threads REQUIRED)

# llama.cpp paths
# In production, this would be found via find_package(llama)
# For now, assume llama.cpp is in a sibling directory or system
set(LLAMA_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../../llama.cpp)

# Check if llama.cpp exists
if(EXISTS ${LLAMA_ROOT}/include/llama.h)
    message(STATUS "Found llama.cpp at ${LLAMA_ROOT}")
    include_directories(${LLAMA_ROOT}/include)
    link_directories(${LLAMA_ROOT}/build)
    set(LLAMA_FOUND TRUE)
else()
    message(WARNING "llama.cpp not found at ${LLAMA_ROOT}")
    message(STATUS "Building without llama.cpp (stub mode)")
    set(LLAMA_FOUND FALSE)
endif()

# Core library (Phase 0)
add_library(gauge_core STATIC
    ../core/gauge_node.c
    ../core/gauge_node.h
)

target_include_directories(gauge_core PUBLIC
    ../core
)

target_link_libraries(gauge_core
    m  # Math library
)

# Phase 2: Looman inference
add_executable(looman
    loom_cli.cpp
    llama_wrapper.cpp
    llama_wrapper.h
)

target_include_directories(looman PRIVATE
    ../core
)

target_link_libraries(looman
    gauge_core
    Threads::Threads
)

# Link llama.cpp if available
if(LLAMA_FOUND)
    target_link_libraries(looman llama)
    target_compile_definitions(looman PRIVATE HAS_LLAMA=1)
else()
    target_compile_definitions(looman PRIVATE STUB_MODE=1)
endif()

# Compiler warnings
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(looman PRIVATE
        -Wall
        -Wextra
        -Wpedantic
    )
endif()

# Install
install(TARGETS looman
    RUNTIME DESTINATION bin
)

# Tests
enable_testing()

add_executable(test_phase2
    test_phase2.cpp
    llama_wrapper.cpp
)

target_link_libraries(test_phase2
    gauge_core
    Threads::Threads
)

if(LLAMA_FOUND)
    target_link_libraries(test_phase2 llama)
endif()

add_test(NAME phase2 COMMAND test_phase2)

# Status message
message(STATUS "")
message(STATUS "Looman Configuration:")
message(STATUS "  llama.cpp: ${LLAMA_FOUND}")
message(STATUS "  CUDA: ${LLAMA_CUDA}")
message(STATUS "  Metal: ${LLAMA_METAL}")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "")
