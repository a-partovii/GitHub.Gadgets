from modules.major_modules import follow, extract_usernames
from modules.utils import filter_list

def follow_back(my_username):
    try:
        my_followers = extract_usernames(my_username, "followers")
        my_following = extract_usernames(my_username, "following")

        usernames = filter_list(my_followers, my_following)
        follow(usernames)
    except:
        pass
# -------------------------------------------------------------------------------------------------
follow_sub_menu = {
    "1": {"label": "Follow back your followers", "action": follow_back},
    # "2": {"label": "Follow from a list file", "action": follow_from_file},
    # "3": {"label": "Follow from a user's followers", "action": follow_followers},
    # "4": {"label": "Follow from a user's following", "action": follow_following},
    # "5": {"label": "Follow who starred your repositories", "action": follow_my_stargazers},
    # "6": {"label": "Follow who starred a given repository", "action": follow_repo_stargazers},
    # "7": {"label": "Bulk follow with a count limit", "action": follow_bulk},
    # "0": {"label": "Back to main menu", "action": return_to_main},
}
