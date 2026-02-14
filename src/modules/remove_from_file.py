import os
from read_txt_file import read_txt_file
from write_in_file import write_in_file

def remove_items_from_file(file_path:str, items):
    """
    Remove given item or a list of items from a text file.

    Args:
        file_path: path to file, including its file extension
        items: a single item or a list of items to remove
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    if isinstance(items, list):
        remove_set = {str(i).strip() for i in items}
    else:
        remove_set = {str(items).strip()}

    # read file and make it a list
    raw_list = read_txt_file(file_path)

    # filter
    new_list = [i for i in raw_list if i not in remove_set]

    write_in_file(file_path, new_list, writing_mode="w")
