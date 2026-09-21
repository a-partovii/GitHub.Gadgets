from modules.major_modules import load_tokens
from modules.tui import show_menu
from modules.operations import (
                            follow_submenu,
                            unfollow_submenu,
                            extract_submenu,
                            config_submenu)
load_tokens()

main_menu = {
    "1": {"label": "Follow", "action": lambda: show_menu(follow_submenu)},
    "2": {"label": "Unfollow", "action": lambda:show_menu(unfollow_submenu)},
    "3": {"label": "Extract usernames", "action": lambda:show_menu(extract_submenu)},
    "4": {"label": "Adjust Configuration", "action": lambda: show_menu(config_submenu)},
    # "0": {"label": "Exit", "action": "exit_app"},
}

show_menu(main_menu)