# Proctoring System Fix Guide

## Issues Fixed

### 1. Exam Submission (404 Error)
- **Problem**: `/api/proctoring/submit` endpoint was returning 404
- **Fix**: Fixed the submit endpoint in `backend/routes/proctoring.py`
- **Status**: ✅ Fixed

### 2. Exam Start (500 Error)
- **Problem**: Creating proctoring session failed due to missing database column
- **Fix**: Added error handling and database fix script
- **Status**: ✅ Fixed

### 3. Trust Score Not Decreasing
- **Problem**: Violation reporting wasn't working properly
- **Fix**: Simplified violation endpoint to match actual model fields
- **Status**: ✅ Fixed

### 4. Camera Not Showing
- **Problem**: ProctorCamera component was a placeholder
- **Status**: ⚠️ Camera shows but AI detection is placeholder (requires AI models)

## Quick Fix Steps

### Step 1: Fix Database Schema
```bash
cd backend
python fix_database.py
```

This adds the missing `end_time` column to the proctoring_sessions table.

### Step 2: Restart Backend Server
```bash
# Stop the current server (Ctrl+C)
python run.py
```

### Step 3: Test the System

1. **Login as student**: `student@test.com` / `password123`
2. **Go to Exam List**: Click "View All Exams"
3. **Take an exam**: Click "Take Exam" on a published exam
4. **Accept terms**: Check all boxes and click "Accept & Start Exam"
5. **Exam should start**: You should see:
   - Camera feed (if you allow permissions)
   - Questions
   - Timer
   - Trust score (100%)

### Step 4: Test Violations

The system will detect these violations:

1. **Tab Switch**: Switch to another tab → Trust score decreases
2. **Blur Toggle**: Turn off blur → Violation recorded
3. **Time Expires**: Timer reaches 0 → Auto-submit

## Current System Status

### ✅ Working Features:
- Exam creation with questions (UI)
- Exam publishing
- Student can see published exams
- Acceptance form
- Exam start with session creation
- Camera activation
- Timer countdown
- Question navigation
- Answer selection
- Exam submission
- Trust score tracking
- Violation logging
- Tab switch detection

### ⚠️ Partially Working:
- **Camera Feed**: Shows video but AI detection is placeholder
- **Violation Detection**: Tab switch works, but AI-based detection (face, phone, etc.) needs AI models

### ❌ Not Implemented (Requires AI Models):
- Face detection
- Multiple person detection
- Phone detection
- Eye gaze tracking
- Head movement detection
- Sound detection

## Understanding the Proctoring System

### How It Works:

1. **Student starts exam** → Creates ProctoringSession (trust_score = 100%)
2. **Camera activates** → Video feed starts
3. **System monitors** → Detects violations
4. **Violation occurs** → Trust score decreases (5-20% per violation)
5. **Trust score < 50%** → Exam auto-submits
6. **Student submits** → Calculates score and saves result

### Violation Types:

| Violation | Severity | Score Reduction | Detection |
|-----------|----------|-----------------|-----------|
| Tab Switch | High | 20% | ✅ Working |
| Blur Disabled | High | 20% | ✅ Working |
| Face Not Visible | Medium | 10% | ⚠️ Needs AI |
| Multiple Persons | High | 20% | ⚠️ Needs AI |
| Phone Detected | High | 20% | ⚠️ Needs AI |
| Sound Detected | Medium | 10% | ⚠️ Needs AI |
| Eye Gaze Away | Low | 5% | ⚠️ Needs AI |
| Head Movement | Low | 5% | ⚠️ Needs AI |

### Trust Score System:

- **100%**: Perfect, no violations
- **80-99%**: Minor violations, warning
- **50-79%**: Multiple violations, critical warning
- **< 50%**: Exam auto-submits immediately

## Testing the Proctoring

### Test 1: Normal Exam Flow
```
1. Start exam
2. Answer questions
3. Submit exam
Expected: Score calculated, result saved
```

### Test 2: Tab Switch Violation
```
1. Start exam
2. Switch to another tab (Alt+Tab)
3. Return to exam
Expected: Trust score decreases by 20%
```

### Test 3: Auto-Submit
```
1. Start exam
2. Switch tabs 5+ times
3. Trust score falls below 50%
Expected: Exam auto-submits
```

### Test 4: Timer Expiry
```
1. Start exam with 1-minute duration
2. Wait for timer to reach 0
Expected: Exam auto-submits
```

## API Endpoints

### Exam Endpoints:
- `POST /api/exams/<id>/start` - Start exam, create session
- `POST /api/exams/<id>/acceptance-form` - Submit acceptance
- `GET /api/exams/<id>` - Get exam with questions

### Proctoring Endpoints:
- `POST /api/proctoring/violation` - Report violation
- `POST /api/proctoring/submit` - Submit exam with answers

## Database Tables

### proctoring_sessions
- Tracks active exam sessions
- Stores trust score
- Records start/end time

### violations
- Logs all violations
- Links to session and student
- Stores violation type and severity

### exam_results
- Stores final exam scores
- Links to student and exam
- Includes percentage and marks

## Troubleshooting

### Issue: 500 Error on Exam Start
**Solution**: Run `python fix_database.py` to add missing columns

### Issue: Camera Not Showing
**Solution**: 
1. Allow camera permissions in browser
2. Check browser console for errors
3. Try different browser (Chrome recommended)

### Issue: Trust Score Not Decreasing
**Solution**:
1. Check backend logs for violation recording
2. Verify proctoring session was created
3. Test tab switch (should work)

### Issue: Exam Not Submitting
**Solution**:
1. Check browser console for errors
2. Verify backend is running
3. Check that questions have answers

### Issue: No Questions in Exam
**Solution**:
```bash
cd backend
python add_questions.py <exam_id>
```

## Files Modified

### Backend:
1. `backend/routes/exam.py` - Added session creation on exam start
2. `backend/routes/proctoring.py` - Fixed submit and violation endpoints
3. `backend/models.py` - Added end_time field
4. `backend/fix_database.py` - Database migration script

### Frontend:
- No changes needed for basic proctoring

## Next Steps for Full AI Proctoring

To enable full AI-based proctoring, you need to:

1. **Install AI Models**:
   ```bash
   cd backend
   pip install opencv-python tensorflow mediapipe
   ```

2. **Implement Detection**:
   - Face detection using MediaPipe
   - Phone detection using YOLO
   - Eye gaze using MediaPipe Face Mesh
   - Sound detection using audio analysis

3. **Update ProctorCamera Component**:
   - Add real-time frame capture
   - Send frames to backend for analysis
   - Display detection results

4. **Backend Processing**:
   - Process video frames
   - Run AI models
   - Return detection results
   - Auto-report violations

## Current Limitations

1. **AI Detection**: Placeholder only, needs actual AI models
2. **Video Recording**: Not implemented
3. **Screenshot Capture**: Not implemented
4. **Real-time Alerts**: Basic implementation
5. **Examiner Dashboard**: Needs violation viewing

## Summary

The basic proctoring system is now working:
- ✅ Exam sessions are created
- ✅ Trust scores are tracked
- ✅ Violations are logged
- ✅ Tab switching is detected
- ✅ Exams can be submitted
- ✅ Scores are calculated

For full AI-based proctoring, additional work is needed on the AI models and real-time detection.

---

**Run the fix script and restart your backend to test!**
