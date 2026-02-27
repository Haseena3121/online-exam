# 🎓 Online Exam Proctoring System - Complete Testing Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Testing Camera & AI Models](#testing-camera--ai-models)
3. [Creating Exams](#creating-exams)
4. [Taking Exams](#taking-exams)
5. [Testing All Features](#testing-all-features)

---

## 🚀 Quick Start

### 1. Access the Application
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

### 2. Create Accounts

#### Create Examiner Account:
1. Go to http://localhost:3000/register
2. Fill in:
   - Name: `Test Examiner`
   - Email: `examiner@test.com`
   - Password: `password123`
   - Role: Select **Examiner**
3. Click Register

#### Create Student Account:
1. Go to http://localhost:3000/register
2. Fill in:
   - Name: `Test Student`
   - Email: `student@test.com`
   - Password: `password123`
   - Role: Select **Student**
3. Click Register

---

## 📹 Testing Camera & AI Models

### Method 1: Camera Test Page
1. Login as Student
2. Go to: http://localhost:3000/camera-test
3. Allow camera and microphone permissions
4. You should see:
   - ✅ Live video feed
   - ✅ Camera status indicator
   - ✅ List of AI features

### Method 2: During Exam
1. Login as Student
2. Go to Exam List
3. Start any exam
4. Camera will activate automatically

### AI Models Being Tested:
- **Face Detection**: Detects if your face is visible
- **Multiple Person Detection**: Alerts if more than one person
- **Phone Detection**: Detects mobile phones
- **Eye Gaze Tracking**: Monitors eye movement
- **Head Movement**: Tracks head position
- **Sound Detection**: Monitors audio
- **Tab Switch Detection**: Detects if you leave the page

---

## 📝 Creating Exams (As Examiner)

### Step 1: Login as Examiner
- Email: `examiner@test.com`
- Password: `password123`

### Step 2: Create Exam
1. Click "Create New Exam" button
2. Fill in the form:
   - **Title**: "Sample Math Exam"
   - **Description**: "Basic mathematics test"
   - **Instructions**: "Answer all questions carefully"
   - **Duration**: 60 (minutes)
   - **Total Marks**: 100
   - **Passing Marks**: 40
3. Click "Create Exam"

### Step 3: Add Questions (Coming Soon)
Currently, you need to add questions via backend API or database directly.

---

## 📖 Taking Exams (As Student)

### Step 1: Login as Student
- Email: `student@test.com`
- Password: `password123`

### Step 2: Test Camera First
1. Go to http://localhost:3000/camera-test
2. Verify camera is working
3. Click "Continue to Exams"

### Step 3: View Available Exams
1. Go to "Exam List" from dashboard
2. You'll see all published exams

### Step 4: Start Exam
1. Click on an exam
2. Accept terms and conditions
3. Camera will activate
4. Answer questions
5. Submit exam

---

## 🧪 Testing All Features

### 1. Test Face Detection
- **Action**: Cover your face with your hand
- **Expected**: Violation alert, trust score decreases

### 2. Test Multiple Person Detection
- **Action**: Have someone else appear in camera
- **Expected**: Alert for multiple faces detected

### 3. Test Phone Detection
- **Action**: Hold a phone near your face
- **Expected**: Phone detection alert

### 4. Test Eye Gaze Tracking
- **Action**: Look away from screen for extended time
- **Expected**: Gaze violation warning

### 5. Test Head Movement
- **Action**: Move your head significantly
- **Expected**: Unusual movement alert

### 6. Test Tab Switch Detection
- **Action**: Press Alt+Tab or switch browser tabs
- **Expected**: Tab switch violation logged

### 7. Test Sound Detection
- **Action**: Talk or play audio
- **Expected**: Sound detection alert

---

## 🔧 Troubleshooting

### Camera Not Working?
1. Check browser permissions
2. Make sure no other app is using camera
3. Try different browser (Chrome recommended)
4. Restart browser

### Exam Creation Failing?
1. Make sure you're logged in as Examiner
2. Check all required fields are filled
3. Check backend logs for errors

### Backend Not Running?
```bash
cd backend
python run.py
```

### Frontend Not Running?
```bash
cd frontend
npm start
```

---

## 📊 Monitoring & Results

### View Violations (As Examiner)
1. Login as Examiner
2. Go to "Examiner Dashboard"
3. Click on "Violation Details"
4. See all violations with timestamps

### View Results (As Student)
1. Login as Student
2. Go to "Results" page
3. See your exam scores and trust scores

---

## 🎯 Complete Test Workflow

### Full End-to-End Test:

1. **Setup** (5 minutes)
   - Create examiner account
   - Create student account
   - Test camera access

2. **Create Exam** (5 minutes)
   - Login as examiner
   - Create new exam with details
   - Publish exam

3. **Take Exam** (10 minutes)
   - Login as student
   - Test camera
   - Start exam
   - Trigger various violations intentionally
   - Submit exam

4. **Review** (5 minutes)
   - Login as examiner
   - Check violation logs
   - Review student performance

---

## 📱 Quick Access URLs

- **Login**: http://localhost:3000/login
- **Register**: http://localhost:3000/register
- **Camera Test**: http://localhost:3000/camera-test
- **Student Dashboard**: http://localhost:3000/dashboard
- **Examiner Dashboard**: http://localhost:3000/examiner-dashboard
- **Create Exam**: http://localhost:3000/create-exam
- **Exam List**: http://localhost:3000/exam-list

---

## ✅ Checklist

- [ ] Both servers running (frontend & backend)
- [ ] Examiner account created
- [ ] Student account created
- [ ] Camera permissions granted
- [ ] Exam created successfully
- [ ] Camera test passed
- [ ] Exam taken with AI monitoring
- [ ] Violations logged
- [ ] Results viewable

---

## 🆘 Need Help?

If something isn't working:
1. Check browser console (F12)
2. Check backend terminal for errors
3. Verify both servers are running
4. Clear browser cache and reload

---

**Happy Testing! 🎉**
