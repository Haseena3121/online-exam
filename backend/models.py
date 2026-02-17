"""
Complete SQLAlchemy database models
"""
from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
from enum import Enum

# Enums
class UserRole(str, Enum):
    STUDENT = 'student'
    EXAMINER = 'examiner'
    ADMIN = 'admin'

class ExamStatus(str, Enum):
    ENROLLED = 'enrolled'
    STARTED = 'started'
    SUBMITTED = 'submitted'
    COMPLETED = 'completed'

class ResultStatus(str, Enum):
    PASS = 'pass'
    FAIL = 'fail'
    AUTO_SUBMITTED = 'auto_submitted'

class SessionStatus(str, Enum):
    ACTIVE = 'active'
    PAUSED = 'paused'
    ENDED = 'ended'

class ViolationSeverity(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class QuestionType(str, Enum):
    MCQ = 'mcq'
    SHORT_ANSWER = 'short-answer'
    ESSAY = 'essay'

# ============ USER MODELS ============

class User(db.Model):
    """User model for students, examiners, and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='student', index=True)
    profile_picture = db.Column(db.String(500))
    bio = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    
    # Relationships
    exams_created = db.relationship('Exam', backref='examiner', lazy=True, foreign_keys='Exam.examiner_id', cascade='all, delete-orphan')
    enrollments = db.relationship('ExamEnrollment', backref='student', lazy=True, cascade='all, delete-orphan')
    proctoring_sessions = db.relationship('ProctoringSession', backref='student_user', lazy=True, cascade='all, delete-orphan')
    violations = db.relationship('ViolationLog', backref='student_user', lazy=True, cascade='all, delete-orphan')
    exam_results = db.relationship('ExamResult', backref='student_user', lazy=True, cascade='all, delete-orphan')
    acceptance_forms = db.relationship('AcceptanceForm', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verify password hash"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'profile_picture': self.profile_picture,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def to_full_dict(self):
        """Convert to full dictionary"""
        data = self.to_dict()
        data.update({
            'bio': self.bio,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        })
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'

# ============ EXAM MODELS ============

class Exam(db.Model):
    """Exam model"""
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    examiner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    total_marks = db.Column(db.Integer, nullable=False)
    passing_marks = db.Column(db.Integer, nullable=False)
    negative_marking = db.Column(db.Float, default=0)
    is_published = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    exam_code = db.Column(db.String(50), unique=True)
    category = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))  # easy, medium, hard
    
    # Relationships
    questions = db.relationship('ExamQuestion', backref='exam', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('ExamEnrollment', backref='exam', lazy=True, cascade='all, delete-orphan')
    acceptance_forms = db.relationship('AcceptanceForm', backref='exam', lazy=True, cascade='all, delete-orphan')
    proctoring_sessions = db.relationship('ProctoringSession', backref='exam', lazy=True, cascade='all, delete-orphan')
    violations = db.relationship('ViolationLog', backref='exam', lazy=True, cascade='all, delete-orphan')
    results = db.relationship('ExamResult', backref='exam', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('ExaminerNotification', backref='exam', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'instructions': self.instructions,
            'examiner_id': self.examiner_id,
            'duration': self.duration,
            'total_marks': self.total_marks,
            'passing_marks': self.passing_marks,
            'negative_marking': self.negative_marking,
            'is_published': self.is_published,
            'is_active': self.is_active,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'question_count': len(self.questions),
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Exam {self.title}>'

class ExamQuestion(db.Model):
    """Exam question model"""
    __tablename__ = 'exam_questions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500))
    option_b = db.Column(db.String(500))
    option_c = db.Column(db.String(500))
    option_d = db.Column(db.String(500))
    correct_answer = db.Column(db.String(1))
    marks = db.Column(db.Integer, nullable=False, default=1)
    question_type = db.Column(db.String(50), default='mcq')
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    order = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_answers = db.relationship('StudentAnswer', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_answer=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'exam_id': self.exam_id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'marks': self.marks,
            'question_type': self.question_type,
            'explanation': self.explanation,
            'difficulty': self.difficulty,
            'order': self.order,
            'image_url': self.image_url
        }
        if include_answer:
            data['correct_answer'] = self.correct_answer
        return data
    
    def __repr__(self):
        return f'<ExamQuestion {self.id}>'

# ============ ENROLLMENT MODELS ============

class ExamEnrollment(db.Model):
    """Student exam enrollment"""
    __tablename__ = 'exam_enrollments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, index=True)
    enrollment_status = db.Column(db.String(20), default='enrolled', index=True)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_accessed = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'exam_id', name='unique_enrollment'),)
    
    # Relationships
    proctoring_session = db.relationship('ProctoringSession', uselist=False, backref='enrollment_ref', cascade='all, delete-orphan')
    exam_result = db.relationship('ExamResult', uselist=False, backref='enrollment_ref', cascade='all, delete-orphan')
    acceptance_form = db.relationship('AcceptanceForm', uselist=False, backref='enrollment_ref', cascade='all, delete-orphan')
    student_answers = db.relationship('StudentAnswer', backref='enrollment', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'exam_id': self.exam_id,
            'enrollment_status': self.enrollment_status,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ExamEnrollment {self.student_id}-{self.exam_id}>'

class AcceptanceForm(db.Model):
    """Exam acceptance form"""
    __tablename__ = 'acceptance_forms'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, index=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('exam_enrollments.id'))
    accepted = db.Column(db.Boolean, default=False)
    rules_accepted = db.Column(db.Boolean, default=False)
    honor_code_accepted = db.Column(db.Boolean, default=False)
    privacy_accepted = db.Column(db.Boolean, default=False)
    technical_requirements_met = db.Column(db.Boolean, default=False)
    trust_score = db.Column(db.Integer, default=100)
    acceptance_ip = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    acceptance_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'exam_id', name='unique_acceptance'),)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'exam_id': self.exam_id,
            'accepted': self.accepted,
            'rules_accepted': self.rules_accepted,
            'honor_code_accepted': self.honor_code_accepted,
            'privacy_accepted': self.privacy_accepted,
            'technical_requirements_met': self.technical_requirements_met,
            'trust_score': self.trust_score,
            'acceptance_timestamp': self.acceptance_timestamp.isoformat() if self.acceptance_timestamp else None
        }
    
    def __repr__(self):
        return f'<AcceptanceForm {self.id}>'

# ============ PROCTORING MODELS ============

class ProctoringSession(db.Model):
    """Proctoring session"""
    __tablename__ = 'proctoring_sessions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, index=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('exam_enrollments.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    current_trust_score = db.Column(db.Integer, default=100)
    status = db.Column(db.String(20), default='active', index=True)
    final_status = db.Column(db.String(20))
    camera_active = db.Column(db.Boolean, default=True)
    mic_active = db.Column(db.Boolean, default=True)
    screen_locked = db.Column(db.Boolean, default=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    browser_info = db.Column(db.JSON)
    
    # Relationships
    violations = db.relationship('ViolationLog', backref='session', lazy=True, cascade='all, delete-orphan')
    analytics = db.relationship('SessionAnalytics', uselist=False, backref='session_ref', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'exam_id': self.exam_id,
            'enrollment_id': self.enrollment_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'current_trust_score': self.current_trust_score,
            'status': self.status,
            'final_status': self.final_status,
            'camera_active': self.camera_active,
            'mic_active': self.mic_active,
            'screen_locked': self.screen_locked,
            'duration_minutes': int((self.end_time - self.start_time).total_seconds() / 60) if self.end_time else None
        }
    
    def __repr__(self):
        return f'<ProctoringSession {self.id}>'

class ViolationLog(db.Model):
    """Violation log"""
    __tablename__ = 'violations_log'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('proctoring_sessions.id'), nullable=False)
    violation_type = db.Column(db.String(100), nullable=False, index=True)
    severity = db.Column(db.String(20), default='medium')
    trust_score_reduction = db.Column(db.Integer, default=10)
    description = db.Column(db.Text)
    screenshot_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    additional_data = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_notified = db.Column(db.Boolean, default=False)
    
    # Relationships
    notifications = db.relationship('ExaminerNotification', backref='violation', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'violation_type': self.violation_type,
            'severity': self.severity,
            'trust_score_reduction': self.trust_score_reduction,
            'description': self.description,
            'screenshot_url': self.screenshot_url,
            'video_url': self.video_url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'is_notified': self.is_notified
        }
    
    def __repr__(self):
        return f'<ViolationLog {self.id}>'

class ExaminerNotification(db.Model):
    """Examiner notification"""
    __tablename__ = 'examiner_notifications'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    examiner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    violation_id = db.Column(db.Integer, db.ForeignKey('violations_log.id'))
    message = db.Column(db.Text, nullable=False)
    proof_type = db.Column(db.String(20), default='alert')
    proof_url = db.Column(db.String(500))
    is_read = db.Column(db.Boolean, default=False, index=True)
    severity_level = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    examiner = db.relationship('User', foreign_keys=[examiner_id], backref='notifications_received')
    reported_student = db.relationship('User', foreign_keys=[student_id], backref='violations_reported')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'examiner_id': self.examiner_id,
            'student_id': self.student_id,
            'exam_id': self.exam_id,
            'message': self.message,
            'proof_type': self.proof_type,
            'proof_url': self.proof_url,
            'is_read': self.is_read,
            'severity_level': self.severity_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ExaminerNotification {self.id}>'

class StudentAnswer(db.Model):
    """Student answer"""
    __tablename__ = 'student_answers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('exam_enrollments.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('exam_questions.id'), nullable=False)
    selected_answer = db.Column(db.String(500))
    is_correct = db.Column(db.Boolean)
    marks_obtained = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer)  # in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_correct=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'question_id': self.question_id,
            'selected_answer': self.selected_answer,
            'marks_obtained': self.marks_obtained,
            'time_spent': self.time_spent
        }
        if include_correct:
            data['is_correct'] = self.is_correct
        return data
    
    def __repr__(self):
        return f'<StudentAnswer {self.id}>'

# ============ RESULT MODELS ============

class ExamResult(db.Model):
    """Exam result"""
    __tablename__ = 'exam_results'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('exam_enrollments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, index=True)
    obtained_marks = db.Column(db.Integer, default=0)
    total_marks = db.Column(db.Integer)
    percentage = db.Column(db.Float)
    status = db.Column(db.String(20), default='auto_submitted', index=True)
    violation_count = db.Column(db.Integer, default=0)
    final_trust_score = db.Column(db.Integer, default=100)
    total_time_taken = db.Column(db.Integer)  # in minutes
    correct_answers = db.Column(db.Integer, default=0)
    incorrect_answers = db.Column(db.Integer, default=0)
    unanswered = db.Column(db.Integer, default=0)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)
    remarks = db.Column(db.Text)
    
    # Relationships
    enrollment = db.relationship('ExamEnrollment', backref='exam_result_ref')
    student = db.relationship('User', foreign_keys=[student_id], backref='exam_results_ref')
    exam = db.relationship('Exam', foreign_keys=[exam_id], backref='exam_results_ref')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'exam_id': self.exam_id,
            'obtained_marks': self.obtained_marks,
            'total_marks': self.total_marks,
            'percentage': round(self.percentage, 2) if self.percentage else 0,
            'status': self.status,
            'violation_count': self.violation_count,
            'final_trust_score': self.final_trust_score,
            'total_time_taken': self.total_time_taken,
            'correct_answers': self.correct_answers,
            'incorrect_answers': self.incorrect_answers,
            'unanswered': self.unanswered,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }
    
    def __repr__(self):
        return f'<ExamResult {self.id}>'

class SessionAnalytics(db.Model):
    """Session analytics"""
    __tablename__ = 'session_analytics'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.Integer, db.ForeignKey('proctoring_sessions.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    eye_gaze_warnings = db.Column(db.Integer, default=0)
    phone_detection_count = db.Column(db.Integer, default=0)
    tab_switch_count = db.Column(db.Integer, default=0)
    sound_detection_count = db.Column(db.Integer, default=0)
    multiple_persons_detected = db.Column(db.Integer, default=0)
    blur_exit_attempts = db.Column(db.Integer, default=0)
    face_not_visible_count = db.Column(db.Integer, default=0)
    head_movement_warnings = db.Column(db.Integer, default=0)
    suspicious_movement = db.Column(db.Integer, default=0)
    low_light_detected = db.Column(db.Integer, default=0)
    total_violations = db.Column(db.Integer, default=0)
    average_trust_score = db.Column(db.Float, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    session = db.relationship('ProctoringSession', backref='analytics_ref')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'session_id': self.session_id,
            'eye_gaze_warnings': self.eye_gaze_warnings,
            'phone_detection_count': self.phone_detection_count,
            'tab_switch_count': self.tab_switch_count,
            'sound_detection_count': self.sound_detection_count,
            'multiple_persons_detected': self.multiple_persons_detected,
            'blur_exit_attempts': self.blur_exit_attempts,
            'face_not_visible_count': self.face_not_visible_count,
            'head_movement_warnings': self.head_movement_warnings,
            'suspicious_movement': self.suspicious_movement,
            'low_light_detected': self.low_light_detected,
            'total_violations': self.total_violations,
            'average_trust_score': round(self.average_trust_score, 2) if self.average_trust_score else 100
        }
    
    def __repr__(self):
        return f'<SessionAnalytics {self.id}>'

# ============ AUDIT MODELS ============

class AuditLog(db.Model):
    """Audit log for tracking changes"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255), nullable=False)
    table_name = db.Column(db.String(100))
    record_id = db.Column(db.Integer)
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<AuditLog {self.id}>'