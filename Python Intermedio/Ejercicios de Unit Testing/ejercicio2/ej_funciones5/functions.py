def count_case(s):
    upper = 0
    lower = 0

    for char in s:
        if char.isupper():
            upper += 1
        elif char.islower():
            lower += 1

    return f"There’s {upper} upper cases and {lower} lower cases"