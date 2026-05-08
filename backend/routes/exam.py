"""
Exam Routes — MongoDB
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId

from database import mongo
from models import make_exam, exam_to_dict, make_question

exam_bp = Blueprint('exam', __name__)


def _get_user(user_id):
    return mongo.db.users.find_one({'_id': ObjectId(user_id)})


@exam_bp.route('/auth-test', methods=['GET'])
@jwt_required()
def auth_test():
    try:
        user = _get_user(get_jwt_identity())
        return jsonify({"message": "Authentication successful", "user": {
            "id": str(user['_id']), "name": user['name'],
            "email": user['email'], "role": user['role']
        }}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@exam_bp.route('/test', methods=['POST'])
def test_create():
    data = request.get_json()
    return jsonify({"message": "Test successful", "data": data}), 200


@exam_bp.route('/', methods=['GET'])
@jwt_required()
def list_exams():
    user = _get_user(get_jwt_identity())
    query = {} if user['role'] == 'examiner' else {'is_published': True}
    exams = list(mongo.db.exams.find(query).sort('created_at', -1))
    return jsonify({"exams": [
        {
            "id": str(e['_id']),
            "title": e['title'],
            "description": e.get('description'),
            "duration": e.get('duration'),
            "total_marks": e.get('total_marks'),
            "passing_marks": e.get('passing_marks'),
            "is_published": e.get('is_published', False)
        } for e in exams
    ]}), 200


@exam_bp.route('/my-exams', methods=['GET'])
@jwt_required()
def get_my_exams():
    user_id = get_jwt_identity()
    user = _get_user(user_id)
    if user['role'] != 'examiner':
        return jsonify({"error": "Only examiners can access this"}), 403

    exams = list(mongo.db.exams.find({'examiner_id': user_id}).sort('created_at', -1))
    return jsonify({"exams": [
        {
            "id": str(e['_id']),
            "title": e['title'],
            "description": e.get('description'),
            "duration": e.get('duration'),
            "total_marks": e.get('total_marks'),
            "passing_marks": e.get('passing_marks'),
            "is_published": e.get('is_published', False),
            "created_at": e['created_at'].isoformat() if e.get('created_at') else None
        } for e in exams
    ]}), 200


@exam_bp.route('/<exam_id>/publish', methods=['PATCH'])
@jwt_required()
def toggle_publish(exam_id):
    try:
        user_id = get_jwt_identity()
        user = _get_user(user_id)
        if user['role'] != 'examiner':
            return jsonify({"error": "Only examiners can publish exams"}), 403

        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return jsonify({"error": "Exam not found"}), 404
        if exam['examiner_id'] != user_id:
            return jsonify({"error": "You can only publish your own exams"}), 403

        data = request.get_json()
        is_published = data.get('is_published', False)
        mongo.db.exams.update_one({'_id': ObjectId(exam_id)}, {'$set': {'is_published': is_published}})

        return jsonify({"message": "Exam status updated successfully", "is_published": is_published}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@exam_bp.route('/<exam_id>/acceptance-form', methods=['POST'])
@jwt_required()
def submit_acceptance(exam_id):
    try:
        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return jsonify({"error": "Exam not found"}), 404
        if not exam.get('is_published'):
            return jsonify({"error": "This exam is not available"}), 403

        data = request.get_json()
        required = ['accepted', 'rules_accepted', 'honor_code_accepted',
                    'privacy_accepted', 'technical_requirements_met']
        for field in required:
            if not data.get(field):
                return jsonify({"error": "You must accept all terms to continue"}), 400

        return jsonify({"message": "Acceptance form submitted successfully", "exam_id": exam_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@exam_bp.route('/<exam_id>/start', methods=['POST'])
@jwt_required()
def start_exam(exam_id):
    try:
        student_id = get_jwt_identity()
        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return jsonify({"error": "Exam not found"}), 404
        if not exam.get('is_published'):
            return jsonify({"error": "This exam is not available"}), 403

        existing = mongo.db.proctoring_sessions.find_one({
            'student_id': student_id, 'exam_id': exam_id, 'status': 'active'
        })
        if existing:
            sid = str(existing['_id'])
            return jsonify({
                "message": "Resuming existing session",
                "session_id": f"{student_id}_{exam_id}_{sid}",
                "exam_id": exam_id,
                "duration": exam.get('duration'),
                "proctoring_session_id": sid
            }), 200

        from models import make_proctoring_session
        session_doc = make_proctoring_session(student_id=student_id, exam_id=exam_id)
        result = mongo.db.proctoring_sessions.insert_one(session_doc)
        sid = str(result.inserted_id)

        return jsonify({
            "message": "Exam started successfully",
            "session_id": f"{student_id}_{exam_id}_{sid}",
            "exam_id": exam_id,
            "duration": exam.get('duration'),
            "proctoring_session_id": sid
        }), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@exam_bp.route('/<exam_id>', methods=['GET'])
@jwt_required()
def get_exam(exam_id):
    try:
        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        questions = list(mongo.db.exam_questions.find({'exam_id': exam_id}).sort('order', 1))
        return jsonify({
            "id": str(exam['_id']),
            "title": exam['title'],
            "description": exam.get('description'),
            "duration": exam.get('duration'),
            "total_marks": exam.get('total_marks'),
            "passing_marks": exam.get('passing_marks'),
            "questions": [
                {
                    "id": str(q['_id']),
                    "question_text": q['question_text'],
                    "option_a": q.get('option_a'),
                    "option_b": q.get('option_b'),
                    "option_c": q.get('option_c'),
                    "option_d": q.get('option_d'),
                    "marks": q.get('marks', 1),
                    "question_type": q.get('question_type', 'mcq')
                } for q in questions
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@exam_bp.route('/<exam_id>/questions', methods=['POST'])
@jwt_required()
def add_questions(exam_id):
    try:
        user_id = get_jwt_identity()
        user = _get_user(user_id)
        if user['role'] != 'examiner':
            return jsonify({"error": "Only examiners can add questions"}), 403

        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return jsonify({"error": "Exam not found"}), 404
        if exam['examiner_id'] != user_id:
            return jsonify({"error": "You can only add questions to your own exams"}), 403

        data = request.get_json()
        questions_data = data.get('questions', [])
        if not questions_data:
            return jsonify({"error": "No questions provided"}), 400

        docs = [make_question(
            exam_id=exam_id,
            question_text=q.get('question_text'),
            option_a=q.get('option_a'),
            option_b=q.get('option_b'),
            option_c=q.get('option_c'),
            option_d=q.get('option_d'),
            correct_answer=q.get('correct_answer'),
            marks=int(q.get('marks', 1)),
            order=idx
        ) for idx, q in enumerate(questions_data, 1)]

        mongo.db.exam_questions.insert_many(docs)
        return jsonify({
            "message": f"Successfully added {len(docs)} questions",
            "exam_id": exam_id,
            "questions_added": len(docs)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@exam_bp.route('/', methods=['POST'])
@jwt_required()
def create_exam():
    try:
        user_id = get_jwt_identity()
        user = _get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if user['role'] != 'examiner':
            return jsonify({"error": "Only examiners can create exams"}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        if not data.get("title"):
            return jsonify({"error": "Title is required"}), 400
        if not data.get("duration"):
            return jsonify({"error": "Duration is required"}), 400
        if not data.get("total_marks"):
            return jsonify({"error": "Total marks is required"}), 400

        exam_doc = make_exam(
            title=str(data["title"]),
            description=str(data.get("description", "")),
            instructions=str(data.get("instructions", "")),
            examiner_id=user_id,
            duration=int(data["duration"]),
            total_marks=int(data["total_marks"]),
            passing_marks=int(data.get("passing_marks", 0)),
            negative_marking=float(data.get("negative_marking", 0)),
            is_published=bool(data.get("is_published", False))
        )
        result = mongo.db.exams.insert_one(exam_doc)
        exam_id = str(result.inserted_id)

        return jsonify({
            "message": "Exam created successfully",
            "exam_id": exam_id,
            "exam": {"id": exam_id, "title": exam_doc['title'],
                     "duration": exam_doc['duration'], "total_marks": exam_doc['total_marks']}
        }), 201

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": f"Failed to create exam: {str(e)}"}), 500


@exam_bp.route('/<exam_id>/results', methods=['GET'])
@jwt_required()
def get_exam_results(exam_id):
    try:
        user_id = get_jwt_identity()
        user = _get_user(user_id)
        if not user or user['role'] != 'examiner':
            return jsonify({'error': 'Unauthorized'}), 403

        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        if exam['examiner_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        results = list(mongo.db.exam_results.find({'exam_id': exam_id}))
        results_data = []
        for r in results:
            student = mongo.db.users.find_one({'_id': ObjectId(r['student_id'])})
            violations = list(mongo.db.violations.find(
                {'exam_id': exam_id, 'student_id': r['student_id']}
            ).sort('created_at', -1))
            session = mongo.db.proctoring_sessions.find_one(
                {'exam_id': exam_id, 'student_id': r['student_id']}
            )
            results_data.append({
                'result_id': str(r['_id']),
                'student': {
                    'id': str(student['_id']), 'name': student['name'], 'email': student['email']
                } if student else {'id': r['student_id'], 'name': 'Unknown', 'email': ''},
                'marks': {
                    'obtained': r.get('obtained_marks'),
                    'total': r.get('total_marks'),
                    'percentage': round(r['percentage'], 2) if r.get('percentage') else 0
                },
                'trust_score': r.get('final_trust_score') or (session['current_trust_score'] if session else 100),
                'status': r.get('status', 'completed'),
                'violation_count': len(violations),
                'total_time_taken': r.get('total_time_taken'),
                'violations': [{
                    'id': str(v['_id']),
                    'type': v.get('violation_type'),
                    'severity': v.get('severity', 'medium'),
                    'description': v.get('description'),
                    'reduction': v.get('trust_score_reduction'),
                    'evidence_path': v.get('evidence_path'),
                    'evidence_url': f"/api/proctoring/evidence/{v['evidence_path']}" if v.get('evidence_path') else None,
                    'time': v['created_at'].isoformat() + 'Z' if v.get('created_at') else None
                } for v in violations],
                'submitted_at': r['submitted_at'].isoformat() + 'Z' if r.get('submitted_at') else None
            })

        return jsonify({
            'exam': {
                'id': str(exam['_id']),
                'title': exam['title'],
                'total_marks': exam.get('total_marks'),
                'duration': exam.get('duration'),
                'auto_delete_enabled': exam.get('auto_delete_enabled', False),
                'auto_delete_date': exam['auto_delete_date'].isoformat() + 'Z' if exam.get('auto_delete_date') else None
            },
            'results': results_data,
            'total_students': len(results_data)
        }), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500
