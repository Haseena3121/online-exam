"""
Application constants
"""

VIOLATION_TYPES = {
    'PHONE_DETECTED': 'phone_detected',
    'TAB_SWITCH': 'tab_switch',
    'EYE_GAZE': 'eye_gaze_suspicious',
    'MULTIPLE_PERSONS': 'multiple_persons',
    'SOUND': 'sound_detected',
    'BLUR_EXIT': 'blur_exit_attempt',
    'FACE_NOT_VISIBLE': 'face_not_visible',
    'HEAD_MOVEMENT': 'extreme_head_movement',
}

SEVERITY_LEVELS = {
    'LOW': 'low',
    'MEDIUM': 'medium',
    'HIGH': 'high'
}

EXAM_STATUS = {
    'ENROLLED': 'enrolled',
    'STARTED': 'started',
    'SUBMITTED': 'submitted',
    'COMPLETED': 'completed'
}

RESULT_STATUS = {
    'PASS': 'pass',
    'FAIL': 'fail',
    'AUTO_SUBMITTED': 'auto_submitted'
}

ROLES = {
    'STUDENT': 'student',
    'EXAMINER': 'examiner',
    'ADMIN': 'admin'
}

TRUST_SCORE_THRESHOLDS = {
    'CRITICAL': 50,
    'WARNING': 75,
    'NORMAL': 100
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB