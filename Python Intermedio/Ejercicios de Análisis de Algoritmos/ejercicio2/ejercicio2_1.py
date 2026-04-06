def print_numbers_times_2(numbers_list):
    for number in numbers_list:
        print(number * 2)

#Complejidad temporal: O(n)
#Complejidad espacial: O(1)

#Análisis:
#La función recorre cada elemento de la lista una sola vez. Si la lista tiene n elementos, el ciclo se ejecuta n veces. Por lo tanto, la complejidad es lineal. No se utiliza memoria adicional significativa, por lo que la complejidad espacial es constante.