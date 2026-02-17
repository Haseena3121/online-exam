"""
Notification service for real-time updates
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NotificationService:
    """Handle notifications"""
    
    @staticmethod
    def create_violation_notification(examiner_id, student_id, exam_id, violation_id, message, proof_type=None, proof_url=None):
        """Create violation notification"""
        from models import ExaminerNotification, db
        
        try:
            notification = ExaminerNotification(
                examiner_id=examiner_id,
                student_id=student_id,
                exam_id=exam_id,
                violation_id=violation_id,
                message=message,
                proof_type=proof_type or 'alert',
                proof_url=proof_url,
                is_read=False,
                severity_level='high',
                created_at=datetime.utcnow()
            )
            
            db.session.add(notification)
            db.session.commit()
            
            logger.info(f"Violation notification created for examiner {examiner_id}")
            return notification
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating notification: {str(e)}")
            return None
    
    @staticmethod
    def mark_as_read(notification_id, user_id):
        """Mark notification as read"""
        from models import ExaminerNotification, db
        
        try:
            notification = ExaminerNotification.query.get(notification_id)
            
            if not notification or notification.examiner_id != user_id:
                return False
            
            notification.is_read = True
            db.session.commit()
            
            logger.info(f"Notification {notification_id} marked as read")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error marking notification: {str(e)}")
            return False
    
    @staticmethod
    def get_unread_count(examiner_id):
        """Get unread notification count"""
        from models import ExaminerNotification
        
        try:
            count = ExaminerNotification.query.filter_by(
                examiner_id=examiner_id,
                is_read=False
            ).count()
            
            return count
            
        except Exception as e:
            logger.error(f"Error getting unread count: {str(e)}")
            return 0
    
    @staticmethod
    def get_recent_notifications(examiner_id, limit=10):
        """Get recent notifications"""
        from models import ExaminerNotification
        
        try:
            notifications = ExaminerNotification.query.filter_by(
                examiner_id=examiner_id
            ).order_by(
                ExaminerNotification.created_at.desc()
            ).limit(limit).all()
            
            return [n.to_dict() for n in notifications]
            
        except Exception as e:
            logger.error(f"Error getting notifications: {str(e)}")
            return []

notification_service = NotificationService()