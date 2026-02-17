-- ============================================
-- ONLINE EXAM PROCTORING SYSTEM - SCHEMA
-- ============================================

-- Create Database
CREATE DATABASE IF NOT EXISTS online_exam_proctoring;
USE online_exam_proctoring;

-- ============ USERS TABLE ============
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('student', 'examiner', 'admin') NOT NULL DEFAULT 'student',
    profile_picture VARCHAR(500),
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    last_login DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_is_active (is_active),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ EXAMS TABLE ============
CREATE TABLE IF NOT EXISTS exams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT,
    examiner_id INT NOT NULL,
    duration INT NOT NULL,
    total_marks INT NOT NULL,
    passing_marks INT NOT NULL,
    negative_marking FLOAT DEFAULT 0,
    is_published BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    start_time DATETIME,
    end_time DATETIME,
    exam_code VARCHAR(50) UNIQUE,
    category VARCHAR(100),
    difficulty_level VARCHAR(20),
    FOREIGN KEY (examiner_id) REFERENCES users(id),
    INDEX idx_examiner_id (examiner_id),
    INDEX idx_title (title),
    INDEX idx_is_published (is_published),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ EXAM QUESTIONS TABLE ============
CREATE TABLE IF NOT EXISTS exam_questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exam_id INT NOT NULL,
    question_text LONGTEXT NOT NULL,
    option_a VARCHAR(500),
    option_b VARCHAR(500),
    option_c VARCHAR(500),
    option_d VARCHAR(500),
    correct_answer VARCHAR(1),
    marks INT NOT NULL DEFAULT 1,
    question_type VARCHAR(50) DEFAULT 'mcq',
    explanation LONGTEXT,
    difficulty VARCHAR(20),
    `order` INT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
    INDEX idx_exam_id (exam_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ EXAM ENROLLMENTS TABLE ============
CREATE TABLE IF NOT EXISTS exam_enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    enrollment_status VARCHAR(20) DEFAULT 'enrolled',
    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_accessed DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_enrollment (student_id, exam_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    INDEX idx_student_id (student_id),
    INDEX idx_exam_id (exam_id),
    INDEX idx_status (enrollment_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ ACCEPTANCE FORMS TABLE ============
CREATE TABLE IF NOT EXISTS acceptance_forms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    enrollment_id INT,
    accepted BOOLEAN DEFAULT FALSE,
    rules_accepted BOOLEAN DEFAULT FALSE,
    honor_code_accepted BOOLEAN DEFAULT FALSE,
    privacy_accepted BOOLEAN DEFAULT FALSE,
    technical_requirements_met BOOLEAN DEFAULT FALSE,
    trust_score INT DEFAULT 100,
    acceptance_ip VARCHAR(45),
    user_agent VARCHAR(500),
    acceptance_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_acceptance (student_id, exam_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (enrollment_id) REFERENCES exam_enrollments(id),
    INDEX idx_student_id (student_id),
    INDEX idx_exam_id (exam_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ PROCTORING SESSIONS TABLE ============
CREATE TABLE IF NOT EXISTS proctoring_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    enrollment_id INT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    current_trust_score INT DEFAULT 100,
    status VARCHAR(20) DEFAULT 'active',
    final_status VARCHAR(20),
    camera_active BOOLEAN DEFAULT TRUE,
    mic_active BOOLEAN DEFAULT TRUE,
    screen_locked BOOLEAN DEFAULT TRUE,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    browser_info JSON,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (enrollment_id) REFERENCES exam_enrollments(id),
    INDEX idx_student_id (student_id),
    INDEX idx_exam_id (exam_id),
    INDEX idx_status (status),
    INDEX idx_start_time (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ VIOLATIONS LOG TABLE ============
CREATE TABLE IF NOT EXISTS violations_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    session_id INT NOT NULL,
    violation_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium',
    trust_score_reduction INT DEFAULT 10,
    description LONGTEXT,
    screenshot_url VARCHAR(500),
    video_url VARCHAR(500),
    additional_data JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_notified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (session_id) REFERENCES proctoring_sessions(id),
    INDEX idx_student_id (student_id),
    INDEX idx_exam_id (exam_id),
    INDEX idx_session_id (session_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_violation_type (violation_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ EXAMINER NOTIFICATIONS TABLE ============
CREATE TABLE IF NOT EXISTS examiner_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    examiner_id INT NOT NULL,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    violation_id INT,
    message LONGTEXT NOT NULL,
    proof_type VARCHAR(20) DEFAULT 'alert',
    proof_url VARCHAR(500),
    is_read BOOLEAN DEFAULT FALSE,
    severity_level VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (examiner_id) REFERENCES users(id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (violation_id) REFERENCES violations_log(id),
    INDEX idx_examiner_id (examiner_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ STUDENT ANSWERS TABLE ============
CREATE TABLE IF NOT EXISTS student_answers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    enrollment_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_answer VARCHAR(500),
    is_correct BOOLEAN,
    marks_obtained INT DEFAULT 0,
    time_spent INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (enrollment_id) REFERENCES exam_enrollments(id),
    FOREIGN KEY (question_id) REFERENCES exam_questions(id),
    INDEX idx_enrollment_id (enrollment_id),
    INDEX idx_question_id (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ EXAM RESULTS TABLE ============
CREATE TABLE IF NOT EXISTS exam_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    enrollment_id INT NOT NULL,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    obtained_marks INT DEFAULT 0,
    total_marks INT,
    percentage FLOAT,
    status VARCHAR(20) DEFAULT 'auto_submitted',
    violation_count INT DEFAULT 0,
    final_trust_score INT DEFAULT 100,
    total_time_taken INT,
    correct_answers INT DEFAULT 0,
    incorrect_answers INT DEFAULT 0,
    unanswered INT DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_by INT,
    reviewed_at DATETIME,
    remarks LONGTEXT,
    FOREIGN KEY (enrollment_id) REFERENCES exam_enrollments(id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    INDEX idx_student_id (student_id),
    INDEX idx_exam_id (exam_id),
    INDEX idx_status (status),
    INDEX idx_submitted_at (submitted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ SESSION ANALYTICS TABLE ============
CREATE TABLE IF NOT EXISTS session_analytics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    eye_gaze_warnings INT DEFAULT 0,
    phone_detection_count INT DEFAULT 0,
    tab_switch_count INT DEFAULT 0,
    sound_detection_count INT DEFAULT 0,
    multiple_persons_detected INT DEFAULT 0,
    blur_exit_attempts INT DEFAULT 0,
    face_not_visible_count INT DEFAULT 0,
    head_movement_warnings INT DEFAULT 0,
    suspicious_movement INT DEFAULT 0,
    low_light_detected INT DEFAULT 0,
    total_violations INT DEFAULT 0,
    average_trust_score FLOAT DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES proctoring_sessions(id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    INDEX idx_session_id (session_id),
    INDEX idx_student_id (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ AUDIT LOGS TABLE ============
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    table_name VARCHAR(100),
    record_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_action (action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ CREATE VIEWS ============

-- View for exam statistics
CREATE OR REPLACE VIEW exam_statistics AS
SELECT 
    e.id,
    e.title,
    COUNT(DISTINCT ee.id) as total_enrolled,
    COUNT(DISTINCT er.id) as total_submitted,
    COUNT(DISTINCT CASE WHEN er.status = 'pass' THEN er.id END) as total_passed,
    COUNT(DISTINCT CASE WHEN er.status = 'fail' THEN er.id END) as total_failed,
    AVG(er.percentage) as average_percentage,
    MAX(er.percentage) as highest_score,
    MIN(er.percentage) as lowest_score
FROM exams e
LEFT JOIN exam_enrollments ee ON e.id = ee.exam_id
LEFT JOIN exam_results er ON ee.id = er.enrollment_id
GROUP BY e.id;

-- View for student statistics
CREATE OR REPLACE VIEW student_statistics AS
SELECT 
    u.id,
    u.name,
    COUNT(DISTINCT ee.id) as total_exams,
    COUNT(DISTINCT CASE WHEN er.status = 'pass' THEN er.id END) as passed,
    COUNT(DISTINCT CASE WHEN er.status = 'fail' THEN er.id END) as failed,
    AVG(er.percentage) as average_percentage,
    COUNT(DISTINCT vl.id) as total_violations
FROM users u
LEFT JOIN exam_enrollments ee ON u.id = ee.student_id
LEFT JOIN exam_results er ON ee.id = er.enrollment_id
LEFT JOIN violations_log vl ON u.id = vl.student_id
WHERE u.role = 'student'
GROUP BY u.id;

-- ============ CREATE INDEXES ============
CREATE INDEX idx_users_email_role ON users(email, role);
CREATE INDEX idx_exams_examiner_published ON exams(examiner_id, is_published);
CREATE INDEX idx_enrollments_status ON exam_enrollments(enrollment_status);
CREATE INDEX idx_violations_severity ON violations_log(severity);
CREATE INDEX idx_results_percentage ON exam_results(percentage);

-- ============ CREATE TRIGGERS ============

-- Trigger to update user last_login
DELIMITER $$
CREATE TRIGGER update_last_login
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = NEW.id;
END$$
DELIMITER ;

-- Trigger to maintain exam enrollment status consistency
DELIMITER $$
CREATE TRIGGER check_enrollment_status
BEFORE INSERT ON exam_enrollments
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = NEW.student_id AND role = 'student') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student not found';
    END IF;
END$$
DELIMITER ;