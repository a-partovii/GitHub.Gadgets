"""
Put your GitHub Personal Access Tokens in the dictionaries below.
The key is just a name to identify each token, and the value is the token itself.

You can add multiple secondary tokens to spread API requests between them.
This helps reduce rate limiting and lowers the risk of getting blocked.

The primary token is used for modifying actions (such as starring or following).
The secondary tokens are only used for doing background tasks.

Using secondary tokens is optional, but recommended.
"""

from modules.read_txt_file import read_txt_file
from modules.write_in_file import write_in_file

# The main GitHub personal access token for modifying tasks
primary_token = {
    "name": "ghp_####################################" 
}
# The secondary GitHub personal access tokens to help proccess
secondary_tokens = {
    "name1": "ghp_####################################",
    "name2": "token2",
    "name3": "token3"
}

def headeres(token):
    """
    Generate GitHub API headers using the provided token."""
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

def token_manager(tokens_dict):
    """
    Manages round-robin rotation of non-duplicate tokens from a dictionary (secondary_tokens).

    Reads token index from the file, returns the token,
    and updates the index file for next calls.
    
    Args:
        tokens_dict (dict): Dictionary containing tokens as values
        
    Returns:
        str or None: Next token in sequence, None if dict is empty
    """
    token_list = list(tokens_dict.values())
    length_token_list = len(token_list)
    if not token_list:
        # If "token_list" was empty try primary token, works for "secondary_tokens"
        if primary_token:
            token_list = list(primary_token.values())
            length_token_list = len(token_list)
            
        else:
            print("Error: both primary and secondary tokens are empty!")
            return None
        
    # If there is only one token, just return it
    elif length_token_list == 1:
        return token_list[0]
    
    # Read current token index from file
    index = int(read_txt_file(filename="inputs/token_manager_index_assist")[0])
    token = token_list[index]
    # If was equal "last_token" will be zero
    index = (index + 1) % length_token_list
    # Update and save index in the file
    write_in_file(file_path="inputs/token_manager_index_assist", input_item=index, writing_mode="w")
    return token
