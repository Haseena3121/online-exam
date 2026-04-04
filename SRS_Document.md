# Software Requirements Specification (SRS)
## Online Exam Proctoring System

---

## Table of Contents

1. Introduction
   - 1.1 Purpose
   - 1.2 Document Conventions
   - 1.3 Intended Audience and Reading Suggestions
   - 1.4 Product Scope
   - 1.5 References
2. Overall Description
   - 2.1 Product Perspective
   - 2.2 Product Functions
   - 2.3 User Classes and Characteristics
   - 2.4 Operating Environment
   - 2.5 Design and Implementation Constraints
   - 2.6 User Documentation
   - 2.7 Assumptions and Dependencies
3. External Interface Requirements
   - 3.1 User Interfaces
   - 3.2 Hardware Interfaces
   - 3.3 Software Interfaces
   - 3.4 Communications Interfaces
4. System Features
   - 4.1 User Authentication and Authorization
   - 4.2 Exam Management
   - 4.3 AI-Powered Proctoring
   - 4.4 Violation Detection and Reporting
   - 4.5 Real-time Monitoring
   - 4.6 Results and Analytics
5. Other Nonfunctional Requirements
   - 5.1 Performance Requirements
   - 5.2 Safety Requirements
   - 5.3 Security Requirements
   - 5.4 Software Quality Attributes
   - 5.5 Business Rules
6. Other Requirements

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification document describes the Online Exam Proctoring System, an AI-powered platform for secure online examinations. The document establishes clear functional and non-functional requirements for design, development, testing, and deployment phases.

The system provides user authentication, exam creation and management, real-time AI-based proctoring, violation detection, automated evidence collection, and comprehensive analytics. This document ensures all stakeholders have a unified understanding of system capabilities and operations.

### 1.2 Document Conventions

This document follows IEEE Standard 830-1998 for Software Requirements Specifications. The modal verb "shall" indicates mandatory requirements while "should" indicates desirable features.

Priority levels are assigned as: High (critical for system operation, must be in first release), Medium (important but can be deferred), and Low (desirable enhancements). Technical terms are defined upon first use. Database fields, API endpoints, and code references use monospace formatting.

### 1.3 Intended Audience and Reading Suggestions

Software developers should focus on Sections 3 and 4 for technical specifications and implementation details. Project managers should review Sections 1, 2, and 5 for scope, timeline, and quality attributes.

QA teams should concentrate on Sections 4 and 5 for functional requirements and acceptance criteria. Examiners and administrators should read Sections 2 and 4 to understand system capabilities and workflows. Students should review Section 2.3 and relevant portions of Section 4 for their role and expectations.

System administrators should focus on Sections 2.4, 2.5, and 3.3 for deployment requirements and infrastructure needs.

### 1.4 Product Scope

The Online Exam Proctoring System is a web-based platform leveraging AI and computer vision for secure online examinations. It addresses the need for remote assessment solutions that maintain academic integrity while providing flexibility.

The platform consists of three components: a React frontend for intuitive user interfaces, a Python Flask backend for business logic and data management, and AI models for real-time video, audio, and behavioral analysis.

Key capabilities include user registration with role-based authentication, comprehensive exam creation tools, real-time monitoring with AI analysis, automated violation detection (face detection, multiple persons, phone usage, head movements, eye gaze, audio patterns), automatic evidence capture, real-time alerts, automatic exam submission, detailed violation reports, and analytics dashboards.

The system scales to support hundreds of concurrent exam sessions with low latency and seamless user experience across desktop and laptop devices.

### 1.5 References

This document references IEEE Standard 830-1998, React 17.x Documentation, Flask 2.x Documentation, OpenCV 4.x Documentation, MediaPipe Framework, PostgreSQL 13.x Documentation, Redis Documentation, Celery Documentation, Docker Documentation, WCAG 2.1 Guidelines, OWASP Top 10, and RESTful API Design Principles.

Additional references include academic research on automated proctoring systems, computer vision-based behavior analysis, and ethical considerations in AI-powered educational surveillance.

---

## 2. Overall Description

### 2.1 Product Perspective

The system is a standalone web application with a three-tier architecture: presentation layer (React frontend), application layer (Flask backend with RESTful APIs), and data layer (PostgreSQL with Redis caching).

It interfaces with client hardware (webcams, microphones) through browser APIs. The backend integrates AI frameworks including OpenCV, MediaPipe, and TensorFlow for violation detection. Celery with Redis handles asynchronous video processing.

The application is containerized using Docker for consistent deployment. Nginx handles load balancing, SSL termination, and static file serving. The system can be self-hosted or offered as SaaS.

### 2.2 Product Functions

User management includes registration with role assignment, JWT-based authentication, profile management, and password recovery.

Exam management allows examiners to create exams with configurable parameters, define questions (multiple choice, true/false, short answer), configure violation thresholds, schedule exams, and manage lifecycle states.

Proctoring functionality provides real-time video streaming with AI analysis for face detection, multiple person detection, phone detection, head movement tracking, eye gaze estimation, background analysis, and audio monitoring.

Violation management includes automatic detection with severity levels, real-time evidence capture, timestamped logs, examiner notifications, configurable thresholds for warnings or termination, and comprehensive reports.

Results and analytics provide automatic grading, manual grading interfaces, performance reports, examiner dashboards, historical analytics, and evidence review with playback capabilities.

### 2.3 User Classes and Characteristics

Students are the largest user group with varying technical expertise. They register accounts, browse exams, accept terms, complete timed examinations under monitoring, and view results. They need user-friendly interfaces with clear instructions and require computers with webcams, microphones, and stable internet.

Examiners possess intermediate to advanced technical skills. They create and configure exams, schedule sessions, monitor active exams through dashboards, review violations and evidence, grade responses, and analyze performance metrics. They require powerful administrative tools and comprehensive reporting.

Administrators have advanced technical skills and manage user accounts, configure system settings, monitor system health, manage data retention policies, handle technical support, and ensure compliance. They require full system access and detailed monitoring tools.

### 2.4 Operating Environment

Client requirements include modern browsers (Chrome 90+, Firefox 88+, Edge 90+, Safari 14+) with JavaScript enabled. Hardware needs include Intel Core i3 or equivalent, 4GB RAM minimum, 720p webcam, microphone, 2 Mbps upload/5 Mbps download internet, and 1280x720 display resolution.

Server requirements include Linux-based servers (Ubuntu 20.04 LTS or CentOS 8), Docker and Docker Compose, Python 3.8+, Flask, PostgreSQL 13.x, Redis 6.x, Celery, and Nginx. GPU acceleration is recommended for production environments.

Storage requirements are approximately 500MB to 2GB per exam session. Cloud deployment is supported on AWS, Google Cloud Platform, or Azure.

### 2.5 Design and Implementation Constraints

Privacy regulations (GDPR, FERPA) impose strict requirements on data collection, storage, processing, and retention. The system must implement explicit consent, data access and deletion capabilities, encryption, and audit logs.

Accessibility requirements mandate WCAG 2.1 Level AA compliance. Browser compatibility limits use of cutting-edge technologies. Real-time processing requires AI models to analyze frames with minimal latency (1-2 fps minimum).

Scalability requires support for hundreds of concurrent sessions through horizontal scaling and asynchronous processing. Network bandwidth limitations require adaptive streaming. Security constraints mandate industry-standard practices against common vulnerabilities.

Ethical considerations include transparency about monitoring, fairness in AI models, and appropriate human oversight. Technology stack uses open-source frameworks to minimize costs. Budget constraints influence infrastructure and feature scope decisions.


### 2.6 User Documentation

Student documentation includes a user guide with registration, system requirements, webcam/microphone testing, exam enrollment, acceptance process, exam interface navigation, monitored behaviors, technical issue handling, and results viewing. Video tutorials demonstrate the exam process and troubleshooting. FAQs address privacy concerns and technical issues.

Examiner documentation covers account setup, exam creation with detailed parameters, question management, exam scheduling, real-time monitoring dashboard usage, violation review, grading, and analytics interpretation. Advanced topics include violation threshold best practices and dispute handling.

Administrator documentation provides installation and deployment instructions, database setup, system configuration, user management, performance monitoring, backup procedures, troubleshooting, and security best practices.

API documentation includes endpoint specifications, authentication, request/response formats, error codes, and code examples. All documentation is available in web-based and PDF formats, version-controlled, and updated with each release.

### 2.7 Assumptions and Dependencies

The system assumes students have appropriate hardware (webcam, microphone, computer) and stable internet connections. Students will use supported browsers with JavaScript enabled and grant necessary permissions. Students will comply with exam rules and understand violation consequences.

Examiners have technical competence to create exams and interpret reports. The deployment environment provides adequate computational resources and reliable network infrastructure.

The system depends on third-party libraries (React, Flask, OpenCV, MediaPipe, TensorFlow, PostgreSQL, Redis) and their continued stability. Browser APIs for media device access must remain available and compatible.

AI model accuracy depends on training data quality and periodic retraining. Institutional policies regarding online proctoring and data privacy must align with system capabilities. Technical support resources must be available during exam sessions. Regular maintenance including updates, patches, and backups is required.

---

## 3. External Interface Requirements

### 3.1 User Interfaces

The Student Interface includes a clean login/registration page with validation, a dashboard displaying available exams in card layout, an Acceptance Form outlining proctoring requirements and consent, and an Exam Interface with countdown timer, question navigation panel, current question display, and webcam preview. Violation warnings appear as non-intrusive notifications. A Results page shows scores, pass/fail status, and violation summaries.

The Examiner Interface provides an Exam Management page listing all exams with create/edit/delete options. The Exam Creation interface includes metadata forms, question builder with multiple types, proctoring configuration settings, and preview functionality. The Real-time Monitoring Dashboard displays a grid of live video feeds with status indicators, violations panel with real-time alerts, and filtering options. The Violation Review interface shows student lists with violation counts, detailed reports with timestamps and evidence, and playback controls. The Results and Analytics page provides statistical summaries, comparative analytics, and exportable reports.

The Administrator Interface includes User Management with searchable tables and role assignment, System Configuration with settings forms, and System Monitoring displaying real-time metrics and error logs.

All interfaces are responsive with consistent navigation, color schemes, and typography. Accessibility features include keyboard navigation, ARIA labels, color contrast, and focus indicators.

### 3.2 Hardware Interfaces

The system interfaces with webcams through WebRTC getUserMedia API, requesting 640x480 minimum (1280x720 preferred) resolution at 15-30 fps. Video streams are processed frame-by-frame by backend AI models. The system handles various webcam types with automatic adaptation and error handling for access denial or malfunctions.

Microphone interface captures audio at 16kHz+ sample rate with echo cancellation and noise suppression. Audio is analyzed for unusual sounds, multiple voices, or communication attempts. Various microphone types are supported.

Standard input devices (keyboard, mouse) are monitored through browser events for unusual patterns like rapid application switching or copy-paste operations.

Display requirements include 1280x720 minimum resolution with responsive layout adaptation. Server-side hardware includes network interfaces, storage interfaces (local disk, NAS, SAN), and optional GPU interfaces for accelerated AI inference through CUDA-enabled GPUs.

### 3.3 Software Interfaces

The frontend uses React 17.x with React Router, Context API, and Axios for HTTP requests. It communicates with the backend through RESTful API over HTTPS using JSON format. Authentication uses JWT tokens in Authorization headers.

The backend uses Flask 2.x with extensions: Flask-CORS, Flask-JWT-Extended, Flask-SQLAlchemy, and Flask-Migrate. It interfaces with PostgreSQL 13.x through SQLAlchemy ORM with connection pooling and parameterized queries.

Redis 6.x is used for session storage, caching, and as Celery message broker, accessed through redis-py. Celery handles asynchronous tasks including video analysis, evidence storage, email notifications, and scheduled tasks.

AI libraries include OpenCV for image processing, MediaPipe for face detection and pose estimation, TensorFlow for deep learning models, and NumPy for numerical operations.

File system storage supports local and cloud storage (AWS S3, Azure Blob, Google Cloud Storage). Email uses SMTP through smtplib or Flask-Mail with Jinja2 templates.

Nginx handles SSL/TLS termination, static file serving, load balancing, and rate limiting. Docker provides containerization with docker-compose for multi-container orchestration.

Logging integrates with Python's logging module and can connect to ELK Stack, CloudWatch, or APM tools like New Relic. Dependencies are versioned in requirements.txt and package.json.

### 3.4 Communications Interfaces

All client-server communication uses HTTPS with TLS 1.2+ for encryption. SSL/TLS certificates are from trusted authorities or Let's Encrypt. HSTS headers enforce secure connections. HTTP/1.1 is primary with HTTP/2 support.

RESTful API uses standard HTTP methods (GET, POST, PUT, DELETE) with JSON payloads. Status codes include 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error, and 503 Service Unavailable.

Authentication uses JWT in Authorization header with Bearer scheme. Tokens have configurable expiration and can be refreshed.

Real-time video streaming uses WebRTC protocols (STUN, TURN, SRTP) with VP8 or H.264 codecs. Adaptive bitrate streaming adjusts quality based on bandwidth. WebSocket connections (WSS) provide bidirectional communication for live notifications and updates.

Internal communication between backend components uses Redis as message broker with Celery protocol. Database communication uses PostgreSQL wire protocol over TCP/IP with SSL/TLS and connection pooling.

Email uses SMTP over TLS/SSL with credentials in environment variables. Rate limiting prevents abuse using token bucket or sliding window algorithms. CORS headers allow frontend-backend communication with security restrictions. Compression uses gzip or Brotli encoding.

---

## 4. System Features

### 4.1 User Authentication and Authorization

**Description and Priority:** High priority, fundamental to all system functionality.

**Functional Requirements:**

FR-1.1: Registration interface with username, email, password (8+ chars, mixed case, numbers, special chars), and role selection.

FR-1.2: Real-time input validation for username uniqueness, email format, and password strength.

FR-1.3: Password hashing using bcrypt or Argon2 with salt before database storage.

FR-1.4: Email verification required before account activation.

FR-1.5: Login interface with username/email and password authentication.

FR-1.6: JWT issuance upon successful authentication containing user ID, username, role, and expiration.

FR-1.7: Token-based session management with JWT in client storage and Authorization header.

FR-1.8: JWT validation on each protected request, verifying signature and expiration.

FR-1.9: Role-based access control with three roles: Student (enroll, take exams, view results), Examiner (create/manage exams, monitor, review, grade), Administrator (manage users, configure system, full access).

FR-1.10: Authorization checks on all endpoints, returning 403 for unauthorized access.

FR-1.11: Password reset via email link with configurable expiration (typically 1 hour).

FR-1.12: Account lockout after configurable failed attempts (typically 5 in 15 minutes).

FR-1.13: Logout functionality invalidating session token and clearing client storage.

FR-1.14: Token refresh for session continuity during long exams.

FR-1.15: Authentication event logging for security auditing.

### 4.2 Exam Management

**Description and Priority:** High priority, essential for core functionality.

**Functional Requirements:**

FR-2.1: Exam creation interface with title, description, duration, start/end times, passing score, and max violations.

FR-2.2: Question addition supporting multiple-choice (2-6 options), true/false, and short answer types.

FR-2.3: Question builder with dynamic add/remove, reordering, point values, and correct answer marking.

FR-2.4: Proctoring configuration enabling/disabling AI features, setting sensitivity thresholds, and configuring automatic actions.

FR-2.5: Exam lifecycle states: Draft (being created), Published (visible to students), Active (in progress), Completed (ended).

FR-2.6: Draft exam editing with full modification capability.

FR-2.7: Prevention of published/active exam modification to maintain integrity.

FR-2.8: Exam listing with filtering by state and sorting by date or title.

FR-2.9: Draft exam deletion with confirmation prompts.

FR-2.10: Automatic state transition from Published to Active at scheduled start time.

FR-2.11: Automatic transition from Active to Completed at scheduled end time or when all students finish.

FR-2.12: Preview functionality showing student view of exam.

FR-2.13: Exam duplication for creating new exams based on existing ones.

FR-2.14: Exam configuration validation ensuring logical parameters and complete questions.

FR-2.15: Database storage with appropriate relationships between exams, questions, answers, and examiners.

