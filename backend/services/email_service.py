"""
Email notification service
"""
from flask_mail import Mail, Message
from flask import current_app
import logging

logger = logging.getLogger(__name__)

mail = Mail()

class EmailService:
    """Email service for notifications"""
    
    @staticmethod
    def send_exam_enrollment_email(user_email, exam_title, exam_id):
        """Send exam enrollment confirmation"""
        try:
            subject = f"✓ Successfully Enrolled: {exam_title}"
            html = f"""
            <html>
                <body>
                    <h2>Exam Enrollment Confirmation</h2>
                    <p>You have successfully enrolled in:</p>
                    <h3>{exam_title}</h3>
                    <p>Exam ID: {exam_id}</p>
                    <p>Please review the exam rules and accept the terms before starting the exam.</p>
                    <a href="http://localhost:3000/exam/{exam_id}/acceptance">Accept Terms & Start Exam</a>
                </body>
            </html>
            """
            
            msg = Message(subject=subject, recipients=[user_email], html=html)
            mail.send(msg)
            logger.info(f"Enrollment email sent to {user_email}")
            
        except Exception as e:
            logger.error(f"Error sending enrollment email: {str(e)}")

    @staticmethod
    def send_exam_result_email(user_email, exam_title, score, total, status):
        """Send exam result email"""
        try:
            percentage = (score / total * 100) if total > 0 else 0
            subject = f"📊 Your Exam Result: {exam_title}"
            
            result_status = "✓ PASSED" if status == 'pass' else "✗ FAILED"
            
            html = f"""
            <html>
                <body>
                    <h2>Exam Result</h2>
                    <p>Your exam result for <strong>{exam_title}</strong>:</p>
                    <h3>{result_status}</h3>
                    <p>Your Score: <strong>{score}/{total}</strong></p>
                    <p>Percentage: <strong>{percentage:.2f}%</strong></p>
                    <p>View detailed results at your dashboard.</p>
                </body>
            </html>
            """
            
            msg = Message(subject=subject, recipients=[user_email], html=html)
            mail.send(msg)
            logger.info(f"Result email sent to {user_email}")
            
        except Exception as e:
            logger.error(f"Error sending result email: {str(e)}")

    @staticmethod
    def send_violation_alert_email(examiner_email, student_email, exam_title, violation_type):
        """Send violation alert to examiner"""
        try:
            subject = f"⚠️ Exam Violation Alert: {exam_title}"
            html = f"""
            <html>
                <body>
                    <h2>Exam Violation Detected</h2>
                    <p>A violation has been detected in your exam:</p>
                    <p><strong>Exam:</strong> {exam_title}</p>
                    <p><strong>Student:</strong> {student_email}</p>
                    <p><strong>Violation Type:</strong> {violation_type}</p>
                    <p>Please check your dashboard for more details and proof.</p>
                </body>
            </html>
            """
            
            msg = Message(subject=subject, recipients=[examiner_email], html=html)
            mail.send(msg)
            logger.info(f"Violation alert sent to {examiner_email}")
            
        except Exception as e:
            logger.error(f"Error sending violation alert: {str(e)}")

    @staticmethod
    def send_auto_submit_notification(user_email, exam_title, reason):
        """Send auto-submit notification"""
        try:
            subject = f"⊙ Exam Auto-Submitted: {exam_title}"
            html = f"""
            <html>
                <body>
                    <h2>Exam Auto-Submitted</h2>
                    <p>Your exam has been automatically submitted.</p>
                    <p><strong>Exam:</strong> {exam_title}</p>
                    <p><strong>Reason:</strong> {reason}</p>
                    <p>Your exam will be graded and results will be available soon.</p>
                </body>
            </html>
            """
            
            msg = Message(subject=subject, recipients=[user_email], html=html)
            mail.send(msg)
            logger.info(f"Auto-submit notification sent to {user_email}")
            
        except Exception as e:
            logger.error(f"Error sending auto-submit notification: {str(e)}")

# Initialize email service
email_service = EmailService()