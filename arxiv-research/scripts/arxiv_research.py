#!/usr/bin/env python3
"""
arXiv Research Tool - Main script for fetching, parsing, and summarizing arXiv papers.
"""

import argparse
import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any

# Check and install dependencies if needed
try:
    import arxiv
except ImportError:
    print("Installing arxiv library...")
    os.system(f"{sys.executable} -m pip install arxiv -q")
    import arxiv

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing pymupdf...")
    os.system(f"{sys.executable} -m pip install pymupdf -q")
    import fitz


class ArxivCache:
    """Simple file-based cache for downloaded papers."""
    
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/arxiv-research")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def get_paper_path(self, paper_id: str) -> Optional[Path]:
        """Get cached paper path if it exists."""
        paper_id = self._normalize_id(paper_id)
        if paper_id in self.metadata:
            pdf_path = self.cache_dir / f"{paper_id}.pdf"
            if pdf_path.exists():
                return pdf_path
        return None
    
    def cache_paper(self, paper_id: str, pdf_path: str, metadata: Dict = None):
        """Cache a downloaded paper."""
        paper_id = self._normalize_id(paper_id)
        dest_path = self.cache_dir / f"{paper_id}.pdf"
        
        # Copy file to cache if not already there
        import shutil
        if Path(pdf_path) != dest_path:
            shutil.copy2(pdf_path, dest_path)
        
        # Update metadata
        self.metadata[paper_id] = {
            "pdf_path": str(dest_path),
            "metadata": metadata or {}
        }
        self._save_metadata()
        return dest_path
    
    def _normalize_id(self, paper_id: str) -> str:
        """Normalize paper ID (remove version, lowercase)."""
        paper_id = paper_id.lower().strip()
        if 'v' in paper_id and paper_id.split('v')[-1].isdigit():
            paper_id = paper_id.rsplit('v', 1)[0]
        return paper_id
    
    def list_cached(self) -> List[str]:
        """List all cached paper IDs."""
        return list(self.metadata.keys())
    
    def clear_cache(self):
        """Clear all cached papers."""
        for pdf_file in self.cache_dir.glob("*.pdf"):
            pdf_file.unlink()
        self.metadata = {}
        self._save_metadata()


class ArxivResearch:
    """Main class for arXiv research operations."""
    
    def __init__(self, cache_dir: str = None):
        self.cache = ArxivCache(cache_dir)
        self.client = arxiv.Client()
    
    def search(self, query: str, max_results: int = 10, sort_by: str = 'relevance') -> List[Dict]:
        """
        Search for papers on arXiv.
        
        Args:
            query: Search query string
            max_results: Maximum number of results (default: 10)
            sort_by: Sort by 'relevance', 'lastUpdatedDate', or 'submittedDate'
        
        Returns:
            List of paper dictionaries
        """
        sort_criteria = {
            'relevance': arxiv.SortCriterion.Relevance,
            'lastupdateddate': arxiv.SortCriterion.LastUpdatedDate,
            'submitteddate': arxiv.SortCriterion.SubmittedDate,
        }
        
        sort_criterion = sort_criteria.get(sort_by.lower(), arxiv.SortCriterion.Relevance)
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criterion
        )
        
        results = []
        for paper in self.client.results(search):
            results.append({
                'id': paper.get_short_id(),
                'title': paper.title,
                'authors': [str(a) for a in paper.authors],
                'summary': paper.summary,
                'published': paper.published.isoformat() if paper.published else None,
                'updated': paper.updated.isoformat() if paper.updated else None,
                'primary_category': paper.primary_category,
                'categories': paper.categories,
                'pdf_url': paper.pdf_url,
                'entry_id': paper.entry_id
            })
        
        return results
    
    def download(self, paper_id: str, output_dir: str = None, use_cache: bool = True) -> str:
        """
        Download a paper from arXiv.
        
        Args:
            paper_id: arXiv paper ID
            output_dir: Directory to save the PDF (default: current directory)
            use_cache: Whether to use cached version if available
        
        Returns:
            Path to downloaded PDF file
        """
        # Check cache first
        if use_cache:
            cached_path = self.cache.get_paper_path(paper_id)
            if cached_path:
                print(f"Using cached paper: {cached_path}")
                return str(cached_path)
        
        # Download from arXiv
        search = arxiv.Search(id_list=[paper_id])
        paper = next(self.client.results(search), None)
        
        if paper is None:
            raise ValueError(f"Paper not found: {paper_id}")
        
        # Determine output path
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = Path.cwd()
        
        # Download PDF
        pdf_path = paper.download_pdf(dirpath=str(output_path))
        
        # Cache the downloaded paper
        metadata = {
            'title': paper.title,
            'authors': [str(a) for a in paper.authors],
            'published': paper.published.isoformat() if paper.published else None,
            'primary_category': paper.primary_category
        }
        self.cache.cache_paper(paper_id, pdf_path, metadata)
        
        return pdf_path
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract full text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
        
        Returns:
            Full text content of the PDF
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        text = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text.append(page.get_text())
        
        return "\n\n".join(text)
    
    def extract_sections(self, pdf_path: str) -> Dict[str, str]:
        """
        Extract text organized by sections.
        
        Args:
            pdf_path: Path to the PDF file
        
        Returns:
            Dictionary mapping section names to their text content
        """
        full_text = self.extract_text(pdf_path)
        sections = {}
        
        # Common section headers in academic papers
        common_sections = [
            'abstract', 'introduction', 'related work', 'background',
            'method', 'methods', 'methodology', 'approach',
            'experiments', 'experimental setup', 'evaluation',
            'results', 'discussion', 'conclusion', 'conclusions',
            'future work', 'acknowledgments', 'references'
        ]
        
        lines = full_text.split('\n')
        current_section = 'header'
        current_text = []
        
        for line in lines:
            line_stripped = line.strip().lower()
            # Check if line looks like a section header
            is_header = False
            for section in common_sections:
                if (line_stripped == section or 
                    line_stripped == section + '.' or
                    line_stripped.startswith(section + ' ') or
                    line_stripped.startswith(str(common_sections.index(section) + 1) + ' ') or
                    (len(line_stripped) < 50 and section in line_stripped and line_stripped.isupper())):
                    
                    if current_text:
                        sections[current_section] = '\n'.join(current_text).strip()
                    current_section = section
                    current_text = []
                    is_header = True
                    break
            
            if not is_header:
                current_text.append(line)
        
        # Add the last section
        if current_text:
            sections[current_section] = '\n'.join(current_text).strip()
        
        return sections
    
    def summarize(self, paper_id: str = None, pdf_path: str = None, method: str = 'abstract') -> Dict[str, Any]:
        """
        Summarize a paper.
        
        Args:
            paper_id: arXiv paper ID (alternative to pdf_path)
            pdf_path: Path to PDF file (alternative to paper_id)
            method: Summarization method - 'abstract', 'full', or 'sections'
        
        Returns:
            Dictionary with summary information
        """
        if paper_id:
            # Get paper metadata from arXiv
            search = arxiv.Search(id_list=[paper_id])
            paper = next(self.client.results(search), None)
            
            if paper is None:
                raise ValueError(f"Paper not found: {paper_id}")
            
            # Download if needed for full text methods
            if method in ['full', 'sections']:
                pdf_path = self.download(paper_id, use_cache=True)
            
            result = {
                'id': paper.get_short_id(),
                'title': paper.title,
                'authors': [str(a) for a in paper.authors],
                'published': paper.published.isoformat() if paper.published else None,
                'primary_category': paper.primary_category,
                'url': paper.pdf_url
            }
            
            if method == 'abstract':
                result['summary'] = paper.summary
                result['method'] = 'abstract'
            
            elif method == 'full':
                result['full_text'] = self.extract_text(pdf_path)
                result['method'] = 'full'
            
            elif method == 'sections':
                result['sections'] = self.extract_sections(pdf_path)
                result['method'] = 'sections'
            
            return result
        
        elif pdf_path:
            result = {
                'pdf_path': str(pdf_path),
            }
            
            if method == 'full':
                result['full_text'] = self.extract_text(pdf_path)
                result['method'] = 'full'
            
            elif method == 'sections':
                result['sections'] = self.extract_sections(pdf_path)
                result['method'] = 'sections'
            
            else:
                result['full_text'] = self.extract_text(pdf_path)
                result['method'] = 'full'
            
            return result
        
        else:
            raise ValueError("Either paper_id or pdf_path must be provided")
    
    def get_bibtex(self, paper_id: str) -> str:
        """
        Get BibTeX citation for a paper.
        
        Args:
            paper_id: arXiv paper ID
        
        Returns:
            BibTeX formatted citation string
        """
        search = arxiv.Search(id_list=[paper_id])
        paper = next(self.client.results(search), None)
        
        if paper is None:
            raise ValueError(f"Paper not found: {paper_id}")
        
        # Generate BibTeX entry
        authors = ' and '.join([str(a) for a in paper.authors])
        year = paper.published.year if paper.published else 'Unknown'
        
        # Create cite key from first author and year
        first_author = str(paper.authors[0]).split()[-1] if paper.authors else 'Unknown'
        cite_key = f"{first_author.lower()}{year}{paper.get_short_id().split('.')[0]}"
        
        bibtex = f"""@article{{{cite_key},
  title={{ {paper.title} }},
  author={{ {authors} }},
  journal={{arXiv preprint arXiv:{paper.get_short_id()}}},
  year={{ {year} }},
  url={{ {paper.pdf_url} }}
}}"""
        
        return bibtex
    
    def batch_download(self, query: str, max_results: int, output_dir: str = None) -> List[str]:
        """
        Download multiple papers matching a query.
        
        Args:
            query: Search query string
            max_results: Maximum number of papers to download
            output_dir: Directory to save PDFs (default: current directory)
        
        Returns:
            List of downloaded PDF file paths
        """
        papers = self.search(query, max_results=max_results)
        downloaded = []
        
        for paper_info in papers:
            try:
                pdf_path = self.download(paper_info['id'], output_dir, use_cache=True)
                downloaded.append(pdf_path)
                print(f"Downloaded: {paper_info['title'][:60]}...")
            except Exception as e:
                print(f"Failed to download {paper_info['id']}: {e}")
        
        return downloaded


def main():
    parser = argparse.ArgumentParser(description='arXiv Research Tool')
    parser.add_argument('--cache-dir', help='Custom cache directory')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for papers')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--max-results', type=int, default=10, help='Maximum results')
    search_parser.add_argument('--sort-by', default='relevance', 
                               choices=['relevance', 'lastUpdatedDate', 'submittedDate'],
                               help='Sort criteria')
    search_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download a paper')
    download_parser.add_argument('paper_id', help='arXiv paper ID')
    download_parser.add_argument('--output-dir', '-o', help='Output directory')
    download_parser.add_argument('--no-cache', action='store_true', help='Skip cache')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract text from PDF')
    extract_parser.add_argument('pdf_path', help='Path to PDF file')
    extract_parser.add_argument('--sections', action='store_true', help='Extract by sections')
    
    # Summarize command
    summarize_parser = subparsers.add_parser('summarize', help='Summarize a paper')
    summarize_parser.add_argument('--paper-id', help='arXiv paper ID')
    summarize_parser.add_argument('--pdf-path', help='Path to PDF file')
    summarize_parser.add_argument('--method', default='abstract',
                                  choices=['abstract', 'full', 'sections'],
                                  help='Summarization method')
    summarize_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # BibTeX command
    bibtex_parser = subparsers.add_parser('bibtex', help='Get BibTeX citation')
    bibtex_parser.add_argument('paper_id', help='arXiv paper ID')
    
    # Batch download command
    batch_parser = subparsers.add_parser('batch-download', help='Download multiple papers')
    batch_parser.add_argument('query', help='Search query')
    batch_parser.add_argument('--max-results', type=int, default=10, help='Maximum papers')
    batch_parser.add_argument('--output-dir', '-o', help='Output directory')
    
    # Cache commands
    cache_parser = subparsers.add_parser('cache', help='Cache management')
    cache_parser.add_argument('--list', action='store_true', help='List cached papers')
    cache_parser.add_argument('--clear', action='store_true', help='Clear cache')
    
    args = parser.parse_args()
    
    # Initialize research tool
    research = ArxivResearch(cache_dir=args.cache_dir)
    
    if args.command == 'search':
        results = research.search(args.query, args.max_results, args.sort_by)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for i, paper in enumerate(results, 1):
                print(f"\n{'='*60}")
                print(f"{i}. {paper['title']}")
                print(f"   ID: {paper['id']}")
                print(f"   Authors: {', '.join(paper['authors'][:3])}")
                if len(paper['authors']) > 3:
                    print(f"   ... and {len(paper['authors']) - 3} more")
                print(f"   Published: {paper['published']}")
                print(f"   Category: {paper['primary_category']}")
                print(f"   URL: {paper['pdf_url']}")
                print(f"   Abstract: {paper['summary'][:200]}...")
    
    elif args.command == 'download':
        pdf_path = research.download(args.paper_id, args.output_dir, use_cache=not args.no_cache)
        print(f"Downloaded to: {pdf_path}")
    
    elif args.command == 'extract':
        if args.sections:
            sections = research.extract_sections(args.pdf_path)
            for section, text in sections.items():
                print(f"\n{'='*60}")
                print(f"SECTION: {section.upper()}")
                print(f"{'='*60}")
                print(text[:2000] if len(text) > 2000 else text)
                if len(text) > 2000:
                    print(f"... [{len(text)} characters total]")
        else:
            text = research.extract_text(args.pdf_path)
            print(text)
    
    elif args.command == 'summarize':
        if not args.paper_id and not args.pdf_path:
            print("Error: Either --paper-id or --pdf-path must be provided")
            sys.exit(1)
        
        summary = research.summarize(args.paper_id, args.pdf_path, args.method)
        
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"PAPER SUMMARY")
            print(f"{'='*60}")
            
            if 'title' in summary:
                print(f"\nTitle: {summary['title']}")
                print(f"Authors: {', '.join(summary['authors'])}")
                print(f"Published: {summary['published']}")
                print(f"Category: {summary['primary_category']}")
            
            if args.method == 'abstract':
                print(f"\nAbstract:\n{summary['summary']}")
            elif args.method == 'full':
                text = summary['full_text']
                print(f"\nFull Text Preview:\n{text[:2000]}...")
                print(f"\n[Total: {len(text)} characters]")
            elif args.method == 'sections':
                print("\nSections:")
                for section, text in summary['sections'].items():
                    preview = text[:200].replace('\n', ' ')
                    print(f"  - {section}: {preview}...")
    
    elif args.command == 'bibtex':
        bibtex = research.get_bibtex(args.paper_id)
        print(bibtex)
    
    elif args.command == 'batch-download':
        paths = research.batch_download(args.query, args.max_results, args.output_dir)
        print(f"\nDownloaded {len(paths)} papers:")
        for path in paths:
            print(f"  - {path}")
    
    elif args.command == 'cache':
        if args.list:
            cached = research.cache.list_cached()
            print(f"Cached papers ({len(cached)}):")
            for pid in cached:
                meta = research.cache.metadata.get(pid, {})
                title = meta.get('metadata', {}).get('title', 'Unknown')
                print(f"  - {pid}: {title[:50]}...")
        elif args.clear:
            research.cache.clear_cache()
            print("Cache cleared")
        else:
            print("Use --list or --clear")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
