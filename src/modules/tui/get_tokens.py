from modules.file_modules import write_json, read_json
from config.tokens import get_token_username
from pprint import pprint

def get_primary_token():
    """
    Get, validate, and save the primary GitHub token.
    """
    while True:
        token = input("Enter GitHub token: ").strip()

        if not token:
            print("[ERROR] Primary token cannot be empty.")
            continue

        username = get_token_username(token)

        if username is None:
            print("[ERROR] Invalid GitHub token.")
            print("[HINT] Please check the token and try again.\n")
            continue

        primary_token = {username: token}

        save_tokens_json("config/primary_token.json", primary_token)

        print(f"[SUCCESS] Primary token added for '{username}'.")
        return
    
from pprint import pprint
from modules.file_modules import write_json, read_json
from config.tokens import get_token_username


def get_secondary_tokens():
    """
    Get and validate multiple secondary GitHub tokens.

    Press Enter without entering a token to finish.
    Secondary tokens are optional.
    """
    file_path = "config/secondary_tokens.json"

    try: # Load existing tokens if file exists
        secondary_tokens = read_json(file_path)
        if not isinstance(secondary_tokens, dict):
            secondary_tokens = {}
    except FileNotFoundError:
        secondary_tokens = {}

    print("\nEnter secondary GitHub tokens.")
    print("[INFO] Using secondary tokens is recommended, but not necessary.\n"
          "[HINT] Press Enter without entering a token to finish.\n")

    if secondary_tokens:
        print("Existing secondary tokens:")
        pprint(secondary_tokens)
        print()

    while True:
        token = input("Enter secondary GitHub token: ").strip()

        if not token:
            break
        # Skip duplicate token
        if token in secondary_tokens.values():
            print("[WARNING] This token has already been added.")
            continue

        username = get_token_username(token)

        if username is None:
            print("[ERROR] Invalid GitHub token.")
            print("[HINT] Please check the token and try again.\n")
            continue
        # Skip duplicate username
        if username in secondary_tokens:
            print(f"[WARNING] A token for '{username}' has already been added.")
            continue

        secondary_tokens[username] = token
        print(f"[SUCCESS] Token for '{username}' added successfully.\n")

    if not secondary_tokens:
        print("[INFO] No secondary tokens were added.")
        return {}

    if not save_tokens_json(file_path, secondary_tokens):
        print("[ERROR] Secondary tokens could not be saved.")
        return {}

    return secondary_tokens


def save_tokens_json(file_path: str, data: dict) -> bool:
    """
    Save token data to a JSON file.
    """
    try:
        write_json(file_path, data)
        return True
    except Exception as error:
        print(f"[ERROR] Failed to save tokens: {error}")
