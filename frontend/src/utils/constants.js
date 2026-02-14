export const VIOLATION_TYPES = {
  PHONE_DETECTED: 'phone_detected',
  TAB_SWITCH: 'tab_switch',
  EYE_GAZE_SUSPICIOUS: 'eye_gaze_suspicious',
  MULTIPLE_PERSONS: 'multiple_persons',
  SOUND_DETECTED: 'sound_detected',
  BLUR_EXIT_ATTEMPT: 'blur_exit_attempt',
  FACE_NOT_VISIBLE: 'face_not_visible',
  EXTREME_HEAD_MOVEMENT: 'extreme_head_movement',
  PERSON_LEFT_SEAT: 'person_left_seat',
  OTHER_PERSON_DETECTED: 'other_person_detected',
  SUSPICIOUS_MOVEMENT: 'suspicious_movement',
  LOW_LIGHT_DETECTED: 'low_light_detected'
};

export const SEVERITY_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high'
};

export const SEVERITY_REDUCTION = {
  low: 5,
  medium: 10,
  high: 20
};

export const EXAM_STATUS = {
  ENROLLED: 'enrolled',
  STARTED: 'started',
  SUBMITTED: 'submitted',
  COMPLETED: 'completed'
};

export const RESULT_STATUS = {
  PASS: 'pass',
  FAIL: 'fail',
  AUTO_SUBMITTED: 'auto_submitted'
};

export const ROLES = {
  STUDENT: 'student',
  EXAMINER: 'examiner',
  ADMIN: 'admin'
};

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    ME: '/auth/me',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh-token'
  },
  EXAMS: {
    GET_ALL: '/exams',
    GET_BY_ID: '/exams/:id',
    CREATE: '/exams',
    ADD_QUESTION: '/exams/:id/questions',
    MY_EXAMS: '/exams/my-exams',
    ENROLL: '/exams/:id/enroll',
    ACCEPTANCE_FORM: '/exams/:id/acceptance-form',
    START: '/exams/:id/start'
  },
  PROCTORING: {
    REPORT_VIOLATION: '/proctoring/violation',
    SESSION_STATUS: '/proctoring/session/:id',
    WARNING: '/proctoring/session/:id/warning',
    SUBMIT: '/proctoring/submit',
    ANALYTICS: '/proctoring/analytics/:id'
  },
  VIOLATIONS: {
    HISTORY: '/violations/history/:id',
    BY_EXAM: '/violations/by-exam/:id',
    DETAILS: '/violations/:id'
  },
  RESULTS: {
    GET: '/results/:id',
    ALL: '/results/all',
    DETAILED: '/results/detailed/:id',
    EXAM_RESULTS: '/results/exam/:id/all-students'
  }
};

export const TRUST_SCORE_THRESHOLDS = {
  CRITICAL: 50,
  WARNING: 75,
  NORMAL: 100
};

export const DETECTION_INTERVALS = {
  FACE_DETECTION: 1000, // 1 second
  PHONE_DETECTION: 2000, // 2 seconds
  BRIGHTNESS_CHECK: 3000, // 3 seconds
  HEAD_MOVEMENT: 2000 // 2 seconds
};