def log_function(func):
    def wrapper(*args, **kwargs):
        print(f"\nCalling function: {func.__name__}")
        print(f"Parameters: args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)

        print(f"Return: {result}\n")

        return result
    return wrapper


@log_function
def add(a, b):
    return a + b


add(5, 3)