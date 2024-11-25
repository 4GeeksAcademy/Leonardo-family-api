"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")

# Add default members to the family
jackson_family.add_member({"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]})
jackson_family.add_member({"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]})
jackson_family.add_member({"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint to get all members
@app.route('/members', methods=['GET'])
def all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Endpoint to get a single member by ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

# Endpoint to add a new member
@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Invalid data. Required fields: first_name, age, lucky_numbers"}), 400
    jackson_family.add_member(data)
    return jsonify(data), 200

# Endpoint to delete a member by ID
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.get_member(member_id):
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

# Run the server if this file is executed directly
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
