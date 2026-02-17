"""
Examiner routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from models import User, ExaminerNotification, Exam, ExamResult
from database import db

examiner_bp = Blueprint('examiner', __name__, url_prefix='/api/examiner')
logger = logging.getLogger(__name__)

@examiner_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get examiner notifications"""
    try:
        examiner_id = get_jwt_identity()
        
        notifications = ExaminerNotification.query.filter_by(
            examiner_id=examiner_id
        ).order_by(ExaminerNotification.created_at.desc()).all()
        
        unread = len([n for n in notifications if not n.is_read])
        
        return jsonify({
            'notifications': [n.to_dict() for n in notifications],
            'unread_count': unread
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting notifications: {str(e)}")
        return jsonify({'error': str(e)}), 500

@examiner_bp.route('/notifications/<int:notif_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notif_id):
    """Mark notification as read"""
    try:
        examiner_id = get_jwt_identity()
        
        notification = ExaminerNotification.query.get(notif_id)
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        if notification.examiner_id != examiner_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'message': 'Marked as read'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking notification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@examiner_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Get examiner dashboard"""
    try:
        examiner_id = get_jwt_identity()
        
        exams = Exam.query.filter_by(examiner_id=examiner_id).all()
        
        dashboard_data = {
            'total_exams': len(exams),
            'published_exams': len([e for e in exams if e.is_published]),
            'total_students': 0,
            'total_results': 0,
            'recent_exams': []
        }
        
        for exam in exams:
            dashboard_data['total_students'] += len(exam.enrollments)
            dashboard_data['total_results'] += len(exam.results)
            if len(exam.results) > 0:
                dashboard_data['recent_exams'].append(exam.to_dict())
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        logger.error(f"Error getting dashboard: {str(e)}")
        return jsonify({'error': str(e)}), 500