import json
import os

# Ruta de la carpeta donde está este archivo .py
carpeta_actual = os.path.dirname(__file__)

# Ruta completa del archivo pokemon.json
ruta_json = os.path.join(carpeta_actual, "pokemon.json")

# 1. Leer el archivo JSON existente
with open(ruta_json, "r", encoding="utf-8") as archivo:
    pokemones = json.load(archivo)

# 2. Pedir la información del nuevo Pokémon
nombre = input("Nombre del Pokémon: ")
nivel = int(input("Nivel: "))

cantidad_tipos = int(input("¿Cuántos tipos tiene?: "))
tipos = []

for i in range(cantidad_tipos):
    tipo = input(f"Tipo {i + 1}: ")
    tipos.append(tipo)

hp = int(input("HP: "))
attack = int(input("Attack: "))
defense = int(input("Defense: "))
sp_attack = int(input("Sp. Attack: "))
sp_defense = int(input("Sp. Defense: "))
speed = int(input("Speed: "))

# 3. Crear el nuevo Pokémon
nuevo_pokemon = {
    "name": {
        "english": nombre
    },
    "level": nivel,
    "type": tipos,
    "base": {
        "HP": hp,
        "Attack": attack,
        "Defense": defense,
        "Sp. Attack": sp_attack,
        "Sp. Defense": sp_defense,
        "Speed": speed
    }
}

# 4. Agregar el nuevo Pokémon
pokemones.append(nuevo_pokemon)

# 5. Guardar en el mismo archivo JSON
with open(ruta_json, "w", encoding="utf-8") as archivo:
    json.dump(pokemones, archivo, indent=2, ensure_ascii=False)

print("Pokémon agregado correctamente.")