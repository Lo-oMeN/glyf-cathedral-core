cmake_minimum_required(VERSION 3.14)
project(looman VERSION 0.2.0 LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(Threads REQUIRED)

# Find llama.cpp
# First try pkg-config
find_package(PkgConfig)
if(PkgConfig_FOUND)
    pkg_check_modules(LLAMA llama)
endif()

# If not found via pkg-config, try manual find
if(NOT LLAMA_FOUND)
    # Try to find llama.cpp in common locations
    find_path(LLAMA_INCLUDE_DIR llama.h
        PATHS
            /usr/include
            /usr/local/include
            /opt/llama.cpp/include
            ${CMAKE_CURRENT_SOURCE_DIR}/../../llama.cpp
            ${CMAKE_CURRENT_SOURCE_DIR}/../../llama.cpp/include
            ${CMAKE_CURRENT_SOURCE_DIR}/../../../llama.cpp
            ${CMAKE_CURRENT_SOURCE_DIR}/../../../llama.cpp/include
        DOC "Path to llama.h"
    )
    
    find_library(LLAMA_LIBRARY llama
        PATHS
            /usr/lib
            /usr/local/lib
            /opt/llama.cpp/lib
            ${CMAKE_CURRENT_SOURCE_DIR}/../../llama.cpp/build
            ${CMAKE_CURRENT_SOURCE_DIR}/../../llama.cpp/build/src
            ${CMAKE_CURRENT_SOURCE_DIR}/../../../llama.cpp/build
            ${CMAKE_CURRENT_SOURCE_DIR}/../../../llama.cpp/build/src
        DOC "Path to llama library"
    )
    
    if(LLAMA_INCLUDE_DIR AND LLAMA_LIBRARY)
        set(LLAMA_FOUND TRUE)
        set(LLAMA_INCLUDE_DIRS ${LLAMA_INCLUDE_DIR})
        set(LLAMA_LIBRARIES ${LLAMA_LIBRARY})
        message(STATUS "Found llama.cpp: ${LLAMA_LIBRARY}")
        message(STATUS "Found llama.h: ${LLAMA_INCLUDE_DIR}")
    else()
        message(WARNING "llama.cpp not found. Please install llama.cpp or set LLAMA_INCLUDE_DIR and LLAMA_LIBRARY")
    endif()
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../core
)

if(LLAMA_FOUND)
    include_directories(${LLAMA_INCLUDE_DIRS})
endif()

# Source files
set(LOOMAN_SOURCES
    loom_cli.cpp
    llama_wrapper.cpp
    attention_mask.c
    ../core/gauge_node.c
)

# Create main executable
add_executable(looman ${LOOMAN_SOURCES})

# Link libraries
target_link_libraries(looman
    Threads::Threads
)

if(LLAMA_FOUND)
    target_link_libraries(looman ${LLAMA_LIBRARIES})
    target_compile_definitions(looman PRIVATE HAS_LLAMA_CPP=1)
else()
    message(WARNING "Building without llama.cpp support (stub mode)")
    target_compile_definitions(looman PRIVATE HAS_LLAMA_CPP=0)
endif()

# Set compiler flags for optimization
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(looman PRIVATE -O3 -march=native -ffast-math)
elseif(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_options(looman PRIVATE -g -O0 -Wall -Wextra)
else()
    target_compile_options(looman PRIVATE -O2 -Wall)
endif()

# Test executable
set(TEST_SOURCES
    test_phase2.cpp
    llama_wrapper.cpp
    attention_mask.c
    ../core/gauge_node.c
)

add_executable(test_phase2 ${TEST_SOURCES})
target_link_libraries(test_phase2 Threads::Threads)

if(LLAMA_FOUND)
    target_link_libraries(test_phase2 ${LLAMA_LIBRARIES})
    target_compile_definitions(test_phase2 PRIVATE HAS_LLAMA_CPP=1)
else()
    target_compile_definitions(test_phase2 PRIVATE HAS_LLAMA_CPP=0)
endif()

# Install targets
install(TARGETS looman
    RUNTIME DESTINATION bin
)

# Print configuration
message(STATUS "")
message(STATUS "Looman Inference Configuration:")
message(STATUS "  Version: ${PROJECT_VERSION}")
message(STATUS "  C Standard: ${CMAKE_C_STANDARD}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  llama.cpp: ${LLAMA_FOUND}")
if(LLAMA_FOUND)
    message(STATUS "  llama.cpp include: ${LLAMA_INCLUDE_DIRS}")
    message(STATUS "  llama.cpp library: ${LLAMA_LIBRARIES}")
endif()
message(STATUS "")
