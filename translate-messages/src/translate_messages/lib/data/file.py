def atomic_write(file_path, data, encoding='utf-8'): # to prevent TOCTOU
    import os
    from pathlib import Path

    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = file_path.parent / f'.{file_path.name}.tmp'

    try:
        with open(tmp_path, 'w', encoding=encoding) as file:
            file.write(data) ; file.flush() ; os.fsync(file.fileno())
        os.replace(tmp_path, file_path) # atomic rename
    except Exception:
        if tmp_path.exists() : tmp_path.unlink()
        raise

def read(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()

def write(file_path, data, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as file:
        file.write(data)
