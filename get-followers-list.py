import requests as req



github_token = "YOUR_PERSONAL_ACCESS_TOKEN"

headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json"
}
# -------------------------------------------

def get_followers_list(username, headers, output_type):
    page = 1
    # per_page = 100  # Max items per request
    followers_list = []
    while True:
        url = f"https://api.github.com/users/{username}/followers?per_page=100&page={page}"
        response = req.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching followers — HTTP {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for follower in data:
            followers_list.append(follower.get("login"))

            # username = follower.get("login")
            # with open(f"({username})followers.txt", "w", encoding="utf-8") as file:
            #     file.write(username + "\n")
            #     print(f"Saved: {username}")
        page += 1
        # Random delay per request (2–6 seconds)
        delay(2, 6)

    if output_type == "file": # "file" or "list(default)"
        try:
            with open(f"({username})followers.txt", "w") as file:
                for username in followers_list:
                    file.write(username + "\n")
        except :
            print("Writing in the file was not success, check this error and try again: \n")
    else:
        return followers_list
    print("Done! All follower usernames saved.")
