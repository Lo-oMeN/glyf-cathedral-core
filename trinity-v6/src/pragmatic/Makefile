# Pragmatic Geometric AI - Makefile
# Buildable on Raspberry Pi 4 or RTX 4090

CC = gcc
CFLAGS = -Wall -Wextra -O3 -std=c11 -fPIC
LDFLAGS = -lm

# Directories
SRC_DIR = src/pragmatic
CORE_DIR = $(SRC_DIR)/core
MGIS_DIR = $(SRC_DIR)/mgis
INFERENCE_DIR = $(SRC_DIR)/inference
BUILD_DIR = build

# Targets
LIBRARY = $(BUILD_DIR)/libgauge.so
STATIC_LIB = $(BUILD_DIR)/libgauge.a
TEST_BIN = $(BUILD_DIR)/test_gauge

# Source files
CORE_SRCS = $(CORE_DIR)/gauge_node.c
CORE_OBJS = $(patsubst %.c,$(BUILD_DIR)/%.o,$(notdir $(CORE_SRCS)))

# Python extension (optional)
PYBIND_FLAGS = $(shell python3 -m pybind11 --includes 2>/dev/null || echo "")
PYTHON_EXT = $(BUILD_DIR)/gauge_node_ext.so

# Default target
all: directories $(LIBRARY) $(STATIC_LIB) $(TEST_BIN)

# Create build directories
directories:
	@mkdir -p $(BUILD_DIR)

# Pattern rule for core objects
$(BUILD_DIR)/%.o: $(CORE_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Shared library
$(LIBRARY): $(CORE_OBJS)
	$(CC) -shared -o $@ $^ $(LDFLAGS)

# Static library
$(STATIC_LIB): $(CORE_OBJS)
	ar rcs $@ $^

# Test binary
test_src = tests/test_gauge_node.c
$(TEST_BIN): $(test_src) $(STATIC_LIB)
	$(CC) $(CFLAGS) -o $@ $< -L$(BUILD_DIR) -lgauge $(LDFLAGS)

# Python extension (optional, requires pybind11)
python: $(PYTHON_EXT)

$(PYTHON_EXT): $(CORE_DIR)/py_gauge.cpp $(STATIC_LIB)
	$(CXX) -O3 -Wall -shared -std=c++17 -fPIC $(PYBIND_FLAGS) \
		$< -o $@ -L$(BUILD_DIR) -lgauge $(LDFLAGS)

# Run tests
test: $(TEST_BIN)
	./$(TEST_BIN)

# Pi 4 specific build (ARM optimizations)
pi4: CFLAGS += -march=armv8-a+crc -mtune=cortex-a72
pi4: all

# Clean
clean:
	rm -rf $(BUILD_DIR)

# Install (system-wide)
install: all
	cp $(LIBRARY) /usr/local/lib/
	cp $(CORE_DIR)/gauge_node.h /usr/local/include/
	ldconfig

# Development install (local)
dev-install: all
	pip install -e .

# Format code
format:
	clang-format -i $(CORE_DIR)/*.c $(CORE_DIR)/*.h

# Lint
lint:
	cppcheck --enable=all $(CORE_DIR)

# Documentation
docs:
	doxygen Doxyfile 2>/dev/null || echo "Doxygen not installed"

.PHONY: all directories python test pi4 clean install dev-install format lint docs
