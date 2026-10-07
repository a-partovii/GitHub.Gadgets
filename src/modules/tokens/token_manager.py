from modules.file_modules import read_file, write_file

def token_manager(tokens_dict):
    from modules.tokens import primary_token
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
    
    try: # Read current token index from file
        index = int(read_file(file_path="app_data/states/.token_manager_index_assist.ghg")[0])
        token = token_list[index]
    # If the current token index missing or out of range, fall back to 0.
    except (FileNotFoundError, IndexError, ValueError, TypeError):
        index = 0
        token = token_list[index]

    # If was equal "last_token" will be zero
    index = (index + 1) % length_token_list
    # Update and save index in the file
    write_file(file_path="app_data/states/.token_manager_index_assist.ghg", input_item=index, writing_mode="w")
    return token
