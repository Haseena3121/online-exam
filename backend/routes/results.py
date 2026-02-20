from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import ExamResult

results_bp = Blueprint('results', __name__)


# ===============================
# GET STUDENT RESULTS
# ===============================
@results_bp.route('/all', methods=['GET'])
@jwt_required()
def get_results():
    student_id = get_jwt_identity()

    results = ExamResult.query.filter_by(student_id=student_id).all()

    return jsonify({
        "results": [
            {
                "id": r.id,
                "exam_id": r.exam_id,
                "obtained_marks": r.obtained_marks,
                "percentage": r.percentage,
                "created_at": r.created_at
            } for r in results
        ]
    }), 200