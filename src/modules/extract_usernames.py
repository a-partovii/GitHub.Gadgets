import requests as req
from datetime import datetime
import os
from modules.delay import delay
from modules.write_in_file import write_in_file
from inputs.tokens import secondary_tokens, token_manager, make_headers

def extract_usernames(target_username:str, source:str, output_type:str ="list"):
    """
    Fetch usernames of a specified GitHub user's followers or followed accounts.

    Args:
        target_username (str): Username of the account whose data will be extracted.
        source (str): "followers" to extract followers, "following" to extract followings of the given username.
        output_type (str): "list" to return as a list (default = list), "file" to save output file too.

    Returns:
        list[str] | None: List of usernames,
        None if there was an error.
    """
    current_date = datetime.now().strftime("%Y-%m-%d_%H;%M") # Get current date and time for the output file naming
    file_path = f"outputs/({target_username}){source} [{current_date}].txt"

    page = 1
    usernames_list = []
    if source not in {"followers", "following"}:
        raise ValueError('Invalid arqument, "source" must be "followers" or following"')
    while True:
        # per_page = 100, max items per request
        url = f"https://api.github.com/users/{target_username}/{source}?per_page=100&page={page}"
        headers = make_headers(token_manager(secondary_tokens))
        response = req.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: HTTP request failed ({response.status_code}): {response.reason}")

            break

        data_json = response.json()
        if not data_json:
            break

        for user in data_json:
            usernames_list.append(user.get("login"))

        if output_type == "file": # "file" or "list" (default=List)
            try:
                os.makedirs("outputs", exist_ok=True) # Create outputs folder if it doesn't exist
                write_in_file(file_path=file_path, input_item=usernames_list, writing_mode="w")

            except Exception as error:
                print(f"Writing in the file was not successful, check this error and try again: \n{error}")

        page += 1
        delay(message=f'SUCCESS: "{len(usernames_list)}" usernames saved to "{file_path}"') # Random delay per request (2–6 seconds)
              
    if output_type == "file":
        print(f'SUCCESS: Extracting usernames is done, "{len(usernames_list)}" usernames saved to "{file_path}"')
    else:
        print(f'SUCCESS: Extracting usernames is done, "{len(usernames_list)}" usernames saved.')
    return usernames_list
