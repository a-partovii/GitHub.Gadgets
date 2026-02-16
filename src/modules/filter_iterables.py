import os
from read_txt_file import read_txt_file
from write_in_file import write_in_file

def filter_file(file_path:str, filter_items):
    """
    Remove given item or a list of items from a text file.

    Args:
        file_path: path to file, including its file extension
        filter_items: a single item or a list of items to remove from the file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    try:
        if isinstance(filter_items, list):
            remove_set = {str(i).strip() for i in filter_items}
        else:
            remove_set = {str(filter_items).strip()}
    except Exception as error:
        raise ValueError(f"Invalid <filter_items>: {error}")
    
    # read file and make it a list
    raw_list = read_txt_file(file_path)

    # filter
    new_list = [i for i in raw_list if i not in remove_set]

    write_in_file(file_path, new_list, writing_mode="w")

# -------------------------------------------------------------
def filter_list(raw_list, filter_items, output_mode="list", file_name="filtered_list.txt"):
    """
    Remove given item or a list of items from another list.

    Args:
        main_list: The main list that will remove items from.
        filter_items: a single item or a list of items to remove from the list.
        output_mode: "list" to return a list (default) "file" to save it as a text file too.

    returns:
        The filtered list.
    """
    try:
        if isinstance(filter_items, list):
            remove_set = {str(i).strip() for i in filter_items}
        else:
            remove_set = {str(filter_items).strip()}
    except Exception as error:
        raise ValueError(f"Invalid <filter_items>: {error}")
    
    # filter
    new_list = [i for i in raw_list if i not in remove_set]
    if output_mode not in ("list", "file"):
        raise ValueError('<output_mode> must be "list" or "file"')
    
    elif output_mode == "file":
        write_in_file(f"outputs/{file_name}", new_list, writing_mode="w")

    return new_list

# -------------------------------------------------------------
def deduplicate_file_content(file_path:str):
    """
    Remove duplicated items from a text file.

    Args:
        file_path: path to the file, including its file extension
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    raw_list = read_txt_file(file_path)
    seen = set()
    new_list = []
    for i in raw_list:
        if i not in seen:
            seen.add(i)
            new_list.append(i)

    write_in_file(file_path, new_list, writing_mode="w")
