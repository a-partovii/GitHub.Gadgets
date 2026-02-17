import os
from datetime import datetime

def unique_filename(filename:str) -> str:
    """
    Returns a unique filename. If the file exists, appends a counter (e.g., filename (1).txt).
    
    Args:
        filename (str): Base filename (with extension).
        
    Returns:
        str: Unique filename that doesn't exist in the directory.
    """
    name, ext = os.path.splitext(filename)
    count = 1
    while os.path.exists(filename):
        filename = f"{name} ({count}){ext}"
        count += 1
    return filename

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