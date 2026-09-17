from modules.file_modules import write_json
from config.tokens import get_token_username

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
    
def get_secondary_tokens():
    """
    Get and validate multiple secondary GitHub tokens.

    Press Enter without entering a token to finish.
    Secondary tokens are optional.
    """
    secondary_tokens = {}

    print("\nEnter secondary GitHub tokens.")
    print("[INFO] Using secondary tokens is recommended, but not necessary.\n"
          "[HINT] Press Enter without entering a token to finish.\n")

    while True:
        token = input("Enter secondary GitHub token: ").strip()

        if not token:
            break

        if token in secondary_tokens.values():
            print("[WARN] This token has already been added.")
            continue

        username = get_token_username(token)

        if username is None:
            print("[ERROR] Invalid GitHub token.")
            print("[HINT] Please check the token and try again.\n")
            continue

        if username in secondary_tokens:
            print(f"[WARN] A token for '{username}' has already been added.")
            continue

        secondary_tokens[username] = token
        print(f"[SUCCESS] Token for '{username}' received successfully.\n")

    if not secondary_tokens:
        print("[INFO] No secondary tokens were added.")
        return

    save_tokens_json("config/secondary_tokens.json", secondary_tokens)
    return

def save_tokens_json(file_path:str, data:dict):
    """
    Save token data to a JSON file.
    """

    try:
        write_json(file_path, data)
        return True

    except Exception as error:
        print(f"[ERROR] Failed to save tokens: {error}")
