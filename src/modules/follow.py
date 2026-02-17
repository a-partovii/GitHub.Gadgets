from config import primary_token, token_manager, make_header
from modules.utils import delay_and_super_delay
import requests as req

total = 0
def follow(username:str):
    global total
    url = f"https://api.github.com/user/following/{username}"
    headers = make_header(token_manager(primary_token))
    try:
        response = req.put(url, headers=headers, timeout=5)
        total += 1
        try:
            delay_and_super_delay(message= f'User: {username} followed, Total Follow: "{total}", Token RateLimit Remaining: "{response.headers["X-RateLimit-Remaining"]}"',
                                min=7,
                                max=15)
        except:
            pass
        return response
        
    except req.RequestException:
        return None
