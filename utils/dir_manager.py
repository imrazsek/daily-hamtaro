import os

def create_directory(dir_name):
    dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/", dir_name)

    EXIST_FOLDER = os.path.isdir(dir_path)
    if not EXIST_FOLDER:
        os.makedirs(dir_path)
    return dir_path
