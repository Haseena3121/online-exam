"""
Violations routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from models import ViolationLog, User, Exam
from database import db

violations_bp = Blueprint('violations', __name__, url_prefix='/api/violations')
logger = logging.getLogger(__name__)

@violations_bp.route('/history/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_violation_history(exam_id):
    """Get violation history"""
    try:
        student_id = get_jwt_identity()
        
        violations = ViolationLog.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).order_by(ViolationLog.timestamp.desc()).all()
        
        return jsonify({
            'violations': [v.to_dict() for v in violations],
            'total_violations': len(violations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@violations_bp.route('/by-exam/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_exam_violations(exam_id):
    """Get exam violations"""
    try:
        examiner_id = get_jwt_identity()
        
        user = User.query.get(examiner_id)
        if user.role != 'examiner':
            return jsonify({'error': 'Only examiners can view'}), 403
        
        violations = ViolationLog.query.filter_by(exam_id=exam_id).order_by(ViolationLog.timestamp.desc()).all()
        
        grouped = {}
        for v in violations:
            if v.violation_type not in grouped:
                grouped[v.violation_type] = 0
            grouped[v.violation_type] += 1
        
        return jsonify({
            'violations': [v.to_dict() for v in violations],
            'total_violations': len(violations),
            'grouped_by_type': grouped
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting exam violations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@violations_bp.route('/<int:violation_id>', methods=['GET'])
@jwt_required()
def get_violation_details(violation_id):
    """Get violation details"""
    try:
        violation = ViolationLog.query.get(violation_id)
        
        if not violation:
            return jsonify({'error': 'Violation not found'}), 404
        
        return jsonify({'violation': violation.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Error getting details: {str(e)}")
        return jsonify({'error': str(e)}), 500