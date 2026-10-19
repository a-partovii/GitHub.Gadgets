import os

def delete_file(file_path, show_message=True):
    """
    Takes a file path and deletes the file.
    If the file does not exist, it prints an error message.

    Args:
        file_path (str): The path to the file to be deleted, including extension.
    """
    try:
        os.remove(file_path)
        if show_message:
            print(f"[SUCCESS] File deleted: {file_path}")
        return True
    
    except FileNotFoundError:
        if show_message:
            print(f"The file doesn't exist: {file_path}")
        return False
    
    except Exception as error:
        print(f"[ERROR] Deleting File: {error}")
        return False