# student manager project

from menu import show_menu, get_menu_option
from actions import (
    add_students,
    show_all_students,
    show_top_3_students,
    show_average_of_all_students
)
from data import export_to_csv, import_from_csv

def main():
    students = []

    while True:
        show_menu()
        option = get_menu_option()

        if option == "1":
            add_students(students)

        elif option == "2":
            show_all_students(students)

        elif option == "3":
            show_top_3_students(students)

        elif option == "4":
            show_average_of_all_students(students)

        elif option == "5":
            export_to_csv(students)

        elif option == "6":
            students = import_from_csv()

        elif option == "7":
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()