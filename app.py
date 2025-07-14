from flask import Flask, request, jsonify
import json
import os

app = Flask(_name_)
DATA_FILE = 'kpas.json'

def load_kpas():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_kpas(kpas):
    with open(DATA_FILE, 'w') as file:
        json.dump(kpas, file, indent=2)

@app.route('/')
def index():
    return "KPA API is running!"

@app.route('/kpas', methods=['GET'])
def get_all_kpas():
    kpas = load_kpas()
    return jsonify(kpas)

@app.route('/kpas/<int:kpa_id>', methods=['GET'])
def get_kpa_by_id(kpa_id):
    kpas = load_kpas()
    for kpa in kpas:
        if kpa['id'] == kpa_id:
            return jsonify(kpa)
    return jsonify({"error": "KPA not found"}), 404

@app.route('/kpas', methods=['POST'])
def create_kpa():
    data = request.get_json()
    kpas = load_kpas()
    new_id = max([k['id'] for k in kpas], default=0) + 1
    new_kpa = {
        "id": new_id,
        "name": data.get("name", ""),
        "description": data.get("description", "")
    }
    kpas.append(new_kpa)
    save_kpas(kpas)
    return jsonify(new_kpa), 201

@app.route('/kpas/<int:kpa_id>', methods=['PUT'])
def update_kpa(kpa_id):
    data = request.get_json()
    kpas = load_kpas()
    for kpa in kpas:
        if kpa['id'] == kpa_id:
            kpa['name'] = data.get("name", kpa['name'])
            kpa['description'] = data.get("description", kpa['description'])
            save_kpas(kpas)
            return jsonify(kpa)
    return jsonify({"error": "KPA not found"}), 404

@app.route('/kpas/<int:kpa_id>', methods=['DELETE'])
def delete_kpa(kpa_id):
    kpas = load_kpas()
    updated_kpas = [k for k in kpas if k['id'] != kpa_id]
    if len(updated_kpas) == len(kpas):
        return jsonify({"error": "KPA not found"}), 404
    save_kpas(updated_kpas)
    return jsonify({"message": "KPA deleted"})

if _name_ == "_main_":
    app.run(debug=True)
