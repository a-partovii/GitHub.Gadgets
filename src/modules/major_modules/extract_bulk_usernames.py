from modules.file_modules import read_file
from modules.utils import filter_list, deduplicate_list_content
from config.tokens import primary_token
from .extract_usernames import extract_usernames
import random

def extract_bulk_usernames(limit_count:int) -> list:
    """
    Extract a filtered bulk list of usernames based on followers of random seed users.

    Args:
        limit_count (int): Minimum number of usernames to collect.

    Returns:
        list[str] | bool: Filtered usernames list or False on error.
    """
    try: 
        # Extract first list of usernames (hard coded source)
        target_username = random.choice(["a-partovii", "torvalds", "gaearon", "yyx990803", "karpathy",
                                         "bradtraversy", "sindresorhus", "trekhleb", "antirez", "google",
                                         "github", "OpenAI", "aws", "kde", "oracle", "python", "nodejs", "milvus-io"])
        usernames_list = extract_usernames(
                                target_username,
                                source="followers",
                                limit_count=limit_count,
                                show_message=False)
        
        my_username = next(iter(primary_token))
        my_following = set(extract_usernames(my_username, "following", show_message=False) or [])
        blacklist = set(read_file("config/blacklist.txt") or [])

        while True: # Loop to ensure we have at least `limit_count` usernames after filtering
            usernames_list = deduplicate_list_content(usernames_list)
            spare_list = usernames_list.copy() # Save as a fallback source
            usernames_list = filter_list(usernames_list, my_following)
            usernames_list = filter_list(usernames_list, blacklist)

            # If after filtering we still have fewer than the desired count,
            # try to fetch more from new in-loop sources
            if len(usernames_list) < limit_count:
                for target_username in spare_list[:]:
                    temp_list = extract_usernames(
                            target_username= target_username,
                            source="followers",
                            limit_count=limit_count,
                            show_message=False)
                    
                    usernames_list.extend(temp_list)
                    spare_list.remove(target_username)

                    # Checking False is for the extracting module force break
                    if len(usernames_list) >= limit_count or temp_list is False:
                        break
            else:
                return usernames_list

    except Exception as error:
        print(f"[ERROR] {error}")
        return False
