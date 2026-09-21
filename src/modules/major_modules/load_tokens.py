from modules.tui import get_primary_token, get_secondary_tokens
from modules.file_modules import write_json, read_json, check_file_exists
from config import primary_token, secondary_tokens
def load_tokens():
    """
    Load tokens from their JSON configuration files.
    If a configuration file does not exist, then calls the functions to set
    the tokens.
    """
    global primary_token, secondary_tokens

    if not check_file_exists("config/primary_token.json"):
        get_primary_token()

        if not check_file_exists("config/secondary_tokens.json") :
            get_secondary_tokens()
    """
    Mutate the existing dicts in place (clear + update) so modules that
    imported "primary_token"/"secondary_tokens" as references still
    observe the loaded data, instead of holding a stale empty dict.
    A legacy bug has died here.
    """
    try:
        primary_token.clear()
        primary_token.update(read_json("config/primary_token.json"))
    except:
        print("[ERROR] The primary token file is invalid. "
              "[ERROR] The secondary tokens file is invalid. "
              "Your secondary token configuration will be reset."
              "Your primary token configuration will be reset.")
        write_json("config/primary_token.json", {})

    try:
        secondary_tokens.clear()
        secondary_tokens.update(read_json("config/secondary_tokens.json"))
    except:
        # Reset the file if it is empty or invalid JSON (wrong file manipulating).
        print("[ERROR] The secondary tokens file is invalid. "
              "Your secondary tokens configuration will be reset.")
        write_json("config/secondary_tokens.json", {})
        
    if not primary_token:
        print("[WARN] No primary access token is configured.\n"
              "Primary token cannot be empty.\n"
              "Please set a valid token.")
        get_primary_token()
        if not secondary_tokens :
            get_secondary_tokens()
            
        load_tokens()