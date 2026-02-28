from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Exam, ExamQuestion, User
from database import db
from datetime import datetime

exam_bp = Blueprint('exam', __name__)


# ===============================
# AUTH TEST ENDPOINT
# ===============================
@exam_bp.route('/auth-test', methods=['GET'])
@jwt_required()
def auth_test():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        return jsonify({
            "message": "Authentication successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# TEST ENDPOINT (NO AUTH)
# ===============================
@exam_bp.route('/test', methods=['POST'])
def test_create():
    try:
        data = request.get_json()
        print(f"TEST ENDPOINT - Received data: {data}")
        return jsonify({"message": "Test successful", "data": data}), 200
    except Exception as e:
        print(f"TEST ENDPOINT - Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ===============================
# LIST ALL EXAMS (Students see only published)
# ===============================
@exam_bp.route('/', methods=['GET'])
@jwt_required()
def list_exams():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    # Examiners see all exams, students see only published
    if user.role == "examiner":
        exams = Exam.query.order_by(Exam.created_at.desc()).all()
    else:
        exams = Exam.query.filter_by(is_published=True).order_by(Exam.created_at.desc()).all()

    return jsonify({
        "exams": [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "duration": e.duration,
                "total_marks": e.total_marks,
                "passing_marks": e.passing_marks,
                "is_published": e.is_published
            } for e in exams
        ]
    }), 200


# ===============================
# GET EXAMINER'S EXAMS
# ===============================
@exam_bp.route('/my-exams', methods=['GET'])
@jwt_required()
def get_my_exams():
    examiner_id = int(get_jwt_identity())  # Convert string to int
    user = User.query.get(examiner_id)

    if user.role != "examiner":
        return jsonify({"error": "Only examiners can access this"}), 403

    exams = Exam.query.filter_by(examiner_id=examiner_id).order_by(Exam.created_at.desc()).all()

    return jsonify({
        "exams": [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "duration": e.duration,
                "total_marks": e.total_marks,
                "passing_marks": e.passing_marks,
                "is_published": e.is_published,
                "created_at": e.created_at.isoformat() if e.created_at else None
            } for e in exams
        ]
    }), 200


# ===============================
# PUBLISH/UNPUBLISH EXAM
# ===============================
@exam_bp.route('/<int:exam_id>/publish', methods=['PATCH'])
@jwt_required()
def toggle_publish(exam_id):
    try:
        examiner_id = int(get_jwt_identity())
        user = User.query.get(examiner_id)

        if user.role != "examiner":
            return jsonify({"error": "Only examiners can publish exams"}), 403

        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        if exam.examiner_id != examiner_id:
            return jsonify({"error": "You can only publish your own exams"}), 403

        data = request.get_json()
        exam.is_published = data.get('is_published', False)
        
        db.session.commit()

        return jsonify({
            "message": "Exam status updated successfully",
            "is_published": exam.is_published
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating exam: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ===============================
# SUBMIT ACCEPTANCE FORM
# ===============================
@exam_bp.route('/<int:exam_id>/acceptance-form', methods=['POST'])
@jwt_required()
def submit_acceptance(exam_id):
    try:
        student_id = int(get_jwt_identity())
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        if not exam.is_published:
            return jsonify({"error": "This exam is not available"}), 403

        data = request.get_json()
        
        # Check if all required fields are accepted
        required_fields = ['accepted', 'rules_accepted', 'honor_code_accepted', 
                          'privacy_accepted', 'technical_requirements_met']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"You must accept all terms to continue"}), 400

        return jsonify({
            "message": "Acceptance form submitted successfully",
            "exam_id": exam_id
        }), 200

    except Exception as e:
        print(f"Error submitting acceptance: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ===============================
# START EXAM
# ===============================
@exam_bp.route('/<int:exam_id>/start', methods=['POST'])
@jwt_required()
def start_exam(exam_id):
    try:
        student_id = int(get_jwt_identity())
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        if not exam.is_published:
            return jsonify({"error": "This exam is not available"}), 403

        # Check if there's already an active session
        from models import ProctoringSession
        from datetime import datetime
        
        existing_session = ProctoringSession.query.filter_by(
            student_id=student_id,
            exam_id=exam_id,
            status='active'
        ).first()

        if existing_session:
            session_id = f"{student_id}_{exam_id}_{existing_session.id}"
            return jsonify({
                "message": "Resuming existing session",
                "session_id": session_id,
                "exam_id": exam_id,
                "duration": exam.duration,
                "proctoring_session_id": existing_session.id
            }), 200

        # Create a new proctoring session - MUST SUCCEED
        session = ProctoringSession(
            student_id=student_id,
            exam_id=exam_id,
            current_trust_score=100,
            status='active',
            camera_active=True,
            mic_active=True,
            screen_locked=True,
            start_time=datetime.utcnow()
        )
        
        db.session.add(session)
        db.session.commit()
        
        proctoring_session_id = session.id
        print(f"✅ Proctoring session created successfully: ID {proctoring_session_id}")

        # Create a simple session ID
        import time
        session_id = f"{student_id}_{exam_id}_{proctoring_session_id}"

        return jsonify({
            "message": "Exam started successfully",
            "session_id": session_id,
            "exam_id": exam_id,
            "duration": exam.duration,
            "proctoring_session_id": proctoring_session_id
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error starting exam: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ===============================
# GET EXAM WITH QUESTIONS
# ===============================
@exam_bp.route('/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_exam(exam_id):
    try:
        exam = Exam.query.get(exam_id)

        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        return jsonify({
            "id": exam.id,
            "title": exam.title,
            "description": exam.description,
            "duration": exam.duration,
            "total_marks": exam.total_marks,
            "passing_marks": exam.passing_marks,
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "option_a": q.option_a,
                    "option_b": q.option_b,
                    "option_c": q.option_c,
                    "option_d": q.option_d,
                    "marks": q.marks,
                    "question_type": q.question_type
                } for q in exam.questions
            ]
        }), 200
    except Exception as e:
        print(f"Error fetching exam: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ===============================
# ADD QUESTIONS TO EXAM
# ===============================
@exam_bp.route('/<int:exam_id>/questions', methods=['POST'])
@jwt_required()
def add_questions(exam_id):
    try:
        examiner_id = int(get_jwt_identity())
        user = User.query.get(examiner_id)

        if user.role != "examiner":
            return jsonify({"error": "Only examiners can add questions"}), 403

        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        if exam.examiner_id != examiner_id:
            return jsonify({"error": "You can only add questions to your own exams"}), 403

        data = request.get_json()
        questions_data = data.get('questions', [])

        if not questions_data:
            return jsonify({"error": "No questions provided"}), 400

        added_count = 0
        for idx, q_data in enumerate(questions_data, 1):
            question = ExamQuestion(
                exam_id=exam.id,
                question_text=q_data.get('question_text'),
                option_a=q_data.get('option_a'),
                option_b=q_data.get('option_b'),
                option_c=q_data.get('option_c'),
                option_d=q_data.get('option_d'),
                correct_answer=q_data.get('correct_answer'),
                marks=int(q_data.get('marks', 1)),
                question_type='mcq',
                order=idx
            )
            db.session.add(question)
            added_count += 1

        db.session.commit()

        return jsonify({
            "message": f"Successfully added {added_count} questions",
            "exam_id": exam.id,
            "questions_added": added_count
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error adding questions: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ===============================
# CREATE EXAM (Examiner Only)
# ===============================
@exam_bp.route('/', methods=['POST'])
@jwt_required()
def create_exam():
    try:
        examiner_id = int(get_jwt_identity())  # Convert string to int
        print(f"=== CREATE EXAM START ===")
        print(f"Examiner ID from JWT: {examiner_id}")
        
        user = User.query.get(examiner_id)
        print(f"User found: {user}")

        if not user:
            print("ERROR: User not found in database")
            return jsonify({"error": "User not found"}), 404

        print(f"User role: {user.role}")
        if user.role != "examiner":
            print("ERROR: User is not an examiner")
            return jsonify({"error": "Only examiners can create exams"}), 403

        data = request.get_json()
        print(f"Received data: {data}")

        # Validate required fields
        if not data:
            print("ERROR: No data received")
            return jsonify({"error": "No data provided"}), 400
            
        if not data.get("title"):
            print("ERROR: Title missing")
            return jsonify({"error": "Title is required"}), 400
        
        if not data.get("duration"):
            print("ERROR: Duration missing")
            return jsonify({"error": "Duration is required"}), 400
        
        if not data.get("total_marks"):
            print("ERROR: Total marks missing")
            return jsonify({"error": "Total marks is required"}), 400

        print("Creating exam object...")
        exam = Exam(
            title=str(data["title"]),
            description=str(data.get("description", "")),
            instructions=str(data.get("instructions", "")),
            examiner_id=int(examiner_id),
            duration=int(data["duration"]),
            total_marks=int(data["total_marks"]),
            passing_marks=int(data.get("passing_marks", 0)),
            negative_marking=float(data.get("negative_marking", 0)),
            is_published=bool(data.get("is_published", False)),
            created_at=datetime.utcnow()
        )

        print(f"Exam object created: {exam.title}")
        print("Adding to session...")
        db.session.add(exam)
        print("Committing...")
        db.session.commit()
        print(f"SUCCESS: Exam saved with ID: {exam.id}")

        return jsonify({
            "message": "Exam created successfully",
            "exam_id": exam.id,
            "exam": {
                "id": exam.id,
                "title": exam.title,
                "duration": exam.duration,
                "total_marks": exam.total_marks
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"=== ERROR creating exam ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to create exam: {str(e)}"}), 500


@exam_bp.route('/<int:exam_id>/results', methods=['GET'])
@jwt_required()
def get_exam_results(exam_id):
    """Get all results for an exam (examiner only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or user.role != 'examiner':
            return jsonify({'error': 'Unauthorized'}), 403
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        # Verify examiner owns this exam
        if exam.examiner_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get all results for this exam
        from models import ExamResult, ViolationLog, ProctoringSession
        results = ExamResult.query.filter_by(exam_id=exam_id).all()
        
        results_data = []
        for result in results:
            student = User.query.get(result.student_id)
            
            # Get violations for this student with evidence
            violations = ViolationLog.query.filter_by(
                exam_id=exam_id,
                student_id=result.student_id
            ).order_by(ViolationLog.created_at.desc()).all()
            
            # Get proctoring session
            session = ProctoringSession.query.filter_by(
                exam_id=exam_id,
                student_id=result.student_id
            ).first()
            
            results_data.append({
                'result_id': result.id,
                'student': {
                    'id': student.id,
                    'name': student.name,
                    'email': student.email
                },
                'marks': {
                    'obtained': result.obtained_marks,
                    'total': result.total_marks,
                    'percentage': round(result.percentage, 2) if result.percentage else 0
                },
                'trust_score': result.final_trust_score if result.final_trust_score else (session.current_trust_score if session else 100),
                'status': result.status if result.status else 'completed',
                'violation_count': len(violations),
                'violations': [{
                    'id': v.id,
                    'type': v.violation_type,
                    'severity': v.severity if hasattr(v, 'severity') and v.severity else 'medium',
                    'description': v.description if hasattr(v, 'description') and v.description else None,
                    'reduction': v.trust_score_reduction,
                    'evidence_path': v.evidence_path if hasattr(v, 'evidence_path') and v.evidence_path else None,
                    'evidence_url': f'http://localhost:5000/api/proctoring/evidence/{v.evidence_path.split("/")[-1]}' if hasattr(v, 'evidence_path') and v.evidence_path else None,
                    'time': v.created_at.isoformat() + 'Z' if v.created_at else None  # Add 'Z' to indicate UTC
                } for v in violations],
                'submitted_at': result.submitted_at.isoformat() + 'Z' if result.submitted_at else None  # Add 'Z' to indicate UTC
            })
        
        return jsonify({
            'exam': {
                'id': exam.id,
                'title': exam.title,
                'total_marks': exam.total_marks,
                'duration': exam.duration
            },
            'results': results_data,
            'total_students': len(results_data)
        }), 200
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting exam results: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
