import os

def create(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def delete(path):
    try:
        os.rmdir(path)
    except FileNotFoundError:
        pass
    
def clear(path):
    if not os.path.exists(path):
        return

    if not os.path.isdir(path):
        return

    files = os.listdir(path)

    for file in files:
        filepath = os.path.join(path, file)
        if os.path.isfile(filepath):
            os.remove(filepath)