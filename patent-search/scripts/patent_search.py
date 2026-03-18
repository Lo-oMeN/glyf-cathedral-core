#!/usr/bin/env python3
"""
Patent Search Skill - Prior Art Research Tool
Supports USPTO Patent Public Search API and Google Patents
"""

import os
import sys
import json
import time
import hashlib
import requests
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from difflib import SequenceMatcher
import re

# Cache configuration
CACHE_DIR = Path(os.path.expanduser("~/.cache/patent-search"))
CACHE_TTL_HOURS = 24  # Cache expiry in hours

# API endpoints
USPTO_PATENT_API = "https://api.patentsview.org/patents/query"  # Note: API discontinued
USPTO_OPEN_DATA = "https://developer.uspto.gov/ibd-api/v1/application/publications"
GOOGLE_PATENTS_DETAIL = "https://patents.google.com/patent/{}/en"

# EPO Open Patent Services
EPO_SEARCH_URL = "https://ops.epo.org/3.2/rest-services/published-data/search"

class PatentCache:
    """Simple file-based cache for patent data."""
    
    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, key: str) -> str:
        """Generate a safe cache key from input."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{self._get_cache_key(key)}.json"
    
    def get(self, key: str) -> Optional[Dict]:
        """Retrieve cached data if not expired."""
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cached = json.load(f)
            
            # Check expiry
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time > timedelta(hours=CACHE_TTL_HOURS):
                cache_path.unlink()  # Delete expired cache
                return None
            
            return cached['data']
        except (json.JSONDecodeError, KeyError, OSError):
            return None
    
    def set(self, key: str, data: Dict) -> None:
        """Store data in cache."""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'data': data
                }, f, indent=2)
        except OSError:
            pass  # Fail silently if cache can't be written


class PatentSearch:
    """Main patent search class supporting multiple sources."""
    
    def __init__(self):
        self.cache = PatentCache()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search(self, query: str, patent_office: str = 'USPTO', max_results: int = 20) -> Dict[str, Any]:
        """
        Search for patents by query string.
        
        Args:
            query: Search query (e.g., "machine learning", "inventor:Tesla")
            patent_office: Patent office to search ('USPTO', 'Google', or 'EPO')
            max_results: Maximum number of results (default: 20)
        
        Returns:
            Dictionary with search results
        """
        cache_key = f"search:{patent_office}:{query}:{max_results}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        if patent_office.upper() == 'EPO':
            results = self._search_epo(query, max_results)
        else:
            # Default to Google Patents as USPTO API is limited
            results = self._search_google_patents(query, max_results)
        
        self.cache.set(cache_key, results)
        return results
    
    def _search_google_patents(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search using Google Patents web interface."""
        try:
            # Parse field-specific queries
            search_query = query
            if ':' in query:
                field, value = query.split(':', 1)
                field = field.strip().lower()
                value = value.strip().strip('"\'')
                
                # Build Google Patents search syntax
                field_map = {
                    'inventor': 'inventor:',
                    'assignee': 'assignee:',
                    'title': 'title:',
                    'number': ''  # Just the number
                }
                
                if field in field_map:
                    search_query = f"{field_map[field]}{value}"
                else:
                    search_query = value
            
            # Google Patents uses a specific search URL format
            url = f"https://patents.google.com/?q={requests.utils.quote(search_query)}"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}',
                    'patents': [],
                    'source': 'Google Patents'
                }
            
            html = response.text
            patents = []
            
            # Extract patent data from embedded JSON if available
            json_match = re.search(r'var\s+patents\s*=\s*(\[.*?\]);', html, re.DOTALL)
            if json_match:
                try:
                    patent_data = json.loads(json_match.group(1))
                    for item in patent_data[:max_results]:
                        patent = {
                            'number': item.get('publication_number', 'N/A'),
                            'title': item.get('title', 'N/A'),
                            'date': item.get('publication_date', 'N/A'),
                            'inventor': item.get('inventor', 'N/A'),
                            'assignee': item.get('assignee', 'N/A')
                        }
                        patents.append(patent)
                except json.JSONDecodeError:
                    pass
            
            # Fallback: extract from HTML patterns
            if not patents:
                # Extract patent numbers from links
                patent_links = re.findall(r'href="/patent/([^"]+)"', html)
                seen = set()
                for link in patent_links[:max_results]:
                    patent_num = link.split('/')[0] if '/' in link else link
                    if patent_num not in seen:
                        seen.add(patent_num)
                        patents.append({
                            'number': patent_num,
                            'title': 'Details available via get_details()',
                            'date': 'N/A',
                            'inventor': 'N/A',
                            'assignee': 'N/A'
                        })
            
            return {
                'success': True,
                'total': len(patents),
                'patents': patents,
                'source': 'Google Patents'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'patents': [],
                'source': 'Google Patents'
            }
    
    def _search_epo(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search using EPO Open Patent Services (requires registration)."""
        # EPO OPS requires OAuth authentication
        # This is a placeholder for EPO integration
        return {
            'success': False,
            'error': 'EPO API requires OAuth authentication. Please configure credentials.',
            'patents': [],
            'source': 'EPO'
        }
    
    def get_details(self, patent_number: str) -> Dict[str, Any]:
        """
        Get full patent details including abstract and claims.
        
        Args:
            patent_number: Patent number (e.g., "US6304886B1" or "6,304,886")
        
        Returns:
            Dictionary with full patent information
        """
        cache_key = f"details:{patent_number}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Normalize patent number
        patent_number = self._normalize_patent_number(patent_number)
        
        try:
            result = self._get_details_google(patent_number)
            self.cache.set(cache_key, result)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'patent_number': patent_number
            }
    
    def _normalize_patent_number(self, number: str) -> str:
        """Normalize patent number format."""
        # Remove commas and whitespace
        number = number.replace(',', '').replace(' ', '').upper()
        
        # Add US prefix if not present and no other country code
        if not any(number.startswith(prefix) for prefix in ['US', 'EP', 'WO', 'CN', 'JP', 'KR', 'DE', 'FR', 'GB']):
            number = 'US' + number
        
        return number
    
    def _get_details_google(self, patent_number: str) -> Dict[str, Any]:
        """Get patent details from Google Patents."""
        url = GOOGLE_PATENTS_DETAIL.format(patent_number)
        
        response = self.session.get(url, timeout=30)
        
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'Failed to retrieve patent details (HTTP {response.status_code})'
            }
        
        html = response.text
        
        # Extract patent data from embedded JSON
        json_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', html, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                # Navigate the JSON structure
                patent_data = data.get('patent', {})
                if patent_data:
                    return self._parse_google_patent_json(patent_data, patent_number)
            except json.JSONDecodeError:
                pass
        
        # Fallback to HTML parsing
        return self._parse_google_patent_html(html, patent_number)
    
    def _parse_google_patent_json(self, data: Dict, patent_number: str) -> Dict[str, Any]:
        """Parse patent data from Google Patents JSON structure."""
        metadata = data.get('metadata', {})
        
        # Extract bibliographic data
        biblio = data.get('biblio', {})
        
        # Get title
        title = biblio.get('title', {}).get('text', ['Unknown'])[0] if isinstance(biblio.get('title'), dict) else 'Unknown'
        
        # Get abstract
        abstract_data = biblio.get('abstract', [])
        abstract = ' '.join([a.get('text', '') for a in abstract_data]) if abstract_data else 'No abstract available'
        
        # Get inventors
        inventors = []
        for inv in biblio.get('parties', {}).get('inventors', []):
            name = inv.get('name', {}).get('name', '')
            if name:
                inventors.append(name)
        
        # Get assignees
        assignees = []
        for assignee in biblio.get('parties', {}).get('assignees', []):
            name = assignee.get('name', {}).get('name', '')
            if name:
                assignees.append(name)
        
        # Get date
        dates = biblio.get('publication', {}).get('date', '')
        
        # Get claims
        claims_data = data.get('claims', {}).get('claims', [])
        claims = []
        for claim in claims_data:
            claim_text = claim.get('text', '')
            if claim_text:
                claims.append(claim_text)
        
        return {
            'success': True,
            'patent_number': patent_number,
            'title': title,
            'date': dates,
            'kind': biblio.get('publication', {}).get('kind', ''),
            'abstract': abstract,
            'inventors': inventors,
            'assignees': assignees,
            'claims': claims[:10],  # Limit to first 10 claims
            'source': 'Google Patents'
        }
    
    def _parse_google_patent_html(self, html: str, patent_number: str) -> Dict[str, Any]:
        """Parse patent data from Google Patents HTML."""
        # Extract title
        title_match = re.search(r'<title>(.*?) - Google Patents</title>', html, re.IGNORECASE)
        title = title_match.group(1) if title_match else 'Unknown'
        
        # Extract abstract
        abstract_match = re.search(r'class="abstract"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
        if abstract_match:
            abstract = re.sub(r'<[^>]+>', '', abstract_match.group(1)).strip()
        else:
            # Try alternative patterns
            abstract_match = re.search(r'Abstract[\s\S]*?<div[^>]*>(.*?)</div>', html, re.IGNORECASE)
            abstract = re.sub(r'<[^>]+>', '', abstract_match.group(1)).strip() if abstract_match else 'No abstract available'
        
        # Extract inventors
        inventors = []
        inventor_matches = re.findall(r'inventor[^>]*>([^<]+)</a>', html, re.IGNORECASE)
        for inv in inventor_matches:
            if inv.strip() and inv not in inventors:
                inventors.append(inv.strip())
        
        # Extract assignee
        assignee_match = re.search(r'assignee[^>]*>([^<]+)</', html, re.IGNORECASE)
        assignee = assignee_match.group(1).strip() if assignee_match else 'Unknown'
        
        # Extract date
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
        date = date_match.group(1) if date_match else 'Unknown'
        
        # Extract claims
        claims = []
        claims_section = re.search(r'Claims[\s\S]*?<ol[^>]*>(.*?)</ol>', html, re.IGNORECASE)
        if claims_section:
            claim_items = re.findall(r'<li[^>]*>(.*?)</li>', claims_section.group(1), re.DOTALL)
            for claim in claim_items:
                claim_text = re.sub(r'<[^>]+>', ' ', claim).strip()
                if claim_text:
                    claims.append(claim_text)
        
        return {
            'success': True,
            'patent_number': patent_number,
            'title': title,
            'date': date,
            'abstract': abstract,
            'inventors': inventors,
            'assignees': [assignee] if assignee != 'Unknown' else [],
            'claims': claims,
            'source': 'Google Patents'
        }
    
    def download_pdf(self, patent_number: str, output_path: str) -> Dict[str, Any]:
        """
        Download patent PDF from available sources.
        
        Args:
            patent_number: Patent number
            output_path: Path to save the PDF
        
        Returns:
            Dictionary with download status
        """
        patent_number = self._normalize_patent_number(patent_number)
        clean_number = patent_number.replace('US', '').replace('B1', '').replace('B2', '').replace('A1', '')
        
        try:
            # Try USPTO PDF download first
            uspto_url = f"https://patents.google.com/patent/US{clean_number}/en"
            
            response = self.session.get(uspto_url, timeout=60)
            
            if response.status_code == 200:
                # Check if we got HTML (need to extract PDF link) or direct PDF
                content_type = response.headers.get('Content-Type', '')
                
                if 'pdf' in content_type:
                    # Direct PDF response
                    output_path = Path(output_path)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    
                    return {
                        'success': True,
                        'patent_number': patent_number,
                        'output_path': str(output_path),
                        'size_bytes': len(response.content),
                        'source': 'USPTO'
                    }
                else:
                    # HTML response - try to extract PDF link
                    pdf_match = re.search(r'href="([^"]*\.pdf)"', response.text)
                    if pdf_match:
                        pdf_link = pdf_match.group(1)
                        if pdf_link.startswith('/'):
                            pdf_link = f"https://patents.google.com{pdf_link}"
                        
                        pdf_response = self.session.get(pdf_link, timeout=60)
                        
                        if pdf_response.status_code == 200:
                            output_path = Path(output_path)
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            with open(output_path, 'wb') as f:
                                f.write(pdf_response.content)
                            
                            return {
                                'success': True,
                                'patent_number': patent_number,
                                'output_path': str(output_path),
                                'size_bytes': len(pdf_response.content),
                                'source': 'Google Patents'
                            }
            
            return {
                'success': False,
                'error': 'Could not download PDF. Patent may not be available in PDF format.'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def compare(self, patent1: str, patent2: str) -> Dict[str, Any]:
        """
        Compare two patents for similarity analysis.
        
        Args:
            patent1: First patent number
            patent2: Second patent number
        
        Returns:
            Dictionary with similarity analysis
        """
        details1 = self.get_details(patent1)
        details2 = self.get_details(patent2)
        
        if not details1.get('success'):
            return {'success': False, 'error': f'Could not retrieve details for {patent1}'}
        
        if not details2.get('success'):
            return {'success': False, 'error': f'Could not retrieve details for {patent2}'}
        
        # Calculate text similarities
        title_sim = self._text_similarity(details1.get('title', ''), details2.get('title', ''))
        abstract_sim = self._text_similarity(details1.get('abstract', ''), details2.get('abstract', ''))
        
        # Compare claims if available
        claims1 = ' '.join(details1.get('claims', []))
        claims2 = ' '.join(details2.get('claims', []))
        claims_sim = self._text_similarity(claims1, claims2) if claims1 and claims2 else 0.0
        
        # Check for common inventors
        inventors1 = set(details1.get('inventors', []))
        inventors2 = set(details2.get('inventors', []))
        common_inventors = inventors1.intersection(inventors2)
        
        # Check for common assignees
        assignees1 = set(details1.get('assignees', []))
        assignees2 = set(details2.get('assignees', []))
        common_assignees = assignees1.intersection(assignees2)
        
        # Overall similarity score (weighted average)
        overall_sim = (title_sim * 0.25 + abstract_sim * 0.35 + claims_sim * 0.25 + 
                      (0.1 if common_inventors else 0) + (0.05 if common_assignees else 0))
        overall_sim = min(overall_sim, 1.0)  # Cap at 1.0
        
        return {
            'success': True,
            'patent1': patent1,
            'patent2': patent2,
            'similarity_scores': {
                'title': round(title_sim, 3),
                'abstract': round(abstract_sim, 3),
                'claims': round(claims_sim, 3),
                'overall': round(overall_sim, 3)
            },
            'common_inventors': list(common_inventors),
            'common_assignees': list(common_assignees),
            'patent1_details': {
                'title': details1.get('title'),
                'date': details1.get('date'),
                'assignees': details1.get('assignees', [])
            },
            'patent2_details': {
                'title': details2.get('title'),
                'date': details2.get('date'),
                'assignees': details2.get('assignees', [])
            }
        }
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings using SequenceMatcher."""
        if not text1 or not text2:
            return 0.0
        
        # Normalize text
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()
        
        return SequenceMatcher(None, text1, text2).ratio()
    
    def track_family(self, patent_number: str) -> Dict[str, Any]:
        """
        Track patent family - related patents in other jurisdictions.
        
        Args:
            patent_number: Patent number
        
        Returns:
            Dictionary with related patents in other jurisdictions
        """
        patent_number = self._normalize_patent_number(patent_number)
        
        cache_key = f"family:{patent_number}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        try:
            # Get current patent details
            details = self.get_details(patent_number)
            
            if not details.get('success'):
                return {'success': False, 'error': 'Could not retrieve patent details'}
            
            # Search for related patents using title keywords
            title = details.get('title', '')
            title_keywords = ' '.join(title.split()[:5]) if title else ''
            
            if not title_keywords:
                return {
                    'success': True,
                    'original_patent': patent_number,
                    'original_title': title,
                    'family_members': [],
                    'family_count': 0
                }
            
            # Search in different jurisdictions
            family_members = []
            jurisdictions = ['EP', 'WO', 'CN', 'JP', 'KR']
            
            for jurisdiction in jurisdictions:
                # Add small delay to be respectful
                time.sleep(0.5)
                
                search_result = self._search_google_patents(f"{jurisdiction} {title_keywords}", 3)
                for patent in search_result.get('patents', []):
                    if patent['number'].startswith(jurisdiction):
                        family_members.append({
                            'number': patent['number'],
                            'jurisdiction': jurisdiction,
                            'title': patent.get('title', 'N/A'),
                            'status': 'potential_family_member'
                        })
            
            result = {
                'success': True,
                'original_patent': patent_number,
                'original_title': title,
                'family_members': family_members,
                'family_count': len(family_members)
            }
            
            self.cache.set(cache_key, result)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    parser = argparse.ArgumentParser(description='Patent Search Tool for Prior Art Research')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for patents')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--office', default='Google', choices=['Google', 'EPO'], 
                               help='Patent source to search (default: Google)')
    search_parser.add_argument('--max-results', type=int, default=20, 
                               help='Maximum number of results (default: 20)')
    search_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Details command
    details_parser = subparsers.add_parser('details', help='Get patent details')
    details_parser.add_argument('patent_number', help='Patent number (e.g., US6304886B1)')
    details_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download patent PDF')
    download_parser.add_argument('patent_number', help='Patent number')
    download_parser.add_argument('output_path', help='Output file path')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two patents')
    compare_parser.add_argument('patent1', help='First patent number')
    compare_parser.add_argument('patent2', help='Second patent number')
    compare_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Family command
    family_parser = subparsers.add_parser('family', help='Track patent family')
    family_parser.add_argument('patent_number', help='Patent number')
    family_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    search_tool = PatentSearch()
    
    if args.command == 'search':
        result = search_tool.search(args.query, args.office, args.max_results)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get('success'):
                print(f"\nFound {result['total']} patents from {result['source']}:\n")
                print(f"{'Patent Number':<18} {'Date':<12} {'Title':<50}")
                print("-" * 80)
                for p in result['patents']:
                    title = p['title'][:47] + '...' if len(p['title']) > 50 else p['title']
                    print(f"{p['number']:<18} {p['date']:<12} {title:<50}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
    
    elif args.command == 'details':
        result = search_tool.get_details(args.patent_number)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get('success'):
                print(f"\n{'='*70}")
                print(f"Patent: {result['patent_number']}")
                print(f"Title: {result['title']}")
                print(f"Date: {result.get('date', 'N/A')}")
                if result.get('kind'):
                    print(f"Kind: {result['kind']}")
                print(f"Source: {result.get('source', 'Unknown')}")
                print(f"{'='*70}\n")
                print(f"Inventors: {', '.join(result.get('inventors', ['N/A']))}")
                print(f"Assignees: {', '.join(result.get('assignees', ['N/A']))}")
                print(f"\nAbstract:\n{result.get('abstract', 'N/A')}")
                
                claims = result.get('claims', [])
                if claims:
                    print(f"\n{'='*70}")
                    print(f"Claims ({len(claims)} shown):")
                    print(f"{'='*70}")
                    for i, claim in enumerate(claims[:5], 1):
                        claim_preview = claim[:200] + '...' if len(claim) > 200 else claim
                        print(f"\n{i}. {claim_preview}")
                    if len(claims) > 5:
                        print(f"\n... and {len(claims) - 5} more claims")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
    
    elif args.command == 'download':
        result = search_tool.download_pdf(args.patent_number, args.output_path)
        
        if result.get('success'):
            print(f"Downloaded PDF for {result['patent_number']}")
            print(f"Saved to: {result['output_path']}")
            print(f"Size: {result['size_bytes']:,} bytes ({result['size_bytes']/1024/1024:.2f} MB)")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    elif args.command == 'compare':
        result = search_tool.compare(args.patent1, args.patent2)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get('success'):
                print(f"\n{'='*70}")
                print(f"Patent Comparison")
                print(f"{'='*70}\n")
                print(f"Patent 1: {result['patent1']}")
                print(f"  Title: {result['patent1_details']['title']}")
                print(f"  Date: {result['patent1_details']['date']}")
                print(f"\nPatent 2: {result['patent2']}")
                print(f"  Title: {result['patent2_details']['title']}")
                print(f"  Date: {result['patent2_details']['date']}")
                print(f"\n{'='*70}")
                print(f"Similarity Scores:")
                print(f"{'='*70}")
                scores = result['similarity_scores']
                print(f"  Title:      {scores['title']:.1%}")
                print(f"  Abstract:   {scores['abstract']:.1%}")
                if 'claims' in scores:
                    print(f"  Claims:     {scores['claims']:.1%}")
                print(f"  Overall:    {scores['overall']:.1%}")
                print(f"\nCommon Inventors: {', '.join(result['common_inventors']) or 'None'}")
                print(f"Common Assignees: {', '.join(result['common_assignees']) or 'None'}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
    
    elif args.command == 'family':
        result = search_tool.track_family(args.patent_number)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get('success'):
                print(f"\n{'='*70}")
                print(f"Patent Family Tracking")
                print(f"{'='*70}\n")
                print(f"Original Patent: {result['original_patent']}")
                print(f"Title: {result['original_title']}")
                print(f"\nFamily Members Found: {result['family_count']}\n")
                
                if result['family_members']:
                    print(f"{'Patent Number':<18} {'Jurisdiction':<15} {'Title':<40}")
                    print("-" * 73)
                    for member in result['family_members']:
                        title = member['title'][:37] + '...' if len(member['title']) > 40 else member['title']
                        print(f"{member['number']:<18} {member['jurisdiction']:<15} {title:<40}")
                else:
                    print("No family members found in other jurisdictions.")
                    print("\nTip: Try searching with the patent title keywords directly.")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == '__main__':
    main()
