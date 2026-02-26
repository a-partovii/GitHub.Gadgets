from modules.tui import show_menu
from modules.operations import follow_submenu

main_menu = {
    "1": {"label": "Follow", "action": lambda: show_menu(follow_submenu)},
    # "2": {"label": "Unfollow", "action": "unfollow"},
    # "3": {"label": "Extract usernames", "action": ""},
    # "4": {"label": "Adjust Blacklist", "action": ""},
    # "5": {"label": "Adjust Whitelist", "action": ""},
    # "6": {"label": "Adjust GitHub tokens", "action": ""},
    # "7": {"label": "Visit credits", "action": ""},
    # "0": {"label": "Exit", "action": "exit_app"},
}

show_menu(main_menu)