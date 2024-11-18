from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)

# Временные хранилища данных
users = []
skins = []

# Пользователи
@api.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data or 'balance' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'balance': data['balance']
    }
    users.append(new_user)
    return jsonify({'message': 'User created successfully', 'user': new_user}), 201

@api.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@api.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if 'name' in data:
        user['name'] = data['name']
    if 'balance' in data:
        user['balance'] = data['balance']
    return jsonify({'message': 'User updated successfully', 'user': user})

@api.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    global users
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    users = [u for u in users if u['id'] != id]
    return jsonify({'message': f'User {id} deleted successfully'})

# Скины
@api.route('/api/skins', methods=['POST'])
def create_skin():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_skin = {
        'id': len(skins) + 1,
        'name': data['name'],
        'price': data['price']
    }
    skins.append(new_skin)
    return jsonify({'message': 'Skin created successfully', 'skin': new_skin}), 201

@api.route('/api/skins', methods=['GET'])
def get_skins():
    return jsonify(skins)

@api.route('/api/skins/<int:id>', methods=['GET'])
def get_skin(id):
    skin = next((s for s in skins if s['id'] == id), None)
    if not skin:
        return jsonify({'error': 'Skin not found'}), 404
    return jsonify(skin)

@api.route('/api/skins/<int:id>', methods=['PUT'])
def update_skin(id):
    data = request.json
    skin = next((s for s in skins if s['id'] == id), None)
    if not skin:
        return jsonify({'error': 'Skin not found'}), 404

    if 'name' in data:
        skin['name'] = data['name']
    if 'price' in data:
        skin['price'] = data['price']
    return jsonify({'message': 'Skin updated successfully', 'skin': skin})

@api.route('/api/skins/<int:id>', methods=['DELETE'])
def delete_skin(id):
    global skins
    skin = next((s for s in skins if s['id'] == id), None)
    if not skin:
        return jsonify({'error': 'Skin not found'}), 404

    skins = [s for s in skins if s['id'] != id]
    return jsonify({'message': f'Skin {id} deleted successfully'})
