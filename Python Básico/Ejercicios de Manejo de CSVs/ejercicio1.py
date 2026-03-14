import csv

# Pedir cuántos videojuegos se van a ingresar
n = int(input("¿Cuántos videojuegos quieres registrar?: "))

# Abrir el archivo CSV en modo escritura
with open("videojuegos.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)

    # Escribir encabezado
    escritor.writerow(["nombre", "genero", "desarrollador", "clasificacion"])

    # Pedir los datos de cada videojuego
    for i in range(n):
        print(f"\nVideojuego {i + 1}")

        nombre = input("Nombre: ")
        genero = input("Género: ")
        desarrollador = input("Desarrollador: ")
        clasificacion = input("Clasificación ESRB: ")

        # Guardar fila en el CSV
        escritor.writerow([nombre, genero, desarrollador, clasificacion])

print("\nLos datos se guardaron correctamente en 'videojuegos.csv'.")