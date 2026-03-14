def count_cases(text):
    upper_count = 0
    lower_count = 0

    for char in text:
        if char.isupper():
            upper_count += 1
        elif char.islower():
            lower_count += 1

    print(f"There are {upper_count} upper cases and {lower_count} lower cases")


# Prueba
count_cases("I love Nación Sushi")