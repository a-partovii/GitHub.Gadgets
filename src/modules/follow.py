from config import primary_token, token_manager, make_headers
from modules.utils import delay_and_super_delay, filter_file
from modules.file_modules import write_file, delete_file
import requests as req

def follow(usernames: list[str], save_progress: bool = True) -> bool:
    """
    Follow a list of GitHub usernames using the provided token.

    Args:
        usernames (list[str]): A list of GitHub usernames to follow.
        save_progress (bool): Whether to save progress in a file for resuming later.
    """
    total = 0 # Total followed accounts

    # Save an initial list, so the process can be resumed if interrupted
    progress_file = "outputs/follow_in_progress"
    save_progress and write_file(progress_file, usernames, writing_mode="w")

    headers = make_headers(token_manager(primary_token))
    for username in usernames:
        url = f"https://api.github.com/user/following/{username}"
        try:
            response = req.put(url, headers=headers, timeout=10)

        # Network errors
        except req.RequestException as error:
            message = f"[ERROR] Network Error, {type(error).__name__} while following -> {error}"
            continue

        # Response handling
        status = response.status_code
        remaining = response.headers.get("X-RateLimit-Remaining", "?")

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

        # Rate limit reached
        elif status == 403 or remaining <= "5":
            message = f'[WARN] Token Rate Limit is Close to Being Reached, Remaining: "{remaining}"\n Take a break and continue later...'
            return False

        # Token error
        elif status == 401:
            print("[ERROR] Invalid or Expired Token.")
            return False

        # GitHub internal error
        elif status >= 500:
            message = f"[GITHUB] Server Error {status}"
            continue

        else:
            message = f"[ERROR] http={status} reason={response.reason}"

        delay_and_super_delay(message, min=7, max=15)

    print(f'[SUCCESS] Follow Process Finished Successfully, total followed Accounts: "{total}"')
    # Delete "progress_file" if the loop finished normally
    delete_file(progress_file)
    return True
