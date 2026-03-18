#!/usr/bin/env python3
"""
Vector Memory - Long-term research context with embeddings and retrieval across sessions.
Uses scikit-learn's TF-IDF for embeddings and cosine similarity for retrieval.
"""

import os
import sys
import json
import pickle
import argparse
from typing import List, Dict, Any, Optional
from pathlib import Path

# Default storage path
DEFAULT_DB_PATH = os.path.expanduser("~/.openclaw/vector-store")

class VectorMemory:
    """Simple vector memory using TF-IDF and cosine similarity."""
    
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
        self.collections = {}
        self._load_collections()
    
    def _get_collection_path(self, name: str) -> str:
        """Get the file path for a collection."""
        return os.path.join(self.db_path, f"{name}.pkl")
    
    def _load_collections(self):
        """Load all existing collections."""
        for filename in os.listdir(self.db_path):
            if filename.endswith('.pkl'):
                name = filename[:-4]
                self.collections[name] = self._load_collection(name)
    
    def _load_collection(self, name: str) -> Dict:
        """Load a single collection from disk."""
        path = self._get_collection_path(name)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def _save_collection(self, name: str, data: Dict):
        """Save a collection to disk."""
        path = self._get_collection_path(name)
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        self.collections[name] = data
    
    def _get_or_create_collection(self, name: str) -> Dict:
        """Get or create a collection."""
        if name in self.collections and self.collections[name]:
            return self.collections[name]
        
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        collection = {
            'name': name,
            'documents': [],
            'metadata': [],
            'ids': [],
            'vectorizer': TfidfVectorizer(stop_words='english'),
            'vectors': None
        }
        self._save_collection(name, collection)
        return collection
    
    def add_documents(
        self,
        texts: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None,
        collection_name: str = "default",
        auto_index: bool = True
    ) -> Dict[str, Any]:
        """Add documents to a collection."""
        try:
            import numpy as np
            
            collection = self._get_or_create_collection(collection_name)
            
            # Generate IDs
            start_idx = len(collection['documents'])
            ids = [f"{collection_name}_{start_idx + i}" for i in range(len(texts))]
            
            # Add documents
            collection['documents'].extend(texts)
            collection['ids'].extend(ids)
            
            if metadata:
                collection['metadata'].extend(metadata)
            else:
                collection['metadata'].extend([{} for _ in texts])
            
            # Re-index if auto_index is True
            if auto_index and collection['documents']:
                collection['vectors'] = collection['vectorizer'].fit_transform(
                    collection['documents']
                )
            
            self._save_collection(collection_name, collection)
            
            return {
                "success": True,
                "collection": collection_name,
                "added_count": len(texts),
                "document_ids": ids,
                "total_documents": len(collection['documents'])
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        collection_name: str = "default",
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Query documents by semantic similarity."""
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
            
            if collection_name not in self.collections or not self.collections[collection_name]:
                return {
                    "success": False,
                    "error": f"Collection '{collection_name}' not found"
                }
            
            collection = self.collections[collection_name]
            
            if not collection['documents']:
                return {
                    "success": False,
                    "error": f"Collection '{collection_name}' is empty"
                }
            
            # Transform query
            query_vector = collection['vectorizer'].transform([query_text])
            
            # Calculate similarities
            similarities = cosine_similarity(
                query_vector, 
                collection['vectors']
            ).flatten()
            
            # Get top results
            top_indices = similarities.argsort()[-n_results:][::-1]
            
            # Format results
            formatted_results = []
            for idx in top_indices:
                # Apply metadata filter if provided
                if filter_metadata:
                    match = all(
                        collection['metadata'][idx].get(k) == v 
                        for k, v in filter_metadata.items()
                    )
                    if not match:
                        continue
                
                formatted_results.append({
                    "id": collection['ids'][idx],
                    "document": collection['documents'][idx],
                    "distance": float(1 - similarities[idx]),  # Convert similarity to distance
                    "metadata": collection['metadata'][idx]
                })
            
            return {
                "success": True,
                "collection": collection_name,
                "query": query_text,
                "results": formatted_results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_collections(self) -> Dict[str, Any]:
        """List all collections."""
        try:
            collection_info = []
            for name, col in self.collections.items():
                if col:
                    collection_info.append({
                        "name": name,
                        "document_count": len(col['documents'])
                    })
            
            return {
                "success": True,
                "collections": collection_info,
                "total_collections": len(collection_info)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_collection(self, name: str) -> Dict[str, Any]:
        """Delete a collection."""
        try:
            path = self._get_collection_path(name)
            if os.path.exists(path):
                os.remove(path)
            
            if name in self.collections:
                del self.collections[name]
            
            return {
                "success": True,
                "deleted": name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_collection_info(self, name: str) -> Dict[str, Any]:
        """Get detailed info about a collection."""
        try:
            if name not in self.collections or not self.collections[name]:
                return {
                    "success": False,
                    "error": f"Collection '{name}' not found"
                }
            
            collection = self.collections[name]
            
            return {
                "success": True,
                "name": name,
                "document_count": len(collection['documents']),
                "sample_documents": collection['documents'][:5]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global memory instance
_memory = None

def get_memory(db_path: str = DEFAULT_DB_PATH) -> VectorMemory:
    """Get or create the global memory instance."""
    global _memory
    if _memory is None:
        _memory = VectorMemory(db_path)
    return _memory


def add_documents(
    texts: List[str],
    metadata: Optional[List[Dict[str, Any]]] = None,
    collection_name: str = "default",
    db_path: str = DEFAULT_DB_PATH,
    auto_index: bool = True
) -> Dict[str, Any]:
    """Add documents to a collection."""
    memory = get_memory(db_path)
    return memory.add_documents(texts, metadata, collection_name, auto_index)


def query(
    query_text: str,
    n_results: int = 5,
    collection_name: str = "default",
    db_path: str = DEFAULT_DB_PATH,
    filter_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Query documents by semantic similarity."""
    memory = get_memory(db_path)
    return memory.query(query_text, n_results, collection_name, filter_metadata)


def list_collections(db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """List all collections."""
    memory = get_memory(db_path)
    return memory.list_collections()


def delete_collection(name: str, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """Delete a collection."""
    memory = get_memory(db_path)
    return memory.delete_collection(name)


def get_collection_info(name: str, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """Get detailed info about a collection."""
    memory = get_memory(db_path)
    return memory.get_collection_info(name)


def main():
    parser = argparse.ArgumentParser(
        description="Vector Memory - Long-term research context with embeddings"
    )
    parser.add_argument(
        "--db-path",
        default=DEFAULT_DB_PATH,
        help=f"Path to vector store (default: {DEFAULT_DB_PATH})"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add documents to a collection")
    add_parser.add_argument("--collection", "-c", default="default", help="Collection name")
    add_parser.add_argument("--texts", "-t", required=True, nargs="+", help="Texts to add")
    add_parser.add_argument("--metadata", "-m", help="JSON metadata string")
    add_parser.add_argument("--auto-index", action="store_true", default=True, help="Auto-index after adding")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query documents")
    query_parser.add_argument("--collection", "-c", default="default", help="Collection name")
    query_parser.add_argument("--query", "-q", required=True, help="Query text")
    query_parser.add_argument("--n-results", "-n", type=int, default=5, help="Number of results")
    
    # List command
    subparsers.add_parser("list", help="List all collections")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a collection")
    delete_parser.add_argument("name", help="Collection name to delete")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Get collection info")
    info_parser.add_argument("name", help="Collection name")
    
    args = parser.parse_args()
    
    if args.command == "add":
        metadata = None
        if args.metadata:
            try:
                metadata = [json.loads(args.metadata)] * len(args.texts)
            except json.JSONDecodeError:
                print(json.dumps({"success": False, "error": "Invalid JSON metadata"}))
                sys.exit(1)
        
        result = add_documents(
            texts=args.texts,
            metadata=metadata,
            collection_name=args.collection,
            db_path=args.db_path,
            auto_index=args.auto_index
        )
        print(json.dumps(result, indent=2))
    
    elif args.command == "query":
        result = query(
            query_text=args.query,
            n_results=args.n_results,
            collection_name=args.collection,
            db_path=args.db_path
        )
        print(json.dumps(result, indent=2))
    
    elif args.command == "list":
        result = list_collections(db_path=args.db_path)
        print(json.dumps(result, indent=2))
    
    elif args.command == "delete":
        result = delete_collection(name=args.name, db_path=args.db_path)
        print(json.dumps(result, indent=2))
    
    elif args.command == "info":
        result = get_collection_info(name=args.name, db_path=args.db_path)
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
