from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

ARCHIVO = "tareas.json"
ESTADOS = ["Por Hacer", "En Progreso", "Completada"]


def leer_tareas():
    if not os.path.exists(ARCHIVO):
        return []

    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_tareas(tareas):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(tareas, archivo, indent=4, ensure_ascii=False)


@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    tareas = leer_tareas()
    estado = request.args.get("estado")

    if estado:
        tareas = [tarea for tarea in tareas if tarea["estado"] == estado]

    return jsonify(tareas), 200


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    tareas = leer_tareas()
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    if "id" not in datos:
        return jsonify({"error": "Debe indicar un identificador"}), 400

    for tarea in tareas:
        if tarea["id"] == datos["id"]:
            return jsonify({"error": "El identificador ya existe"}), 400

    if not datos.get("titulo"):
        return jsonify({"error": "No se pueden agregar tareas sin nombre"}), 400

    if not datos.get("descripcion"):
        return jsonify({"error": "No se pueden agregar tareas sin descripción"}), 400

    if not datos.get("estado"):
        return jsonify({"error": "No se pueden agregar tareas sin estado"}), 400

    if datos["estado"] not in ESTADOS:
        return jsonify({"error": "Estado inválido"}), 400

    nueva_tarea = {
        "id": datos["id"],
        "titulo": datos["titulo"],
        "descripcion": datos["descripcion"],
        "estado": datos["estado"]
    }

    tareas.append(nueva_tarea)
    guardar_tareas(tareas)

    return jsonify({
        "mensaje": "Tarea creada correctamente",
        "tarea": nueva_tarea
    }), 201


@app.route("/tareas/<int:id>", methods=["PUT"])
def editar_tarea(id):
    tareas = leer_tareas()
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    for tarea in tareas:
        if tarea["id"] == id:

            if "titulo" in datos:
                if not datos["titulo"]:
                    return jsonify({"error": "El título no puede estar vacío"}), 400
                tarea["titulo"] = datos["titulo"]

            if "descripcion" in datos:
                if not datos["descripcion"]:
                    return jsonify({"error": "La descripción no puede estar vacía"}), 400
                tarea["descripcion"] = datos["descripcion"]

            if "estado" in datos:
                if not datos["estado"]:
                    return jsonify({"error": "El estado no puede estar vacío"}), 400

                if datos["estado"] not in ESTADOS:
                    return jsonify({"error": "Estado inválido"}), 400

                tarea["estado"] = datos["estado"]

            guardar_tareas(tareas)

            return jsonify({
                "mensaje": "Tarea actualizada correctamente",
                "tarea": tarea
            }), 200

    return jsonify({"error": "Tarea no encontrada"}), 404


@app.route("/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    tareas = leer_tareas()

    for tarea in tareas:
        if tarea["id"] == id:
            tareas.remove(tarea)
            guardar_tareas(tareas)

            return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200

    return jsonify({"error": "Tarea no encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)