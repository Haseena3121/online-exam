"""
Custom decorators
"""
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify

def examiner_required(fn):
    """Require examiner role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        from models import User
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'examiner':
            return jsonify({'error': 'Examiner role required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def student_required(fn):
    """Require student role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        from models import User
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'student':
            return jsonify({'error': 'Student role required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper