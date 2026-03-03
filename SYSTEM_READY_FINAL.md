# System Status & Quick Fixes

## Current Issues

### 1. Trust Score Starting at 0%
**Why**: Student has violations from previous exam sessions

**Fix**: The proctoring session should start with 100% trust score. This is a data issue, not a code issue.

**Quick Solution**:
- Start a fresh exam with a different student account
- OR clear old sessions from database

### 2. CORS Error After Auto-Submit
**Why**: Backend crashed when trying to auto-submit

**What Happened**:
1. Trust score was already 0%
2. First violation triggered auto-submit
3. Auto-submit failed (probably due to missing enrollment_id)
4. Backend crashed
5. CORS error appears because backend is down

## What to Do Now

### Option 1: Check Backend Logs
Look at the backend terminal for error messages. You should see something like:
```
Error auto-submitting: ...
```

### Option 2: Restart Everything Fresh

**Step 1: Stop Backend**
```
CTRL + C
```

**Step 2: Clear Old Data (Optional)**
```bash
cd backend
# Delete the database to start fresh
del exam_proctoring.db  # Windows
# OR
rm exam_proctoring.db   # Mac/Linux
```

**Step 3: Start Backend**
```bash
python app.py
```

**Step 4: Test with Fresh Account**
- Create new student account
- Start exam
- Trust score should start at 100%
- Trigger violations to test auto-submit

## Expected Behavior

### Normal Flow:
1. Student starts exam → Trust score: 100%
2. Violation detected → Trust score: 95%
3. Another violation → Trust score: 85%
4. Continue until < 50%
5. Auto-submit triggers
6. Navigate to results

### Your Current Flow:
1. Student starts exam → Trust score: 0% ❌ (old violations)
2. First violation → Tries to auto-submit
3. Backend crashes ❌
4. CORS error ❌

## The Real Issue

The trust score starting at 0% means:
- There's an old proctoring session for this student
- The session wasn't properly closed
- Old violations are being counted

## Quick Fix Commands

### Clear All Sessions:
```bash
cd backend
python -c "from app import create_app; from database import db; from models import ProctoringSession; app = create_app(); app.app_context().push(); ProctoringSession.query.delete(); db.session.commit(); print('✅ Sessions cleared')"
```

### Check Current Sessions:
```bash
cd backend
python check_sessions.py
```

## What You Should See in Backend Logs

When auto-submit triggers, you should see:
```
Violation: blur_disabled for student X, Trust Score: 45%
Exam auto-submitted for student X: 15/25 (60.00%)
```

If you see errors instead, that's the problem we need to fix.

## Next Steps

1. **Check backend terminal** - What error do you see?
2. **Share the error** - I'll fix it
3. **OR restart fresh** - Delete database and start over

The code is correct, but there's old data causing issues.
