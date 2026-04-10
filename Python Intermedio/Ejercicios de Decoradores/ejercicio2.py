def validate_numbers(func):
    def wrapper(*args, **kwargs):

        for value in args:
            if not isinstance(value, (int, float)):
                raise ValueError("All parameters must be numbers")

        for value in kwargs.values():
            if not isinstance(value, (int, float)):
                raise ValueError("All parameters must be numbers")

        return func(*args, **kwargs)

    return wrapper

@validate_numbers
def add(a, b):
    return a + b

print(add(5, 3))  # valid

try:
    print(add(5, "3"))  # invalid
except ValueError as e:
    print(f"Error: {e}")