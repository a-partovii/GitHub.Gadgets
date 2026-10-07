from modules.major_modules import send_request

def fetch_token_username(token:str) -> str:
    """
    Returns the GitHub username of a given GitHub access token.

    Args:
        token (str): A GitHub Personal Access Token (PAT) or OAuth token.

    Returns:
        str: The login (username) of the token owner.
    """
    url = "https://api.github.com/user"
    try:
        response = send_request("get", url, token)
        response.raise_for_status()

        user_data = response.json()
        return user_data["login"]

    except Exception as error:
        print(f"[ERROR] Failed to fetch the token username: {error}")
