from datetime import date


class User:
    def __init__(self, date_of_birth):
        self.date_of_birth = date_of_birth

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year
    

def validate_adult(func):
    def wrapper(user, *args, **kwargs):

        if user.age < 18:
            raise ValueError("User must be 18 or older")

        return func(user, *args, **kwargs)

    return wrapper

@validate_adult
def access_system(user):
    return "Access granted"

# Usuario mayor de edad
adult_user = User(date(2000, 1, 1))

print(access_system(adult_user))


# Usuario menor de edad
minor_user = User(date(2010, 1, 1))

try:
    print(access_system(minor_user))
except ValueError as e:
    print(f"Error: {e}")