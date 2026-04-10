list_a = ['first_name', 'last_name', 'role']
list_b = ['Alek', 'Castillo', 'Software Engineer']

# Crear diccionario vacío
my_dict = {}

# Recorrer usando índice
for i in range(len(list_a)):
    key = list_a[i]
    value = list_b[i]
    my_dict[key] = value

print(my_dict)