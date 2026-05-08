"""
MongoDB document helpers — replaces SQLAlchemy models.
All data is stored as plain dicts in MongoDB collections.
These classes provide to_dict() and password helpers only.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId


def _str_id(doc):
    """Convert ObjectId _id to string 'id' field."""
    if doc and '_id' in doc:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return doc


# ── Helpers used by routes ──────────────────────────────────────────────────

def make_user(name, email, password, role='student'):
    return {
        'name': name,
        'email': email,
        'password': generate_password_hash(password),
        'role': role,
        'created_at': datetime.utcnow()
    }

def check_user_password(user_doc, password):
    return check_password_hash(user_doc['password'], password)

def user_to_dict(user_doc):
    return {
        'id': str(user_doc['_id']),
        'name': user_doc['name'],
        'email': user_doc['email'],
        'role': user_doc['role']
    }


def make_exam(title, description, instructions, examiner_id,
              duration, total_marks, passing_marks,
              negative_marking=0, is_published=False):
    return {
        'title': title,
        'description': description,
        'instructions': instructions,
        'examiner_id': examiner_id,
        'duration': duration,
        'total_marks': total_marks,
        'passing_marks': passing_marks,
        'negative_marking': negative_marking,
        'is_published': is_published,
        'is_active': True,
        'auto_delete_enabled': False,
        'auto_delete_date': None,
        'created_at': datetime.utcnow()
    }

def exam_to_dict(e):
    return {
        'id': str(e['_id']),
        'title': e['title'],
        'description': e.get('description'),
        'instructions': e.get('instructions'),
        'examiner_id': e['examiner_id'],
        'duration': e.get('duration'),
        'total_marks': e.get('total_marks'),
        'passing_marks': e.get('passing_marks'),
        'negative_marking': e.get('negative_marking', 0),
        'is_published': e.get('is_published', False),
        'is_active': e.get('is_active', True),
        'auto_delete_enabled': e.get('auto_delete_enabled', False),
        'auto_delete_date': e['auto_delete_date'].isoformat() if e.get('auto_delete_date') else None,
        'created_at': e['created_at'].isoformat() if e.get('created_at') else None
    }


def make_question(exam_id, question_text, option_a, option_b, option_c, option_d,
                  correct_answer, marks=1, question_type='mcq', order=0, explanation=None):
    return {
        'exam_id': exam_id,
        'question_text': question_text,
        'option_a': option_a,
        'option_b': option_b,
        'option_c': option_c,
        'option_d': option_d,
        'correct_answer': correct_answer,
        'marks': marks,
        'question_type': question_type,
        'order': order,
        'explanation': explanation
    }


def make_proctoring_session(student_id, exam_id, enrollment_id=None):
    return {
        'student_id': student_id,
        'exam_id': exam_id,
        'enrollment_id': enrollment_id,
        'current_trust_score': 100,
        'status': 'active',
        'camera_active': True,
        'mic_active': True,
        'screen_locked': True,
        'start_time': datetime.utcnow(),
        'end_time': None
    }

def session_to_dict(s):
    return {
        'id': str(s['_id']),
        'student_id': s['student_id'],
        'exam_id': s['exam_id'],
        'enrollment_id': s.get('enrollment_id'),
        'current_trust_score': s.get('current_trust_score', 100),
        'status': s.get('status', 'active'),
        'camera_active': s.get('camera_active', True),
        'mic_active': s.get('mic_active', True),
        'screen_locked': s.get('screen_locked', True),
        'start_time': s['start_time'].isoformat() if s.get('start_time') else None,
        'end_time': s['end_time'].isoformat() if s.get('end_time') else None
    }


def make_violation(student_id, exam_id, session_id, violation_type,
                   severity='medium', description=None, evidence_path=None,
                   trust_score_reduction=10):
    return {
        'student_id': student_id,
        'exam_id': exam_id,
        'session_id': session_id,
        'violation_type': violation_type,
        'severity': severity,
        'description': description,
        'evidence_path': evidence_path,
        'trust_score_reduction': trust_score_reduction,
        'created_at': datetime.utcnow()
    }

def violation_to_dict(v):
    return {
        'id': str(v['_id']),
        'student_id': v['student_id'],
        'exam_id': v['exam_id'],
        'session_id': v['session_id'],
        'violation_type': v.get('violation_type'),
        'severity': v.get('severity', 'medium'),
        'description': v.get('description'),
        'evidence_path': v.get('evidence_path'),
        'trust_score_reduction': v.get('trust_score_reduction', 10),
        'created_at': v['created_at'].isoformat() if v.get('created_at') else None
    }


def make_exam_result(student_id, exam_id, enrollment_id, obtained_marks, total_marks,
                     percentage, status='completed', violation_count=0,
                     final_trust_score=100, correct_answers=0, incorrect_answers=0,
                     unanswered=0, total_time_taken=None):
    now = datetime.utcnow()
    return {
        'student_id': student_id,
        'exam_id': exam_id,
        'enrollment_id': enrollment_id,
        'obtained_marks': obtained_marks,
        'total_marks': total_marks,
        'percentage': percentage,
        'status': status,
        'violation_count': violation_count,
        'final_trust_score': final_trust_score,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'unanswered': unanswered,
        'total_time_taken': total_time_taken,
        'submitted_at': now,
        'created_at': now,
        'reviewed_by': None,
        'reviewed_at': None,
        'remarks': None
    }


def make_notification(examiner_id, student_id, exam_id, message, severity_level='medium'):
    return {
        'examiner_id': examiner_id,
        'student_id': student_id,
        'exam_id': exam_id,
        'message': message,
        'severity_level': severity_level,
        'is_read': False,
        'created_at': datetime.utcnow()
    }

def notification_to_dict(n):
    return {
        'id': str(n['_id']),
        'examiner_id': n['examiner_id'],
        'student_id': n['student_id'],
        'exam_id': n['exam_id'],
        'message': n.get('message'),
        'severity_level': n.get('severity_level', 'medium'),
        'is_read': n.get('is_read', False),
        'created_at': n['created_at'].isoformat() if n.get('created_at') else None
    }


def make_analytics(session_id, student_id=None, exam_id=None):
    return {
        'session_id': session_id,
        'student_id': student_id,
        'exam_id': exam_id,
        'face_detected': True,
        'multiple_faces_detected': False,
        'phone_detected': False,
        'sound_detected': False,
        'tab_switch_detected': False,
        'gaze_direction': None,
        'head_movement': None,
        'trust_score_after_event': None,
        'eye_gaze_warnings': 0,
        'phone_detection_count': 0,
        'tab_switch_count': 0,
        'sound_detection_count': 0,
        'multiple_persons_detected': 0,
        'blur_exit_attempts': 0,
        'face_not_visible_count': 0,
        'head_movement_warnings': 0,
        'total_violations': 0,
        'created_at': datetime.utcnow()
    }

def analytics_to_dict(a):
    return {
        'id': str(a['_id']),
        'session_id': a['session_id'],
        'eye_gaze_warnings': a.get('eye_gaze_warnings', 0),
        'phone_detection_count': a.get('phone_detection_count', 0),
        'tab_switch_count': a.get('tab_switch_count', 0),
        'sound_detection_count': a.get('sound_detection_count', 0),
        'multiple_persons_detected': a.get('multiple_persons_detected', 0),
        'blur_exit_attempts': a.get('blur_exit_attempts', 0),
        'face_not_visible_count': a.get('face_not_visible_count', 0),
        'head_movement_warnings': a.get('head_movement_warnings', 0),
        'total_violations': a.get('total_violations', 0),
        'face_detected': a.get('face_detected', True),
        'multiple_faces_detected': a.get('multiple_faces_detected', False),
        'phone_detected': a.get('phone_detected', False),
        'sound_detected': a.get('sound_detected', False),
        'tab_switch_detected': a.get('tab_switch_detected', False),
        'gaze_direction': a.get('gaze_direction'),
        'head_movement': a.get('head_movement'),
        'trust_score_after_event': a.get('trust_score_after_event'),
        'created_at': a['created_at'].isoformat() if a.get('created_at') else None
    }
