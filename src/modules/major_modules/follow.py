from config import primary_token, make_headers, token_manager, get_token_username
from modules.utils import delay_and_super_delay, filter_file, filter_list, response_error_handler
from modules.file_modules import write_file, read_file, delete_file, check_file_exists
from .send_request import send_request
from .extract_usernames import extract_usernames

def follow(
        usernames:list[str],
        save_progress:bool =True,
        skip_followed:bool =True,
        skip_blacklist:bool =True) -> bool :
    """
    Follow a list of GitHub usernames using the provided token.

    Args:
        usernames (list[str]): A list of GitHub usernames to follow.
        save_progress (bool): Whether to save progress in a file for resuming later.
        skip_blacklist (bool): Whether to skip usernames that are in the blacklist.
    
    Returns:
        bool: True if the process completed successfully, False otherwise.
    """

    # Filter usernames based on the "blacklist.txt" file
    if skip_blacklist:
        usernames = filter_list(usernames, read_file("config/blacklist.txt"))
                        
    if skip_followed: # Filter accounts already followed 
        my_username = get_token_username(token_manager(primary_token))
        usernames = filter_list(usernames, extract_usernames(my_username, "following", show_message=False)) 

    if save_progress: # Save an initial file, so the process can be resumed if interrupted
        progress_file = "outputs/.follow_in_progress"
        write_file(progress_file, usernames, writing_mode="w")

    headers = make_headers(token_manager(primary_token))
    total = 0 # Total followed accounts
    for username in usernames:
        url = f"https://api.github.com/user/following/{username}"
        response = send_request("put", url, headers)

        # Response handling
        if response is False:
            return False
        
        status = response.status_code
        rl_remaining = response.headers.get("X-RateLimit-Remaining", "unknown")

        if status == 204: # Success
            total += 1
            message = f'[OK] "{username}" Followed | Total Follow: "{total}" | Token RateLimit Remaining: "{rl_remaining}"'
            # Remove the followed username from the "progress_file"
            save_progress and filter_file(progress_file, username)

        elif status == 422: # Already followed (GitHub returns 422)
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

def continue_follow_progress() -> bool:
    """
    Checks if a [.follow_in_progress] file exists, asks the user
    to continue the previous follow process.

    Returns:
        bool: True if the follow process was resumed, False otherwise.
    """
    try:
        if not check_file_exists("outputs/.follow_in_progress"):
            return False

        user_input = input("A follow progress file was found from your last action.\n"
                           "Do you want to continue the last process? [Y/n]: ").strip().lower()

        if user_input in {"y", "yes"}:
            follow(
                usernames=read_file("outputs/.follow_in_progress"),
                save_progress=True,
                skip_blacklist=False,
                skip_followed=False)
            return True
        return False

    except Exception as error:
        print(f"An error occurred while trying to continue the follow process.\n{error}")
        return False
