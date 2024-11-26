"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")

# Añadir los mienbros principales de la familia
jackson_family.add_member({"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]})
jackson_family.add_member({"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]})
jackson_family.add_member({"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]})


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Obtener todos los miembros
@app.route('/members', methods=['GET'])
def all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Mostrar integrante por ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

# Agregar integrante
@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Datos no válidos. Campos obligatorios: nombre, edad, números de la suerte"}), 400
    jackson_family.add_member(data)
    return jsonify(data), 200

# Eliminar integrante
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.get_member(member_id):
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

# Run the server if this file is executed directly
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
