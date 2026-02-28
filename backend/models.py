from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# ============================
# USER MODEL
# ============================

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    exams_created = db.relationship('Exam', backref='examiner', lazy=True)
    enrollments = db.relationship('ExamEnrollment', backref='student', lazy=True)
    results = db.relationship('ExamResult', backref='student_user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }


# ============================
# EXAM MODEL
# ============================

class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)

    examiner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    duration = db.Column(db.Integer)
    total_marks = db.Column(db.Integer)
    passing_marks = db.Column(db.Integer)

    negative_marking = db.Column(db.Float, default=0)
    is_published = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # Auto-deletion settings
    auto_delete_enabled = db.Column(db.Boolean, default=False)  # False = Forever, True = Custom date
    auto_delete_date = db.Column(db.DateTime, nullable=True)  # Date when exam should be deleted

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('ExamQuestion', backref='exam', lazy=True)
    enrollments = db.relationship('ExamEnrollment', backref='exam', lazy=True)
    results = db.relationship('ExamResult', backref='exam', lazy=True)


# ============================
# EXAM QUESTION
# ============================

class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)

    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255))
    option_b = db.Column(db.String(255))
    option_c = db.Column(db.String(255))
    option_d = db.Column(db.String(255))
    correct_answer = db.Column(db.String(10))

    marks = db.Column(db.Integer, default=1)
    question_type = db.Column(db.String(50), default="mcq")
    explanation = db.Column(db.Text)
    order = db.Column(db.Integer)


# ============================
# STUDENT ANSWER
# ============================

class StudentAnswer(db.Model):
    __tablename__ = 'student_answers'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('exam_questions.id'))
    selected_answer = db.Column(db.String(10))
    marks_awarded = db.Column(db.Float, default=0)


# ============================
# EXAM ENROLLMENT
# ============================

class ExamEnrollment(db.Model):
    __tablename__ = 'exam_enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))

    enrollment_status = db.Column(db.String(50), default="enrolled")
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================
# ACCEPTANCE FORM
# ============================

class AcceptanceForm(db.Model):
    __tablename__ = 'acceptance_forms'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    enrollment_id = db.Column(db.Integer)

    accepted = db.Column(db.Boolean, default=False)
    rules_accepted = db.Column(db.Boolean, default=False)
    honor_code_accepted = db.Column(db.Boolean, default=False)
    privacy_accepted = db.Column(db.Boolean, default=False)
    technical_requirements_met = db.Column(db.Boolean, default=False)

    trust_score = db.Column(db.Integer, default=100)
    acceptance_timestamp = db.Column(db.DateTime)


# ============================
# EXAM RESULT
# ============================

class ExamResult(db.Model):
    __tablename__ = 'exam_results'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))

    reviewed_by = db.Column(db.Integer)
    obtained_marks = db.Column(db.Float)
    total_marks = db.Column(db.Float)
    percentage = db.Column(db.Float)
    final_trust_score = db.Column(db.Integer, default=100)
    status = db.Column(db.String(50), default='completed')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================
# PROCTORING SESSION
# ============================

class ProctoringSession(db.Model):
    __tablename__ = 'proctoring_sessions'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    enrollment_id = db.Column(db.Integer)

    current_trust_score = db.Column(db.Integer, default=100)
    status = db.Column(db.String(50), default="active")

    camera_active = db.Column(db.Boolean, default=True)
    mic_active = db.Column(db.Boolean, default=True)
    screen_locked = db.Column(db.Boolean, default=True)

    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)


# ============================
# EXAMINER NOTIFICATION
# ============================

class ExaminerNotification(db.Model):
    __tablename__ = 'examiner_notifications'

    id = db.Column(db.Integer, primary_key=True)
    examiner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    message = db.Column(db.Text)
    severity_level = db.Column(db.String(20), default='medium')
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================
# VIOLATION LOG
# ============================

class ViolationLog(db.Model):
    __tablename__ = 'violations'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('proctoring_sessions.id'))

    violation_type = db.Column(db.String(100))
    severity = db.Column(db.String(20), default='medium')
    description = db.Column(db.Text)
    evidence_path = db.Column(db.String(255))
    trust_score_reduction = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # ============================
# SESSION ANALYTICS
# ============================

class SessionAnalytics(db.Model):
    __tablename__ = 'session_analytics'

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey('proctoring_sessions.id')
    )

    face_detected = db.Column(db.Boolean, default=True)
    multiple_faces_detected = db.Column(db.Boolean, default=False)
    phone_detected = db.Column(db.Boolean, default=False)
    sound_detected = db.Column(db.Boolean, default=False)
    tab_switch_detected = db.Column(db.Boolean, default=False)

    gaze_direction = db.Column(db.String(50))
    head_movement = db.Column(db.String(50))

    trust_score_after_event = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)