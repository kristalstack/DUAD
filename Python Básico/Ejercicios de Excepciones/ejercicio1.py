def show_menu():
    print("\n--- CALCULATOR ---")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Clear result")
    print("6. Exit")


def get_number(prompt):
    while True:
        user_input = input(prompt)
        try:
            return float(user_input)
        except ValueError:
            print("Error: Please enter a valid number.")


def add(current):
    number = get_number("Number to add: ")
    return current + number


def subtract(current):
    number = get_number("Number to subtract: ")
    return current - number


def multiply(current):
    number = get_number("Number to multiply: ")
    return current * number

def divide(current):
    number = get_number("Number to divide: ")

    if number == 0:
        print("Error: Cannot divide by zero.")
        return current

    return current / number

def clear():
    print("Result cleared.")
    return 0.0


def calculator():
    current_number = 0.0

    while True:
        print(f"\nCurrent number: {current_number}")
        show_menu()

        option = input("Select an option: ")

        if option == "1":
            current_number = add(current_number)

        elif option == "2":
            current_number = subtract(current_number)

        elif option == "3":
            current_number = multiply(current_number)

        elif option == "4":
            current_number = divide(current_number)

        elif option == "5":
            current_number = clear()

        elif option == "6":
            print("Exiting calculator...")
            break

        else:
            print("Invalid option.")


calculator()