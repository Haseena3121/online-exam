"""
UPDATED Exam routes - COMPLETE with all endpoints from frontend
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import logging

from models import (
    Exam, ExamQuestion, ExamEnrollment, AcceptanceForm,
    ProctoringSession, User, ExamResult
)
from database import db
from utils.validators import validate_exam_data

exam_bp = Blueprint('exam', __name__, url_prefix='/api/exams')
logger = logging.getLogger(__name__)

@exam_bp.route('/', methods=['POST'])
@jwt_required()
def create_exam():
    """Create new exam - for examiners only"""
    try:
        examiner_id = get_jwt_identity()
        user = User.query.get(examiner_id)
        
        if user.role != 'examiner':
            return jsonify({'error': 'Only examiners can create exams'}), 403
        
        data = request.get_json()
        
        is_valid, errors = validate_exam_data(data)
        if not is_valid:
            return jsonify({'error': ', '.join(errors)}), 400
        
        exam = Exam(
            title=data['title'],
            description=data.get('description', ''),
            instructions=data.get('instructions', ''),
            examiner_id=examiner_id,
            duration=data['duration'],
            total_marks=data['total_marks'],
            passing_marks=data['passing_marks'],
            negative_marking=data.get('negative_marking', 0),
            is_published=data.get('is_published', False)
        )
        
        db.session.add(exam)
        db.session.commit()
        
        logger.info(f"Exam created: {exam.id}")
        
        return jsonify({
            'message': 'Exam created',
            'exam': exam.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/<int:exam_id>/questions', methods=['POST'])
@jwt_required()
def add_question(exam_id):
    """Add question to exam"""
    try:
        examiner_id = get_jwt_identity()
        data = request.get_json()
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.examiner_id != examiner_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        if not data.get('question_text') or not data.get('marks'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        question = ExamQuestion(
            exam_id=exam_id,
            question_text=data['question_text'],
            option_a=data.get('option_a'),
            option_b=data.get('option_b'),
            option_c=data.get('option_c'),
            option_d=data.get('option_d'),
            correct_answer=data.get('correct_answer'),
            marks=data['marks'],
            question_type=data.get('question_type', 'mcq'),
            explanation=data.get('explanation'),
            order=data.get('order')
        )
        
        db.session.add(question)
        db.session.commit()
        
        return jsonify({
            'message': 'Question added',
            'question': question.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/', methods=['GET'])
@jwt_required()
def list_exams():
    """List all published exams"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        exams_query = Exam.query.filter_by(
            is_published=True,
            is_active=True
        ).order_by(Exam.created_at.desc())
        
        paginated = exams_query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'exams': [e.to_dict() for e in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_exam(exam_id):
    """Get exam details with questions"""
    try:
        exam = Exam.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        exam_data = exam.to_dict()
        exam_data['questions'] = [q.to_dict() for q in exam.questions]
        
        return jsonify({'exam': exam_data}), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/my-exams', methods=['GET'])
@jwt_required()
def get_my_exams():
    """Get exams created by current examiner"""
    try:
        examiner_id = get_jwt_identity()
        user = User.query.get(examiner_id)
        
        if user.role != 'examiner':
            return jsonify({'error': 'Only examiners can view'}), 403
        
        exams = Exam.query.filter_by(examiner_id=examiner_id).all()
        
        return jsonify({
            'exams': [e.to_dict() for e in exams],
            'total': len(exams)
        }), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/<int:exam_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_in_exam(exam_id):
    """Enroll student in exam"""
    try:
        student_id = get_jwt_identity()
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if not exam.is_published:
            return jsonify({'error': 'Exam not available'}), 403
        
        existing = ExamEnrollment.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Already enrolled'}), 409
        
        enrollment = ExamEnrollment(
            student_id=student_id,
            exam_id=exam_id,
            enrollment_status='enrolled'
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        logger.info(f"Student {student_id} enrolled in exam {exam_id}")
        
        return jsonify({
            'message': 'Enrolled successfully',
            'enrollment_id': enrollment.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/<int:exam_id>/acceptance-form', methods=['POST'])
@jwt_required()
def submit_acceptance_form(exam_id):
    """Submit exam acceptance form"""
    try:
        student_id = get_jwt_identity()
        data = request.get_json()
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        enrollment = ExamEnrollment.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not enrollment:
            return jsonify({'error': 'Not enrolled'}), 404
        
        # Check all required acceptances
        required_acceptances = [
            'accepted', 'rules_accepted', 'honor_code_accepted',
            'privacy_accepted', 'technical_requirements_met'
        ]
        
        if not all(data.get(field) for field in required_acceptances):
            return jsonify({'error': 'Must accept all terms'}), 400
        
        acceptance = AcceptanceForm.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not acceptance:
            acceptance = AcceptanceForm(
                student_id=student_id,
                exam_id=exam_id,
                enrollment_id=enrollment.id
            )
        
        for field in required_acceptances:
            setattr(acceptance, field, data.get(field, False))
        
        acceptance.trust_score = 100
        acceptance.acceptance_timestamp = datetime.utcnow()
        
        db.session.add(acceptance)
        db.session.commit()
        
        logger.info(f"Student {student_id} accepted exam terms")
        
        return jsonify({
            'message': 'Terms accepted',
            'acceptance_form': acceptance.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/<int:exam_id>/start', methods=['POST'])
@jwt_required()
def start_exam(exam_id):
    """Start exam session"""
    try:
        student_id = get_jwt_identity()
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        enrollment = ExamEnrollment.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not enrollment:
            return jsonify({'error': 'Not enrolled'}), 404
        
        acceptance = AcceptanceForm.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not acceptance or not acceptance.accepted:
            return jsonify({'error': 'Accept terms first'}), 403
        
        if acceptance.trust_score < 50:
            return jsonify({'error': 'Trust score below threshold'}), 403
        
        # Check for active session
        active_session = ProctoringSession.query.filter_by(
            student_id=student_id,
            exam_id=exam_id,
            status='active'
        ).first()
        
        if active_session:
            return jsonify({
                'message': 'Exam in progress',
                'session_id': active_session.id
            }), 200
        
        session = ProctoringSession(
            student_id=student_id,
            exam_id=exam_id,
            enrollment_id=enrollment.id,
            current_trust_score=acceptance.trust_score,
            status='active',
            camera_active=True,
            mic_active=True,
            screen_locked=True
        )
        
        enrollment.enrollment_status = 'started'
        
        db.session.add(session)
        db.session.commit()
        
        logger.info(f"Exam started: student {student_id}, session {session.id}")
        
        return jsonify({
            'message': 'Exam started',
            'session_id': session.id,
            'duration_minutes': exam.duration,
            'total_marks': exam.total_marks,
            'exam_title': exam.title
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/<int:exam_id>/questions', methods=['GET'])
@jwt_required()
def get_exam_questions(exam_id):
    """Get all questions for exam"""
    try:
        exam = Exam.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        questions = ExamQuestion.query.filter_by(exam_id=exam_id).order_by(
            ExamQuestion.order
        ).all()
        
        return jsonify({
            'questions': [q.to_dict() for q in questions],
            'total': len(questions)
        }), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/<int:exam_id>/publish', methods=['POST'])
@jwt_required()
def publish_exam(exam_id):
    """Publish exam (examiner only)"""
    try:
        examiner_id = get_jwt_identity()
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.examiner_id != examiner_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        if len(exam.questions) == 0:
            return jsonify({'error': 'Add questions before publishing'}), 400
        
        exam.is_published = True
        db.session.commit()
        
        logger.info(f"Exam {exam_id} published")
        
        return jsonify({
            'message': 'Exam published',
            'exam': exam.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@exam_bp.route('/<int:exam_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_exam(exam_id):
    """Delete exam (examiner only)"""
    try:
        examiner_id = get_jwt_identity()
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.examiner_id != examiner_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        # Check if exam has submissions
        if len(exam.results) > 0:
            return jsonify({'error': 'Cannot delete exam with submissions'}), 400
        
        db.session.delete(exam)
        db.session.commit()
        
        logger.info(f"Exam {exam_id} deleted")
        
        return jsonify({'message': 'Exam deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500