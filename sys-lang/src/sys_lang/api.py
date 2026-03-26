def get_sys_lang(region: bool = True) -> str: # e.g. 'en_US'
    import sys

    if sys.platform == 'win32':
        import subprocess
        lang_result = subprocess.run(
            ['powershell', '-Command', '(Get-Culture).Name'], capture_output=True, text=True, check=True).stdout.strip()
        if not lang_result : raise RuntimeError('Could not detect Windows system language')
        lang_code = lang_result.replace('-', '_')
        return lang_code if region or '_' not in lang_code else lang_code.split('_')[0]

    else: # *nix sys
        import os
        for lang_env_var in ('LC_ALL', 'LC_MESSAGES', 'LANG', 'LANGUAGE'):
            lang_val = os.environ.get(lang_env_var)
            if not lang_val : continue
            lang_val = lang_val.split(':')[0]
            lang_val = lang_val.split('.')[0]
            lang_val = lang_val.split('@')[0]
            if lang_val.upper() in ('C', 'POSIX') : return 'en'
            return lang_val if region or '_' not in lang_val else lang_val.split('_')[0]
        raise RuntimeError('Could not detect *nix system language')
