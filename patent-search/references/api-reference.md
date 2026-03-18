# Patent API Reference

## Google Patents

### Web Interface
```
https://patents.google.com/?q={query}
```

### Patent Detail Page
```
https://patents.google.com/patent/{PATENT_NUMBER}/en
```

### Patent Number Formats
- US patents: `US6304886B1`, `US20200123456A1`
- EP patents: `EP1234567A1`
- WO patents: `WO2020123456A1`
- JP patents: `JP2020123456A`
- CN patents: `CN123456789A`

## Patent Number Normalization

Input formats that are accepted:
- `6,304,886` → `US6304886`
- `US 6,304,886 B1` → `US6304886B1`
- `6304886` → `US6304886`

## EPO Open Patent Services (OPS)

### Base URL
```
https://ops.epo.org/3.2/rest-services/
```

### Authentication
EPO OPS requires OAuth 2.0 authentication:
1. Register at https://developers.epo.org/
2. Obtain consumer key and secret
3. Request access token

### Search Endpoint
```
GET /published-data/search/{consistency}/{range}
```

### Example with Authentication
```python
import requests

# Get access token
token_url = "https://ops.epo.org/3.2/auth/accesstoken"
response = requests.post(token_url, auth=(consumer_key, consumer_secret))
access_token = response.json()['access_token']

# Make authenticated request
headers = {'Authorization': f'Bearer {access_token}'}
search_url = "https://ops.epo.org/3.2/rest-services/published-data/search"
params = {'q': 'search engine', 'Range': '1-10'}
response = requests.get(search_url, headers=headers, params=params)
```

## Caching Strategy

The skill implements file-based caching:
- Location: `~/.cache/patent-search/`
- TTL: 24 hours
- Cache key: MD5 hash of query parameters
- Format: JSON with timestamp

## Rate Limits

### Google Patents
- No official API (web scraping)
- Be respectful: add delays between requests
- Use cache to avoid repeated requests
- Recommended: 1 request per second maximum

### EPO OPS
- 4 requests per second for registered users
- 10 requests per minute for anonymous users

## Data Fields

### Patent Metadata
- `patent_number` - Publication number
- `title` - Patent title
- `date` - Publication date (YYYY-MM-DD)
- `kind` - Kind code (B1, B2, A1, etc.)
- `inventors` - List of inventor names
- `assignees` - List of assignee/company names
- `abstract` - Patent abstract text
- `claims` - List of patent claims

### Similarity Scores
- `title` - SequenceMatcher ratio for titles
- `abstract` - SequenceMatcher ratio for abstracts
- `claims` - SequenceMatcher ratio for claims text
- `overall` - Weighted average of all scores
