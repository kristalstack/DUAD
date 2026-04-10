def reverse_string(text):
    reversed_text = ""
    
    for i in range(len(text) - 1, -1, -1):
        reversed_text += text[i]
    
    return reversed_text


# Prueba
result = reverse_string("Hola mundo")
print(result)