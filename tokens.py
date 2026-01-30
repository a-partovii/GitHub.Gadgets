import random

primary_token = {
    "name": "token" 
}

secondary_tokens = {
    "name1": "token1",
    "name2": "token2",
    "name3": "token3"
}

def headeres(token):
    return {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

last_token = None
def random_token(tokens_dict):
    global last_token
    tokens_list = list(tokens_dict.values())

    if len(tokens_list) == 1:
        return tokens_list[0]
    
    while True:
        token = random.choice(tokens_list)
        if token != last_token:
            last_token = token
            return token

# print(random_token(secondary_tokens))