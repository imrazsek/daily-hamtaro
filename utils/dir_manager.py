import os


def create_directory(dir_name):
    """Create a directory if not exists in the relative path"""
    # Get relative path and concat the directory name (images)
    dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/", dir_name)

    # Checks if the directory exists
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    return dir_path


def delete_directory(dir_path, image_files):
    """Delete a directory if exists in the relative path"""
    if os.path.isdir(dir_path):
        # First remove all files from the directory
        for file in image_files:
            os.remove(file)
        os.rmdir(dir_path)
