def read(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()

def write(file_path, data, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as file:
        file.write(data)
