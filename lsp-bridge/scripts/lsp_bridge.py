#!/usr/bin/env python3
"""
LSP Bridge - Multi-language Language Server Protocol integration for OpenClaw.

Supports: pylsp (Python), typescript-language-server (JS/TS), gopls (Go), rust-analyzer (Rust)
"""

import asyncio
import json
import os
import subprocess
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

# LSP JSON-RPC communication
from pylsp_jsonrpc.endpoint import Endpoint
from pylsp_jsonrpc.streams import JsonRpcStreamReader, JsonRpcStreamWriter


@dataclass
class ServerConfig:
    """Configuration for a language server."""
    command: List[str]
    language_id: str
    extensions: List[str]


# Language server configurations
LANGUAGE_SERVERS = {
    "python": ServerConfig(
        command=["pylsp"],
        language_id="python",
        extensions=[".py"]
    ),
    "typescript": ServerConfig(
        command=["typescript-language-server", "--stdio"],
        language_id="typescript",
        extensions=[".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"]
    ),
    "go": ServerConfig(
        command=["gopls"],
        language_id="go",
        extensions=[".go"]
    ),
    "rust": ServerConfig(
        command=["rust-analyzer"],
        language_id="rust",
        extensions=[".rs"]
    ),
}


class LspServerProcess:
    """Manages a language server subprocess and LSP client."""
    
    def __init__(self, server_id: str, config: ServerConfig, project_path: str):
        self.server_id = server_id
        self.config = config
        self.project_path = Path(project_path).resolve()
        self.process: Optional[subprocess.Popen] = None
        self.client: Optional[LspClient] = None
        self.endpoint: Optional[LspEndpoint] = None
        self.rpc_endpoint: Optional[JsonRpcEndpoint] = None
        self.initialized = False
        self.open_documents: Dict[str, Dict[str, Any]] = {}
        self.diagnostics: Dict[str, List[Dict]] = {}
        
    def start(self) -> bool:
        """Start the language server process."""
        try:
            self.process = subprocess.Popen(
                self.config.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.project_path)
            )
            
            # Set up JSON-RPC endpoint
            self.rpc_endpoint = JsonRpcEndpoint(
                self.process.stdin,
                self.process.stdout
            )
            
            # Set up LSP endpoint with notification handlers
            self.endpoint = LspEndpoint(
                self.rpc_endpoint,
                notify_callbacks={
                    "textDocument/publishDiagnostics": self._on_diagnostics,
                    "window/showMessage": self._on_show_message,
                    "window/logMessage": self._on_log_message,
                }
            )
            
            # Create LSP client
            self.client = LspClient(self.endpoint)
            
            # Initialize the server
            self._initialize()
            
            return True
        except Exception as e:
            print(f"Error starting server: {e}", file=sys.stderr)
            return False
    
    def _initialize(self):
        """Initialize the LSP server."""
        capabilities = {
            "textDocument": {
                "synchronization": {"didSave": True},
                "completion": {"dynamicRegistration": True},
                "hover": {"dynamicRegistration": True},
                "definition": {"dynamicRegistration": True},
                "references": {"dynamicRegistration": True},
                "documentHighlight": {"dynamicRegistration": True},
                "documentSymbol": {"dynamicRegistration": True},
                "codeAction": {"dynamicRegistration": True},
                "formatting": {"dynamicRegistration": True},
                "rename": {"dynamicRegistration": True},
                "publishDiagnostics": {"relatedInformation": True},
            },
            "workspace": {
                "applyEdit": True,
                "workspaceEdit": {"documentChanges": True},
            }
        }
        
        root_uri = self.project_path.as_uri() if hasattr(self.project_path, 'as_uri') else f"file://{self.project_path}"
        
        response = self.client.initialize(
            processId=os.getpid(),
            rootPath=str(self.project_path),
            rootUri=root_uri,
            initializationOptions=None,
            capabilities=capabilities,
            trace="verbose",
            workspaceFolders=[{
                "uri": root_uri,
                "name": self.project_path.name
            }]
        )
        
        self.client.initialized()
        self.initialized = True
        
    def _on_diagnostics(self, params: Dict):
        """Handle diagnostic notifications."""
        uri = params.get("uri", "")
        self.diagnostics[uri] = params.get("diagnostics", [])
        
    def _on_show_message(self, params: Dict):
        """Handle show message notifications."""
        print(f"LSP Message: {params.get('message')}", file=sys.stderr)
        
    def _on_log_message(self, params: Dict):
        """Handle log message notifications."""
        print(f"LSP Log: {params.get('message')}", file=sys.stderr)
        
    def open_document(self, file_path: str) -> str:
        """Open a document in the language server."""
        path = Path(file_path).resolve()
        uri = path.as_uri() if hasattr(path, 'as_uri') else f"file://{path}"
        
        if uri in self.open_documents:
            return uri
            
        content = path.read_text(encoding='utf-8')
        version = 1
        
        self.client.didOpen(
            textDocument={
                "uri": uri,
                "languageId": self.config.language_id,
                "version": version,
                "text": content
            }
        )
        
        self.open_documents[uri] = {
            "path": str(path),
            "version": version,
            "content": content
        }
        
        return uri
        
    def update_document(self, uri: str, content: str):
        """Update document content."""
        if uri in self.open_documents:
            self.open_documents[uri]["version"] += 1
            self.open_documents[uri]["content"] = content
            
            self.client.didChange(
                textDocument={
                    "uri": uri,
                    "version": self.open_documents[uri]["version"]
                },
                contentChanges=[{"text": content}]
            )
            
    def get_position(self, file_path: str, line: int, column: int) -> tuple:
        """Get URI and LSP position for a file location."""
        path = Path(file_path).resolve()
        uri = path.as_uri() if hasattr(path, 'as_uri') else f"file://{path}"
        
        # Open document if not already open
        if uri not in self.open_documents:
            self.open_document(file_path)
            
        # LSP uses 0-based line numbers
        position = {"line": line - 1, "character": column - 1}
        
        return uri, position
        
    def goto_definition(self, file_path: str, line: int, column: int) -> List[Dict]:
        """Go to definition at position."""
        uri, position = self.get_position(file_path, line, column)
        
        result = self.client.definition(
            textDocument={"uri": uri},
            position=position
        )
        
        if result is None:
            return []
        if isinstance(result, list):
            return result
        return [result]
        
    def find_references(self, file_path: str, line: int, column: int) -> List[Dict]:
        """Find references at position."""
        uri, position = self.get_position(file_path, line, column)
        
        result = self.client.references(
            textDocument={"uri": uri},
            position=position,
            context={"includeDeclaration": True}
        )
        
        if result is None:
            return []
        return result
        
    def hover_info(self, file_path: str, line: int, column: int) -> Optional[Dict]:
        """Get hover information at position."""
        uri, position = self.get_position(file_path, line, column)
        
        result = self.client.hover(
            textDocument={"uri": uri},
            position=position
        )
        
        return result
        
    def code_action(self, file_path: str, line: int, column: int) -> List[Dict]:
        """Get code actions at position."""
        uri, position = self.get_position(file_path, line, column)
        
        # Get diagnostics for this line
        diagnostics = []
        for diag in self.diagnostics.get(uri, []):
            if diag.get("range", {}).get("start", {}).get("line") == position["line"]:
                diagnostics.append(diag)
        
        result = self.client.codeAction(
            textDocument={"uri": uri},
            range={
                "start": position,
                "end": position
            },
            context={"diagnostics": diagnostics}
        )
        
        if result is None:
            return []
        return result
        
    def rename(self, file_path: str, line: int, column: int, new_name: str) -> Optional[Dict]:
        """Rename symbol at position."""
        uri, position = self.get_position(file_path, line, column)
        
        result = self.client.rename(
            textDocument={"uri": uri},
            position=position,
            newName=new_name
        )
        
        return result
        
    def format_document(self, file_path: str) -> Optional[List[Dict]]:
        """Format the entire document."""
        uri, _ = self.get_position(file_path, 1, 1)
        
        result = self.client.formatting(
            textDocument={"uri": uri},
            options={
                "tabSize": 4,
                "insertSpaces": True,
                "trimTrailingWhitespace": True,
                "insertFinalNewline": True
            }
        )
        
        return result
        
    def get_diagnostics(self, file_path: str) -> List[Dict]:
        """Get diagnostics for a file."""
        path = Path(file_path).resolve()
        uri = path.as_uri() if hasattr(path, 'as_uri') else f"file://{path}"
        
        # Make sure document is open to trigger diagnostics
        if uri not in self.open_documents:
            self.open_document(file_path)
            
        # Give server time to compute diagnostics
        import time
        time.sleep(0.5)
        
        # Process any pending notifications
        if self.endpoint:
            self.endpoint.handle_notification()
            
        return self.diagnostics.get(uri, [])
        
    def shutdown(self):
        """Shutdown the language server gracefully."""
        if self.client and self.initialized:
            try:
                self.client.shutdown()
                self.client.exit()
            except:
                pass
                
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
                
        self.initialized = False


class LspBridge:
    """Main LSP bridge managing multiple language servers."""
    
    def __init__(self):
        self.servers: Dict[str, LspServerProcess] = {}
        
    def start_server(self, language: str, project_path: str) -> str:
        """Start a language server for the given language."""
        if language not in LANGUAGE_SERVERS:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(LANGUAGE_SERVERS.keys())}")
            
        server_id = str(uuid.uuid4())[:8]
        config = LANGUAGE_SERVERS[language]
        
        server = LspServerProcess(server_id, config, project_path)
        if server.start():
            self.servers[server_id] = server
            return server_id
        else:
            raise RuntimeError(f"Failed to start {language} language server")
            
    def stop_server(self, server_id: str) -> bool:
        """Stop a language server."""
        if server_id not in self.servers:
            return False
            
        server = self.servers.pop(server_id)
        server.shutdown()
        return True
        
    def get_server(self, server_id: str) -> LspServerProcess:
        """Get a server by ID."""
        if server_id not in self.servers:
            raise ValueError(f"Server not found: {server_id}")
        return self.servers[server_id]
        
    def list_servers(self) -> Dict[str, Dict]:
        """List all active servers."""
        return {
            sid: {
                "language": s.config.language_id,
                "project_path": str(s.project_path),
                "initialized": s.initialized
            }
            for sid, s in self.servers.items()
        }
        
    def shutdown_all(self):
        """Shutdown all servers."""
        for server in self.servers.values():
            server.shutdown()
        self.servers.clear()


# Global bridge instance
_bridge = LspBridge()


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified"}))
        sys.exit(1)
        
    command = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        if command == "start_server":
            if len(args) < 2:
                raise ValueError("Usage: start_server <language> <project_path>")
            server_id = _bridge.start_server(args[0], args[1])
            print(json.dumps({"server_id": server_id, "status": "started"}))
            
        elif command == "stop_server":
            if len(args) < 1:
                raise ValueError("Usage: stop_server <server_id>")
            success = _bridge.stop_server(args[0])
            print(json.dumps({"success": success}))
            
        elif command == "list_servers":
            servers = _bridge.list_servers()
            print(json.dumps(servers))
            
        elif command == "goto_definition":
            if len(args) < 4:
                raise ValueError("Usage: goto_definition <server_id> <file_path> <line> <column>")
            server = _bridge.get_server(args[0])
            result = server.goto_definition(args[1], int(args[2]), int(args[3]))
            print(json.dumps(result))
            
        elif command == "find_references":
            if len(args) < 4:
                raise ValueError("Usage: find_references <server_id> <file_path> <line> <column>")
            server = _bridge.get_server(args[0])
            result = server.find_references(args[1], int(args[2]), int(args[3]))
            print(json.dumps(result))
            
        elif command == "hover_info":
            if len(args) < 4:
                raise ValueError("Usage: hover_info <server_id> <file_path> <line> <column>")
            server = _bridge.get_server(args[0])
            result = server.hover_info(args[1], int(args[2]), int(args[3]))
            print(json.dumps(result))
            
        elif command == "code_action":
            if len(args) < 4:
                raise ValueError("Usage: code_action <server_id> <file_path> <line> <column>")
            server = _bridge.get_server(args[0])
            result = server.code_action(args[1], int(args[2]), int(args[3]))
            print(json.dumps(result))
            
        elif command == "rename":
            if len(args) < 5:
                raise ValueError("Usage: rename <server_id> <file_path> <line> <column> <new_name>")
            server = _bridge.get_server(args[0])
            result = server.rename(args[1], int(args[2]), int(args[3]), args[4])
            print(json.dumps(result))
            
        elif command == "format_document":
            if len(args) < 2:
                raise ValueError("Usage: format_document <server_id> <file_path>")
            server = _bridge.get_server(args[0])
            result = server.format_document(args[1])
            print(json.dumps(result))
            
        elif command == "diagnostics":
            if len(args) < 2:
                raise ValueError("Usage: diagnostics <server_id> <file_path>")
            server = _bridge.get_server(args[0])
            result = server.get_diagnostics(args[1])
            print(json.dumps(result))
            
        else:
            raise ValueError(f"Unknown command: {command}")
            
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
