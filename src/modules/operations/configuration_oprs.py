from modules.file_modules import read_file, write_file
from modules.tui import print_in_columns, show_menu
from modules.utils import filter_list, filter_file

def adjust_files_menu(list_name:str, file_path:str):
    _ = {
    "1": {"label": f"Show {list_name}", "action": lambda: print_in_columns(read_file(file_path))},
    "2": {"label": f"Add new usernames to {list_name}", "action": lambda: add_usernames_to_file(list_name, file_path)},
    "3": {"label": f"Remove usernames from {list_name}", "action": lambda:remove_usernames_from_file(list_name, file_path)},
    "4": {"label": f"Reset {list_name}", "action": lambda: reset_file_list(list_name, file_path)},
    # "0": {"label": "Exit menu", "action": ""}
    }
    show_menu(_)

# -----------------------------------------------------------------------------------------
def add_usernames_to_file(list_name:str, file_path:str):
    """
    Recives usernames from user input and append them to a given file.

    Args:
        list_name (str): Name of the file-list (used in user messages).
        file_path (str): Path to the target file.
    """
    usernames = []
    print("Type a new username to add and then press <Enter>\n" + 
          "When you're done, press <Enter> to enter a empty input to submit them all.")

    while True:
        user_input = input("Type and enter a username: ").strip()            
        if user_input == "" : 
            break
        usernames.append(user_input)
        print(f"[OK] {len(usernames)} username recived to add to {list_name}")

    if not usernames:
        print("No usernames entered. Operation cancelled.")
        return
    filter_list(usernames, read_file(file_path))
    write_file(file_path, input_item=usernames)
    print(f"[SUCCESS] {len(usernames)} usernames adder to {list_name}")

# -----------------------------------------------------------------------------------------
def remove_usernames_from_file(list_name:str, file_path:str):
    """
    Recives usernames from user input and remove them from a given file.

    Args:
        list_name (str): Name of the file-list (used in user messages).
        file_path (str): Path to the target file.
    """
    usernames = []
    print("Type a username to remove, then press <Enter>\n" + 
          "When you're done, press <Enter> to enter a empty input to submit them all.")

    while True:
        user_input = input("Type and enter a username: ").strip()            
        if user_input == "" : 
            break
        usernames.append(user_input)
        print(f"[OK] {len(usernames)} usernames recived to remove from {list_name}")

    if not usernames:
        print("No usernames entered. Operation cancelled.")
        return
    
    filter_file(file_path=file_path, filter_items=usernames),
    print(f"[SUCCESS] {len(usernames)} usernames removed from {list_name}")

# -----------------------------------------------------------------------------------------
def reset_file_list(list_name:str, file_path:str):
    user_input = input( f"You are about to reset the entire {list_name}.\n"
                       f"This action cannot be undone. Are you sure you want to continue? [y/N]: ")
    if user_input.strip().lower() != 'y':
        print("Operation cancelled.")
        return
    try:
        write_file(file_path, input_item="", writing_mode="w")
        print(f"[SUCCESS] {list_name} has been reset.")
    except Exception as error:
        print(f"[ERROR] Failed to reset {list_name}: {error}")
# -----------------------------------------------------------------------------------------
config_submenu = {
    "1": {"label": "Adjust Blacklist", "action": lambda: adjust_files_menu("Blacklist", "app_data/blacklist.txt")},
    "2": {"label": "Adjust Whitelist", "action": lambda: adjust_files_menu("Whitelist", "app_data/whitelist.txt")},
    "3": {"label": "Adjust Greylist", "action": lambda: adjust_files_menu("Greylist", "app_data/greylist.txt")},
    "4": {"label": "Manage GitHub tokens", "action": ""}
    # "0": {"label": "Back to main menu", "action": return_to_main},
}
