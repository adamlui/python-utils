from typing import List, Optional, Tuple
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen
import webbrowser

def get(url: str, timeout: int = 5, encoding: str = 'utf-8') -> str:
    url = validate(url)
    try:
        with urlopen(url, timeout=timeout) as resp:
            return resp.read().decode(encoding)
    except URLError as err:
        raise RuntimeError(f'Failed to fetch from {url}: {err}')

def open(url: str) -> None:
    url = validate(url)
    try : webbrowser.open(url)
    except Exception as err:
        raise RuntimeError(f'Failed to open {url} in browser: {err}')

def validate(url: str, allowed_schemes: Tuple[str, ...] = ('http', 'https'),
                       allowed_domains: Optional[List[str]] = None) -> str:
    parsed_url = urlparse(url)

    if parsed_url.scheme not in allowed_schemes:
        raise ValueError(f'URL scheme {parsed_url.scheme!r} not allowed. Allowed: {allowed_schemes}')

    if allowed_domains:
        input_domain = parsed_url.netloc.lower()
        if not any(input_domain.endswith(allowed_domain.lower()) for allowed_domain in allowed_domains):
            raise ValueError(f'URL domain {input_domain!r} not allowed. Allowed: {allowed_domains}')
    
    return url
