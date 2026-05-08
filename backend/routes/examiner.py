"""
Examiner Routes — MongoDB
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
import logging

from database import mongo
from models import notification_to_dict, exam_to_dict

examiner_bp = Blueprint('examiner', __name__, url_prefix='/api/examiner')
logger = logging.getLogger(__name__)


@examiner_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        examiner_id = get_jwt_identity()
        notifications = list(mongo.db.examiner_notifications.find(
            {'examiner_id': examiner_id}
        ).sort('created_at', -1))
        unread = sum(1 for n in notifications if not n.get('is_read'))
        return jsonify({
            'notifications': [notification_to_dict(n) for n in notifications],
            'unread_count': unread
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@examiner_bp.route('/notifications/<notif_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notif_id):
    try:
        examiner_id = get_jwt_identity()
        n = mongo.db.examiner_notifications.find_one({'_id': ObjectId(notif_id)})
        if not n:
            return jsonify({'error': 'Notification not found'}), 404
        if n['examiner_id'] != examiner_id:
            return jsonify({'error': 'Not authorized'}), 403
        mongo.db.examiner_notifications.update_one({'_id': ObjectId(notif_id)}, {'$set': {'is_read': True}})
        return jsonify({'message': 'Marked as read'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@examiner_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    try:
        examiner_id = get_jwt_identity()
        exams = list(mongo.db.exams.find({'examiner_id': examiner_id}))
        exam_ids = [str(e['_id']) for e in exams]

        total_students = mongo.db.exam_enrollments.count_documents({'exam_id': {'$in': exam_ids}})
        total_results = mongo.db.exam_results.count_documents({'exam_id': {'$in': exam_ids}})

        recent_exams = []
        for e in exams:
            if mongo.db.exam_results.count_documents({'exam_id': str(e['_id'])}) > 0:
                recent_exams.append(exam_to_dict(e))

        return jsonify({
            'total_exams': len(exams),
            'published_exams': sum(1 for e in exams if e.get('is_published')),
            'total_students': total_students,
            'total_results': total_results,
            'recent_exams': recent_exams
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
