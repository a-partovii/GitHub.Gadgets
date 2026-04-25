import os

def write_file(file_path:str, input_item, writing_mode:str = "a", separator:str = "\n"):
    """
    Write one or multiple items into a text file.

    Args:
        file_path (str): Path to the target text file, including its file extension
        input_item: A single item or an iterable list of items to write.
        writing_mode (str, optional): File opening mode, "a" to append new (default), "w" to overwrite the all.
        separator (str, optional): String added after each item, default is newline ("\n").
    """

    if writing_mode not in {"a", "w", "x"}:
        raise ValueError("writing_mode must be 'a', 'w', or 'x'")
    
    try:
        os.makedirs("outputs", exist_ok=True) # Create outputs folder if it doesn't exist
        with open(file_path, writing_mode, encoding="utf-8") as file:
            if isinstance(input_item, list):
                for item in input_item:
                    file.write(f"{item}{separator}")
            else:
                file.write(f"{input_item}{separator}")
           
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory does not exist for path: {file_path}")

    except PermissionError:
        raise PermissionError(f"No permission to write file: {file_path}")

    except OSError as error:
        raise OSError(f"File writing failed: {error}")
