import os
import requests as req
from modules.utils import delay
from modules.file_modules import write_file
from config.tokens import secondary_tokens, token_manager, make_headers
from modules.file_modules import filename_datetime
from modules.utils import network_error_handler, response_error_handler

def extract_usernames(target_username:str, source:str, output_type:str ="list"):
    """
    Fetch usernames of a specified GitHub user's followers or followed accounts.

    Args:
        target_username (str): Username of the account whose data will be extracted.
        source (str): "followers" to extract followers, "following" to extract followings of the given username.
        output_type (str): "list" to return as a list (default = list), "file" to save output file too.

    Returns:
        list[str] | False: List of usernames, unless there was an critical error
    """
    if output_type == "file":
        file_path = f"outputs/({target_username}){source} {filename_datetime()}"

    if source not in {"followers", "following"}:
        raise ValueError('Invalid argument for {extract_usernames}, `source` must be "followers" or "following"')
    
    page = 1
    usernames_list = []
    while True:
        # per_page = 100, max items per request
        url = f"https://api.github.com/users/{target_username}/{source}?per_page=100&page={page}"
        headers = make_headers(token_manager(secondary_tokens))
        connection = "?"
        retries = 1
        while connection != True:
            try:
                response = req.get(url, headers=headers)
                connection = True

            # Network errors
            except req.RequestException as error:
                connection, message = network_error_handler(error)
                if retries >= 10: # Retries 10 times, then break
                    print(message)
                    return False
                
                retries += 1
                delay(message)

        status = response.status_code
        remaining = response.headers.get("X-RateLimit-Remaining", "unknown")

        if status == 200:
            data_json = response.json()
            if not data_json:
                break

            for user in data_json:
                usernames_list.append(user.get("login"))
            message = f'[OK] "{len(usernames_list)}" Usernames Saved '

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
            
        delay(message ) # Random delay per request (2–6 seconds)
              
    if output_type == "file":
        print(f'[SUCCESS] Extracting Usernames is Done, "{len(usernames_list)}" usernames saved to "{file_path}"')
    else:
        print(f'[SUCCESS] Extracting Usernames is Done, "{len(usernames_list)}" usernames saved.')

    return usernames_list
