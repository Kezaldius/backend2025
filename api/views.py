from api import app
from flask import request, jsonify
import uuid

users = {}
categories = {}
records = {}

@app.route("/healthcheck")
def healthcheck():
    return {"status": "OK", "message": "Application is healthy"}

@app.route("/user", methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_id = str(uuid.uuid4())

    user = {
        "id": user_id,
        "Ім'я": user_data.get("Ім'я")
    }
    users[user_id] = user
    return jsonify(user), 201


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    del users[user_id]
    return '', 204

@app.route('/category', methods = ['POST'])
def create_categoires():
    category_data = request.get_json()
    category_id = str(uuid.uuid4)

    category = {
        "id": category_id,
        "Назва категорії": category_data.get("Назва категорії")
    }

@app.route('/category', methods = ['GET'])
def get_categories():
    return jsonify(list(categories.values())), 200

@app.route('/category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    del categories[category_id]
    return '', 204


