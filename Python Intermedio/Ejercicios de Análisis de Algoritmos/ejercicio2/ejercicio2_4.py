def generate_list_trios(list_a, list_b, list_c):
    result_list = []

    for element_a in list_a:
        for element_b in list_b:
            for element_c in list_c:
                result_list.append(f'{element_a} {element_b} {element_c}')

    return result_list

#Complejidad temporal: O(n * m * p)
#Complejidad espacial: O(n * m * p)

#Análisis:
#El algoritmo tiene tres ciclos anidados. Si las listas tienen tamaños n, m y p, el número total de iteraciones es n * m * p. Además, se almacenan todas las combinaciones en una lista, por lo que la memoria utilizada crece al mismo ritmo.