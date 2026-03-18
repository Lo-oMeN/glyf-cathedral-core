#!/usr/bin/env python3
"""
OpenClaw Skill Wrapper for lsp-bridge
Provides LSP integration for multiple languages.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Path to the main LSP bridge script
SCRIPT_DIR = Path(__file__).parent
LSP_BRIDGE_SCRIPT = SCRIPT_DIR / "lsp_bridge.py"

# Use venv Python if available, otherwise fall back to system Python
VENV_PYTHON = SCRIPT_DIR.parent / "venv" / "bin" / "python"
PYTHON_EXE = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable


def run_lsp_bridge(command: str, *args) -> dict:
    """Run the LSP bridge script with the given command."""
    cmd = [PYTHON_EXE, str(LSP_BRIDGE_SCRIPT), command] + list(args)
    
    # Set up environment with venv packages
    env = os.environ.copy()
    venv_site_packages = SCRIPT_DIR.parent / "venv" / "lib" / "python3.12" / "site-packages"
    if venv_site_packages.exists():
        env["PYTHONPATH"] = str(venv_site_packages) + ":" + env.get("PYTHONPATH", "")
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    
    if result.returncode != 0:
        error_msg = result.stderr or "Unknown error"
        try:
            error_data = json.loads(result.stdout)
            error_msg = error_data.get("error", error_msg)
        except:
            pass
        raise RuntimeError(f"LSP bridge error: {error_msg}")
    
    return json.loads(result.stdout)


def start_server(language: str, project_path: str) -> str:
    """
    Start a language server for the specified language.
    
    Args:
        language: One of 'python', 'typescript', 'go', 'rust'
        project_path: Path to the project root
        
    Returns:
        server_id: Unique identifier for the started server
    """
    result = run_lsp_bridge("start_server", language, project_path)
    return result["server_id"]


def stop_server(server_id: str) -> bool:
    """
    Stop a running language server.
    
    Args:
        server_id: The server ID returned by start_server
        
    Returns:
        True if stopped successfully
    """
    result = run_lsp_bridge("stop_server", server_id)
    return result.get("success", False)


def goto_definition(server_id: str, file_path: str, line: int, column: int) -> list:
    """
    Go to definition at the specified position.
    
    Args:
        server_id: The server ID
        file_path: Path to the source file
        line: Line number (1-based)
        column: Column number (1-based)
        
    Returns:
        List of Location objects with uri and range
    """
    return run_lsp_bridge("goto_definition", server_id, file_path, str(line), str(column))


def find_references(server_id: str, file_path: str, line: int, column: int) -> list:
    """
    Find all references to the symbol at the specified position.
    
    Args:
        server_id: The server ID
        file_path: Path to the source file
        line: Line number (1-based)
        column: Column number (1-based)
        
    Returns:
        List of Location objects
    """
    return run_lsp_bridge("find_references", server_id, file_path, str(line), str(column))


def hover_info(server_id: str, file_path: str, line: int, column: int) -> dict:
    """
    Get hover information (type/documentation) at the specified position.
    
    Args:
        server_id: The server ID
        file_path: Path to the source file
        line: Line number (1-based)
        column: Column number (1-based)
        
    Returns:
        Hover object with contents
    """
    return run_lsp_bridge("hover_info", server_id, file_path, str(line), str(column))


def code_action(server_id: str, file_path: str, line: int, column: int) -> list:
    """
    Get available code actions at the specified position.
    
    Args:
        server_id: The server ID
        file_path: Path to the source file
        line: Line number (1-based)
        column: Column number (1-based)
        
    Returns:
        List of CodeAction objects
    """
    return run_lsp_bridge("code_action", server_id, file_path, str(line), str(column))


def rename(server_id: str, file_path: str, line: int, column: int, new_name: str) -> dict:
    """
    Rename the symbol at the specified position.
    
    Args:
        server_id: The server ID
        file_path: Path to the source file
        line: Line number (1-based)
        column: Column number (1-based)
        new_name: The new name for the symbol
        
    Returns:
        WorkspaceEdit object with document changes
    """
    return run_lsp_bridge("rename", server_id, file_path, str(line), str(column), new_name)


def format_document(server_id: str, file_path: str) -> list:
    """
    Format the entire document.
    
    Args:
        server_id: The server ID
        file_path: Path to the source file
        
    Returns:
        List of TextEdit objects
    """
    return run_lsp_bridge("format_document", server_id, file_path)


def diagnostics(server_id: str, file_path: str) -> list:
    """
    Get diagnostics (errors, warnings) for the file.
    
    Args:
        server_id: The server ID
        file_path: Path to the source file
        
    Returns:
        List of Diagnostic objects
    """
    return run_lsp_bridge("diagnostics", server_id, file_path)


def list_servers() -> dict:
    """
    List all active language servers.
    
    Returns:
        Dictionary mapping server_id to server info
    """
    return run_lsp_bridge("list_servers")


# CLI interface for testing
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: skill_wrapper.py <command> [args...]")
        print("\nCommands:")
        print("  start_server <language> <project_path>")
        print("  stop_server <server_id>")
        print("  list_servers")
        print("  goto_definition <server_id> <file_path> <line> <column>")
        print("  find_references <server_id> <file_path> <line> <column>")
        print("  hover_info <server_id> <file_path> <line> <column>")
        print("  code_action <server_id> <file_path> <line> <column>")
        print("  rename <server_id> <file_path> <line> <column> <new_name>")
        print("  format_document <server_id> <file_path>")
        print("  diagnostics <server_id> <file_path>")
        sys.exit(1)
        
    command = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        result = run_lsp_bridge(command, *args)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
