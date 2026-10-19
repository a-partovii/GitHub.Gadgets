from modules.file_modules import delete_file

def clear_temp():
    try:
        delete_file(file_path="app_data/temp/.my_following.temp", show_message=False)
        delete_file(file_path="app_data/temp/.my_followers.temp", show_message=False)
        return True
    
    except Exception as error:
        print(f"[ERROR] Couldn't clear the old temp files: {error}")
        return False 