from pathlib import Path
import shutil

for target in ['dist', 'build', '*_cache', '__pycache__', '*.egg-info']:
    for path in Path('.').rglob(target):
        if path.is_dir() : shutil.rmtree(path) ; print(f'Removed {path}/')

print('Clean complete!')
