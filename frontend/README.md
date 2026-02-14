# Online Exam Proctoring System - Frontend

A comprehensive React-based frontend for an advanced online exam proctoring system with real-time violation detection using AI models.

## Features

✅ **User Authentication**
- Secure login and registration
- JWT token-based authentication
- Role-based access control (Student, Examiner, Admin)

✅ **Exam Management**
- Browse and enroll in exams
- Real-time exam interface
- Automatic question navigation
- Multiple question types support

✅ **Proctoring System**
- Live camera monitoring with face detection
- Background blur enforcement
- Real-time violation detection
- Automatic screenshot/video capture
- Trust score tracking and warning system

✅ **Violation Detection**
- Face visibility monitoring
- Multiple person detection
- Phone/suspicious device detection
- Tab switching detection
- Sound monitoring
- Eye gaze tracking
- Head movement tracking
- Low light detection

✅ **Results & Analytics**
- Detailed exam results
- Performance analytics
- Violation history
- Trust score analysis

## Tech Stack

- **React 18** - UI Framework
- **React Router v6** - Client-side routing
- **TensorFlow.js** - ML models for detection
- **Facemesh** - Face detection and tracking
- **COCO-SSD** - Object detection
- **Axios** - HTTP client
- **CSS3** - Styling and animations

## Installation

### Prerequisites
- Node.js 14+ 
- npm or yarn

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Haseena3121/online-exam-proctoring.git
cd online-exam-proctoring/frontend