def sort_words(text):
    # 1️⃣ Convertir string a lista
    words = text.split("-")
    
    # 2️⃣ Ordenar alfabéticamente
    words.sort()
    
    # 3️⃣ Convertir lista nuevamente a string
    sorted_text = "-".join(words)
    
    return sorted_text


# Prueba
result = sort_words("python-variable-funcion-computadora-monitor")
print(result)