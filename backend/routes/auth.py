"""
Authentication Routes — MongoDB
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

from database import mongo
from models import make_user, check_user_password, user_to_dict

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Name, email and password required'}), 400

        if mongo.db.users.find_one({'email': data['email']}):
            return jsonify({'error': 'Email already registered'}), 409

        user_doc = make_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'student')
        )
        result = mongo.db.users.insert_one(user_doc)
        user_doc['_id'] = result.inserted_id

        return jsonify({
            'message': 'Registration successful',
            'user': user_to_dict(user_doc)
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400

        user = mongo.db.users.find_one({'email': data['email']})
        if not user or not check_user_password(user, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        access_token = create_access_token(
            identity=str(user['_id']),
            expires_delta=timedelta(hours=24)
        )

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user_to_dict(user)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        from bson import ObjectId
        user_id = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': user_to_dict(user)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
