import tomli, tomli_w

def read(file_path):
    with open(file_path, 'rb') as file:
        return tomli.load(file)

def write(file_path, data):
    with open(file_path, 'wb') as file:
        tomli_w.dump(data, file)
