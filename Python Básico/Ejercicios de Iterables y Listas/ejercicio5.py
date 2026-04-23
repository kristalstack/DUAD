numbers = []

# Ask for 10 numbers
for i in range(10):
    number = int(input("Enter a number: "))
    numbers.append(number)

# Find the highest number manually
highest = numbers[0]

for num in numbers:
    if num > highest:
        highest = num

# Show results
print("\nNumbers entered:", numbers)
print("The highest number is:", highest)
