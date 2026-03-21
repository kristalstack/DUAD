def show_menu():
    print("\n=== STUDENT MANAGEMENT MENU ===")
    print("1. Add students")
    print("2. Show all students")
    print("3. Show top 3 students")
    print("4. Show average of all students")
    print("5. Export data to CSV")
    print("6. Import data from CSV")
    print("7. Exit")


def get_menu_option():
    valid_options = ["1", "2", "3", "4", "5", "6", "7"]

    while True:
        option = input("Choose an option: ").strip()

        if option in valid_options:
            return option
        else:
            print("Invalid option. Please try again.")