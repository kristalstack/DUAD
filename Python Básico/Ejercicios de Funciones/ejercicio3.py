def sum_list(numbers):
    total = 0
    
    for num in numbers:
        total += num
    
    return total


# Prueba
my_list = [4, 6, 2, 29]
result = sum_list(my_list)

print("Sum:", result)