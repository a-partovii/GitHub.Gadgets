def show_menu(menu_dict:dict) :
    """
    Display a menu and execute the selected action.

    Args:
        menu_dict (dict): Dictionary of menu options.
            e.g. Format: 
            {
                "1": {"label": "Option name", "action": callable},
                ...
            }

    Notice: For functions that require arguments, use a lambda in the action field
    """
    while True:
        # Display menu options
        print("Choose an option to continue:\n")
        for key, item in menu_dict.items():
            print(f"{key}. {item['label']}")

        print()
        while True: # Ask user until a valid choice
            choice = input("Enter your choice: ").strip()

            if choice in menu_dict:
                break
            else:
                print("Please just enter a valid option number and press <Enter>.")

        # Execute selected action
        menu_dict[choice]["action"]()
