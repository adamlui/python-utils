import json, re, urllib.request as http
from pathlib import Path
from typing import Union, List, Optional

api = json.loads((Path(__file__).parent / 'data/package_data.json').read_text())

def get_min_py(pkg_names: Union[str, List[str]]) -> Union[Optional[str], List[Optional[str]]]:
    if isinstance(pkg_names, str) : pkg_names = [pkg_names]
    results: List[Optional[str]] = []

    for pkg_name in pkg_names: # get min py
        try:
            req = http.Request(f'https://pypi.org/pypi/{pkg_name}/json')
            req.add_header('User-Agent', f"{api['name']}/{api['version']}")
            resp = http.urlopen(req, timeout=5)
            pkg_info = json.loads(resp.read())['info']

            # Check `requires_python`
            requires_python = pkg_info.get('requires_python')
            if requires_python:
                ver_match = re.search(r'(>|>=|==|~=)\s*(\d+\.\d+(?:\.\d+)?)', requires_python)
                if ver_match:
                    op, version = ver_match.group(1), ver_match.group(2)
                    if op == '>': # return minor-bumped
                        major, minor = version.split('.')[:2]
                        results.append(f'{major}.{int(minor) + 1}')
                    else: # >=|==|~=
                        results.append(version) # as-is
                    continue # to next pkg

            # Check classifiers
            classifiers, versions = pkg_info.get('classifiers', []), []
            for classifier in classifiers:
                if classifier.startswith('Programming Language :: Python ::'):
                    ver_match = re.search(r'(\d+(?:\.\d+)?)', classifier)
                    if ver_match : versions.append(ver_match.group())
            if versions: # append lowest
                decimal_vers = [ver for ver in versions if '.' in ver]
                if decimal_vers:
                    decimal_vers.sort(key=lambda ver: [int(x) for x in ver.split('.')])
                    results.append(decimal_vers[0])
                else:
                    results.append(min(versions, key=int))
                continue # to next pkg
            else : results.append(None)

        except Exception : results.append(None)

    return results[0] if len(pkg_names) == 1 else results
