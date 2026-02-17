import os

def unique_filename(filename):
    name, ext = os.path.splitext(filename)
    count = 1
    while os.path.exists(filename):
        filename = f"{name} ({count}){ext}"
        count += 1
    return filename