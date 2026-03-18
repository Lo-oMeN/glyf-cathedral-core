# Test Automation Framework Reference

Detailed reference for supported test frameworks and their configurations.

## Python (pytest)

### Dependencies

```bash
pip install pytest coverage pytest-benchmark mutmut
```

### Project Structure

```
myproject/
├── mypackage/
│   ├── __init__.py
│   └── module.py
├── tests/
│   ├── __init__.py
│   └── test_module.py
├── pytest.ini (optional)
└── pyproject.toml (optional)
```

### pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### Coverage Configuration

In `pyproject.toml`:
```toml
[tool.coverage.run]
source = ["mypackage"]
omit = ["*/tests/*", "*/test_*"]

[tool.coverage.report]
show_missing = true
skip_covered = false
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_module.py

# Run with coverage
pytest --cov=mypackage --cov-report=term-missing

# Run benchmarks
pytest --benchmark-only
```

## JavaScript/TypeScript (Jest)

### Dependencies

```bash
npm install --save-dev jest @types/jest nyc
# or
yarn add -D jest @types/jest nyc
```

### Project Structure

```
myproject/
├── src/
│   └── module.js
├── tests/
│   └── module.test.js
├── package.json
└── jest.config.js (optional)
```

### package.json Configuration

```json
{
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage",
    "test:watch": "jest --watch"
  },
  "jest": {
    "testEnvironment": "node",
    "coverageDirectory": "coverage",
    "collectCoverageFrom": [
      "src/**/*.js",
      "!src/**/*.test.js"
    ]
  }
}
```

### Jest Configuration (jest.config.js)

```javascript
module.exports = {
  testEnvironment: 'node',
  coverageProvider: 'v8',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/**/*.test.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
jest tests/module.test.js

# Run in watch mode
jest --watch
```

### Alternative: Vitest

Vitest is a fast Vite-native test runner:

```bash
npm install --save-dev vitest @vitest/coverage-v8
```

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html']
    }
  }
});
```

## Go (testing)

### Project Structure

```
myproject/
├── go.mod
├── main.go
└── main_test.go
```

### go.mod

```
module myproject

go 1.21
```

### Test File Pattern

Go tests follow the `_test.go` suffix convention:
- `foo.go` → `foo_test.go`
- Tests functions start with `Test` (e.g., `TestFoo`)
- Benchmark functions start with `Benchmark` (e.g., `BenchmarkFoo`)

### Table-Driven Tests

Go idiomatic pattern for multiple test cases:

```go
func TestFunction(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
        wantErr  bool
    }{
        {
            name:     "valid case",
            input:    "test",
            expected: "result",
            wantErr:  false,
        },
        {
            name:     "error case",
            input:    "invalid",
            expected: "",
            wantErr:  true,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Function(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("Function() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if result != tt.expected {
                t.Errorf("Function() = %v, want %v", result, tt.expected)
            }
        })
    }
}
```

### Running Tests

```bash
# Run all tests
go test ./...

# Run with verbose output
go test -v ./...

# Run with coverage
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
go tool cover -html=coverage.out -o coverage.html

# Run benchmarks
go test -bench=. -benchmem ./...

# Run specific test
go test -run TestFunction ./...
```

### Benchmarks

```go
func BenchmarkFunction(b *testing.B) {
    // Setup (runs once)
    data := prepareData()
    
    // Reset timer after setup
    b.ResetTimer()
    
    // Benchmark loop
    for i := 0; i < b.N; i++ {
        Function(data)
    }
}
```

## Coverage Tools Comparison

| Language | Tool | Report Format | Missing Lines |
|----------|------|---------------|---------------|
| Python | coverage.py | terminal, HTML, JSON | Yes |
| JavaScript | nyc/Istanbul | terminal, HTML, LCOV | Yes |
| Go | built-in | terminal, HTML | Limited |

## Mutation Testing

### Python (mutmut)

```bash
pip install mutmut
mutmut run --paths-to-mutate=src
mutmut results
mutmut show <id>  # Show specific mutation
```

### JavaScript (Stryker)

```bash
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner
npx stryker init
npx stryker run
```

### Go (Gremlins)

```bash
go install github.com/go-gremlins/gremlins/cmd/gremlins@latest
gremlins run
```

## Best Practices

### Test Organization

1. **Name tests clearly**: `test_calculates_total_correctly` not `test1`
2. **One concept per test**: Test one behavior at a time
3. **Use descriptive assertions**: Prefer `assertEqual(actual, expected)` over `assertTrue(actual == expected)`
4. **Arrange-Act-Assert**: Structure tests consistently

### Coverage Targets

- **Minimum**: 60-70% for legacy code
- **Target**: 80%+ for new code
- **Critical paths**: 100% for security/financial code

### Mutation Testing Thresholds

- **Good**: 70%+ mutation score
- **Excellent**: 85%+ mutation score

Remember: 100% coverage doesn't mean 100% correctness. Mutation testing finds gaps in test quality.
