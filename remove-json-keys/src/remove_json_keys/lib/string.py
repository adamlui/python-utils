def removeprefix(str: str, prefix: str) -> str:
    return str[len(prefix):] if str.startswith(prefix) else str
