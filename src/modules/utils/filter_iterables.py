import os
from modules.file_modules import read_file
from modules.file_modules import write_file

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
    raw_list = read_file(file_path)

    # filter
    result_list = [i for i in raw_list if i not in remove_set]

    write_file(file_path, result_list, writing_mode="w")

# -------------------------------------------------------------
def filter_list(raw_list:list, filter_items, output_mode:str = "list", file_name:str = "filtered_list.txt"):
    """
    Remove given item or a list of items from another list.

    Args:
        main_list (list): The main list that items will remove from.
        filter_items: a single item or a list of items to remove from the list.
        output_mode (str): "list" to return a list (default), "file" to save it as a text file too.
        file_name (str): the output file name (default = "filtered_list.txt")

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
    result_list = [i for i in raw_list if i not in remove_set]

    if output_mode not in ("list", "file"):
        raise ValueError('<output_mode> must be "list" or "file"')
    
    elif output_mode == "file":
        write_file(f"outputs/{file_name}", result_list, writing_mode="w")

    return result_list

# -------------------------------------------------------------
def deduplicate_file_content(file_path:str):
    """
    Remove duplicated items from a text file.

    Args:
        file_path: path to the file, including its file extension
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    raw_list = read_file(file_path)
    seen = set()
    result_list = []
    for i in raw_list:
        if i not in seen:
            seen.add(i)
            result_list.append(i)

    write_file(file_path, result_list, writing_mode="w")

# -------------------------------------------------------------
def deduplicate_list_content(raw_list:list, output_mode="list", file_name="deduplicate_list.txt"):
    """
    Remove duplicated items from a given list.

    Args:
        raw_list (list): The main list that will be filtered.
        output_mode (str): "list" to return a list (default), "file" to save it as a text file too.
        file_name (str): the output file name (default = "deduplicate_list.txt").
    
    returns: 
        The deduplicated list.
    """
    seen = set()
    result_list = []
    for i in raw_list:
        if i not in seen:
            seen.add(i)
            result_list.append(i)

    if output_mode not in ("list", "file"):
        raise ValueError('<output_mode> must be "list" or "file"')
    
    elif output_mode == "file":
        write_file(f"outputs/{file_name}", result_list, writing_mode="w")
    
    return result_list
