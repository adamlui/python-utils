import urllib.request, urllib.error

def get(url, timeout=5, encoding='utf-8'):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.read().decode(encoding)
    except (urllib.error.URLError, urllib.error.HTTPError) as err:
        raise RuntimeError(f'Failed to fetch from {url}: {err}')
