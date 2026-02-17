# Online Exam Proctoring System

A comprehensive, production-ready online exam proctoring platform with advanced AI-based violation detection, real-time monitoring, and automated exam management.

## 🎯 Features

### Core Features
- ✅ Student exam enrollment and management
- ✅ Real-time exam interface with multiple question types
- ✅ Automatic exam submission and result calculation
- ✅ Examiner dashboard with student monitoring
- ✅ Detailed analytics and reporting

### Proctoring Features
- ✅ Real-time video stream monitoring
- ✅ Camera and microphone enforcement
- ✅ Background blur enforcement
- ✅ Screen locking during exam
- ✅ Tab-switching detection
- ✅ Automatic session recording

### AI-Based Violation Detection
- ✅ Face detection and visibility monitoring
- ✅ Eye-gaze tracking for suspicious behavior
- ✅ Phone/device detection
- ✅ Sound/speech detection
- ✅ Multiple person detection
- ✅ Head movement and extreme pose detection
- ✅ Background blur detection
- ✅ Brightness and lighting analysis

### Security Features
- ✅ JWT authentication
- ✅ Role-based access control (Student, Examiner, Admin)
- ✅ Password strength enforcement
- ✅ Session management
- ✅ Audit logging
- ✅ Encrypted data transmission
- ✅ CORS protection

### Analytics & Reporting
- ✅ Real-time exam statistics
- ✅ Student performance analytics
- ✅ Violation history and patterns
- ✅ Trust score tracking
- ✅ Downloadable reports

## 🛠 Technology Stack

### Backend
- **Framework**: Flask 3.0 (Python)
- **Database**: MySQL 5.7+
- **Cache**: Redis 7+
- **Task Queue**: Celery
- **ORM**: SQLAlchemy
- **Authentication**: JWT

### Frontend
- **Library**: React 18
- **Routing**: React Router v6
- **State Management**: Context API
- **Styling**: CSS3
- **API Client**: Axios

### AI/ML
- **Face Detection**: MediaPipe
- **Pose Estimation**: MediaPipe
- **Object Detection**: TensorFlow
- **Audio Processing**: Librosa
- **Image Processing**: OpenCV

### DevOps
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx
- **Server**: Gunicorn
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- MySQL 5.7+
- Redis 6+
- Docker & Docker Compose (optional)
- 8GB RAM (recommended)
- Ubuntu 20.04+ (recommended)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/Haseena3121/online-exam-proctoring.git
cd online-exam-proctoring

# Copy environment file
cp backend/.env.example backend/.env

# Edit .env with your configuration
nano backend/.env

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend flask db upgrade

# Load seed data
docker-compose exec backend python seed_data.py