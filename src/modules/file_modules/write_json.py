import json
import os

def write_json(file_path:str, input_data, writing_mode:str = "w", indent: int = 4):
    """
    Write data to a JSON file.

    Args:
        file_path (str): Path to the target JSON file.
        data: Python object to serialize as JSON.
        writing_mode (str, optional): File opening mode. Defaults to "w".
        indent (int, optional): JSON indentation level. Defaults to 4.

    """

    if writing_mode not in {"w", "x"}:
        raise ValueError("writing_mode must be \'w\' or \'x\'")

    # Ensure parent directories exist before writing
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, writing_mode, encoding="utf-8") as file:
            json.dump(input_data, file, indent=indent)

    except TypeError as error:
        raise TypeError(f"[ERROR] Data is not JSON type: {error}")

    except FileNotFoundError:
        raise FileNotFoundError(
            f"[ERROR] Couldn\'t find: {file_path}"
        )

    except PermissionError:
        raise PermissionError(
            f"[ERROR] No permission to write file: {file_path}"
        )

    except OSError as error:
        raise OSError(f"[ERROR] Writing JSON failed: {error}")