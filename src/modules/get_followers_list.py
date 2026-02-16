import requests as req
from datetime import datetime
import os
from modules.delay import delay
from modules.write_in_file import write_in_file
from inputs.tokens import secondary_tokens, token_manager, make_headers

def get_followers_list(target_username, output_type):
    """
    Fetch followers of the specified GitHub user.

    Args:
        target_username: Username of the account whose followers will be extracted
        headers: Request headers (available from the token module)
        output_type: "file" to save output, "list" to return as a list (default = list)
    """
    current_date = datetime.now().strftime("%Y-%m-%d_%H;%M") # Get current date and time for the output file naming
    file_path = f"outputs/({target_username})followers [{current_date}].txt"

    page = 1
    followers_list = []
    while True:
        # per_page = 100, max items per request
        url = f"https://api.github.com/users/{target_username}/followers?per_page=100&page={page}"
        headers = make_headers(token_manager(secondary_tokens))
        response = req.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching followers — HTTP {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for follower in data:
            followers_list.append(follower.get("login"))

        if output_type == "file": # "file" or "list" (default=List)
            try:
                os.makedirs("outputs", exist_ok=True) # Create outputs folder if it doesn't exist
                write_in_file(file_path=file_path, input_item=followers_list, writing_mode="w")

            except Exception as error:
                print(f"Writing in the file was not successful, check this error and try again: \n{error}")

        page += 1
        delay(message=f'SUCCESS: "{len(followers_list)}" usernames saved to "{file_path}"') # Random delay per request (2–6 seconds)
              
    if output_type == "file":
        print(f'SUCCESS: Extracting usernames is done, "{len(followers_list)}" usernames saved to "{file_path}"')
    else:
        print(f'SUCCESS: Extracting usernames is done, "{len(followers_list)}" usernames saved.')
    return followers_list
