import sys, webbrowser
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

def get(url, timeout=5, encoding='utf-8'):
    url = validate_url(url)
    try:
        with urlopen(url, timeout=timeout) as resp:
            return resp.read().decode(encoding)
    except URLError as err:
        raise RuntimeError(f'Failed to fetch from {url}: {err}')

def open(url):
    url = validate_url(url)
    try:
        webbrowser.open(url)
    except Exception as err:
        print(f'Failed to open browser: {err}', file=sys.stderr)
        sys.exit(1)

def validate_url(url, allowed_schemes=('http', 'https'), allowed_domains=[]):
    parsed_url = urlparse(url)

    if parsed_url.scheme not in allowed_schemes:
        raise ValueError(f"URL scheme '{parsed_url.scheme}' not allowed. Allowed: {allowed_schemes}")

    if allowed_domains:
        input_domain = parsed_url.netloc.lower()
        if not any(input_domain.endswith(allowed_domain.lower()) for allowed_domain in allowed_domains):
            raise ValueError(f"URL domain '{input_domain}' not allowed. Allowed: {allowed_domains}")
    
    return url
