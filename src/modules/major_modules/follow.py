from config import primary_token, make_headers, token_manager, get_token_username
from modules.utils import delay_and_super_delay, filter_file, filter_list, response_error_handler, network_error_handler
from modules.file_modules import write_file, read_file, delete_file
from .extract_usernames import extract_usernames
import requests as req

def follow(usernames:list[str], save_progress:bool =True, skip_blacklist:bool =True, skip_followed:bool =True) -> bool:
    """
    Follow a list of GitHub usernames using the provided token.

    Args:
        usernames (list[str]): A list of GitHub usernames to follow.
        save_progress (bool): Whether to save progress in a file for resuming later.
        skip_blacklist (bool): Whether to skip usernames that are in the blacklist.
    
    Returns:
        bool: True if the process completed successfully, False otherwise.
    """
    if skip_blacklist: # Filter usernames based on the "blacklist.txt" file
        blacklist = read_file("config/blacklist.txt")
        usernames = filter_list(usernames, blacklist)
                        
    if skip_followed: # Filter accounts already followed 
        my_username = get_token_username(token_manager(primary_token))
        usernames = filter_list(usernames, extract_usernames(my_username, "following")) 

    # Save an initial list, so the process can be resumed if interrupted
    progress_file = "outputs/.follow_in_progress"
    save_progress and write_file(progress_file, usernames, writing_mode="w")

    headers = make_headers(token_manager(primary_token))
    total = 0 # Total followed accounts
    for username in usernames:
        url = f"https://api.github.com/user/following/{username}"
        connection = "?"
        retries = 1
        while connection != True: # Retry loop for network failures
            try:
                response = req.put(url, headers=headers, timeout=10)
                connection = True
                
            # Network errors
            except req.RequestException as error:
                connection, message = network_error_handler(error)
                if retries >= 10: # Retries 10 times, then break
                    print(message)
                    return False
                
                retries += 1
                delay_and_super_delay(message, min=7, max=15)

        # Response handling
        status = response.status_code
        remaining = response.headers.get("X-RateLimit-Remaining", "unknown")

        if status == 204: # Success
            total += 1
            message = f'[OK] "{username}" Followed | Total Follow: "{total}" | Token RateLimit Remaining: "{remaining}"'
            # Remove the followed username from the "progress_file"
            save_progress and filter_file(progress_file, username)

        # Already followed (GitHub returns 422)
        elif status == 422:
            message = f'[SKIP] Already Followed:"{username}"'
            save_progress and filter_file(progress_file, username)

        elif status == 404: # Username does not exist
            message = f'[WARN] User Not Found: "{username}"'
            save_progress and filter_file(progress_file, username)

        else:
            action, message = response_error_handler(response)
            if action == "break":
                print(message)
                return False
            
        delay_and_super_delay(message, min=7, max=15)

    print(f'[SUCCESS] Follow Process Finished Successfully, total followed accounts: "{total}"')
    # Delete "progress_file" if the loop finished normally
    delete_file(progress_file)
    return True