"""
Celery configuration and tasks
"""
from celery import Celery
from flask import Flask
import os
from datetime import datetime, timedelta

# Create Celery app
celery = Celery(__name__)

def make_celery(app):
    """Create Celery instance with Flask app context"""
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# Celery configuration
celery.conf.update(
    broker_url=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    beat_schedule={
        'clean-old-uploads': {
            'task': 'celery_app.clean_old_uploads',
            'schedule': timedelta(hours=24),
        },
        'generate-reports': {
            'task': 'celery_app.generate_exam_reports',
            'schedule': timedelta(hours=6),
        },
        'send-pending-notifications': {
            'task': 'celery_app.send_pending_notifications',
            'schedule': timedelta(minutes=5),
        },
    }
)

@celery.task(name='celery_app.send_email')
def send_email(recipient, subject, html_body):
    """Send email asynchronously"""
    try:
        from flask_mail import Mail, Message
        from app import create_app
        
        app = create_app()
        mail = Mail(app)
        
        msg = Message(
            subject=subject,
            recipients=[recipient],
            html=html_body
        )
        mail.send(msg)
        return {'status': 'Email sent successfully'}
    except Exception as e:
        return {'status': 'Email failed', 'error': str(e)}

@celery.task(name='celery_app.process_violation')
def process_violation(violation_id):
    """Process and analyze violation"""
    try:
        from models import ViolationLog
        from app import create_app
        
        app = create_app()
        with app.app_context():
            violation = ViolationLog.query.get(violation_id)
            if violation:
                # Analyze violation
                # Update analytics
                # Send notifications
                pass
        
        return {'status': 'Violation processed'}
    except Exception as e:
        return {'status': 'Processing failed', 'error': str(e)}

@celery.task(name='celery_app.generate_exam_reports')
def generate_exam_reports():
    """Generate exam reports periodically"""
    try:
        from models import Exam
        from app import create_app
        from services.analytics_service import analytics_service
        
        app = create_app()
        with app.app_context():
            exams = Exam.query.filter_by(is_active=True).all()
            
            for exam in exams:
                report = analytics_service.generate_report(exam.id)
                # Save report
                # Send to examiner
                pass
        
        return {'status': 'Reports generated'}
    except Exception as e:
        return {'status': 'Report generation failed', 'error': str(e)}

@celery.task(name='celery_app.clean_old_uploads')
def clean_old_uploads():
    """Clean old uploaded files"""
    try:
        import os
        import time
        
        upload_dir = 'uploads/evidence'
        cutoff_time = time.time() - (30 * 24 * 60 * 60)  # 30 days
        
        for filename in os.listdir(upload_dir):
            filepath = os.path.join(upload_dir, filename)
            if os.path.isfile(filepath):
                if os.stat(filepath).st_mtime < cutoff_time:
                    os.remove(filepath)
        
        return {'status': 'Old files cleaned'}
    except Exception as e:
        return {'status': 'Cleanup failed', 'error': str(e)}

@celery.task(name='celery_app.send_pending_notifications')
def send_pending_notifications():
    """Send pending notifications to examiners"""
    try:
        from models import ExaminerNotification
        from app import create_app
        
        app = create_app()
        with app.app_context():
            notifications = ExaminerNotification.query.filter_by(
                is_read=False
            ).all()
            
            # Send notifications via WebSocket or email
            pass
        
        return {'status': 'Notifications sent'}
    except Exception as e:
        return {'status': 'Notification sending failed', 'error': str(e)}

@celery.task(name='celery_app.auto_check_exam_time')
def auto_check_exam_time():
    """Auto-end exams when time is up"""
    try:
        from models import ProctoringSession, ExamResult, ExamEnrollment
        from app import create_app
        from datetime import datetime
        
        app = create_app()
        with app.app_context():
            active_sessions = ProctoringSession.query.filter_by(
                status='active'
            ).all()
            
            for session in active_sessions:
                exam = session.exam
                time_elapsed = (datetime.utcnow() - session.start_time).total_seconds() / 60
                
                if time_elapsed >= exam.duration:
                    # Auto-submit exam
                    session.status = 'ended'
                    session.final_status = 'completed'
                    session.end_time = datetime.utcnow()
                    # Create result
                    # Notify student
        
        return {'status': 'Exams checked'}
    except Exception as e:
        return {'status': 'Exam check failed', 'error': str(e)}