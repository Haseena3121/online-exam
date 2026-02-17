"""
Results routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from models import ExamResult, StudentAnswer, ExamQuestion, User, Exam
from database import db

results_bp = Blueprint('results', __name__, url_prefix='/api/results')
logger = logging.getLogger(__name__)

@results_bp.route('/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_exam_result(exam_id):
    """Get exam result"""
    try:
        student_id = get_jwt_identity()
        
        result = ExamResult.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not result:
            return jsonify({'error': 'Result not found'}), 404
        
        return jsonify({'result': result.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Error getting result: {str(e)}")
        return jsonify({'error': str(e)}), 500

@results_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_results():
    """Get all results"""
    try:
        student_id = get_jwt_identity()
        
        results = ExamResult.query.filter_by(student_id=student_id).order_by(ExamResult.submitted_at.desc()).all()
        
        passed = len([r for r in results if r.status == 'pass'])
        failed = len([r for r in results if r.status == 'fail'])
        
        return jsonify({
            'results': [r.to_dict() for r in results],
            'total_exams': len(results),
            'passed': passed,
            'failed': failed,
            'auto_submitted': len([r for r in results if r.status == 'auto_submitted'])
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting all results: {str(e)}")
        return jsonify({'error': str(e)}), 500

@results_bp.route('/detailed/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_detailed_result(exam_id):
    """Get detailed result"""
    try:
        student_id = get_jwt_identity()
        
        result = ExamResult.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()
        
        if not result:
            return jsonify({'error': 'Result not found'}), 404
        
        student_answers = StudentAnswer.query.filter_by(
            enrollment_id=result.enrollment_id
        ).all()
        
        answers_detail = []
        for answer in student_answers:
            question = answer.question
            answers_detail.append({
                'question_id': question.id,
                'question_text': question.question_text,
                'selected_answer': answer.selected_answer,
                'correct_answer': question.correct_answer,
                'is_correct': answer.is_correct,
                'marks_obtained': answer.marks_obtained,
                'marks_total': question.marks,
                'explanation': question.explanation
            })
        
        result_data = result.to_dict()
        result_data['answers'] = answers_detail
        
        return jsonify({'result': result_data}), 200
        
    except Exception as e:
        logger.error(f"Error getting detailed result: {str(e)}")
        return jsonify({'error': str(e)}), 500

@results_bp.route('/exam/<int:exam_id>/all-students', methods=['GET'])
@jwt_required()
def get_exam_all_results(exam_id):
    """Get all results for exam"""
    try:
        examiner_id = get_jwt_identity()
        
        user = User.query.get(examiner_id)
        if user.role != 'examiner':
            return jsonify({'error': 'Only examiners can view'}), 403
        
        exam = Exam.query.get(exam_id)
        if exam.examiner_id != examiner_id:
            return jsonify({'error': 'Not authorized'}), 403
        
        results = ExamResult.query.filter_by(exam_id=exam_id).order_by(ExamResult.percentage.desc()).all()
        
        if not results:
            return jsonify({'results': [], 'statistics': {}}), 200
        
        stats = {
            'total_students': len(results),
            'passed': len([r for r in results if r.status == 'pass']),
            'failed': len([r for r in results if r.status == 'fail']),
            'auto_submitted': len([r for r in results if r.status == 'auto_submitted']),
            'average_score': sum([r.percentage for r in results if r.percentage]) / len(results),
            'highest_score': max([r.percentage for r in results if r.percentage]),
            'lowest_score': min([r.percentage for r in results if r.percentage])
        }
        
        return jsonify({
            'results': [r.to_dict() for r in results],
            'statistics': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting exam results: {str(e)}")
        return jsonify({'error': str(e)}), 500