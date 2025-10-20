from api import app
from flask import request, jsonify
from datetime import datetime
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
    if user_id in users:
        del users[user_id]
        return '', 204
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/category', methods = ['POST'])
def create_categoires():
    category_data = request.get_json()
    category_id = str(uuid.uuid4())

    category = {
        "id": category_id,
        "Назва категорії": category_data.get("Назва категорії")
    }

    categories[category_id] = category
    return jsonify(category), 201

@app.route('/category', methods = ['GET'])
def get_categories():
    return jsonify(list(categories.values())), 200

@app.route('/category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id in categories:
        del categories[category_id]
        return '', 204
    else:
        return jsonify({"error": "Category not found"}), 404


@app.route('/record', methods = ['POST'])
def create_record():
    record_data = request.get_json()
    record_id = str(uuid.uuid4())

    record = {
        "id": record_id,
        "Id користувача": record_data.get("user_id"),
        "Id категорії": record_data.get("category_id"),
        "Дата та час створення запису": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "Сума витрати": record_data.get("Сума витрати")
    }

    records[record_id] = record
    return jsonify(record), 201

@app.route('/record/<record_id>', methods=['GET'])
def get_record(record_id):
    record = records.get(record_id)

    if record:
        return jsonify(record), 200
    return jsonify({"error": "Record not found"}), 404

@app.route('/record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in records:
        del records[record_id]
        return '', 204
    else:
        return jsonify({"error": "Record not found"}), 404

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({"error": "At least one parameter (user_id or category_id) is required"}), 400
    
    filtered_records = list(records.values())
    if user_id:
        filtered_records = [rec for rec in filtered_records if rec.get("Id користувача") == user_id]
    if category_id:
        filtered_records = [rec for rec in filtered_records if rec.get("Id категорії") == category_id]

    return jsonify(filtered_records), 200
    

