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

proctoring_bp = Blueprint('proctoring', __name__)
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
        student_id = int(get_jwt_identity())
        
        session = ProctoringSession.query.filter_by(
            student_id=student_id,
            status='active'
        ).first()
        
        if not session:
            return jsonify({'error': 'No active session'}), 404
        
        # Get form data
        violation_type = request.form.get('violation_type')
        severity = request.form.get('severity', 'medium')
        
        # Handle evidence file upload
        evidence_path = None
        if 'evidence' in request.files:
            evidence_file = request.files['evidence']
            if evidence_file and allowed_file(evidence_file.filename):
                evidence_path = save_evidence_file(evidence_file)
        
        # Get trust score reduction
        severity_map = {'low': 5, 'medium': 10, 'high': 20}
        trust_score_reduction = severity_map.get(severity, 10)
        
        violation = ViolationLog(
            student_id=student_id,
            exam_id=session.exam_id,
            session_id=session.id,
            violation_type=violation_type,
            trust_score_reduction=trust_score_reduction,
            created_at=datetime.utcnow()
        )
        
        # Add evidence path if available
        if evidence_path:
            # Store relative path
            violation.evidence_path = evidence_path
        
        # Update trust score
        session.current_trust_score -= trust_score_reduction
        if session.current_trust_score < 0:
            session.current_trust_score = 0
        
        db.session.add(violation)
        db.session.commit()
        
        logger.warning(f"Violation: {violation_type} for student {student_id}, Trust Score: {session.current_trust_score}%")
        
        response_data = {
            'message': 'Violation recorded',
            'violation_id': violation.id,
            'current_trust_score': session.current_trust_score,
            'warning': session.current_trust_score < 80,
            'evidence_saved': evidence_path is not None
        }
        
        # Auto-submit if trust score < 50%
        if session.current_trust_score < 50:
            response_data['critical_message'] = 'Trust score below 50%. Exam will be auto-submitted!'
            session.status = 'ended'
            db.session.commit()
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error reporting violation: {str(e)}")
        import traceback
        traceback.print_exc()
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
        student_id = int(get_jwt_identity())
        data = request.get_json()
        
        session = ProctoringSession.query.filter_by(
            student_id=student_id,
            status='active'
        ).first()
        
        if not session:
            return jsonify({'error': 'No active session found'}), 404
        
        answers = data.get('answers', [])
        
        # Get exam
        exam = Exam.query.get(session.exam_id)
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
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
            elif exam.negative_marking > 0:
                marks_obtained -= exam.negative_marking
                if marks_obtained < 0:
                    marks_obtained = 0
            
            obtained_marks += marks_obtained
            
            student_answer = StudentAnswer(
                student_id=student_id,
                question_id=question_id,
                selected_answer=selected_answer,
                marks_awarded=marks_obtained
            )
            
            db.session.add(student_answer)
        
        # Close session
        session.status = 'ended'
        session.end_time = datetime.utcnow()
        
        # Calculate result
        percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
        
        violation_count = ViolationLog.query.filter_by(
            student_id=student_id,
            exam_id=session.exam_id
        ).count()
        
        result = ExamResult(
            student_id=student_id,
            exam_id=session.exam_id,
            obtained_marks=obtained_marks,
            total_marks=total_marks,
            percentage=percentage
        )
        
        db.session.add(result)
        db.session.commit()
        
        logger.info(f"Exam submitted: student {student_id}, score {obtained_marks}/{total_marks}, {percentage:.2f}%")
        
        return jsonify({
            'message': 'Exam submitted successfully',
            'result': {
                'obtained_marks': obtained_marks,
                'total_marks': total_marks,
                'percentage': round(percentage, 2),
                'correct_answers': correct_count,
                'total_questions': len(answers),
                'violation_count': violation_count,
                'final_trust_score': session.current_trust_score
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error submitting exam: {str(e)}")
        import traceback
        traceback.print_exc()
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


@proctoring_bp.route('/monitor/active-sessions', methods=['GET'])
@jwt_required()
def get_active_sessions():
    """Get all active proctoring sessions for examiner monitoring"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or user.role != 'examiner':
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get all active sessions for this examiner's exams
        active_sessions = db.session.query(
            ProctoringSession, User, Exam
        ).join(
            User, ProctoringSession.student_id == User.id
        ).join(
            Exam, ProctoringSession.exam_id == Exam.id
        ).filter(
            Exam.examiner_id == user_id,
            ProctoringSession.status == 'active'
        ).all()
        
        sessions_data = []
        for session, student, exam in active_sessions:
            # Get recent violations for this session
            recent_violations = ViolationLog.query.filter_by(
                session_id=session.id
            ).order_by(ViolationLog.created_at.desc()).limit(5).all()
            
            sessions_data.append({
                'session_id': session.id,
                'student': {
                    'id': student.id,
                    'name': student.name,
                    'email': student.email
                },
                'exam': {
                    'id': exam.id,
                    'title': exam.title,
                    'duration': exam.duration
                },
                'trust_score': session.current_trust_score,
                'start_time': session.start_time.isoformat() if session.start_time else None,
                'camera_active': session.camera_active,
                'mic_active': session.mic_active,
                'violations': [{
                    'id': v.id,
                    'type': v.violation_type,
                    'reduction': v.trust_score_reduction,
                    'time': v.created_at.isoformat() if v.created_at else None
                } for v in recent_violations]
            })
        
        return jsonify({
            'active_sessions': sessions_data,
            'count': len(sessions_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting active sessions: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@proctoring_bp.route('/monitor/session/<int:session_id>/details', methods=['GET'])
@jwt_required()
def get_session_details(session_id):
    """Get detailed information about a specific session"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or user.role != 'examiner':
            return jsonify({'error': 'Unauthorized'}), 403
        
        session = ProctoringSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Verify this session belongs to examiner's exam
        exam = Exam.query.get(session.exam_id)
        if exam.examiner_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        student = User.query.get(session.student_id)
        
        # Get all violations
        violations = ViolationLog.query.filter_by(
            session_id=session_id
        ).order_by(ViolationLog.created_at.desc()).all()
        
        return jsonify({
            'session': {
                'id': session.id,
                'status': session.status,
                'trust_score': session.current_trust_score,
                'start_time': session.start_time.isoformat() if session.start_time else None,
                'end_time': session.end_time.isoformat() if session.end_time else None,
                'camera_active': session.camera_active,
                'mic_active': session.mic_active
            },
            'student': {
                'id': student.id,
                'name': student.name,
                'email': student.email
            },
            'exam': {
                'id': exam.id,
                'title': exam.title,
                'duration': exam.duration,
                'total_marks': exam.total_marks
            },
            'violations': [{
                'id': v.id,
                'type': v.violation_type,
                'reduction': v.trust_score_reduction,
                'time': v.created_at.isoformat() if v.created_at else None
            } for v in violations],
            'violation_count': len(violations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting session details: {str(e)}")
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/evidence/<path:filename>', methods=['GET'])
@jwt_required()
def serve_evidence(filename):
    """Serve evidence files (screenshots)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        # Only examiners can view evidence
        if not user or user.role != 'examiner':
            return jsonify({'error': 'Unauthorized'}), 403
        
        evidence_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(evidence_path):
            return jsonify({'error': 'Evidence not found'}), 404
        
        from flask import send_file
        return send_file(evidence_path, mimetype='image/jpeg')
        
    except Exception as e:
        logger.error(f"Error serving evidence: {str(e)}")
        return jsonify({'error': str(e)}), 500
