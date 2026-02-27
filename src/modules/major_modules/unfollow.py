from config import primary_token, make_headers, token_manager
from modules.utils import delay_and_super_delay, filter_file, filter_list, response_error_handler
from modules.file_modules import write_file, read_file, delete_file, check_file_exists
from .send_request import send_request
from .extract_usernames import extract_usernames

def unfollow(
        usernames:list[str],
        save_progress:bool =True,
        skip_non_followed:bool =True,
        skip_whitelist:bool =True) -> bool:
    """
    Unfollow a list of GitHub usernames using the provided token.

    Args:
        usernames (list[str]): List of GitHub usernames to unfollow.
        save_progress (bool): Whether to save progress for resuming later.
        skip_unfollowed (bool): Skip accounts not currently followed.
        skip_blacklist (bool): Skip usernames in the blacklist.

    Returns:
        bool: True if process completed, False on failure.
    """
    # Filter usernames based on the "whitelist.txt" file
    if skip_whitelist:
        usernames = filter_list(usernames, read_file("config/whitelist.txt"))

    if skip_non_followed: # Skip accounts not currently followed
        my_username = next(iter(primary_token))
        usernames = filter_list(usernames, extract_usernames(my_username, "followers", show_message=False)) 

    if save_progress: # Save an initial file, so the process can be resumed if interrupted
        progress_file = "outputs/.unfollow_in_progress"
        write_file(progress_file, usernames, writing_mode="w")

    headers = make_headers(token_manager(primary_token))
    total = 0 # Total unfollowed accounts
    for username in usernames:
        url = f"https://api.github.com/user/following/{username}"
        response = send_request("delete", url, headers)

        # Response handling
        if response is False:
            print(f"[ERROR] Network or request error while unfollowing '{username}'")
            return False

        status = response.status_code
        rl_remaining = response.headers.get("X-RateLimit-Remaining", "unknown")

        if status == 204: # Success
            total += 1
            message = f'[OK] "{username}" Unfollowed | Total Unfollowed: "{total}" | Token RateLimit Remaining: "{rl_remaining}"'
            save_progress and filter_file(progress_file, username)

        elif status == 404:  # Not following / user does not exist
            message = f'[WARN] User Not Found: "{username}"'
            save_progress and filter_file(progress_file, username)

        else:
            action, message = response_error_handler(response)
            if action == "break":
                print(message)
                return False

        delay_and_super_delay(message, min=10, max=30)

    print(f'[SUCCESS] Unfollow Process Finished, total unfollowed accounts : "{total}"')
    delete_file(progress_file)
    return True

# -----------------------------------------------------------------------------------------------------
def continue_unfollow_progress() -> bool:
    """
    Checks if a [.unfollow_in_progress] file exists, asks the user
    to continue the previous unfollow process.

    Returns:
        bool: True if the unfollow process was resumed, False otherwise.
    """
    try:
        if not check_file_exists("outputs/.unfollow_in_progress"):
            return False

        user_input = input("A unfollow progress file was found from your last action.\n"
                           "Do you want to continue the last process? [Y/n]: ").strip().lower()

        if user_input in {"y", "yes"}:
            unfollow(
                usernames=read_file("outputs/.unfollow_in_progress"),
                save_progress=True,
                skip_whitelist=False,
                skip_non_followed=False)
            return True
        return False

    except Exception as error:
        print(f"An error occurred while trying to continue the unfollow process.\n{error}")
        return False
