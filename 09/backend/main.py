import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(BASE_DIR, "contacts.json")


def load_data():
    """JSONファイルから連絡先データを読み込みます。

    Returns:
        list: 連絡先データのリスト。ファイルがない、または壊れている場合は空リストを返す。

    """
    if not os.path.exists(DATA_FILE_PATH):
        return []

    try:
        with open(DATA_FILE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []


def save_data(data):
    """連絡先データをJSONファイルに書き込みます。

    Args:
        data (list): 保存したい連絡先データのリスト

    """
    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    """保存されているすべてのアドレス帳データを返します"""
    contacts = load_data()
    return jsonify(contacts), 200


@app.route("/api/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    """指定されたIDの連絡先を1件返します"""
    contacts = load_data()

    contact = next((item for item in contacts if item["id"] == contact_id), None)

    if contact:
        return jsonify(contact), 200
    return jsonify({"error": "Contact not found"}), 404


@app.route("/api/contacts", methods=["POST"])
def create_contact():
    """新しい連絡先を作成し、保存します"""
    request_data = request.get_json()

    if not request_data or "name" not in request_data:
        return jsonify({"error": "Name is required"}), 400

    contacts = load_data()

    if contacts:
        new_id = contacts[-1]["id"] + 1
    else:
        new_id = 1

    new_contact = {
        "id": new_id,
        "name": request_data["name"],
        "phone": request_data.get("phone", ""),
        "email": request_data.get("email", ""),
    }

    contacts.append(new_contact)
    save_data(contacts)

    return jsonify(new_contact), 201


@app.route("/api/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    """指定されたIDの連絡先情報を更新します"""
    request_data = request.get_json()
    contacts = load_data()

    target_index = None
    for i, item in enumerate(contacts):
        if item["id"] == contact_id:
            target_index = i
            break

    if target_index is None:
        return jsonify({"error": "Contact not found"}), 404

    current_contact = contacts[target_index]
    current_contact["name"] = request_data.get("name", current_contact["name"])
    current_contact["phone"] = request_data.get("phone", current_contact["phone"])
    current_contact["email"] = request_data.get("email", current_contact["email"])

    contacts[target_index] = current_contact
    save_data(contacts)

    return jsonify(current_contact), 200


@app.route("/api/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    """指定されたIDの連絡先を削除します"""
    contacts = load_data()

    filtered_contacts = [item for item in contacts if item["id"] != contact_id]

    if len(contacts) == len(filtered_contacts):
        return jsonify({"error": "Contact not found"}), 404

    save_data(filtered_contacts)

    return jsonify({"message": "Contact deleted successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
