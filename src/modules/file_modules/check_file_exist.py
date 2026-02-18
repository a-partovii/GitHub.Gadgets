import os

def check_file_exists(file_path:str) -> bool:
    """
    Check if a file exists at the specified path.

    Args:
        file_path (str): The path to the file to check.
    """         
    return os.path.exists(file_path)