def my_function():
    message = "Hello from inside the function"

my_function()

print(message)  # Gives error


counter = 0

def increase():
    counter += 1   # Gives error

increase()

counter = 0

def increase():
    global counter
    counter += 1

increase()
print(counter)  # 1