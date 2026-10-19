from modules.major_modules import extract_usernames
from modules.file_modules import read_file, write_file, check_file_exists
from modules.tokens import primary_token

def my_followers() -> list:
    """Return the current user's followers from cache or fetch them."""
    if check_file_exists("app_data/temp/.my_followers.temp"):
        my_followers = read_file(file_path="app_data/temp/.my_followers.temp")
        return my_followers
    
    my_followers = extract_usernames(
        next(iter(primary_token)),
        source="followers",
        show_message=False
    )
    write_file(file_path="app_data/temp/.my_followers.temp", input_item=my_followers)
    return my_followers
