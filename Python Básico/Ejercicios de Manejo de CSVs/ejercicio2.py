import csv

# Pedir cantidad de videojuegos
n = int(input("¿Cuántos videojuegos quieres registrar?: "))

with open("videojuegos_tab.txt", "w", newline="", encoding="utf-8") as archivo:
    
    # delimiter="\t" indica que se separará por tabulaciones
    escritor = csv.writer(archivo, delimiter="\t")

    # Encabezado
    escritor.writerow(["nombre", "genero", "desarrollador", "clasificacion"])

    for i in range(n):
        print(f"\nVideojuego {i+1}")

        nombre = input("Nombre: ")
        genero = input("Genero: ")
        desarrollador = input("Desarrollador: ")
        clasificacion = input("Clasificación ESRB: ")

        escritor.writerow([nombre, genero, desarrollador, clasificacion])

print("\nArchivo guardado correctamente con tabulaciones.")