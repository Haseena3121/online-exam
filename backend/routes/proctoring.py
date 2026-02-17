"""
UPDATED Proctoring routes - COMPLETE with all frontend features
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import logging
import os
import uuid
from werkzeug.utils import secure_filename

from models import (
    ProctoringSession, ViolationLog, ExaminerNotification,
    SessionAnalytics, ExamEnrollment, ExamResult, StudentAnswer,
    ExamQuestion, Exam, User
)
from database import db
from services.email_service import email_service
from services.violation_detector import violation_detector

proctoring_bp = Blueprint('proctoring', __name__, url_prefix='/api/proctoring')
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'uploads/evidence'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_evidence_file(file):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        if file and allowed_file(file.filename):
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            return f'/uploads/evidence/{filename}'
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
    
    return None

@proctoring_bp.route('/violation', methods=['POST'])
@jwt_required()
def report_violation():
    """Report exam violation with evidence"""
    try:
        student_id = get_jwt_identity()
        
        session = ProctoringSession.query.filter_by(
            student_id=student_id,
            status='active'
        ).first()
        
        if not session:
            return jsonify({'error': 'No active session'}), 404
        
        data = request.form.to_dict() or {}
        
        violation_type = data.get('violation_type')
        severity = data.get('severity', 'medium')
        description = data.get('description', '')
        
        valid_violations = [
            'phone_detected', 'tab_switch', 'eye_gaze_suspicious',
            'multiple_persons', 'sound_detected', 'blur_exit_attempt',
            'face_not_visible', 'extreme_head_movement',
            'person_left_seat', 'other_person_detected',
            'suspicious_movement', 'low_light_detected'
        ]
        
        if violation_type not in valid_violations:
            return jsonify({'error': 'Invalid violation type'}), 400
        
        # Get trust score reduction
        severity_map = {'low': 5, 'medium': 10, 'high': 20}
        trust_score_reduction = severity_map.get(severity, 10)
        
        violation = ViolationLog(
            student_id=student_id,
            exam_id=session.exam_id,
            session_id=session.id,
            violation_type=violation_type,
            severity=severity,
            trust_score_reduction=trust_score_reduction,
            description=description,
            timestamp=datetime.utcnow(),
            is_notified=False
        )
        
        # Save evidence file
        if 'evidence' in request.files:
            file = request.files['evidence']
            file_path = save_evidence_file(file)
            
            if file_path:
                if file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.webm')):
                    violation.video_url = file_path
                else:
                    violation.screenshot_url = file_path
        
        # Update trust score
        session.current_trust_score -= trust_score_reduction
        if session.current_trust_score < 0:
            session.current_trust_score = 0
        
        db.session.add(violation)
        db.session.commit()
        
        # Create examiner notification
        exam = session.exam
        notification = ExaminerNotification(
            examiner_id=exam.examiner_id,
            student_id=student_id,
            exam_id=session.exam_id,
            violation_id=violation.id,
            message=f"⚠️ {violation_type.replace('_', ' ').title()} detected\nStudent: {student_id}\nTrust Score: {session.current_trust_score}%",
            proof_type='video' if violation.video_url else ('screenshot' if violation.screenshot_url else 'alert'),
            proof_url=violation.video_url or violation.screenshot_url,
            severity_level=severity,
            is_read=False
        )
        
        violation.is_notified = True
        db.session.add(notification)
        db.session.commit()
        
        logger.warning(f"Violation: {violation_type} for student {student_id}, Trust Score: {session.current_trust_score}%")
        
        response_data = {
            'message': 'Violation recorded',
            'violation_id': violation.id,
            'current_trust_score': session.current_trust_score,
            'warning': session.current_trust_score < 50
        }
        
        # Auto-submit if trust score < 50%
        if session.current_trust_score < 50:
            response_data['critical_message'] = 'Trust score below 50%. Exam will be auto-submitted!'
            return auto_submit_exam(session)
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@proctoring_bp.route('/session/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session_status(session_id):
    """Get current session status"""
    try:
        session = ProctoringSession.query.get(session_id)
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify({'session': session.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@proctoring_bp.route('/session/<int:session_id>/warning', methods=['POST'])
@jwt_required()
def send_warning(session_id):
    """Send warning to student"""
    try:
        session = ProctoringSession.query.get(session_id)
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        warning_level = "CRITICAL" if session.current_trust_score < 50 else "WARNING"
        
        return jsonify({
            'warning_level': warning_level,
            'message': f'{warning_level}: Follow exam rules or exam will auto-submit!',
            'current_trust_score': session.current_trust_score,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def auto_submit_exam(session):
    """Auto-submit exam when trust score < 50%"""
    try:
        session.status = 'ended'
        session.final_status = 'auto_submitted'
        session.end_time = datetime.utcnow()
        
        enrollment = session.enrollment_ref
        enrollment.enrollment_status = 'submitted'
        
        exam = session.exam
        violation_count = ViolationLog.query.filter_by(
            student_id=session.student_id,
            exam_id=session.exam_id
        ).count()
        
        result = ExamResult(
            enrollment_id=enrollment.id,
            student_id=session.student_id,
            exam_id=session.exam_id,
            obtained_marks=0,
            total_marks=exam.total_marks,
            percentage=0.0,
            status='auto_submitted',
            violation_count=violation_count,
            final_trust_score=session.current_trust_score,
            submitted_at=datetime.utcnow()
        )
        
        db.session.add(result)
        
        # Notify examiner
        notification = ExaminerNotification(
            examiner_id=exam.examiner_id,
            student_id=session.student_id,
            exam_id=session.exam_id,
            message=f"🔴 EXAM AUTO-SUBMITTED\nStudent: {session.student_id}\nReason: Trust Score Below 50%\nFinal Score: {session.current_trust_score}%",
            severity_level='high',
            is_read=False
        )
        db.session.add(notification)
        
        # Send email to student
        user = User.query.get(session.student_id)
        try:
            email_service.send_auto_submit_notification(
                user.email,
                exam.title,
                "Trust score fell below 50% due to exam rule violations"
            )
        except:
            pass
        
        db.session.commit()
        
        logger.critical(f"Exam auto-submitted for student {session.student_id}")
        
        return jsonify({
            'message': 'Exam auto-submitted',
            'reason': 'Trust score below 50%',
            'final_trust_score': session.current_trust_score,
            'final_status': 'auto_submitted'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error auto-submitting: {str(e)}")
        return jsonify({'error': str(e)}), 500

@proctoring_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_exam():
    """Submit exam with answers"""
    try:
        student_id = get_jwt_identity()
        data = request.get_json()
        
        session = ProctoringSession.query.filter_by(
            student_id=student_id,
            status='active'
        ).first()
        
        if not session:
            return jsonify({'error': 'No active session'}), 404
        
        answers = data.get('answers', [])
        
        enrollment = EnrollmentQuery.get(session.enrollment_id)
        
        total_marks = 0
        obtained_marks = 0
        correct_count = 0
        
        for answer_data in answers:
            question_id = answer_data.get('question_id')
            selected_answer = answer_data.get('selected_answer')
            
            question = ExamQuestion.query.get(question_id)
            if not question:
                continue
            
            total_marks += question.marks
            
            is_correct = selected_answer == question.correct_answer
            marks_obtained = question.marks if is_correct else 0
            
            if is_correct:
                correct_count += 1
            elif question.exam.negative_marking > 0:
                marks_obtained -= question.exam.negative_marking
                if marks_obtained < 0:
                    marks_obtained = 0
            
            obtained_marks += marks_obtained
            
            student_answer = StudentAnswer(
                enrollment_id=enrollment.id,
                question_id=question_id,
                selected_answer=selected_answer,
                is_correct=is_correct,
                marks_obtained=marks_obtained
            )
            
            db.session.add(student_answer)
        
        # Close session
        session.status = 'ended'
        session.final_status = 'completed'
        session.end_time = datetime.utcnow()
        
        enrollment.enrollment_status = 'submitted'
        
        # Calculate result
        exam = session.exam
        percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
        status = 'pass' if obtained_marks >= exam.passing_marks else 'fail'
        
        violation_count = ViolationLog.query.filter_by(
            student_id=student_id,
            exam_id=session.exam_id
        ).count()
        
        total_time_taken = int((session.end_time - session.start_time).total_seconds() / 60)
        
        result = ExamResult(
            enrollment_id=enrollment.id,
            student_id=student_id,
            exam_id=session.exam_id,
            obtained_marks=obtained_marks,
            total_marks=total_marks,
            percentage=percentage,
            status=status,
            violation_count=violation_count,
            final_trust_score=session.current_trust_score,
            total_time_taken=total_time_taken,
            submitted_at=datetime.utcnow()
        )
        
        db.session.add(result)
        db.session.commit()
        
        logger.info(f"Exam submitted: student {student_id}, score {obtained_marks}/{total_marks}, {percentage:.2f}%")
        
        # Send result email
        user = User.query.get(student_id)
        try:
            email_service.send_exam_result_email(
                user.email,
                exam.title,
                obtained_marks,
                total_marks,
                status
            )
        except:
            pass
        
        return jsonify({
            'message': 'Exam submitted successfully',
            'result': result.to_dict(),
            'summary': {
                'correct_answers': correct_count,
                'total_questions': len(answers),
                'percentage': round(percentage, 2),
                'status': status
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@proctoring_bp.route('/analytics/<int:session_id>', methods=['GET'])
@jwt_required()
def get_analytics(session_id):
    """Get session analytics"""
    try:
        analytics = SessionAnalytics.query.filter_by(session_id=session_id).first()
        
        if not analytics:
            return jsonify({'error': 'Analytics not found'}), 404
        
        return jsonify({'analytics': analytics.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@proctoring_bp.route('/update-analytics/<int:session_id>', methods=['POST'])
@jwt_required()
def update_analytics(session_id):
    """Update session analytics"""
    try:
        data = request.get_json()
        
        analytics = SessionAnalytics.query.filter_by(session_id=session_id).first()
        
        if not analytics:
            session = ProctoringSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            analytics = SessionAnalytics(
                session_id=session_id,
                student_id=session.student_id,
                exam_id=session.exam_id
            )
            db.session.add(analytics)
        
        analytics.eye_gaze_warnings += data.get('eye_gaze_warnings', 0)
        analytics.phone_detection_count += data.get('phone_detection_count', 0)
        analytics.tab_switch_count += data.get('tab_switch_count', 0)
        analytics.sound_detection_count += data.get('sound_detection_count', 0)
        analytics.multiple_persons_detected += data.get('multiple_persons_detected', 0)
        analytics.blur_exit_attempts += data.get('blur_exit_attempts', 0)
        analytics.face_not_visible_count += data.get('face_not_visible_count', 0)
        analytics.head_movement_warnings += data.get('head_movement_warnings', 0)
        
        analytics.total_violations = (
            analytics.eye_gaze_warnings + analytics.phone_detection_count +
            analytics.tab_switch_count + analytics.sound_detection_count +
            analytics.multiple_persons_detected + analytics.blur_exit_attempts +
            analytics.face_not_visible_count + analytics.head_movement_warnings
        )
        
        db.session.commit()
        
        return jsonify({
            'message': 'Analytics updated',
            'analytics': analytics.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500