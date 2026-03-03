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