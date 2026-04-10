def second_function():
    print("This is the second function.")

def first_function():
    print("This is the first function.")
    second_function()

# Execute
first_function()