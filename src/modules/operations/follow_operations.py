from modules.major_modules import follow, extract_usernames
from modules.file_modules import file_picker, read_file
from modules.utils import filter_list, deduplicate_list_content

def follow_back(my_username:str):
    try:
        my_followers = extract_usernames(my_username, "followers")
        my_following = extract_usernames(my_username, "following")

        usernames = filter_list(my_followers, my_following)
        follow(usernames)
    except:
        pass

# -----------------------------------------------------------------------------------------
def follow_from_file():
    try:
        file_path = file_picker()
        if not file_path:
            print("Operation cancelled.")
            return

        usernames = read_file(file_path)
        follow(usernames)
    except:
        pass

# -----------------------------------------------------------------------------------------
def follow_from_followers():
    try:
        target_username = input("Enter a username to follow their followers: ")
        usernames = extract_usernames(target_username, "followers", show_message=False)
        follow(usernames)
    except:
        pass

# -----------------------------------------------------------------------------------------
def follow_from_following():
    try:
        target_username = input("Enter a username to follow their following: ")
        usernames = extract_usernames(target_username, "following", show_message=False)
        follow(usernames)
    except:
        pass

# -----------------------------------------------------------------------------------------
def follow_my_stargazers():
    print("coming soon...")

# -----------------------------------------------------------------------------------------
def follow_repo_stargazers():
    print("coming soon...")

# -----------------------------------------------------------------------------------------
def follow_bulk(my_username:str):
    while True:
        try:
            limit_count = int(input("Enter a number for the bulk follow limit count: "))
            if limit_count >= 1:
                break
        except:
            print("Please just enter a valid number and push the <Enter>")
    try: 
        usernames = extract_usernames(
                                "a-partovii",
                                "followers",
                                limit_count=limit_count,
                                show_message=False)
        
        my_following = set(extract_usernames(my_username, "following", show_message=False) or [])
        blacklist = set(read_file("config/blacklist.txt") or [])

        while True: 
            usernames = deduplicate_list_content(usernames)
            spare_list = usernames.copy()
            usernames = filter_list(usernames, my_following)
            usernames = filter_list(usernames, blacklist)
            
            if len(usernames) < limit_count:
                print("make spare")
                for target_username in spare_list[:]:
                    temp_list = extract_usernames(
                            target_username= target_username,
                            source="followers",
                            limit_count=limit_count,
                            show_message=False)
                    
                    usernames.extend(temp_list)
                    spare_list.remove(target_username)

                    if len(usernames) >= limit_count or temp_list is False:
                        break
            else:
                break
    
    except Exception as error:
        print(f"[ERROR] {error}")
        return False

    follow(
        usernames,
        skip_followed=False,
        skip_blacklist=False)
# -----------------------------------------------------------------------------------------
follow_sub_menu = {
    "1": {"label": "Follow back your followers", "action": follow_back},
    "2": {"label": "Follow from a list file", "action": follow_from_file},
    "3": {"label": "Follow from a user's followers", "action": follow_from_followers},
    "4": {"label": "Follow from a user's following", "action": follow_from_following},
    "5": {"label": "Follow who starred your repositories", "action": follow_my_stargazers},
    "6": {"label": "Follow who starred a given repository", "action": follow_repo_stargazers},
    "7": {"label": "Bulk follow with a count limit", "action": follow_bulk},
    # "0": {"label": "Back to main menu", "action": return_to_main},
}
