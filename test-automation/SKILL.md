---
name: test-automation
description: "Automated unit test generation, execution, and coverage analysis for Python (pytest), JavaScript/TypeScript (Jest), and Go (testing). Use when working with unit tests, generating test scaffolding, running test suites, analyzing code coverage, performing mutation testing, or benchmarking code performance. Triggers include - generate tests, run tests, coverage report, mutation testing, performance benchmarks, pytest, jest, go test."
---

# Test Automation Skill

Generate tests, run test suites, analyze coverage, perform mutation testing, and benchmark code across Python, JavaScript, and Go projects.

## Quick Start

```bash
# Generate tests for a source file
python3 scripts/test_automation.py generate path/to/file.py

# Run tests
python3 scripts/test_automation.py run path/to/tests/

# Generate coverage report
python3 scripts/test_automation.py coverage path/to/source/

# Run mutation testing
python3 scripts/test_automation.py mutation path/to/file.py

# Run benchmarks
python3 scripts/test_automation.py benchmark path/to/file.py
```

## Supported Operations

### 1. Generate Tests (`generate_tests`)

Analyzes source code and generates test scaffolding:

- **Python**: Creates `test_*.py` files with pytest structure
- **JavaScript**: Creates `*.test.js` files with Jest describe/it blocks
- **Go**: Creates `*_test.go` files with idiomatic table-driven tests

```bash
python3 scripts/test_automation.py generate src/calculator.py --output tests/
```

### 2. Run Tests (`run_tests`)

Executes test suites and reports results:

```bash
python3 scripts/test_automation.py run tests/ --framework pytest
```

Returns: pass/fail counts, duration, detailed output

### 3. Coverage Report (`coverage_report`)

Generates coverage analysis with missing line identification:

- **Python**: Uses `coverage.py`
- **JavaScript**: Uses `nyc` (Istanbul)
- **Go**: Uses built-in `go test -cover`

```bash
python3 scripts/test_automation.py coverage src/ --framework pytest
```

Returns: coverage percentage, missing lines per file, total statements

### 4. Mutation Testing (`mutation_test`)

Performs basic mutation testing to evaluate test quality:

```bash
python3 scripts/test_automation.py mutation src/calculator.py
```

Uses available tools (mutmut, Stryker, gremlins) or falls back to basic operator mutation.

Returns: mutation score (%), mutations killed/survived, detailed results

### 5. Benchmark (`benchmark`)

Runs performance benchmarks:

```bash
python3 scripts/test_automation.py benchmark src/calculator.py
```

Returns: operations/second, execution time per operation

## Auto-Detection

The skill automatically detects project type and framework:

| Indicator | Detected Language | Framework |
|-----------|-------------------|-----------|
| `.py` files, `pytest.ini`, `requirements.txt` | Python | pytest |
| `.js/.ts` files, `package.json` with jest | JavaScript | Jest |
| `.go` files, `go.mod` | Go | testing |

To override auto-detection, specify `--framework` explicitly.

## Framework Scripts

Framework-specific implementations are in separate scripts:

- `python_runner.py` - Python/pytest operations
- `javascript_runner.py` - JavaScript/Jest operations
- `go_runner.py` - Go/testing operations

Load [references/frameworks.md](references/frameworks.md) for detailed framework configuration, dependencies, and best practices.

## Output Formats

All commands support JSON output with `--json`:

```bash
python3 scripts/test_automation.py run tests/ --json
```

## Requirements

### Python Projects
```bash
pip install pytest coverage
```

### JavaScript Projects
```bash
npm install --save-dev jest nyc
```

### Go Projects
Built-in testing support (no additional dependencies).

## Best Practices

1. **Generate tests first**, then customize for edge cases
2. **Aim for 80%+ coverage** on new code
3. **Run mutation testing** to verify test quality
4. **Use benchmarks** for performance-critical code
5. **Check missing lines** in coverage reports for gaps
