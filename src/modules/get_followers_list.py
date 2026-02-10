import requests as req
from modules.delay import delay
from datetime import datetime
import os

def get_followers_list(target_username, headers, output_type):
    """
    Fetch followers of the specified GitHub user.

    Args:
        target_username: Username of the account whose followers will be extracted
        headers: Request headers (available from the token module)
        output_type: "file" to save output, "list" to return as a list (default = list)
    """
    page = 1
    followers_list = []
    
    while True:
        # per_page = 100, max items per request
        url = f"https://api.github.com/users/{target_username}/followers?per_page=100&page={page}"
        response = req.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching followers — HTTP {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for follower in data:
            followers_list.append(follower.get("login"))

        page += 1
        delay(2, 6) # Random delay per request (2–6 seconds)

    if output_type == "file": # "file" or "list" (default=List)
        try:
            os.makedirs("outputs", exist_ok=True)# Create outputs folder if it doesn't exist
           
            current_date = datetime.now().strftime("%Y-%m-%d_%H;%M") # Get current date and time
            filename = f"outputs/({target_username})followers [{current_date}].txt"
            
            with open(filename, "w") as file:
                for username in followers_list:
                    file.write(username + "\n")
            
            print(f"Done! All follower usernames saved to {filename}")
        except Exception as e:
            print(f"Writing in the file was not successful, check this error and try again: \n{e}")
    else:
        return followers_list
