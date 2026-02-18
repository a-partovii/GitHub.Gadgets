import os
from datetime import datetime

def unique_filename(file_path:str) -> str:
    """
    Returns a unique file path. If the file exists, appends a counter (e.g., outputs/filename(1).txt).
    
    Args:
        file_path (str): Base file path (with slash and extension).
        
    Returns:
        str: A unique file path that doesn't exist in the directory.
    """
    try:
        name, ext = os.path.splitext(file_path)
        count = 1
        while os.path.exists(file_path):
            file_path = f"{name}({count}){ext}"
            count += 1
    except:
        pass
    return file_path

# ----------------------------------------------------------
def filename_date(ext:str =".txt") -> str:
    """
    Returns filename with current date (e.g., [date 2026-02-17].txt).
    
    Args:
        ext (str, optional): File extension. Defaults to ".txt".
        
    Returns:
        str: Filename with date prefix.
    """
    return datetime.now().strftime("[date %Y-%m-%d]") + ext

# ----------------------------------------------------------
def filename_datetime(ext:str =".txt") -> str:
    """
    Returns filename with current date and time (e.g., [date 2026-02-17, time 12-09].txt).
    
    Args:
        ext (str, optional): File extension. Defaults to ".txt".
        
    Returns:
        str: Filename with date and time prefix.
    """
    return datetime.now().strftime("[date %Y-%m-%d, time %H-%M]") + ext
