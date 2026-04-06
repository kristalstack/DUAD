def print_10_or_less_elements(list_to_print):
    list_len = len(list_to_print)

    for index in range(min(list_len, 10)):
        print(list_to_print[index])

#Complejidad temporal: O(1)
#Complejidad espacial: O(1)

#Análisis:
#El ciclo se ejecuta como máximo 10 veces, sin importar el tamaño de la lista. Como el número de operaciones no crece con la entrada, la complejidad es constante. Tampoco se utiliza memoria adicional.