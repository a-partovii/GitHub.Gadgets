import os
from config import secondary_tokens, token_manager, make_headers
from modules.utils import delay, response_error_handler
from modules.file_modules import write_file, filename_datetime
from .send_request import send_request

def extract_usernames(
        target_username:str,
        source:str,
        output_type:str ="list",
        limit_count:int|None =None,
        show_message:bool =True,
        show_logs:bool =True) -> list[str] | bool :
    """
    Extract GitHub usernames from followers or following of a target user.

    Args:
        target_username (str): GitHub username to extract data from.
        source (str): "followers" or "following".
        output_type (str, optional): "list" to return list (defaults="list"), "file" to save output file.
        show_message (bool, optional): Show final message (defalt=True).
        show_logs (bool, optional): Show per-request logs (defalt=True).

    Returns:
        list[str] | bool: List of usernames or False on error.
    """
    if output_type == "file":
        file_path = f"outputs/({target_username}){source} {filename_datetime()}"

    if source not in {"followers", "following"}:
        raise ValueError('Invalid argument for {extract_usernames}, `source` must be "followers" or "following"')
    
    page = 1
    usernames_list = []
    total = 0 # total extracred usernames
    while True:
        # per_page = 100, max items per request
        url = f"https://api.github.com/users/{target_username}/{source}?per_page=100&page={page}"
        headers = make_headers(token_manager(secondary_tokens))

        response = send_request("get", url, headers)

        # Response handling
        if response is False:
            return False
    
        status = response.status_code
        remaining = response.headers.get("X-RateLimit-Remaining", "unknown")
        
        if status == 200:
            data_json = response.json()
            if not data_json:
                break

            for user in data_json:
                usernames_list.append(user.get("login"))
            total = len(usernames_list)
            message = f'[OK] "{total}" Usernames Saved '

            if output_type == "file": # "file" or "list" (default=List)
                try:
                    os.makedirs("outputs", exist_ok=True) # Create outputs folder if it doesn't exist
                    write_file(file_path=file_path, input_item=usernames_list, writing_mode="w")
                    message += f'to "{file_path}" '

                except Exception as error:
                    message = (f"[ERROR] Writing in the File Failed, " +
                              f"check this error and try again: \n{error}\n" + message)

            message += f'| Token RateLimit Remaining: "{remaining}"'
            page += 1

        elif status == 404:
            print(f'[WARN] User "{target_username}" Not Found, check the username and try again.')
            return False

        else:
            action, message = response_error_handler(response)
            if action == "break":
                print(message)
                return False
            
        if show_logs is not True:
            message = ""
        delay(message ) # Random delay per request (2–6 seconds)

        if limit_count is not None and total >= limit_count: 
            break

    if show_message:          
        if output_type == "file":
            print(f'[SUCCESS] Extracting Usernames is Done, "{len(usernames_list)}" usernames saved to "{file_path}"')
        else:
            print(f'[SUCCESS] Extracting Usernames is Done, "{len(usernames_list)}" usernames saved.')

    if limit_count is not None:
        return usernames_list[:limit_count]
    return usernames_list
