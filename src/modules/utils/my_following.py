from modules.major_modules.extract_usernames import extract_usernames
from modules.file_modules import read_file, write_file, check_file_exists
from modules.tokens import primary_token

def my_following() -> list:
    """Return the current user's following from cache or fetch them."""
    if check_file_exists("app_data/temp/.my_following.temp"):
        my_following = read_file(file_path="app_data/temp/.my_following.temp")
        return my_following
    
    my_following = extract_usernames(
        next(iter(primary_token)),
        source="following",
        show_message=False
    )
    write_file(file_path="app_data/temp/.my_following.temp", input_item=my_following)
    return my_following
