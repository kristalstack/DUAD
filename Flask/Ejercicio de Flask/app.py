from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

FILE_NAME = "tareas.json"
VALID_STATUSES = ["Por Hacer", "En Progreso", "Completada"]


def read_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = read_tasks()
    status = request.args.get("status")

    if status:
        tasks = [task for task in tasks if task["status"] == status]

    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    tasks = read_tasks()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Data must be sent in JSON format"}), 400

    if "id" not in data:
        return jsonify({"error": "Task id is required"}), 400

    if not isinstance(data["id"], int):
        return jsonify({"error": "Task id must be an integer"}), 400

    for task in tasks:
        if task["id"] == data["id"]:
            return jsonify({"error": "A task with this id already exists"}), 400

    if not data.get("title"):
        return jsonify({"error": "Task title is required"}), 400

    if not data.get("description"):
        return jsonify({"error": "Task description is required"}), 400

    if not data.get("status"):
        return jsonify({"error": "Task status is required"}), 400

    if data["status"] not in VALID_STATUSES:
        return jsonify({"error": "Invalid status"}), 400

    new_task = {
        "id": data["id"],
        "title": data["title"],
        "description": data["description"],
        "status": data["status"]
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify({
        "message": "Task created successfully",
        "task": new_task
    }), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = read_tasks()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Data must be sent in JSON format"}), 400

    for task in tasks:
        if task["id"] == task_id:

            if "title" in data:
                if not data["title"]:
                    return jsonify({"error": "Task title cannot be empty"}), 400
                task["title"] = data["title"]

            if "description" in data:
                if not data["description"]:
                    return jsonify({"error": "Task description cannot be empty"}), 400
                task["description"] = data["description"]

            if "status" in data:
                if not data["status"]:
                    return jsonify({"error": "Task status cannot be empty"}), 400

                if data["status"] not in VALID_STATUSES:
                    return jsonify({"error": "Invalid status"}), 400

                task["status"] = data["status"]

            save_tasks(tasks)

            return jsonify({
                "message": "Task updated successfully",
                "task": task
            }), 200

    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = read_tasks()

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)

            return jsonify({
                "message": "Task deleted successfully"
            }), 200

    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)