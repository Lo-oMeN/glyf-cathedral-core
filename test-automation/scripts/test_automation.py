#!/usr/bin/env python3
"""
Test Automation Skill - Main wrapper script
Supports Python (pytest), JavaScript (Jest), and Go (testing)
Operations: generate_tests, run_tests, coverage_report, mutation_test, benchmark
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Tuple, Dict, List

# Script directory for accessing framework-specific scripts
SCRIPT_DIR = Path(__file__).parent.resolve()


def detect_project_type(file_path: str) -> Tuple[str, str]:
    """
    Auto-detect project type and test framework based on file extension and project structure.
    Returns (language, framework)
    """
    path = Path(file_path).resolve()
    ext = path.suffix.lower()
    
    # Check parent directories for project files
    current_dir = path.parent if path.is_file() else path
    
    for parent in [current_dir] + list(current_dir.parents):
        # Python detection
        if (parent / "pytest.ini").exists() or (parent / "pyproject.toml").exists():
            if (parent / "pyproject.toml").exists():
                content = (parent / "pyproject.toml").read_text()
                if "pytest" in content or "[tool.pytest" in content:
                    return ("python", "pytest")
            return ("python", "pytest")
        if (parent / "requirements.txt").exists() or (parent / "setup.py").exists():
            return ("python", "pytest")
        if list(parent.glob("*.py")):
            return ("python", "pytest")
        
        # JavaScript/TypeScript detection
        if (parent / "package.json").exists():
            pkg_json = json.loads((parent / "package.json").read_text())
            deps = {**pkg_json.get("dependencies", {}), **pkg_json.get("devDependencies", {})}
            
            if "jest" in deps:
                return ("javascript", "jest")
            if "vitest" in deps:
                return ("javascript", "vitest")
            if "mocha" in deps:
                return ("javascript", "mocha")
            return ("javascript", "jest")  # Default to jest
        
        # Go detection
        if (parent / "go.mod").exists() or (parent / "go.sum").exists():
            return ("go", "testing")
        if list(parent.glob("*.go")):
            return ("go", "testing")
    
    # Fallback to file extension
    if ext == ".py":
        return ("python", "pytest")
    elif ext in [".js", ".jsx", ".ts", ".tsx", ".mjs"]:
        return ("javascript", "jest")
    elif ext == ".go":
        return ("go", "testing")
    
    raise ValueError(f"Cannot detect project type for: {file_path}")


def run_framework_script(operation: str, file_path: str, framework: str, extra_args: Dict = None) -> Dict:
    """Run the appropriate framework-specific script."""
    
    lang_map = {
        "pytest": "python",
        "jest": "javascript",
        "vitest": "javascript",
        "mocha": "javascript",
        "testing": "go"
    }
    
    language = lang_map.get(framework, framework)
    script_path = SCRIPT_DIR / f"{language}_runner.py"
    
    if not script_path.exists():
        raise FileNotFoundError(f"Framework script not found: {script_path}")
    
    cmd = [
        sys.executable,
        str(script_path),
        operation,
        file_path,
        "--framework", framework
    ]
    
    if extra_args:
        for key, value in extra_args.items():
            cmd.extend([f"--{key}", str(value)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Try to parse JSON output
    try:
        output = json.loads(result.stdout)
        output["exit_code"] = result.returncode
        output["stderr"] = result.stderr if result.stderr else None
        return output
    except json.JSONDecodeError:
        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output": result.stdout
        }


def generate_tests(file_path: str, framework: Optional[str] = None, output_path: Optional[str] = None) -> Dict:
    """Generate test scaffolding for the given file."""
    if framework is None:
        _, framework = detect_project_type(file_path)
    
    extra_args = {}
    if output_path:
        extra_args["output"] = output_path
    
    return run_framework_script("generate", file_path, framework, extra_args)


def run_tests(test_path: str, framework: Optional[str] = None) -> Dict:
    """Execute tests and report results."""
    if framework is None:
        _, framework = detect_project_type(test_path)
    
    return run_framework_script("run", test_path, framework)


def coverage_report(source_path: str, framework: Optional[str] = None) -> Dict:
    """Generate coverage analysis with missing lines."""
    if framework is None:
        _, framework = detect_project_type(source_path)
    
    return run_framework_script("coverage", source_path, framework)


def mutation_test(file_path: str, framework: Optional[str] = None) -> Dict:
    """Run basic mutation testing."""
    if framework is None:
        _, framework = detect_project_type(file_path)
    
    return run_framework_script("mutation", file_path, framework)


def benchmark(file_path: str, framework: Optional[str] = None) -> Dict:
    """Run performance benchmarks."""
    if framework is None:
        _, framework = detect_project_type(file_path)
    
    return run_framework_script("benchmark", file_path, framework)


def main():
    parser = argparse.ArgumentParser(
        description="Test Automation Skill - Generate tests, run coverage, mutation testing, and benchmarks"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate test scaffolding")
    gen_parser.add_argument("file_path", help="Path to source file")
    gen_parser.add_argument("--framework", "-f", help="Test framework (auto-detected if not specified)")
    gen_parser.add_argument("--output", "-o", help="Output path for generated tests")
    gen_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # run command
    run_parser = subparsers.add_parser("run", help="Run tests")
    run_parser.add_argument("test_path", help="Path to test file or directory")
    run_parser.add_argument("--framework", "-f", help="Test framework (auto-detected if not specified)")
    run_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # coverage command
    cov_parser = subparsers.add_parser("coverage", help="Generate coverage report")
    cov_parser.add_argument("source_path", help="Path to source file or directory")
    cov_parser.add_argument("--framework", "-f", help="Test framework (auto-detected if not specified)")
    cov_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # mutation command
    mut_parser = subparsers.add_parser("mutation", help="Run mutation testing")
    mut_parser.add_argument("file_path", help="Path to source file")
    mut_parser.add_argument("--framework", "-f", help="Test framework (auto-detected if not specified)")
    mut_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Run performance benchmarks")
    bench_parser.add_argument("file_path", help="Path to source file")
    bench_parser.add_argument("--framework", "-f", help="Test framework (auto-detected if not specified)")
    bench_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # detect command (utility)
    detect_parser = subparsers.add_parser("detect", help="Detect project type and framework")
    detect_parser.add_argument("path", help="Path to analyze")
    detect_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    result = {}
    
    try:
        if args.command == "generate":
            result = generate_tests(args.file_path, args.framework, args.output)
        elif args.command == "run":
            result = run_tests(args.test_path, args.framework)
        elif args.command == "coverage":
            result = coverage_report(args.source_path, args.framework)
        elif args.command == "mutation":
            result = mutation_test(args.file_path, args.framework)
        elif args.command == "benchmark":
            result = benchmark(args.file_path, args.framework)
        elif args.command == "detect":
            lang, fw = detect_project_type(args.path)
            result = {"language": lang, "framework": fw, "detected": True}
        
        if args.json or getattr(args, 'json', False):
            print(json.dumps(result, indent=2))
        else:
            if isinstance(result, dict) and "output" in result:
                print(result["output"])
            else:
                print(json.dumps(result, indent=2))
        
        sys.exit(0 if result.get("success", True) else 1)
        
    except Exception as e:
        error_result = {"success": False, "error": str(e)}
        if args.json or getattr(args, 'json', False):
            print(json.dumps(error_result, indent=2))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
