from modules.major_modules import extract_usernames
from modules.file_modules import read_file, write_file, filename_datetime
from modules.utils import filter_list
from modules.tokens import primary_token
from modules.tui import print_in_columns, ask_output_type

def extract_your_followers():
    output_type = ask_output_type()
    my_username = next(iter(primary_token))
    try:
        my_followers = extract_usernames(
             target_username=my_username,
             source="followers",
             output_type=output_type[1]
        )

        if output_type[0] == 1 :
            print_in_columns(my_followers)

        elif output_type[0] == 3 :
              """ When the 'output_type' argument in the 'extract_usernames()' function is set to "file",
               the function returns the path of the output file.
               Therefore, here the "my_following" variable contains this path."""
              print_in_columns(read_file(my_followers))
        
    except Exception as error:
        print(f"[ERROR] {error}")

# -----------------------------------------------------------------------------------------
def extract_your_following():
    output_type = ask_output_type()
    my_username = next(iter(primary_token))
    try:
        my_following = extract_usernames(
             target_username=my_username,
             source="following",
             output_type= output_type[1]
        )

        if output_type[0] == 1 :
            print_in_columns(my_following)

        elif output_type[0] == 3 :
              print_in_columns(read_file(my_following))

    except Exception as error:
        print(f"[ERROR] {error}")

# -----------------------------------------------------------------------------------------
def extract_non_follower_following():
    output_type = ask_output_type()
    my_username = next(iter(primary_token))
    try:
        my_following = extract_usernames(
                target_username=my_username,
                source="following",
        )
        my_followers = extract_usernames(
                target_username=my_username,
                source="followers",
        )

        if output_type[0] == 2 or output_type[0] == 3 :
            file_path = f"outputs/({my_username})non-follower-following {filename_datetime()}"
            write_file(file_path, filter_list(my_following, my_followers))
            print(f'[SUCCESS] Extracting Usernames is Done, usernames saved to "{file_path}"\n')

        if output_type[0] == 1 or output_type[0] == 3 :
            print("Usernames you follow who don't follow you back:")
            print_in_columns(filter_list(my_following, my_followers))

    except Exception as error:
        print(f"[ERROR] {error}")

# -----------------------------------------------------------------------------------------
def extract_from_followers():
    output_type = ask_output_type()

    try:
        target_username = input("Enter a username to extract their followers: ")
        usernames = extract_usernames(
             target_username=target_username,
             source="followers",
             output_type= output_type[1]
        )

        if output_type[0] == 1 :
            print_in_columns(usernames)

        elif output_type[0] == 3 :
              print_in_columns(read_file(usernames))

    except Exception as error:
        print(f"[ERROR] {error}")

# -----------------------------------------------------------------------------------------
def extract_from_following():
    output_type = ask_output_type()

    try:
        target_username = input("Enter a username to extract their following: ")
        usernames = extract_usernames(
             target_username=target_username,
             source="following",
             output_type= output_type[1]
        )

        if output_type[0] == 1 :
            print_in_columns(usernames)

        elif output_type[0] == 3 :
              print_in_columns(read_file(usernames))

    except Exception as error:
        print(f"[ERROR] {error}")

# -----------------------------------------------------------------------------------------
def extract_my_stargazers():
    print("coming soon...")

# -----------------------------------------------------------------------------------------
def extract_user_stargazers():
    print("coming soon...")

# -----------------------------------------------------------------------------------------
def extract_repo_stargazers():
    print("coming soon...")

# -----------------------------------------------------------------------------------------
extract_submenu = {
    "1": {"label": "Extract your followers usernames", "action": extract_your_followers},
    "2": {"label": "Extract your following usernames", "action": extract_your_following},
    "3": {"label": "Extract usernames you follow who don't follow you back", "action": extract_non_follower_following},
    "4": {"label": "Extract a user's followers", "action": extract_from_followers},
    "5": {"label": "Extract a user's following", "action": extract_from_following},
    "6": {"label": "Extract usernames of users who starred your repositories", "action": extract_my_stargazers},
    "7": {"label": "Extract usernames of users who starred a given user's repositories", "action": extract_user_stargazers},
    "8": {"label": "Extract usernames of users who starred a given repository", "action": extract_repo_stargazers},
    # "0": {"label": "Back to main menu", "action": return_to_main},
}
