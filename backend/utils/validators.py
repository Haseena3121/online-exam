"""
Input validators
"""
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(char.isupper() for char in password):
        return False, "Must contain uppercase letter"
    if not any(char.isdigit() for char in password):
        return False, "Must contain digit"
    if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
        return False, "Must contain special character"
    return True, "Valid password"

def validate_exam_data(data):
    """Validate exam data"""
    errors = []
    
    if not data.get('title'):
        errors.append('Title is required')
    if not data.get('duration') or data['duration'] <= 0:
        errors.append('Valid duration is required')
    if not data.get('total_marks') or data['total_marks'] <= 0:
        errors.append('Valid total marks is required')
    if not data.get('passing_marks') or data['passing_marks'] < 0:
        errors.append('Valid passing marks is required')
    
    return len(errors) == 0, errors