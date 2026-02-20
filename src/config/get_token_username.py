import requests
from config.tokens import make_headers

def get_github_username(token: str) -> str:
    """
    Returns the GitHub username of a given GitHub access token.

    Args:
        token (str): A GitHub Personal Access Token (PAT) or OAuth token.

    Returns:
        str: The login (username) of the token owner.
    """
    url = "https://api.github.com/user"
    headers = make_headers(token)
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        user_data = response.json()
        return user_data["login"]

    except requests.HTTPError as error:
        raise Exception(f"[ERROR] GitHub API Error: {response.status_code}")

    except requests.RequestException as error:
        raise Exception(f"[ERROR]Request Failed: {error}")