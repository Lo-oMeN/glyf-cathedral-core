#!/usr/bin/env python3
"""
Repo Analyzer - Deep codebase indexing and semantic search
"""

import argparse
import os
import sys
import json
import pickle
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import re
from datetime import datetime

# Tree-sitter imports
from tree_sitter import Language, Parser, Node
import tree_sitter_python
import tree_sitter_javascript
import tree_sitter_typescript
import tree_sitter_go
import tree_sitter_rust
import tree_sitter_java
import tree_sitter_cpp

# Vector embeddings
import numpy as np

# Cyclomatic complexity
import ast

# Store index location
INDEX_DIR = Path.home() / ".openclaw" / "repo-indexes"
INDEX_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class CodeSymbol:
    """Represents a code symbol (function, class, variable)"""
    name: str
    symbol_type: str  # function, class, method, variable
    file_path: str
    start_line: int
    end_line: int
    code: str
    docstring: str = ""
    parent: Optional[str] = None
    calls: List[str] = field(default_factory=list)
    called_by: List[str] = field(default_factory=list)


@dataclass
class CodeFile:
    """Represents a parsed code file"""
    file_path: str
    language: str
    content: str
    symbols: List[CodeSymbol] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


class TreeSitterParser:
    """Handles parsing of multiple languages using tree-sitter"""
    
    LANGUAGE_MAP = {
        'python': ('.py', tree_sitter_python, 'language'),
        'javascript': ('.js', tree_sitter_javascript, 'language'),
        'typescript': ('.ts', tree_sitter_typescript, 'language_typescript'),
        'go': ('.go', tree_sitter_go, 'language'),
        'rust': ('.rs', tree_sitter_rust, 'language'),
        'java': ('.java', tree_sitter_java, 'language'),
        'cpp': ('.cpp', tree_sitter_cpp, 'language'),
    }
    
    def __init__(self):
        self.parsers = {}
        self.languages = {}
        self._init_languages()
    
    def _init_languages(self):
        """Initialize tree-sitter languages and parsers"""
        for lang_name, (ext, lang_module, lang_func) in self.LANGUAGE_MAP.items():
            try:
                lang_attr = getattr(lang_module, lang_func)
                self.languages[lang_name] = Language(lang_attr())
                # New tree-sitter API: Parser takes language directly
                parser = Parser(self.languages[lang_name])
                self.parsers[lang_name] = parser
            except Exception as e:
                print(f"Warning: Could not load {lang_name}: {e}")
    
    def get_language_by_extension(self, file_path: str) -> Optional[str]:
        """Determine language from file extension"""
        ext = Path(file_path).suffix.lower()
        for lang_name, (lang_ext, _, _) in self.LANGUAGE_MAP.items():
            if ext == lang_ext:
                return lang_name
        # Handle .jsx, .tsx, .hpp, etc.
        if ext == '.jsx':
            return 'javascript'
        if ext == '.tsx':
            return 'typescript'
        if ext in ['.hpp', '.h', '.cc', '.cxx']:
            return 'cpp'
        return None
    
    def parse_file(self, file_path: str, language: str) -> Optional[CodeFile]:
        """Parse a single file and extract symbols"""
        if language not in self.parsers:
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        
        parser = self.parsers[language]
        tree = parser.parse(bytes(content, 'utf-8'))
        
        code_file = CodeFile(
            file_path=file_path,
            language=language,
            content=content
        )
        
        # Extract symbols based on language
        root_node = tree.root_node
        symbols = self._extract_symbols(root_node, content, file_path, language)
        code_file.symbols = symbols
        
        # Extract imports
        code_file.imports = self._extract_imports(root_node, content, language)
        
        return code_file
    
    def _extract_symbols(self, node: Node, content: str, file_path: str, 
                         language: str, parent: Optional[str] = None) -> List[CodeSymbol]:
        """Extract symbols from AST"""
        symbols = []
        
        symbol_types = self._get_symbol_query_patterns(language)
        
        def traverse(node: Node, parent_name: Optional[str] = None):
            # Check if node is a symbol definition
            symbol = self._node_to_symbol(node, content, file_path, language, parent_name)
            if symbol:
                symbols.append(symbol)
                parent_name = symbol.name
            
            for child in node.children:
                traverse(child, parent_name)
        
        traverse(node)
        return symbols
    
    def _node_to_symbol(self, node: Node, content: str, file_path: str, 
                        language: str, parent: Optional[str]) -> Optional[CodeSymbol]:
        """Convert an AST node to a CodeSymbol"""
        node_type = node.type
        symbol_type = None
        name = None
        
        # Language-specific node type mapping
        if language == 'python':
            if node_type == 'function_definition':
                symbol_type = 'function'
            elif node_type == 'class_definition':
                symbol_type = 'class'
            elif node_type == 'method_definition':
                symbol_type = 'method'
            
            if symbol_type:
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte]
        
        elif language in ['javascript', 'typescript']:
            if node_type in ['function_declaration', 'function', 'arrow_function']:
                symbol_type = 'function'
            elif node_type == 'class_declaration':
                symbol_type = 'class'
            elif node_type == 'method_definition':
                symbol_type = 'method'
            
            if symbol_type:
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte]
        
        elif language == 'go':
            if node_type == 'function_declaration':
                symbol_type = 'function'
            elif node_type == 'method_declaration':
                symbol_type = 'method'
            elif node_type == 'type_spec':
                symbol_type = 'class'  # Go doesn't have classes, but types are similar
            
            if symbol_type:
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte]
        
        elif language == 'rust':
            if node_type == 'function_item':
                symbol_type = 'function'
            elif node_type == 'impl_item':
                symbol_type = 'class'  # impl blocks
            elif node_type == 'struct_item':
                symbol_type = 'class'
            
            if symbol_type:
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte]
        
        elif language == 'java':
            if node_type == 'method_declaration':
                symbol_type = 'method'
            elif node_type == 'class_declaration':
                symbol_type = 'class'
            elif node_type == 'interface_declaration':
                symbol_type = 'interface'
            
            if symbol_type:
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte]
        
        elif language == 'cpp':
            if node_type == 'function_definition':
                symbol_type = 'function'
            elif node_type == 'class_specifier':
                symbol_type = 'class'
            elif node_type == 'struct_specifier':
                symbol_type = 'struct'
            
            if symbol_type:
                # C++ is more complex, try to find name
                for child in node.children:
                    if child.type in ['identifier', 'type_identifier', 'field_identifier']:
                        name = content[child.start_byte:child.end_byte]
                        break
        
        if name and symbol_type:
            code = content[node.start_byte:node.end_byte]
            start_line = content[:node.start_byte].count('\n') + 1
            end_line = content[:node.end_byte].count('\n') + 1
            
            return CodeSymbol(
                name=name,
                symbol_type=symbol_type,
                file_path=file_path,
                start_line=start_line,
                end_line=end_line,
                code=code,
                parent=parent
            )
        
        return None
    
    def _get_symbol_query_patterns(self, language: str) -> Dict[str, str]:
        """Get symbol query patterns for a language"""
        # Return patterns for matching symbol types
        return {}
    
    def _extract_imports(self, node: Node, content: str, language: str) -> List[str]:
        """Extract import statements from code"""
        imports = []
        
        def traverse(node: Node):
            if language == 'python':
                if node.type in ['import_statement', 'import_from_statement']:
                    import_text = content[node.start_byte:node.end_byte]
                    imports.append(import_text)
            
            elif language in ['javascript', 'typescript']:
                if node.type in ['import_statement', 'import_declaration']:
                    import_text = content[node.start_byte:node.end_byte]
                    imports.append(import_text)
            
            elif language == 'go':
                if node.type == 'import_declaration':
                    import_text = content[node.start_byte:node.end_byte]
                    imports.append(import_text)
            
            elif language == 'rust':
                if node.type in ['use_declaration', 'extern_crate_declaration']:
                    import_text = content[node.start_byte:node.end_byte]
                    imports.append(import_text)
            
            elif language == 'java':
                if node.type == 'import_declaration':
                    import_text = content[node.start_byte:node.end_byte]
                    imports.append(import_text)
            
            elif language == 'cpp':
                if node.type == 'preproc_include':
                    import_text = content[node.start_byte:node.end_byte]
                    imports.append(import_text)
            
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return imports


class ComplexityAnalyzer:
    """Analyzes code complexity metrics"""
    
    @staticmethod
    def analyze_python_complexity(file_path: str) -> Dict[str, Any]:
        """Calculate cyclomatic complexity for Python code"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            results = {}
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity = ComplexityAnalyzer._calculate_python_function_complexity(node)
                    results[node.name] = {
                        'complexity': complexity,
                        'lines': node.end_lineno - node.lineno + 1 if node.end_lineno else 0,
                        'start_line': node.lineno
                    }
                elif isinstance(node, ast.ClassDef):
                    class_complexity = 0
                    methods = {}
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            method_complexity = ComplexityAnalyzer._calculate_python_function_complexity(item)
                            methods[item.name] = {
                                'complexity': method_complexity,
                                'lines': item.end_lineno - item.lineno + 1 if item.end_lineno else 0
                            }
                            class_complexity += method_complexity
                    
                    results[node.name] = {
                        'type': 'class',
                        'complexity': class_complexity,
                        'methods': methods,
                        'start_line': node.lineno
                    }
            
            return results
        
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def _calculate_python_function_complexity(node) -> int:
        """Calculate cyclomatic complexity of a Python function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.With):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
        
        return complexity
    
    @staticmethod
    def estimate_complexity(code: str, language: str) -> int:
        """Estimate complexity for non-Python languages"""
        complexity = 1
        
        # Simple heuristics based on control flow keywords
        if language in ['javascript', 'typescript', 'java', 'cpp', 'go', 'rust']:
            # Count control structures
            complexity += len(re.findall(r'\bif\b', code))
            complexity += len(re.findall(r'\belse\s+if\b', code))
            complexity += len(re.findall(r'\bwhile\b', code))
            complexity += len(re.findall(r'\bfor\b', code))
            complexity += len(re.findall(r'\bcase\b', code))
            complexity += len(re.findall(r'\bcatch\b', code))
            complexity += len(re.findall(r'\?\s*[^?]+\s*:', code))  # Ternary operators
            complexity += len(re.findall(r'&&|\|\|', code))  # Logical operators
        
        return complexity


class VectorIndex:
    """Manages vector embeddings for semantic code search"""
    
    def __init__(self, repo_name: str):
        self.repo_name = repo_name
        self.index_path = INDEX_DIR / f"{repo_name}_vector.pkl"
        self.model = None
        self.embeddings = []
        self.symbols = []
    
    def _get_model(self):
        """Lazy load the embedding model"""
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            print("Loading embedding model (this may take a moment)...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model
    
    def add_symbols(self, symbols: List[CodeSymbol]):
        """Add symbols to the index"""
        model = self._get_model()
        
        for symbol in symbols:
            # Create rich text representation for embedding
            text = f"{symbol.name} {symbol.symbol_type}\n{symbol.code[:500]}"
            if symbol.docstring:
                text = f"{symbol.name}: {symbol.docstring}\n{text}"
            
            embedding = model.encode(text, show_progress_bar=False)
            self.embeddings.append(embedding)
            self.symbols.append(symbol)
    
    def search(self, query: str, n_results: int = 10) -> List[Tuple[CodeSymbol, float]]:
        """Search for similar code symbols"""
        if not self.embeddings:
            return []
        
        model = self._get_model()
        query_embedding = model.encode(query, show_progress_bar=False)
        
        # Calculate cosine similarity
        embeddings_matrix = np.array(self.embeddings)
        similarities = np.dot(embeddings_matrix, query_embedding) / (
            np.linalg.norm(embeddings_matrix, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:n_results]
        results = [(self.symbols[i], float(similarities[i])) for i in top_indices]
        
        return results
    
    def save(self):
        """Save the index to disk"""
        data = {
            'embeddings': self.embeddings,
            'symbols': self.symbols
        }
        with open(self.index_path, 'wb') as f:
            pickle.dump(data, f)
        print(f"Vector index saved to {self.index_path}")
    
    def load(self) -> bool:
        """Load the index from disk"""
        if not self.index_path.exists():
            return False
        
        try:
            with open(self.index_path, 'rb') as f:
                data = pickle.load(f)
            self.embeddings = data['embeddings']
            self.symbols = data['symbols']
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False


class RepoIndex:
    """Main class for indexing and analyzing repositories"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()
        self.repo_name = self.repo_path.name
        self.index_path = INDEX_DIR / f"{self.repo_name}.pkl"
        self.parser = TreeSitterParser()
        self.files: List[CodeFile] = []
        self.symbols: Dict[str, CodeSymbol] = {}
        self.vector_index = VectorIndex(self.repo_name)
        self.call_graph: Dict[str, List[str]] = defaultdict(list)
        self.reverse_call_graph: Dict[str, List[str]] = defaultdict(list)
    
    def index(self, languages: List[str] = None):
        """Build a searchable index of the repository"""
        if languages is None:
            languages = list(self.parser.LANGUAGE_MAP.keys())
        
        print(f"Indexing repository: {self.repo_path}")
        print(f"Languages: {languages}")
        
        # Find all files
        files_to_parse = []
        for lang in languages:
            ext, _, _ = self.parser.LANGUAGE_MAP.get(lang, (None, None, None))
            if ext:
                for file_path in self.repo_path.rglob(f"*{ext}"):
                    if self._should_include(file_path):
                        files_to_parse.append((file_path, lang))
            # Also check additional extensions
            extra_exts = {
                'javascript': ['.jsx'],
                'typescript': ['.tsx'],
                'cpp': ['.h', '.hpp', '.cc', '.cxx']
            }
            for extra_ext in extra_exts.get(lang, []):
                for file_path in self.repo_path.rglob(f"*{extra_ext}"):
                    if self._should_include(file_path):
                        files_to_parse.append((file_path, lang))
        
        print(f"Found {len(files_to_parse)} files to parse")
        
        # Parse files
        for i, (file_path, lang) in enumerate(files_to_parse):
            if i % 100 == 0:
                print(f"Parsed {i}/{len(files_to_parse)} files...")
            
            code_file = self.parser.parse_file(str(file_path), lang)
            if code_file:
                self.files.append(code_file)
                for symbol in code_file.symbols:
                    self.symbols[f"{symbol.file_path}::{symbol.name}"] = symbol
        
        print(f"Parsed {len(self.files)} files, found {len(self.symbols)} symbols")
        
        # Build call graph
        self._build_call_graph()
        
        # Build vector index
        print("Building vector index...")
        self.vector_index.add_symbols(list(self.symbols.values()))
        self.vector_index.save()
        
        # Save index
        self.save()
        print("Indexing complete!")
    
    def _should_include(self, file_path: Path) -> bool:
        """Check if file should be included in indexing"""
        # Skip common non-source directories
        skip_dirs = {
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            'dist', 'build', '.idea', '.vscode', 'target', 'vendor',
            'third_party', 'third-party', '.cargo', '.rustup'
        }
        
        for part in file_path.parts:
            if part in skip_dirs or part.startswith('.'):
                return False
        
        return True
    
    def _build_call_graph(self):
        """Build call graph from symbols"""
        for symbol in self.symbols.values():
            # Simple heuristic: look for calls in code
            # This is a basic implementation - a more sophisticated one would use AST analysis
            for other_symbol in self.symbols.values():
                if other_symbol.name != symbol.name:
                    # Check if this symbol calls the other
                    if re.search(rf'\b{re.escape(other_symbol.name)}\s*\(', symbol.code):
                        symbol.calls.append(other_symbol.name)
                        self.call_graph[symbol.name].append(other_symbol.name)
                        self.reverse_call_graph[other_symbol.name].append(symbol.name)
    
    def save(self):
        """Save the index to disk"""
        data = {
            'repo_path': str(self.repo_path),
            'files': self.files,
            'symbols': self.symbols,
            'call_graph': dict(self.call_graph),
            'reverse_call_graph': dict(self.reverse_call_graph)
        }
        with open(self.index_path, 'wb') as f:
            pickle.dump(data, f)
        print(f"Index saved to {self.index_path}")
    
    def load(self) -> bool:
        """Load the index from disk"""
        if not self.index_path.exists():
            return False
        
        try:
            with open(self.index_path, 'rb') as f:
                data = pickle.load(f)
            self.files = data['files']
            self.symbols = data['symbols']
            self.call_graph = defaultdict(list, data.get('call_graph', {}))
            self.reverse_call_graph = defaultdict(list, data.get('reverse_call_graph', {}))
            self.vector_index.load()
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def search(self, query: str, n_results: int = 10) -> List[Dict]:
        """Semantic search across code"""
        if not self.symbols and not self.vector_index.load():
            print("No index found. Please run index first.")
            return []
        
        results = self.vector_index.search(query, n_results)
        
        output = []
        for symbol, score in results:
            output.append({
                'name': symbol.name,
                'type': symbol.symbol_type,
                'file': symbol.file_path,
                'lines': f"{symbol.start_line}-{symbol.end_line}",
                'score': round(score, 4),
                'code_preview': symbol.code[:200] + '...' if len(symbol.code) > 200 else symbol.code
            })
        
        return output
    
    def find_symbol(self, symbol_name: str) -> List[Dict]:
        """Locate functions, classes, variables by name"""
        if not self.symbols and not self.load():
            print("No index found. Please run index first.")
            return []
        
        results = []
        for key, symbol in self.symbols.items():
            if symbol.name == symbol_name or symbol_name in symbol.name:
                results.append({
                    'name': symbol.name,
                    'type': symbol.symbol_type,
                    'file': symbol.file_path,
                    'lines': f"{symbol.start_line}-{symbol.end_line}",
                    'code': symbol.code,
                    'parent': symbol.parent
                })
        
        return results
    
    def get_call_graph(self, function_name: str) -> Dict:
        """Find callers and callees of a function"""
        if not self.symbols and not self.load():
            print("No index found. Please run index first.")
            return {}
        
        # Find all symbols with this name
        matching_symbols = [s for s in self.symbols.values() if s.name == function_name]
        
        if not matching_symbols:
            return {'error': f'Function {function_name} not found'}
        
        callees = self.call_graph.get(function_name, [])
        callers = self.reverse_call_graph.get(function_name, [])
        
        return {
            'function': function_name,
            'definitions': [
                {
                    'file': s.file_path,
                    'lines': f"{s.start_line}-{s.end_line}"
                } for s in matching_symbols
            ],
            'calls': callees,
            'called_by': callers
        }
    
    def analyze_complexity(self, file_path: str) -> Dict:
        """Analyze cyclomatic complexity of a file"""
        full_path = self.repo_path / file_path
        
        if not full_path.exists():
            return {'error': f'File not found: {file_path}'}
        
        language = self.parser.get_language_by_extension(str(full_path))
        
        if language == 'python':
            return ComplexityAnalyzer.analyze_python_complexity(str(full_path))
        else:
            # Use estimation for other languages
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                code_file = self.parser.parse_file(str(full_path), language)
                if code_file:
                    results = {}
                    for symbol in code_file.symbols:
                        complexity = ComplexityAnalyzer.estimate_complexity(symbol.code, language)
                        results[symbol.name] = {
                            'complexity': complexity,
                            'lines': symbol.end_line - symbol.start_line + 1,
                            'start_line': symbol.start_line,
                            'type': symbol.symbol_type
                        }
                    return results
                else:
                    return {'error': f'Could not parse file: {file_path}'}
            except Exception as e:
                return {'error': str(e)}
    
    def export_graph(self, output_path: str):
        """Export dependency graph for visualization"""
        if not self.symbols and not self.load():
            print("No index found. Please run index first.")
            return
        
        # Build dependency graph
        nodes = []
        edges = []
        
        for symbol_name, symbol in self.symbols.items():
            nodes.append({
                'id': symbol_name,
                'label': symbol.name,
                'type': symbol.symbol_type,
                'file': symbol.file_path
            })
            
            for callee in self.call_graph.get(symbol.name, []):
                edges.append({
                    'source': symbol_name,
                    'target': callee,
                    'type': 'calls'
                })
        
        # Export in multiple formats
        output_path = Path(output_path)
        
        # JSON format
        graph_data = {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'repo': str(self.repo_path),
                'generated': str(datetime.now())
            }
        }
        
        with open(output_path.with_suffix('.json'), 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        # Graphviz DOT format
        dot_content = "digraph CallGraph {\n"
        dot_content += "  rankdir=TB;\n"
        dot_content += "  node [shape=box, style=filled, fillcolor=lightblue];\n\n"
        
        for node in nodes:
            shape = 'ellipse' if node['type'] == 'function' else 'box'
            dot_content += f'  "{node["id"]}" [label="{node["label"]}", shape={shape}];\n'
        
        dot_content += "\n"
        
        for edge in edges:
            dot_content += f'  "{edge["source"]}" -> "{edge["target"]}";\n'
        
        dot_content += "}\n"
        
        with open(output_path.with_suffix('.dot'), 'w') as f:
            f.write(dot_content)
        
        print(f"Graph exported to {output_path}.json and {output_path}.dot")
        return str(output_path)


def main():
    parser = argparse.ArgumentParser(description='Repo Analyzer - Deep codebase indexing and semantic search')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Index command
    index_parser = subparsers.add_parser('index', help='Build searchable index')
    index_parser.add_argument('repo_path', help='Path to repository')
    index_parser.add_argument('--languages', nargs='+', 
                              default=['python', 'javascript', 'typescript', 'go', 'rust', 'java', 'cpp'],
                              help='Languages to index')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Semantic search across code')
    search_parser.add_argument('repo_name', help='Repository name (from index)')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--n-results', type=int, default=10, help='Number of results')
    
    # Find symbol command
    symbol_parser = subparsers.add_parser('find-symbol', help='Find symbol by name')
    symbol_parser.add_argument('repo_name', help='Repository name (from index)')
    symbol_parser.add_argument('symbol_name', help='Symbol name to find')
    
    # Call graph command
    call_parser = subparsers.add_parser('call-graph', help='Get call graph for function')
    call_parser.add_argument('repo_name', help='Repository name (from index)')
    call_parser.add_argument('function_name', help='Function name')
    
    # Complexity command
    complexity_parser = subparsers.add_parser('analyze-complexity', help='Analyze code complexity')
    complexity_parser.add_argument('repo_path', help='Path to repository')
    complexity_parser.add_argument('file_path', help='File path (relative to repo)')
    
    # Export graph command
    export_parser = subparsers.add_parser('export-graph', help='Export dependency graph')
    export_parser.add_argument('repo_name', help='Repository name (from index)')
    export_parser.add_argument('output_path', help='Output file path (without extension)')
    
    args = parser.parse_args()
    
    if args.command == 'index':
        repo = RepoIndex(args.repo_path)
        repo.index(args.languages)
    
    elif args.command == 'search':
        repo = RepoIndex(args.repo_name)  # repo_name is used to find index
        results = repo.search(args.query, args.n_results)
        print(json.dumps(results, indent=2))
    
    elif args.command == 'find-symbol':
        repo = RepoIndex(args.repo_name)
        results = repo.find_symbol(args.symbol_name)
        print(json.dumps(results, indent=2))
    
    elif args.command == 'call-graph':
        repo = RepoIndex(args.repo_name)
        results = repo.get_call_graph(args.function_name)
        print(json.dumps(results, indent=2))
    
    elif args.command == 'analyze-complexity':
        repo = RepoIndex(args.repo_path)
        results = repo.analyze_complexity(args.file_path)
        print(json.dumps(results, indent=2))
    
    elif args.command == 'export-graph':
        repo = RepoIndex(args.repo_name)
        repo.export_graph(args.output_path)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
