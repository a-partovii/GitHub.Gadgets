from modules.major_modules import follow, extract_usernames
from modules.file_modules import file_picker, read_file
from modules.utils import filter_list

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
follow_sub_menu = {
    "1": {"label": "Follow back your followers", "action": follow_back},
    "2": {"label": "Follow from a list file", "action": follow_from_file},
    "3": {"label": "Follow from a user's followers", "action": follow_from_followers},
    "4": {"label": "Follow from a user's following", "action": follow_from_following},
    "5": {"label": "Follow who starred your repositories", "action": follow_my_stargazers},
    "6": {"label": "Follow who starred a given repository", "action": follow_repo_stargazers},
    # "7": {"label": "Bulk follow with a count limit", "action": follow_bulk},
    # "0": {"label": "Back to main menu", "action": return_to_main},
}
