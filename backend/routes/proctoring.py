"""
Proctoring Routes — MongoDB
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
import logging
import os
import uuid

from database import mongo
from models import (
    make_violation, violation_to_dict,
    make_exam_result, make_notification,
    make_analytics, analytics_to_dict, session_to_dict
)
from services.email_service import email_service

proctoring_bp = Blueprint('proctoring', __name__)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'uploads/evidence'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_evidence_file(file):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename_ext = 'jpg'
        if file.filename and '.' in file.filename:
            ext = file.filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                filename_ext = ext
        elif file.content_type:
            ct_map = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/gif': 'gif', 'video/mp4': 'mp4'}
            filename_ext = ct_map.get(file.content_type, 'jpg')
        filename = f"{uuid.uuid4()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{filename_ext}"
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename
    except Exception as e:
        logger.error(f"Error saving file: {e}")
    return None


@proctoring_bp.route('/violation', methods=['POST'])
@jwt_required()
def report_violation():
    try:
        student_id = get_jwt_identity()
        session = mongo.db.proctoring_sessions.find_one({'student_id': student_id, 'status': 'active'})
        if not session:
            return jsonify({'error': 'No active session'}), 404

        violation_type = request.form.get('violation_type')
        severity = request.form.get('severity', 'medium')

        evidence_path = None
        if 'evidence' in request.files:
            evidence_path = save_evidence_file(request.files['evidence'])

        severity_map = {'low': 5, 'medium': 10, 'high': 20}
        trust_score_reduction = severity_map.get(severity, 10)

        v_doc = make_violation(
            student_id=student_id,
            exam_id=session['exam_id'],
            session_id=str(session['_id']),
            violation_type=violation_type,
            severity=severity,
            evidence_path=evidence_path,
            trust_score_reduction=trust_score_reduction
        )
        v_result = mongo.db.violations.insert_one(v_doc)

        new_trust = max(0, session['current_trust_score'] - trust_score_reduction)
        mongo.db.proctoring_sessions.update_one(
            {'_id': session['_id']},
            {'$set': {'current_trust_score': new_trust}}
        )

        response_data = {
            'message': 'Violation recorded',
            'violation_id': str(v_result.inserted_id),
            'current_trust_score': new_trust,
            'warning': new_trust < 80,
            'evidence_saved': evidence_path is not None
        }

        if new_trust < 50 and session['status'] == 'active':
            existing_result = mongo.db.exam_results.find_one({
                'student_id': student_id, 'exam_id': session['exam_id']
            })
            if not existing_result:
                response_data['critical_message'] = 'Trust score below 50%. Exam will be auto-submitted!'
                try:
                    # Refresh session doc with updated trust score
                    session['current_trust_score'] = new_trust
                    auto_result = _auto_submit_exam(session)
                    response_data['auto_submitted'] = True
                    if auto_result:
                        response_data['result'] = auto_result
                except Exception as ae:
                    logger.error(f"Auto-submit failed: {ae}")
            else:
                response_data['critical_message'] = 'Exam already submitted.'
                response_data['auto_submitted'] = True

        return jsonify(response_data), 201

    except Exception as e:
        logger.error(f"Error reporting violation: {e}")
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def _auto_submit_exam(session):
    """Auto-submit exam when trust score < 50%"""
    try:
        student_id = session['student_id']
        exam_id = session['exam_id']

        existing = mongo.db.exam_results.find_one({'student_id': student_id, 'exam_id': exam_id})
        if existing:
            return {
                'obtained_marks': existing.get('obtained_marks'),
                'total_marks': existing.get('total_marks'),
                'percentage': existing.get('percentage'),
                'correct_answers': existing.get('correct_answers'),
                'violation_count': existing.get('violation_count'),
                'final_trust_score': existing.get('final_trust_score')
            }

        mongo.db.proctoring_sessions.update_one(
            {'_id': session['_id']},
            {'$set': {'status': 'ended', 'end_time': datetime.utcnow()}}
        )

        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return None

        # Calculate marks from already-submitted answers
        questions = {str(q['_id']): q for q in mongo.db.exam_questions.find({'exam_id': exam_id})}
        student_answers = list(mongo.db.student_answers.find({'student_id': student_id, 'exam_id': exam_id}))

        obtained_marks = 0
        correct_count = 0
        for sa in student_answers:
            q = questions.get(sa.get('question_id'))
            if q:
                if sa.get('selected_answer') == q.get('correct_answer'):
                    obtained_marks += q.get('marks', 1)
                    correct_count += 1
                elif exam.get('negative_marking', 0) > 0:
                    obtained_marks = max(0, obtained_marks - exam['negative_marking'])

        total_marks = exam.get('total_marks', 0)
        percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
        violation_count = mongo.db.violations.count_documents({'student_id': student_id, 'exam_id': exam_id})

        time_taken = None
        if session.get('start_time'):
            time_taken = int((datetime.utcnow() - session['start_time']).total_seconds() / 60)

        result_doc = make_exam_result(
            student_id=student_id, exam_id=exam_id,
            enrollment_id=session.get('enrollment_id'),
            obtained_marks=obtained_marks, total_marks=total_marks,
            percentage=percentage, status='auto_submitted',
            violation_count=violation_count,
            final_trust_score=session['current_trust_score'],
            correct_answers=correct_count, total_time_taken=time_taken
        )
        mongo.db.exam_results.insert_one(result_doc)

        try:
            notif = make_notification(
                examiner_id=exam['examiner_id'], student_id=student_id, exam_id=exam_id,
                message=f"🔴 EXAM AUTO-SUBMITTED\nStudent: {student_id}\nReason: Trust Score Below 50%\nScore: {obtained_marks}/{total_marks} ({percentage:.2f}%)\nFinal Trust Score: {session['current_trust_score']}%",
                severity_level='high'
            )
            mongo.db.examiner_notifications.insert_one(notif)
        except Exception as ne:
            logger.warning(f"Notification failed (non-critical): {ne}")

        try:
            user = mongo.db.users.find_one({'_id': ObjectId(student_id)})
            if user and user.get('email'):
                email_service.send_auto_submit_notification(
                    user['email'], exam['title'],
                    "Trust score fell below 50% due to exam rule violations"
                )
        except Exception as ee:
            logger.warning(f"Email failed (non-critical): {ee}")

        return {
            'obtained_marks': obtained_marks, 'total_marks': total_marks,
            'percentage': round(percentage, 2), 'correct_answers': correct_count,
            'violation_count': violation_count, 'final_trust_score': session['current_trust_score']
        }

    except Exception as e:
        logger.error(f"Error auto-submitting: {e}")
        import traceback; traceback.print_exc()
        return None


@proctoring_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_exam():
    try:
        student_id = get_jwt_identity()
        data = request.get_json()

        session = mongo.db.proctoring_sessions.find_one({'student_id': student_id, 'status': 'active'})
        if not session:
            return jsonify({'error': 'No active session found'}), 404

        exam_id = session['exam_id']
        exam = mongo.db.exams.find_one({'_id': ObjectId(exam_id)})
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404

        answers = data.get('answers', [])
        obtained_marks = 0
        correct_count = 0
        answer_docs = []

        for ans in answers:
            question_id = ans.get('question_id')
            selected = ans.get('selected_answer')
            q = mongo.db.exam_questions.find_one({'_id': ObjectId(question_id)})
            if not q:
                continue
            is_correct = selected == q.get('correct_answer')
            marks = q.get('marks', 1) if is_correct else 0
            if not is_correct and exam.get('negative_marking', 0) > 0:
                marks = max(0, marks - exam['negative_marking'])
            if is_correct:
                correct_count += 1
            obtained_marks += marks
            answer_docs.append({
                'student_id': student_id,
                'exam_id': exam_id,
                'question_id': question_id,
                'selected_answer': selected,
                'marks_awarded': marks
            })

        if answer_docs:
            mongo.db.student_answers.insert_many(answer_docs)

        mongo.db.proctoring_sessions.update_one(
            {'_id': session['_id']},
            {'$set': {'status': 'ended', 'end_time': datetime.utcnow()}}
        )

        total_marks = exam.get('total_marks', 0)
        percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
        violation_count = mongo.db.violations.count_documents({'student_id': student_id, 'exam_id': exam_id})

        time_taken = None
        if session.get('start_time'):
            time_taken = int((datetime.utcnow() - session['start_time']).total_seconds() / 60)

        result_doc = make_exam_result(
            student_id=student_id, exam_id=exam_id,
            enrollment_id=session.get('enrollment_id'),
            obtained_marks=obtained_marks, total_marks=total_marks,
            percentage=percentage, status='completed',
            violation_count=violation_count,
            final_trust_score=session.get('current_trust_score', 100),
            correct_answers=correct_count,
            incorrect_answers=len(answers) - correct_count,
            total_time_taken=time_taken
        )
        mongo.db.exam_results.insert_one(result_doc)

        return jsonify({
            'message': 'Exam submitted successfully',
            'result': {
                'obtained_marks': obtained_marks, 'total_marks': total_marks,
                'percentage': round(percentage, 2), 'correct_answers': correct_count,
                'total_questions': len(answers), 'violation_count': violation_count,
                'final_trust_score': session.get('current_trust_score', 100),
                'time_taken': time_taken
            }
        }), 200

    except Exception as e:
        logger.error(f"Error submitting exam: {e}")
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/session/<session_id>', methods=['GET'])
@jwt_required()
def get_session_status(session_id):
    try:
        session = mongo.db.proctoring_sessions.find_one({'_id': ObjectId(session_id)})
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        return jsonify({'session': session_to_dict(session)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/session/<session_id>/warning', methods=['POST'])
@jwt_required()
def send_warning(session_id):
    try:
        session = mongo.db.proctoring_sessions.find_one({'_id': ObjectId(session_id)})
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        trust = session.get('current_trust_score', 100)
        level = "CRITICAL" if trust < 50 else "WARNING"
        return jsonify({
            'warning_level': level,
            'message': f'{level}: Follow exam rules or exam will auto-submit!',
            'current_trust_score': trust,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/analytics/<session_id>', methods=['GET'])
@jwt_required()
def get_analytics(session_id):
    try:
        a = mongo.db.session_analytics.find_one({'session_id': session_id})
        if not a:
            return jsonify({'error': 'Analytics not found'}), 404
        return jsonify({'analytics': analytics_to_dict(a)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/update-analytics/<session_id>', methods=['POST'])
@jwt_required()
def update_analytics(session_id):
    try:
        data = request.get_json()
        a = mongo.db.session_analytics.find_one({'session_id': session_id})
        if not a:
            session = mongo.db.proctoring_sessions.find_one({'_id': ObjectId(session_id)})
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            from models import make_analytics
            a_doc = make_analytics(session_id=session_id)
            mongo.db.session_analytics.insert_one(a_doc)
            a = mongo.db.session_analytics.find_one({'session_id': session_id})

        inc = {k: data.get(k, 0) for k in [
            'eye_gaze_warnings', 'phone_detection_count', 'tab_switch_count',
            'sound_detection_count', 'multiple_persons_detected', 'blur_exit_attempts',
            'face_not_visible_count', 'head_movement_warnings'
        ]}
        total = sum(a.get(k, 0) + inc[k] for k in inc)
        inc['total_violations'] = total - a.get('total_violations', 0)

        mongo.db.session_analytics.update_one({'session_id': session_id}, {'$inc': inc})
        updated = mongo.db.session_analytics.find_one({'session_id': session_id})
        return jsonify({'message': 'Analytics updated', 'analytics': analytics_to_dict(updated)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/monitor/active-sessions', methods=['GET'])
@jwt_required()
def get_active_sessions():
    try:
        user_id = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user or user['role'] != 'examiner':
            return jsonify({'error': 'Unauthorized'}), 403

        examiner_exam_ids = [str(e['_id']) for e in mongo.db.exams.find({'examiner_id': user_id})]
        active_sessions = list(mongo.db.proctoring_sessions.find({
            'exam_id': {'$in': examiner_exam_ids}, 'status': 'active'
        }))

        sessions_data = []
        for s in active_sessions:
            student = mongo.db.users.find_one({'_id': ObjectId(s['student_id'])})
            exam = mongo.db.exams.find_one({'_id': ObjectId(s['exam_id'])})
            violations = list(mongo.db.violations.find({'session_id': str(s['_id'])}).sort('created_at', -1).limit(5))
            sessions_data.append({
                'session_id': str(s['_id']),
                'student': {'id': str(student['_id']), 'name': student['name'], 'email': student['email']} if student else {},
                'exam': {'id': str(exam['_id']), 'title': exam['title'], 'duration': exam.get('duration')} if exam else {},
                'trust_score': s.get('current_trust_score', 100),
                'start_time': s['start_time'].isoformat() if s.get('start_time') else None,
                'camera_active': s.get('camera_active', True),
                'mic_active': s.get('mic_active', True),
                'violations': [{
                    'id': str(v['_id']), 'type': v.get('violation_type'),
                    'reduction': v.get('trust_score_reduction'),
                    'time': v['created_at'].isoformat() if v.get('created_at') else None,
                    'evidence_url': f"{request.host_url.rstrip('/')}/api/proctoring/evidence/{v['evidence_path'].split('/')[-1]}" if v.get('evidence_path') else None
                } for v in violations]
            })

        return jsonify({'active_sessions': sessions_data, 'count': len(sessions_data)}), 200

    except Exception as e:
        logger.error(f"Error getting active sessions: {e}")
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/monitor/session/<session_id>/details', methods=['GET'])
@jwt_required()
def get_session_details(session_id):
    try:
        user_id = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user or user['role'] != 'examiner':
            return jsonify({'error': 'Unauthorized'}), 403

        session = mongo.db.proctoring_sessions.find_one({'_id': ObjectId(session_id)})
        if not session:
            return jsonify({'error': 'Session not found'}), 404

        exam = mongo.db.exams.find_one({'_id': ObjectId(session['exam_id'])})
        if exam['examiner_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        student = mongo.db.users.find_one({'_id': ObjectId(session['student_id'])})
        violations = list(mongo.db.violations.find({'session_id': session_id}).sort('created_at', -1))

        return jsonify({
            'session': {
                'id': str(session['_id']), 'status': session.get('status'),
                'trust_score': session.get('current_trust_score', 100),
                'start_time': session['start_time'].isoformat() if session.get('start_time') else None,
                'end_time': session['end_time'].isoformat() if session.get('end_time') else None,
                'camera_active': session.get('camera_active', True),
                'mic_active': session.get('mic_active', True)
            },
            'student': {'id': str(student['_id']), 'name': student['name'], 'email': student['email']} if student else {},
            'exam': {'id': str(exam['_id']), 'title': exam['title'], 'duration': exam.get('duration'), 'total_marks': exam.get('total_marks')} if exam else {},
            'violations': [{
                'id': str(v['_id']), 'type': v.get('violation_type'),
                'reduction': v.get('trust_score_reduction'),
                'time': v['created_at'].isoformat() if v.get('created_at') else None,
                'evidence_url': f"{request.host_url.rstrip('/')}/api/proctoring/evidence/{v['evidence_path'].split('/')[-1]}" if v.get('evidence_path') else None
            } for v in violations],
            'violation_count': len(violations)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/evidence/<path:filename>', methods=['GET'])
def serve_evidence(filename):
    try:
        from flask_jwt_extended import decode_token
        token = request.args.get('token')
        if not token:
            return jsonify({'error': 'Unauthorized'}), 403
        try:
            decoded = decode_token(token)
            user_id = decoded['sub']
        except Exception:
            return jsonify({'error': 'Invalid token'}), 403

        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user or user['role'] != 'examiner':
            return jsonify({'error': 'Unauthorized'}), 403

        safe_filename = os.path.basename(filename)
        evidence_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        if not os.path.exists(evidence_path):
            return jsonify({'error': 'Evidence not found'}), 404

        from flask import send_file
        return send_file(evidence_path)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@proctoring_bp.route('/analyze-frame', methods=['POST'])
@jwt_required()
def analyze_frame():
    try:
        student_id = get_jwt_identity()
        session = mongo.db.proctoring_sessions.find_one({'student_id': student_id, 'status': 'active'})
        if not session:
            return jsonify({'error': 'No active session'}), 404

        if 'frame' not in request.files:
            return jsonify({'error': 'No frame provided'}), 400

        frame_bytes = request.files['frame'].read()
        import numpy as np
        import cv2
        frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({'error': 'Invalid frame'}), 400

        from ai_models.model_manager import get_detection_manager
        manager = get_detection_manager()
        detections = {}

        try:
            detections['phone'] = manager.phone_detector.detect_phone(frame) if manager.phone_detector else {'phone_detected': False}
        except Exception as e:
            detections['phone'] = {'phone_detected': False}

        try:
            detections['persons'] = manager.person_detector.detect_persons(frame) if manager.person_detector else {'multiple_persons': False}
        except Exception as e:
            detections['persons'] = {'multiple_persons': False}

        try:
            detections['face'] = manager.face_detector.detect_face(frame) if manager.face_detector else {'face_detected': True}
        except Exception as e:
            detections['face'] = {'face_detected': True}

        return jsonify({'detections': detections}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
