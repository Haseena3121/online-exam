"""
Results Routes — MongoDB
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from database import mongo

results_bp = Blueprint('results', __name__)


@results_bp.route('/all', methods=['GET'])
@jwt_required()
def get_results():
    try:
        student_id = get_jwt_identity()
        results = list(mongo.db.exam_results.find({'student_id': student_id}).sort('submitted_at', -1))

        results_data = []
        for r in results:
            exam = mongo.db.exams.find_one({'_id': ObjectId(r['exam_id'])})
            exam_title = exam['title'] if exam else f"Exam #{r['exam_id']}"
            results_data.append({
                "id": str(r['_id']),
                "exam_id": r['exam_id'],
                "exam_title": exam_title,
                "obtained_marks": r.get('obtained_marks') or 0,
                "total_marks": r.get('total_marks') or 0,
                "percentage": r.get('percentage') or 0.0,
                "status": r.get('status', 'completed'),
                "violation_count": r.get('violation_count') or 0,
                "final_trust_score": r.get('final_trust_score') or 100,
                "correct_answers": r.get('correct_answers') or 0,
                "incorrect_answers": r.get('incorrect_answers') or 0,
                "total_time_taken": r.get('total_time_taken'),
                "submitted_at": r['submitted_at'].isoformat() + 'Z' if r.get('submitted_at') else None,
                "created_at": r['created_at'].isoformat() + 'Z' if r.get('created_at') else None
            })

        return jsonify({"results": results_data}), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@results_bp.route('/<exam_id>/review', methods=['GET'])
@jwt_required()
def get_exam_review(exam_id):
    try:
        student_id = get_jwt_identity()
        result = mongo.db.exam_results.find_one({'student_id': student_id, 'exam_id': exam_id})
        if not result:
            return jsonify({"error": "Result not found"}), 404

        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        questions = list(mongo.db.exam_questions.find({'exam_id': exam_id}).sort('order', 1))
        review_data = []
        for q in questions:
            q_id = str(q['_id'])
            sa = mongo.db.student_answers.find_one({'student_id': student_id, 'question_id': q_id})
            selected = sa['selected_answer'] if sa else None
            is_correct = selected == q.get('correct_answer') if selected else False
            review_data.append({
                "question_id": q_id,
                "question_text": q['question_text'],
                "option_a": q.get('option_a'),
                "option_b": q.get('option_b'),
                "option_c": q.get('option_c'),
                "option_d": q.get('option_d'),
                "correct_answer": q.get('correct_answer'),
                "selected_answer": selected,
                "is_correct": is_correct,
                "marks": q.get('marks', 1),
                "marks_awarded": sa['marks_awarded'] if sa else 0
            })

        return jsonify({
            "exam_title": exam['title'],
            "result": {
                "obtained_marks": result.get('obtained_marks'),
                "total_marks": result.get('total_marks'),
                "percentage": result.get('percentage'),
                "status": result.get('status'),
                "total_time_taken": result.get('total_time_taken'),
                "final_trust_score": result.get('final_trust_score'),
                "submitted_at": result['submitted_at'].isoformat() + 'Z' if result.get('submitted_at') else None
            },
            "questions": review_data
        }), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@results_bp.route('/detailed/<exam_id>', methods=['GET'])
@jwt_required()
def get_detailed_result(exam_id):
    return get_exam_review(exam_id)


@results_bp.route('/exam/<exam_id>/all-students', methods=['GET'])
@jwt_required()
def get_exam_all_results(exam_id):
    try:
        examiner_id = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': ObjectId(examiner_id)})
        if not user or user['role'] != 'examiner':
            return jsonify({'error': 'Only examiners can view this'}), 403

        results = list(mongo.db.exam_results.find({'exam_id': exam_id}))
        data = []
        for r in results:
            student = mongo.db.users.find_one({'_id': ObjectId(r['student_id'])})
            data.append({
                'id': str(r['_id']),
                'student_id': r['student_id'],
                'student_name': student['name'] if student else 'Unknown',
                'student_email': student['email'] if student else '',
                'obtained_marks': r.get('obtained_marks') or 0,
                'total_marks': r.get('total_marks') or 0,
                'percentage': r.get('percentage') or 0,
                'status': r.get('status'),
                'violation_count': r.get('violation_count') or 0,
                'final_trust_score': r.get('final_trust_score') or 100,
                'submitted_at': r['submitted_at'].isoformat() + 'Z' if r.get('submitted_at') else None
            })
        return jsonify({'results': data, 'total': len(data)}), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500
