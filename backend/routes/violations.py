"""
Violations Routes — MongoDB
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
import logging

from database import mongo
from models import violation_to_dict

violations_bp = Blueprint('violations', __name__, url_prefix='/api/violations')
logger = logging.getLogger(__name__)


@violations_bp.route('/history/<exam_id>', methods=['GET'])
@jwt_required()
def get_violation_history(exam_id):
    try:
        student_id = get_jwt_identity()
        violations = list(mongo.db.violations.find(
            {'student_id': student_id, 'exam_id': exam_id}
        ).sort('created_at', -1))
        return jsonify({
            'violations': [violation_to_dict(v) for v in violations],
            'total_violations': len(violations)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@violations_bp.route('/by-exam/<exam_id>', methods=['GET'])
@jwt_required()
def get_exam_violations(exam_id):
    try:
        examiner_id = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': ObjectId(examiner_id)})
        if not user or user['role'] != 'examiner':
            return jsonify({'error': 'Only examiners can view'}), 403

        violations = list(mongo.db.violations.find({'exam_id': exam_id}).sort('created_at', -1))
        grouped = {}
        for v in violations:
            vt = v.get('violation_type', 'unknown')
            grouped[vt] = grouped.get(vt, 0) + 1

        return jsonify({
            'violations': [violation_to_dict(v) for v in violations],
            'total_violations': len(violations),
            'grouped_by_type': grouped
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@violations_bp.route('/<violation_id>', methods=['GET'])
@jwt_required()
def get_violation_details(violation_id):
    try:
        v = mongo.db.violations.find_one({'_id': ObjectId(violation_id)})
        if not v:
            return jsonify({'error': 'Violation not found'}), 404
        return jsonify({'violation': violation_to_dict(v)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
