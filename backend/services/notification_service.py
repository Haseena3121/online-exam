"""
Notification service — MongoDB
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class NotificationService:

    @staticmethod
    def create_violation_notification(examiner_id, student_id, exam_id, violation_id,
                                      message, proof_type=None, proof_url=None):
        from database import mongo
        from models import make_notification
        try:
            doc = make_notification(
                examiner_id=examiner_id, student_id=student_id,
                exam_id=exam_id, message=message, severity_level='high'
            )
            doc['violation_id'] = violation_id
            doc['proof_type'] = proof_type or 'alert'
            doc['proof_url'] = proof_url
            mongo.db.examiner_notifications.insert_one(doc)
            logger.info(f"Notification created for examiner {examiner_id}")
            return doc
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None

    @staticmethod
    def mark_as_read(notification_id, user_id):
        from database import mongo
        from bson import ObjectId
        try:
            n = mongo.db.examiner_notifications.find_one({'_id': ObjectId(notification_id)})
            if not n or n['examiner_id'] != user_id:
                return False
            mongo.db.examiner_notifications.update_one(
                {'_id': ObjectId(notification_id)}, {'$set': {'is_read': True}}
            )
            return True
        except Exception as e:
            logger.error(f"Error marking notification: {e}")
            return False

    @staticmethod
    def get_unread_count(examiner_id):
        from database import mongo
        try:
            return mongo.db.examiner_notifications.count_documents(
                {'examiner_id': examiner_id, 'is_read': False}
            )
        except Exception as e:
            logger.error(f"Error getting unread count: {e}")
            return 0

    @staticmethod
    def get_recent_notifications(examiner_id, limit=10):
        from database import mongo
        from models import notification_to_dict
        try:
            notifications = list(mongo.db.examiner_notifications.find(
                {'examiner_id': examiner_id}
            ).sort('created_at', -1).limit(limit))
            return [notification_to_dict(n) for n in notifications]
        except Exception as e:
            logger.error(f"Error getting notifications: {e}")
            return []


notification_service = NotificationService()
