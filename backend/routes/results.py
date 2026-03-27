from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import ExamResult, Exam, User

results_bp = Blueprint('results', __name__)


# ===============================
# GET STUDENT RESULTS
# ===============================
@results_bp.route('/all', methods=['GET'])
@jwt_required()
def get_results():
    try:
        student_id = get_jwt_identity()
        print(f"📊 Fetching results for student {student_id}")

        results = ExamResult.query.filter_by(student_id=student_id).order_by(ExamResult.submitted_at.desc()).all()
        print(f"✅ Found {len(results)} results")

        results_data = []
        for r in results:
            # Get exam details
            exam = Exam.query.get(r.exam_id)
            exam_title = exam.title if exam else f"Exam #{r.exam_id}"
            
            results_data.append({
                "id": r.id,
                "exam_id": r.exam_id,
                "exam_title": exam_title,
                "obtained_marks": r.obtained_marks if r.obtained_marks is not None else 0,
                "total_marks": r.total_marks if r.total_marks is not None else 0,
                "percentage": r.percentage if r.percentage is not None else 0.0,
                "status": r.status if r.status else 'completed',
                "violation_count": r.violation_count if r.violation_count is not None else 0,
                "final_trust_score": r.final_trust_score if r.final_trust_score is not None else 100,
                "correct_answers": r.correct_answers if hasattr(r, 'correct_answers') and r.correct_answers is not None else 0,
                "incorrect_answers": r.incorrect_answers if hasattr(r, 'incorrect_answers') and r.incorrect_answers is not None else 0,
                "total_time_taken": r.total_time_taken if hasattr(r, 'total_time_taken') and r.total_time_taken is not None else None,
                "submitted_at": r.submitted_at.isoformat() + 'Z' if r.submitted_at else None,
                "created_at": r.created_at.isoformat() + 'Z' if r.created_at else None
            })

        print(f"✅ Returning {len(results_data)} results")
        return jsonify({
            "results": results_data
        }), 200
        
    except Exception as e:
        print(f"❌ ERROR in get_results: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ===============================
# GET EXAM REVIEW (Student views their answers)
# ===============================
@results_bp.route('/<int:exam_id>/review', methods=['GET'])
@jwt_required()
def get_exam_review(exam_id):
    try:
        student_id = int(get_jwt_identity())

        result = ExamResult.query.filter_by(student_id=student_id, exam_id=exam_id).first()
        if not result:
            return jsonify({"error": "Result not found"}), 404

        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        from models import ExamQuestion, StudentAnswer
        questions = ExamQuestion.query.filter_by(exam_id=exam_id).order_by(ExamQuestion.order).all()

        review_data = []
        for q in questions:
            student_ans = StudentAnswer.query.filter_by(
                student_id=student_id, question_id=q.id
            ).first()
            selected = student_ans.selected_answer if student_ans else None
            is_correct = selected == q.correct_answer if selected else False

            review_data.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_answer": q.correct_answer,
                "selected_answer": selected,
                "is_correct": is_correct,
                "marks": q.marks,
                "marks_awarded": student_ans.marks_awarded if student_ans else 0,
            })

        return jsonify({
            "exam_title": exam.title,
            "result": {
                "obtained_marks": result.obtained_marks,
                "total_marks": result.total_marks,
                "percentage": result.percentage,
                "status": result.status,
                "total_time_taken": result.total_time_taken,
                "final_trust_score": result.final_trust_score,
                "submitted_at": result.submitted_at.isoformat() + 'Z' if result.submitted_at else None,
            },
            "questions": review_data,
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
