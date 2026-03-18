#!/usr/bin/env python3
"""
Go test runner using built-in testing package
Supports: generate, run, coverage, mutation, benchmark operations
"""

import argparse
import os
import sys
import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Optional


def parse_go_functions(file_path: str) -> Dict:
    """Parse Go file to extract function signatures."""
    path = Path(file_path)
    if not path.exists():
        return {"functions": [], "types": []}
    
    content = path.read_text()
    
    functions = []
    types = []
    
    # Match function declarations: func Name(args) returnType
    func_pattern = r'^func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(([^)]*)\)\s*(?:\([^)]*\)|(\S+))?'
    
    for match in re.finditer(func_pattern, content, re.MULTILINE):
        func_name = match.group(1)
        args = match.group(2) or ""
        return_type = match.group(3) or ""
        
        # Skip test functions and private
        if func_name.startswith("_") or func_name.startswith("Test"):
            continue
        
        functions.append({
            "name": func_name,
            "args": [a.strip() for a in args.split(",") if a.strip()],
            "return_type": return_type,
            "has_receiver": match.group(0).startswith("func (")
        })
    
    # Match type declarations (for struct methods)
    type_pattern = r'^type\s+(\w+)\s+(struct|interface)'
    for match in re.finditer(type_pattern, content, re.MULTILINE):
        types.append({
            "name": match.group(1),
            "kind": match.group(2)
        })
    
    return {"functions": functions, "types": types}


def generate_go_tests(file_path: str, output_path: Optional[str] = None) -> Dict:
    """Generate Go test scaffolding."""
    path = Path(file_path)
    parsed = parse_go_functions(file_path)
    
    module_name = path.stem
    test_file_name = f"{module_name}_test.go"
    
    if output_path:
        output = Path(output_path)
        if output.is_dir():
            test_file_path = output / test_file_name
        else:
            test_file_path = output
    else:
        test_file_path = path.parent / test_file_name
    
    # Get package name
    package_match = re.search(r'^package\s+(\w+)', path.read_text(), re.MULTILINE)
    package_name = package_match.group(1) if package_match else module_name
    
    lines = [
        f'package {package_name}',
        f'',
        f'import (',
        f'\t"testing"',
        f')',
        f'',
    ]
    
    # Generate test functions
    for func in parsed.get("functions", []):
        func_name = func["name"]
        
        lines.extend([
            f'func Test{func_name}(t *testing.T) {{',
            f'\t// Arrange',
            f'\t// TODO: Set up test inputs',
            f'\t',
            f'\t// Act',
        ])
        
        if func.get("has_receiver"):
            lines.extend([
                f'\t// TODO: Create instance and call method',
                f'\t// result := instance.{func_name}()',
            ])
        else:
            lines.extend([
                f'\t// TODO: Call function with appropriate args',
                f'\t// result := {func_name}()',
            ])
        
        lines.extend([
            f'\t',
            f'\t// Assert',
            f'\t// TODO: Add appropriate assertions',
            f'\t// if result != expected {{',
            f'\t// \tt.Errorf("Expected %%v, got %%v", expected, result)',
            f'\t// }}',
            f'}}',
            f'',
        ])
    
    # Generate table-driven tests example for first function
    if parsed.get("functions"):
        first_func = parsed["functions"][0]
        func_name = first_func["name"]
        
        lines.extend([
            f'func Test{func_name}_TableDriven(t *testing.T) {{',
            f'\ttests := []struct {{',
            f'\t\tname     string',
            f'\t\tinput    string',  # Placeholder
            f'\t\texpected string',  # Placeholder
            f'\t\twantErr  bool',
            f'\t}}{{',
            f'\t\t{{',
            f'\t\t\tname:     "valid input",',
            f'\t\t\tinput:    "test",',
            f'\t\t\texpected: "result",',
            f'\t\t\twantErr:  false,',
            f'\t\t}},',
            f'\t\t// TODO: Add more test cases',
            f'\t}}',
            f'\t',
            f'\tfor _, tt := range tests {{',
            f'\t\tt.Run(tt.name, func(t *testing.T) {{',
            f'\t\t\t// TODO: Call {func_name} and validate',
            f'\t\t}})',
            f'\t}}',
            f'}}',
            f'',
        ])
    
    test_content = "\n".join(lines)
    test_file_path.write_text(test_content)
    
    return {
        "success": True,
        "test_file": str(test_file_path),
        "functions_found": len(parsed.get("functions", [])),
        "types_found": len(parsed.get("types", [])),
        "output": f"Generated test file: {test_file_path}\n{test_content}"
    }


def run_go_tests(test_path: str) -> Dict:
    """Run Go tests and return results."""
    path = Path(test_path)
    
    # Find module root
    module_root = path
    while module_root.parent != module_root:
        if (module_root / "go.mod").exists():
            break
        module_root = module_root.parent
    
    # Determine test target
    if path.is_file():
        target = f"./{path.name}"
        cwd = path.parent
    else:
        target = "./..."
        cwd = path
    
    try:
        result = subprocess.run(
            ["go", "test", "-v", target],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=cwd
        )
        
        output = result.stdout + result.stderr
        
        # Parse Go test output
        passed = len(re.findall(r'^---\s+PASS:', output, re.MULTILINE))
        failed = len(re.findall(r'^---\s+FAIL:', output, re.MULTILINE))
        
        # Extract test summary
        summary_match = re.search(r'(ok|FAIL)\s+\S+\s+([\d.]+)s', output)
        duration = float(summary_match.group(2)) if summary_match else 0
        
        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "passed": passed,
            "failed": failed,
            "duration_seconds": duration,
            "output": output
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Test execution timed out (5 minutes)",
            "output": ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": ""
        }


def run_coverage(source_path: str) -> Dict:
    """Generate Go coverage report."""
    path = Path(source_path)
    
    # Find module root
    module_root = path
    while module_root.parent != module_root:
        if (module_root / "go.mod").exists():
            break
        module_root = module_root.parent
    
    # Determine target
    if path.is_file():
        target = path.parent
    else:
        target = path
    
    try:
        # Run tests with coverage
        result = subprocess.run(
            ["go", "test", "-coverprofile=coverage.out", "-v", "./..."],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=target
        )
        
        # Generate coverage report
        report_result = subprocess.run(
            ["go", "tool", "cover", "-func=coverage.out"],
            capture_output=True,
            text=True,
            cwd=target
        )
        
        output = report_result.stdout
        
        # Parse coverage percentage
        total_line = None
        for line in output.split("\n"):
            if "total:" in line.lower():
                total_line = line
                break
        
        coverage_percent = 0
        if total_line:
            match = re.search(r'(\d+\.?\d*)%', total_line)
            if match:
                coverage_percent = float(match.group(1))
        
        # Get missing lines
        missing_lines = {}
        html_result = subprocess.run(
            ["go", "tool", "cover", "-html=coverage.out", "-o", "coverage.html"],
            capture_output=True,
            cwd=target
        )
        
        return {
            "success": True,
            "coverage_percent": round(coverage_percent, 2),
            "output": output,
            "report_file": str(target / "coverage.html")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": ""
        }


def run_mutation_test(file_path: str) -> Dict:
    """Run basic mutation testing for Go using gremlins or custom approach."""
    path = Path(file_path)
    
    # Check if gremlins is available
    try:
        result = subprocess.run(
            ["gremlins", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        has_gremlins = result.returncode == 0
    except:
        has_gremlins = False
    
    if has_gremlins:
        # Run gremlins
        result = subprocess.run(
            ["gremlins", "run"],
            capture_output=True,
            text=True,
            timeout=600,
            cwd=path.parent
        )
        
        return {
            "success": result.returncode == 0,
            "tool": "gremlins",
            "output": result.stdout + result.stderr
        }
    
    # Fallback: Simple mutation analysis
    try:
        original_content = path.read_text()
        
        # Define simple mutations
        mutations = [
            (" == ", " != "),
            (" != ", " == "),
            (" > ", " < "),
            (" < ", " > "),
            (" >= ", " <= "),
            (" <= ", " >= "),
            ("true", "false"),
            ("false", "true"),
            ("return nil", "return err"),
        ]
        
        killed = 0
        survived = 0
        mutation_details = []
        
        for old_op, new_op in mutations:
            if old_op in original_content:
                mutated = original_content.replace(old_op, new_op, 1)
                
                # Write mutation
                path.write_text(mutated)
                
                # Run tests
                test_result = subprocess.run(
                    ["go", "test", "./..."],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=path.parent
                )
                
                status = "killed" if test_result.returncode != 0 else "survived"
                if test_result.returncode != 0:
                    killed += 1
                else:
                    survived += 1
                
                mutation_details.append({
                    "operator": f"{old_op} -> {new_op}",
                    "status": status
                })
        
        # Restore original
        path.write_text(original_content)
        
        total = killed + survived
        score = (killed / total * 100) if total > 0 else 0
        
        return {
            "success": True,
            "tool": "basic",
            "mutations_tested": total,
            "killed": killed,
            "survived": survived,
            "mutation_score": round(score, 2),
            "mutations": mutation_details,
            "output": f"Mutation Score: {score:.1f}% ({killed}/{total} mutations killed)"
        }
        
    except Exception as e:
        # Ensure original is restored
        try:
            path.write_text(original_content)
        except:
            pass
        return {"success": False, "error": str(e)}


def run_benchmark(file_path: str) -> Dict:
    """Run Go benchmarks."""
    path = Path(file_path)
    
    # First, check if there are existing benchmarks
    content = path.read_text()
    has_benchmarks = "func Benchmark" in content
    
    # Generate benchmark file if none exist
    if not has_benchmarks:
        parsed = parse_go_functions(file_path)
        
        bench_file_path = path.parent / f"{path.stem}_benchmark_test.go"
        
        package_match = re.search(r'^package\s+(\w+)', content, re.MULTILINE)
        package_name = package_match.group(1) if package_match else path.stem
        
        lines = [
            f'package {package_name}',
            f'',
            f'import "testing"',
            f'',
        ]
        
        for func in parsed.get("functions", []):
            func_name = func["name"]
            if func_name.startswith("_"):
                continue
            
            lines.extend([
                f'func Benchmark{func_name}(b *testing.B) {{',
                f'\t// TODO: Set up benchmark inputs',
                f'\tfor i := 0; i < b.N; i++ {{',
            ])
            
            if func.get("has_receiver"):
                lines.append(f'\t\t// instance.{func_name}()')
            else:
                lines.append(f'\t\t// {func_name}()')
            
            lines.extend([
                f'\t}}',
                f'}}',
                f'',
            ])
        
        bench_content = "\n".join(lines)
        bench_file_path.write_text(bench_content)
        
        return {
            "success": True,
            "generated": True,
            "benchmark_file": str(bench_file_path),
            "output": f"Generated benchmark file: {bench_file_path}\n\n{bench_content}\n\nRun with: go test -bench=. -benchmem"
        }
    
    # Run existing benchmarks
    try:
        result = subprocess.run(
            ["go", "test", "-bench=.", "-benchmem", "-v"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=path.parent
        )
        
        output = result.stdout
        
        # Parse benchmark results
        benchmarks = []
        for line in output.split("\n"):
            bench_match = re.match(r'^(Benchmark\S+)\s+(\d+)\s+([\d.]+)\s+\S+/(op|ns/op)', line)
            if bench_match:
                benchmarks.append({
                    "name": bench_match.group(1),
                    "runs": int(bench_match.group(2)),
                    "time_per_op": float(bench_match.group(3))
                })
        
        return {
            "success": result.returncode == 0,
            "benchmarks": benchmarks,
            "output": output
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": ""
        }


def main():
    parser = argparse.ArgumentParser(description="Go test runner")
    parser.add_argument("operation", choices=["generate", "run", "coverage", "mutation", "benchmark"])
    parser.add_argument("file_path")
    parser.add_argument("--framework", default="testing")
    parser.add_argument("--output")
    
    args = parser.parse_args()
    
    result = {}
    
    if args.operation == "generate":
        result = generate_go_tests(args.file_path, args.output)
    elif args.operation == "run":
        result = run_go_tests(args.file_path)
    elif args.operation == "coverage":
        result = run_coverage(args.file_path)
    elif args.operation == "mutation":
        result = run_mutation_test(args.file_path)
    elif args.operation == "benchmark":
        result = run_benchmark(args.file_path)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
