# 🚀 Quick Setup: Violation Evidence System

## What This Fixes

This setup enables examiners to:
1. ✅ View violation screenshots/videos in exam results
2. ✅ See detailed violation information with severity levels
3. ✅ Access evidence proofs for 24 hours after exam
4. ✅ Monitor student marks and trust scores
5. ✅ View auto-submitted exams with full evidence

---

## 🔧 Step-by-Step Setup

### Step 1: Update Database Schema
```bash
cd backend
python update_database_schema.py
```

**What this does:**
- Adds `evidence_path` column to violations table
- Adds `severity` and `description` columns
- Adds `final_trust_score`, `status`, `submitted_at` to exam_results
- Updates examiner_notifications table

**Expected Output:**
```
======================================================================
🔧 UPDATING DATABASE SCHEMA FOR VIOLATION EVIDENCE
======================================================================

📋 Updating violations table...
📋 Updating exam_results table...
📋 Updating examiner_notifications table...

📊 Updates Summary:
   ✅ Added evidence_path column
   ✅ Added severity column
   ✅ Added description column
   ✅ Added final_trust_score column to exam_results
   ✅ Added status column to exam_results
   ✅ Added submitted_at column to exam_results
   ✅ Added student_id column to examiner_notifications
   ✅ Added exam_id column to examiner_notifications
   ✅ Added severity_level column to examiner_notifications

======================================================================
✅ DATABASE SCHEMA UPDATED SUCCESSFULLY!
======================================================================
```

### Step 2: Create Evidence Upload Folder
```bash
cd backend
mkdir -p uploads/evidence
```

### Step 3: Restart Backend
```bash
cd backend
python app.py
```

**Verify backend is running:**
- Should see: `* Running on http://127.0.0.1:5000`
- No errors about missing columns

### Step 4: Restart Frontend (if running)
```bash
cd frontend
npm start
```

---

## ✅ Verification Steps

### 1. Check Database Schema
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(violations)')
columns = [col[1] for col in cursor.fetchall()]
print('Violations columns:', columns)
print('✅ evidence_path present' if 'evidence_path' in columns else '❌ evidence_path missing')
conn.close()
"
```

### 2. Test Examiner Login
1. Go to http://localhost:3000
2. Login as examiner
3. Should see "Examiner Dashboard"

### 3. Test Results Page
1. Click on any exam
2. Click "📊 View Results"
3. Should see list of students
4. Click on a student
5. Should see violations section

### 4. Test Evidence Display
1. If violations exist with evidence:
   - Should see "📷 View Evidence" link
   - Click should open evidence in new window
2. If no evidence:
   - Should see violation details without evidence link

---

## 🎯 Testing the Complete Flow

### Create a Test Exam
1. Login as examiner
2. Create new exam with 2-3 questions
3. Publish the exam

### Take Exam as Student
1. Logout and login as student
2. Start the exam
3. Trigger some violations:
   - Turn off camera briefly (face not visible)
   - Look away from screen (eye gaze)
   - Have someone else in frame (multiple persons)
4. Submit exam

### View Results as Examiner
1. Login as examiner
2. Go to exam results
3. Click on the student
4. Check violations section:
   - Should see all violations
   - Should see severity badges (LOW/MEDIUM/HIGH)
   - Should see trust score reductions
   - Should see timestamps
   - Should see "📷 View Evidence" links (if evidence was captured)

---

## 🐛 Troubleshooting

### Issue: "evidence_path column not found"
**Solution:**
```bash
cd backend
python update_database_schema.py
python app.py
```

### Issue: Evidence links return 404
**Solution:**
1. Check folder exists: `ls backend/uploads/evidence/`
2. Check file permissions: `chmod 755 backend/uploads/evidence/`
3. Check backend logs for errors

### Issue: No violations showing
**Solution:**
1. Check browser console for errors
2. Check backend logs: `tail -f backend/logs/app.log`
3. Verify violations table has data:
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM violations')
print('Total violations:', cursor.fetchone()[0])
conn.close()
"
```

### Issue: "Unauthorized" when viewing evidence
**Solution:**
1. Ensure logged in as examiner (not student)
2. Check JWT token is valid
3. Clear browser cache and re-login

---

## 📊 What Examiners Will See

### Results Page Layout
```
┌─────────────────────────────────────────────────────────────┐
│  ← Back    📊 Exam Results: [Exam Title]                    │
├─────────────────────────────────────────────────────────────┤
│  [Total Students] [Passed] [Failed] [Average Score]         │
├─────────────────────────────────────────────────────────────┤
│  🔍 Search...    [All] [Passed] [Failed]                    │
├──────────────────────┬──────────────────────────────────────┤
│  Student List        │  Selected Student Details            │
│  ┌────────────────┐  │  ┌────────────────────────────────┐ │
│  │ Student Name   │  │  │ 📊 Performance                 │ │
│  │ email@test.com │  │  │ Marks: 15/20 (75%)            │ │
│  │ Score: 75%     │  │  │ Trust Score: 85%              │ │
│  │ Trust: 85%     │  │  └────────────────────────────────┘ │
│  │ Violations: 3  │  │  ┌────────────────────────────────┐ │
│  └────────────────┘  │  │ ⚠️ Violations (3)              │ │
│                      │  │ ┌──────────────────────────┐   │ │
│                      │  │ │ MULTIPLE PERSONS [HIGH]  │   │ │
│                      │  │ │ -20%                     │   │ │
│                      │  │ │ 2024-02-27 10:30 AM      │   │ │
│                      │  │ │ 📷 View Evidence         │   │ │
│                      │  │ └──────────────────────────┘   │ │
│                      │  └────────────────────────────────┘ │
└──────────────────────┴──────────────────────────────────────┘
```

### Violation Evidence Display
When clicking "📷 View Evidence":
- Opens in new window (800x600)
- Shows screenshot captured at violation time
- Image shows what the camera saw
- Timestamp in filename

---

## 🎨 UI Features Enabled

### Color Coding
- 🟢 **Green badges**: Passed students
- 🔴 **Red badges**: Failed students  
- 🟠 **Orange badges**: Auto-submitted exams
- 🟡 **Yellow severity**: Low violations
- 🟠 **Orange severity**: Medium violations
- 🔴 **Red severity**: High violations

### Interactive Elements
- Click student card to view details
- Click evidence link to view proof
- Search students by name/email
- Filter by pass/fail status
- Sort by various metrics

---

## 📝 Notes

### Evidence Retention
- Evidence stored for 24 hours by default
- Run cleanup script to remove old evidence:
```bash
cd backend
python cleanup_evidence.py
```

### Performance
- Evidence files are served directly by Flask
- Large files may take time to load
- Consider implementing CDN for production

### Security
- Only examiners can view evidence
- JWT authentication required
- Evidence URLs are protected

---

## ✅ Success Criteria

You'll know everything is working when:
- [ ] Database schema updated without errors
- [ ] Backend starts without column errors
- [ ] Examiner can login and see dashboard
- [ ] Results page shows student list
- [ ] Clicking student shows violation details
- [ ] Violations show severity badges
- [ ] Evidence links are visible (if evidence exists)
- [ ] Clicking evidence opens image/video
- [ ] Trust scores are displayed correctly
- [ ] Auto-submitted exams show orange badge

---

## 🚀 Next Steps

After setup is complete:
1. Read `VIOLATION_EVIDENCE_GUIDE.md` for detailed usage
2. Test with real exam scenarios
3. Configure evidence retention policy
4. Set up automatic cleanup cron job
5. Train examiners on evidence review process

---

**Setup Time**: ~5 minutes
**Difficulty**: Easy
**Prerequisites**: Backend and frontend already running
