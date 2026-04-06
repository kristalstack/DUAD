def check_if_lists_have_an_equal(list_a, list_b):
    for element_a in list_a:
        for element_b in list_b:
            if element_a == element_b:
                return True
    return False

#Complejidad temporal: O(n * m)
#Complejidad espacial: O(1)

#Análisis:
#El algoritmo utiliza dos ciclos anidados. Por cada elemento de list_a, se comparan todos los elementos de list_b. Si list_a tiene n elementos y list_b tiene m, el número total de comparaciones es n * m. Por eso, la complejidad es O(n * m). No se usa memoria adicional significativa.