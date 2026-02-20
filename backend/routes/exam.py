from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Exam, ExamQuestion, User
from database import db
from datetime import datetime

exam_bp = Blueprint('exam', __name__)


# ===============================
# LIST ALL EXAMS
# ===============================
@exam_bp.route('/', methods=['GET'])
@jwt_required()
def list_exams():
    exams = Exam.query.order_by(Exam.created_at.desc()).all()

    return jsonify({
        "exams": [
            {
                "id": e.id,
                "title": e.title,
                "duration": e.duration,
                "total_marks": e.total_marks
            } for e in exams
        ]
    }), 200


# ===============================
# GET EXAM WITH QUESTIONS
# ===============================
@exam_bp.route('/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_exam(exam_id):
    exam = Exam.query.get(exam_id)

    if not exam:
        return jsonify({"error": "Exam not found"}), 404

    return jsonify({
        "id": exam.id,
        "title": exam.title,
        "duration": exam.duration,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "marks": q.marks
            } for q in exam.questions
        ]
    }), 200


# ===============================
# CREATE EXAM (Examiner Only)
# ===============================
@exam_bp.route('/', methods=['POST'])
@jwt_required()
def create_exam():
    examiner_id = get_jwt_identity()
    user = User.query.get(examiner_id)

    if user.role != "examiner":
        return jsonify({"error": "Only examiners can create exams"}), 403

    data = request.get_json()

    exam = Exam(
        title=data["title"],
        examiner_id=examiner_id,
        duration=data.get("duration", 60),
        total_marks=data.get("total_marks", 100),
        created_at=datetime.utcnow()
    )

    db.session.add(exam)
    db.session.commit()

    return jsonify({"message": "Exam created"}), 201