def show_menu(menu_dict):
    while True:
        print("Choose an option to continue:")

        for key, item in menu_dict.items():
            print(f"{key}. {item['label']}")

        choice = input("\nEnter your choice: ").strip()

        if choice in menu_dict:
            menu_dict[choice]["action"]()
        else:
            print("[ERROR] Invalid option. Please try again.")