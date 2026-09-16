from modules.file_modules import write_json
from config.tokens import get_token_username

def get_primary_token():
    """Get, validate, and save the primary GitHub token."""

    while True:
        token = input("Enter GitHub token: ").strip()

        if not token:
            print("[ERROR] Primary token cannot be empty.")
            continue

        username = get_token_username(token)

        if username is None:
            print("[ERROR] Invalid GitHub token.")
            print("[INFO] Please check the token and try again.\n")
            continue

        primary_token = {
            username: token
        }

        save_tokens_json(
            "config/primary_token.json",
            primary_token
        )

        print(f"[SUCCESS] Primary token added for '{username}'.")
        return primary_token

def get_secondary_tokens():
    """
    Get and validate multiple secondary GitHub tokens.

    Press Enter without entering a token to finish.
    Secondary tokens are optional.
    """
    secondary_tokens = {}

    print("\nEnter secondary GitHub tokens.")
    print("Press Enter without entering a token to finish.\n")

    while True:
        token = input("Enter secondary GitHub token: ").strip()

        if not token:
            break

        if token in secondary_tokens.values():
            print("[WARNING] This token has already been added.")
            continue

        username = get_token_username(token)

        if username is None:
            print("[ERROR] Invalid GitHub token.")
            print("[INFO] Please check the token and try again.\n")
            continue

        if username in secondary_tokens:
            print(
                f"[WARNING] A token for '{username}' "
                "has already been added."
            )
            continue

        secondary_tokens[username] = token

        print(
            f"[SUCCESS] Token for '{username}' added successfully.\n"
        )

    if not secondary_tokens:
        print("[INFO] No secondary tokens were added.")
        return

    save_tokens_json(
        "config/secondary_tokens.json",
        secondary_tokens
    )

def save_tokens_json(file_path:str, data:dict):
    """Save token data to a JSON file."""

    try:
        write_json(file_path, data)
        print(f"[SUCCESS] Tokens saved successfully to '{file_path}'.")

    except Exception as error:
        print(f"[ERROR] Failed to save tokens: {error}")

