from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)

# Example Users API Routes
@api.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    # Logic to create a user
    return jsonify({'message': 'User created successfully', 'user': data}), 201

@api.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    # Logic to get a user by ID
    return jsonify({'id': id, 'name': 'Example User', 'balance': 100})

@api.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    # Logic to update a user
    return jsonify({'message': 'User updated successfully', 'updated_data': data})

@api.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    # Logic to delete a user
    return jsonify({'message': f'User {id} deleted successfully'})

# Example Skins API Routes
@api.route('/api/skins', methods=['POST'])
def create_skin():
    data = request.json
    # Logic to create a skin
    return jsonify({'message': 'Skin created successfully', 'skin': data}), 201

@api.route('/api/skins', methods=['GET'])
def get_skins():
    # Logic to retrieve all skins
    return jsonify([{'id': 1, 'name': 'Skin 1', 'price': 10}, {'id': 2, 'name': 'Skin 2', 'price': 20}])

@api.route('/api/skins/<int:id>', methods=['GET'])
def get_skin(id):
    # Logic to retrieve a skin by ID
    return jsonify({'id': id, 'name': 'Example Skin', 'price': 10})

@api.route('/api/skins/<int:id>', methods=['PUT'])
def update_skin(id):
    data = request.json
    # Logic to update a skin
    return jsonify({'message': 'Skin updated successfully', 'updated_data': data})

@api.route('/api/skins/<int:id>', methods=['DELETE'])
def delete_skin(id):
    # Logic to delete a skin
    return jsonify({'message': f'Skin {id} deleted successfully'})
