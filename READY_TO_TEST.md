# ✅ System Ready to Test!

## 🎉 Everything is Configured

### Current Status
- ✅ Backend running on port 5000
- ✅ Database updated with evidence columns
- ✅ Evidence folder exists: `backend/uploads/evidence/`
- ✅ Evidence retention: **30 days (720 hours)**
- ✅ Auto-cleanup: **DISABLED** (evidence stays automatically)
- ✅ Configuration loaded successfully

---

## 🚀 Start Frontend Now

Open a **NEW terminal** and run:

```bash
cd frontend
npm start
```

Browser will open at http://localhost:3000

---

## 🧪 Test the Complete System

### 1. Test as Student (Trigger Violations)

1. **Login as Student**
   - Go to http://localhost:3000
   - Login with student credentials

2. **Start an Exam**
   - Click on available exam
   - Accept terms
   - Start exam

3. **Trigger Violations** (to test evidence capture)
   - Look away from screen (eye gaze violation)
   - Have someone else in camera frame (multiple persons)
   - Turn off camera briefly (face not visible)
   - Try to switch tabs (tab switch)

4. **Watch Trust Score**
   - Should decrease with each violation
   - Warnings should appear
   - If trust score < 50%, exam auto-submits

5. **Submit Exam**
   - Answer questions
   - Click submit
   - Or let it auto-submit if trust score < 50%

---

### 2. Test as Examiner (View Evidence)

1. **Login as Examiner**
   - Logout from student account
   - Login with examiner credentials

2. **Go to Examiner Dashboard**
   - Click "Examiner Dashboard"
   - See list of your exams

3. **View Exam Results**
   - Click "📊 View Results" on the exam
   - See list of students who took the exam

4. **View Student Details**
   - Click on the student who just took the exam
   - Right panel shows:
     - ✅ Marks obtained/total
     - ✅ Percentage
     - ✅ Trust score
     - ✅ Violations list

5. **View Violation Evidence**
   - Scroll to "⚠️ Violations" section
   - Each violation should show:
     - 🔴/🟠/🟡 Severity badge
     - Violation type
     - Trust score reduction
     - Timestamp
     - **📷 View Evidence** link
   - Click "📷 View Evidence"
   - Screenshot should open in new window

---

## 📊 What You Should See

### Student View During Exam
```
┌─────────────────────────────────────┐
│  Trust Score: 85% ⚠️                │
│  Warning: Multiple persons detected │
│  Please ensure only you are visible │
└─────────────────────────────────────┘
```

### Examiner View - Results
```
┌─────────────────────────────────────────────┐
│  Student: John Doe                          │
│  Marks: 18/20 (90%)                         │
│  Trust Score: 85%                           │
│                                             │
│  ⚠️ Violations (2)                          │
│  ┌───────────────────────────────────────┐ │
│  │ 🔴 MULTIPLE PERSONS [HIGH]           │ │
│  │ -20% | Feb 27, 10:30 AM              │ │
│  │ 📷 View Evidence ← CLICK THIS!       │ │
│  └───────────────────────────────────────┘ │
│  ┌───────────────────────────────────────┐ │
│  │ 🟡 BLUR DISABLED [LOW]               │ │
│  │ -5% | Feb 27, 10:35 AM               │ │
│  │ 📷 View Evidence                     │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Evidence Screenshot
When you click "📷 View Evidence":
- New window opens
- Shows screenshot from student's camera
- Captured at the moment of violation
- Shows what the camera saw

---

## ✅ Verification Checklist

After testing, verify:

- [ ] Student can start exam
- [ ] Camera preview shows with blur
- [ ] Violations are detected
- [ ] Trust score decreases
- [ ] Warnings appear to student
- [ ] Exam auto-submits if trust < 50%
- [ ] Examiner can login
- [ ] Examiner can view results
- [ ] Student marks display correctly
- [ ] Trust scores display correctly
- [ ] Violations list shows
- [ ] Severity badges show (🔴🟠🟡)
- [ ] "📷 View Evidence" links appear
- [ ] Evidence screenshots open
- [ ] Screenshots show camera capture

---

## 🐛 If Something Doesn't Work

### Evidence Links Not Showing
**Check**: Are violations being saved with evidence?
```bash
cd backend
python -c "import sqlite3; conn = sqlite3.connect('instance/exam_proctoring.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM violations WHERE evidence_path IS NOT NULL'); print(f'Violations with evidence: {cursor.fetchone()[0]}'); conn.close()"
```

**Fix**: Check backend logs for errors

### Evidence Screenshots Not Opening
**Check**: Do files exist?
```bash
cd backend
ls uploads/evidence/
```

**Fix**: Check file permissions and backend logs

### Violations Not Being Detected
**Check**: Is camera working?
- Allow camera permissions in browser
- Check camera preview shows in exam

**Fix**: Restart browser and try again

---

## 📁 Evidence Storage

### Where Evidence is Stored
```
backend/
  └── uploads/
      └── evidence/
          ├── abc123_20240227_103015.jpg
          ├── xyz789_20240227_104532.jpg
          └── ...
```

### How Long Evidence is Kept
- **Retention**: 30 days (720 hours)
- **Auto-Delete**: DISABLED
- **Manual Cleanup**: Optional (run `python cleanup_evidence.py` after 30 days)

### Check Evidence Status
```bash
cd backend
python check_evidence.py
```

---

## 🎯 Expected Results

### After Student Takes Exam
- ✅ Violations recorded in database
- ✅ Evidence files saved to disk
- ✅ Evidence paths stored in database
- ✅ Trust score calculated correctly

### When Examiner Views Results
- ✅ All student data visible
- ✅ Marks and percentages correct
- ✅ Violations list complete
- ✅ Evidence links working
- ✅ Screenshots accessible

---

## 💡 Tips for Testing

1. **Use Multiple Browsers**
   - Student in Chrome
   - Examiner in Firefox
   - Easier to switch between roles

2. **Test Different Violations**
   - Multiple persons (have someone join you)
   - Phone detection (hold phone in view)
   - Eye gaze (look away from screen)
   - Face not visible (cover camera briefly)

3. **Check Trust Score**
   - Should start at 100%
   - Decreases with each violation
   - Shows warnings at < 80%
   - Auto-submits at < 50%

4. **Verify Evidence**
   - Each violation should have evidence
   - Screenshots should be clear
   - Timestamps should match violation time

---

## 📞 Quick Commands

```bash
# Check backend status
Test-NetConnection -ComputerName localhost -Port 5000

# Check evidence configuration
cd backend
python -c "from config_evidence import *; print(f'Retention: {EVIDENCE_RETENTION_HOURS}h')"

# Check evidence files
cd backend
ls uploads/evidence/

# Check database
cd backend
python check_evidence.py

# View backend logs
# Check the terminal where backend is running
```

---

## 🎉 You're Ready!

Everything is configured and ready to test:
- ✅ Backend running
- ✅ Database updated
- ✅ Evidence retention configured (30 days)
- ✅ Auto-cleanup disabled
- ✅ Evidence folder ready

**Next Step**: Start frontend and test!

```bash
cd frontend
npm start
```

Then follow the testing steps above.

---

**Status**: ✅ READY TO TEST
**Backend**: Running on port 5000
**Frontend**: Ready to start
**Evidence**: Automatic (30 days retention)
**Commands**: None needed

🚀 Start the frontend and test it now!
