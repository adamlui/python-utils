def read(file_path):
    with open(file_path, 'r', encoding='utf-8') as file : file_content = file.read()
    return file_content

def write(file_path, file_content):
    with open(file_path, 'w', encoding='utf-8') as file : file.write(file_content)
