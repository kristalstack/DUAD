# Program to classify age group

first_name = input("Enter your name: ")
last_name = input("Enter your last name: ")
age = int(input("Enter your age: "))

if age >= 0 and age <= 2:
    category = "baby"
elif age <= 12:
    category = "child"
elif age <= 15:
    category = "preadolescent"
elif age <= 18:
    category = "adolescent"
elif age <= 30:
    category = "young adult"
elif age <= 59:
    category = "adult"
else:
    category = "senior adult"

print("\n--- Result ---")
print("Name:", first_name, last_name)
print("Age:", age)
print("Your age category is:", category)