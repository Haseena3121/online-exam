# 🔧 Evidence Not Saving - Complete Fix

## 🎯 Problem Identified

**Issue 1**: 403 Forbidden when viewing exams
- **Cause**: Logged in as student, not examiner
- **Solution**: Logout and login as examiner

**Issue 2**: Evidence not being saved after exam
- **Cause**: "No active session" error - proctoring session not created
- **Solution**: Fix session creation in exam start

---

## ✅ Quick Fix Steps

### Step 1: Login as Examiner (Not Student)

1. **Logout** from current account
2. **Login** with examiner credentials:
   - Email: examiner account
   - Password: examiner password
3. **Go to** "Examiner Dashboard"
4. **Click** "📊 View Results"

### Step 2: Check if Evidence is Being Saved

The real issue is that violations show "No active session" error. This means:
- Violations ARE being detected ✅
- Screenshots ARE being captured ✅
- But they're NOT being saved ❌ (because no session)

---

## 🔍 Root Cause Analysis

### What's Happening

```
Student starts exam
  ↓
Exam interface loads
  ↓
Proctoring session should be created ← FAILING HERE
  ↓
Violations detected
  ↓
Try to save evidence
  ↓
ERROR: "No active session" ← Can't save without session
```

### Why Evidence Isn't Saving

From the logs:
```
POST /api/proctoring/violation HTTP/1.1" 404
Error: No active session
```

This means:
1. Exam starts but proctoring session isn't created
2. Violations are detected
3. Evidence can't be saved (no session to attach to)
4. Returns 404 error

---

## 🛠️ Complete Solution

### Fix 1: Ensure Session is Created on Exam Start

The issue is in the exam start flow. Let me check and fix it:

**File**: `backend/routes/exam.py` - `start_exam()` function

The session creation might be failing silently. We need to ensure it's created properly.

### Fix 2: Make Evidence Saving More Robust

Even if session creation fails, we should still save evidence.

---

## 🚀 Immediate Workaround

While we fix the session issue, here's how to test if evidence CAN be saved:

### Test 1: Check if Evidence Folder Works

```bash
cd backend
python -c "
import os
from datetime import datetime

# Create test evidence file
test_file = f'uploads/evidence/test_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.txt'
with open(test_file, 'w') as f:
    f.write('Test evidence file')

print(f'✅ Test file created: {test_file}')
print(f'✅ Evidence folder is writable')

# Clean up
os.remove(test_file)
print(f'✅ Test file deleted')
"
```

### Test 2: Manually Create a Session

```bash
cd backend
python -c "
from app import create_app
from models import ProctoringSession, User, Exam
from database import db
from datetime import datetime

app = create_app()
with app.app_context():
    # Get a student and exam
    student = User.query.filter_by(role='student').first()
    exam = Exam.query.first()
    
    if student and exam:
        # Create session
        session = ProctoringSession(
            student_id=student.id,
            exam_id=exam.id,
            current_trust_score=100,
            status='active',
            camera_active=True,
            mic_active=True,
            screen_locked=True,
            start_time=datetime.utcnow()
        )
        
        db.session.add(session)
        db.session.commit()
        
        print(f'✅ Session created: ID {session.id}')
        print(f'   Student: {student.name}')
        print(f'   Exam: {exam.title}')
    else:
        print('❌ No student or exam found')
"
```

---

## 📋 Detailed Fix Implementation

### Step 1: Update Exam Start Route

Edit `backend/routes/exam.py`:

```python
@exam_bp.route('/<int:exam_id>/start', methods=['POST'])
@jwt_required()
def start_exam(exam_id):
    try:
        student_id = int(get_jwt_identity())
        
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify({"error": "Exam not found"}), 404

        if not exam.is_published:
            return jsonify({"error": "This exam is not available"}), 403

        # Check for existing active session
        from models import ProctoringSession
        from datetime import datetime
        
        existing_session = ProctoringSession.query.filter_by(
            student_id=student_id,
            exam_id=exam_id,
            status='active'
        ).first()

        if existing_session:
            session_id = f"{student_id}_{exam_id}_{existing_session.id}"
            return jsonify({
                "message": "Resuming existing session",
                "session_id": session_id,
                "exam_id": exam_id,
                "duration": exam.duration,
                "proctoring_session_id": existing_session.id
            }), 200

        # Create new proctoring session - MUST SUCCEED
        session = ProctoringSession(
            student_id=student_id,
            exam_id=exam_id,
            current_trust_score=100,
            status='active',
            camera_active=True,
            mic_active=True,
            screen_locked=True,
            start_time=datetime.utcnow()
        )
        
        db.session.add(session)
        db.session.commit()
        
        proctoring_session_id = session.id
        session_id = f"{student_id}_{exam_id}_{proctoring_session_id}"
        
        print(f"✅ Proctoring session created: ID {proctoring_session_id}")

        return jsonify({
            "message": "Exam started successfully",
            "session_id": session_id,
            "exam_id": exam_id,
            "duration": exam.duration,
            "proctoring_session_id": proctoring_session_id
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error starting exam: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
```

### Step 2: Update Violation Reporting

Make it more robust - save evidence even if session lookup fails:

```python
@proctoring_bp.route('/violation', methods=['POST'])
@jwt_required()
def report_violation():
    try:
        student_id = int(get_jwt_identity())
        
        # Try to find active session
        session = ProctoringSession.query.filter_by(
            student_id=student_id,
            status='active'
        ).first()
        
        if not session:
            # Log but don't fail completely
            print(f"⚠️ No active session for student {student_id}")
            # Try to find most recent session
            session = ProctoringSession.query.filter_by(
                student_id=student_id
            ).order_by(ProctoringSession.start_time.desc()).first()
            
            if not session:
                return jsonify({'error': 'No session found'}), 404
        
        # Rest of the code...
```

---

## 🧪 Testing After Fix

### Test 1: Start Exam
1. Login as student
2. Start exam
3. Check backend logs for: "✅ Proctoring session created"

### Test 2: Trigger Violation
1. During exam, look away from camera
2. Check browser console for: "✅ Violation reported"
3. Should NOT see: "No active session" error

### Test 3: Check Evidence
```bash
cd backend
ls -la uploads/evidence/
```

Should see new files created.

### Test 4: View as Examiner
1. Login as examiner
2. View results
3. Click student
4. See violations with evidence links

---

## 📊 Verification Commands

### Check Sessions in Database
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT id, student_id, exam_id, status, start_time FROM proctoring_sessions ORDER BY start_time DESC LIMIT 5')
print('Recent sessions:')
for row in cursor.fetchall():
    print(f'  ID: {row[0]}, Student: {row[1]}, Exam: {row[2]}, Status: {row[3]}, Time: {row[4]}')
conn.close()
"
```

### Check Violations with Evidence
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT id, violation_type, evidence_path, created_at FROM violations WHERE evidence_path IS NOT NULL ORDER BY created_at DESC LIMIT 5')
print('Violations with evidence:')
for row in cursor.fetchall():
    print(f'  ID: {row[0]}, Type: {row[1]}, Evidence: {row[2]}, Time: {row[3]}')
conn.close()
"
```

---

## 🎯 Summary

### Current Issues
1. ❌ 403 error - Wrong user role (student vs examiner)
2. ❌ Evidence not saving - No active session created
3. ❌ Violations returning 404 - Session lookup failing

### Solutions
1. ✅ Login as examiner to view results
2. ✅ Fix session creation in exam start
3. ✅ Make violation reporting more robust
4. ✅ Ensure evidence is saved even if session lookup fails

### Next Steps
1. Apply the fixes above
2. Restart backend
3. Test with new exam
4. Verify evidence is saved
5. Check as examiner

---

**The core issue is that proctoring sessions aren't being created when exams start, so violations can't be saved. Once we fix the session creation, evidence will be saved automatically.**
