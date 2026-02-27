from modules.major_modules import unfollow, extract_usernames, extract_bulk_usernames
from modules.file_modules import file_picker, read_file
from modules.utils import filter_list
from config.tokens import primary_token

def unfollow_non_followers():
    try:
        my_username = next(iter(primary_token))
        my_following = extract_usernames(my_username, "following")
        my_followers = extract_usernames(my_username, "followers")

        usernames = filter_list(my_following, my_followers)
        unfollow(usernames)
    except:
        pass

# -----------------------------------------------------------------------------------------
unfollow_submenu = {
    "1": {"label": "Unfollow users who don't follow you back", "action": unfollow_non_followers},
    "2": {"label": "Unfollow from a list file", "action": unfollow_from_file},
    "3": {"label": "Unfollow from a user's followers", "action": unfollow_from_followers},
    "4": {"label": "Unfollow from a user's following", "action": unfollow_from_following},
    "5": {"label": "Unfollow who starred a given user's repositories", "action": unfollow_user_stargazers},
    "6": {"label": "Unfollow who starred a given repository", "action": unfollow_repo_stargazers},
    "7": {"label": "Bulk unfollow with a limit count", "action": unfollow_bulk},
    "0": {"label": "Back to main menu", "action": return_to_main},
}