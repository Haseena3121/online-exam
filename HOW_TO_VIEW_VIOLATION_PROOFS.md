# 📷 How to View Violation Proofs (Screenshots)

## Step-by-Step Guide for Examiners

### Step 1: Login as Examiner
```
URL: http://localhost:3000
Email: skhaseena0@gmail.com
Password: password123
```

### Step 2: Go to Examiner Dashboard
- After login, you'll see "Examiner Dashboard"
- You'll see a list of your exams

### Step 3: Click "📊 View Results" Button
- Find the exam you want to check (e.g., "test_2")
- Click the blue "📊 View Results" button on that exam

### Step 4: You'll See Results Page
This page shows:
- **Top:** Statistics (Total Students, Passed, Failed, Average Score)
- **Left Side:** List of students who took the exam
- **Right Side:** Detailed view (when you click a student)

### Step 5: Click on a Student Card
- On the left side, you'll see student cards
- Each card shows:
  - Student name
  - Email
  - Score (e.g., "8/10 (80%)")
  - Trust Score (e.g., "75%")
  - Violations count (e.g., "3 🚨")
- **Click on any student card**

### Step 6: View Violation Details
After clicking a student, the right side shows:

**📊 Performance Section:**
- Marks Obtained
- Total Marks
- Percentage
- Trust Score

**⚠️ Violations Section:**
This is where you see the proofs!

Each violation shows:
```
COPY ATTEMPT                    -20%
2026-02-27 10:30:45    📷 View Evidence
```

### Step 7: Click "📷 View Evidence"
- Click the blue "📷 View Evidence" link
- **Screenshot will open in a NEW TAB**
- You'll see the camera capture from when the violation occurred

---

## Visual Layout

```
┌─────────────────────────────────────────────────────────┐
│  📊 Exam Results: test_2                                │
│  [← Back]                                               │
└─────────────────────────────────────────────────────────┘

┌──────────┬──────────┬──────────┬──────────┐
│ Total: 5 │ Passed:3 │ Failed:2 │ Avg:75%  │
└──────────┴──────────┴──────────┴──────────┘

┌─────────────────────┬───────────────────────────────────┐
│ STUDENTS LIST       │ STUDENT DETAILS                   │
│                     │                                   │
│ ┌─────────────────┐ │ John Doe                          │
│ │ John Doe        │ │                                   │
│ │ john@email.com  │ │ 📊 Performance                    │
│ │ Score: 8/10     │ │ Marks: 8/10                       │
│ │ Trust: 75%      │ │ Percentage: 80%                   │
│ │ Violations: 3🚨 │ │ Trust Score: 75%                  │
│ └─────────────────┘ │                                   │
│                     │ ⚠️ Violations (3)                 │
│ ┌─────────────────┐ │                                   │
│ │ Jane Smith      │ │ ┌───────────────────────────────┐ │
│ │ jane@email.com  │ │ │ COPY ATTEMPT          -20%    │ │
│ │ Score: 6/10     │ │ │ 2026-02-27 10:30:45           │ │
│ │ Trust: 60%      │ │ │ 📷 View Evidence  ← CLICK HERE│ │
│ │ Violations: 5🚨 │ │ └───────────────────────────────┘ │
│ └─────────────────┘ │                                   │
│                     │ ┌───────────────────────────────┐ │
│                     │ │ TAB SWITCH            -20%    │ │
│                     │ │ 2026-02-27 10:31:12           │ │
│                     │ │ 📷 View Evidence  ← CLICK HERE│ │
│                     │ └───────────────────────────────┘ │
└─────────────────────┴───────────────────────────────────┘
```

---

## If You Don't See "📷 View Evidence" Links

### Possible Reasons:

1. **No violations occurred during exam**
   - Student followed all rules
   - No screenshots captured

2. **Screenshots not saved**
   - Backend not running when violations occurred
   - Evidence folder doesn't exist

3. **Old violations (before screenshot feature)**
   - Violations logged before we added screenshot capture
   - Only NEW violations will have evidence

---

## How to Test and See Proofs

### Create New Violations with Screenshots:

1. **Student Takes New Exam:**
   ```
   Login: skhaseena009@gmail.com / password123
   Start exam #2
   ```

2. **Trigger Violations:**
   - Try to copy text (Ctrl+C)
   - Switch tabs (Alt+Tab)
   - Turn off blur

3. **Submit Exam**

4. **Examiner Checks:**
   ```
   Login: skhaseena0@gmail.com / password123
   Click "📊 View Results" on exam #2
   Click on the student
   Look for "📷 View Evidence" links
   ```

---

## Check if Screenshots Are Being Saved

### Method 1: Check Folder
```powershell
cd C:\Projects\online-exam\backend\uploads\evidence
dir
```

You should see files like:
```
abc123def456_20260227_103045.jpg
xyz789ghi012_20260227_103112.jpg
```

### Method 2: Check Database
```powershell
cd C:\Projects\online-exam\backend
python -c "import sqlite3; conn = sqlite3.connect('instance/exam_proctoring.db'); cursor = conn.cursor(); cursor.execute('SELECT id, violation_type, evidence_path FROM violations ORDER BY id DESC LIMIT 5'); print('\n'.join([str(row) for row in cursor.fetchall()]))"
```

Should show:
```
(25, 'copy_attempt', 'uploads/evidence/abc123.jpg')
(24, 'tab_switch', 'uploads/evidence/xyz789.jpg')
```

---

## Troubleshooting

### Issue: No "View Evidence" links showing

**Check 1: Are there violations?**
- Look at "Violations (X)" count
- If 0, no violations occurred

**Check 2: Do violations have evidence_path?**
```powershell
cd backend
python -c "import sqlite3; conn = sqlite3.connect('instance/exam_proctoring.db'); cursor = conn.cursor(); cursor.execute('SELECT violation_type, evidence_path FROM violations WHERE evidence_path IS NOT NULL LIMIT 5'); print('\n'.join([str(row) for row in cursor.fetchall()]))"
```

**Check 3: Backend restarted?**
- Backend must be restarted for new code to work
- Old violations won't have screenshots

**Check 4: Frontend restarted?**
- Frontend must be restarted
- Browser cache must be cleared (Ctrl+Shift+R)

### Issue: "View Evidence" link shows 404

**Possible Causes:**
1. File doesn't exist
2. Backend not running
3. Wrong path

**Solution:**
```powershell
# Check if file exists
cd backend/uploads/evidence
dir

# Check backend is running
# Should see: Server running at http://localhost:5000
```

---

## Quick Test

### 1. Take Fresh Exam
```
Student login → Start exam → Trigger violations → Submit
```

### 2. Check Evidence Saved
```powershell
cd backend/uploads/evidence
dir
```

### 3. View in Examiner Dashboard
```
Examiner login → View Results → Click student → See violations → Click "📷 View Evidence"
```

---

## What Screenshot Shows

The screenshot captures:
- **Camera feed** at the moment of violation
- **Student's face** (if camera was on)
- **Timestamp** when violation occurred

Example violations with screenshots:
- **Copy Attempt:** Shows student at moment they pressed Ctrl+C
- **Tab Switch:** Shows student when they switched away
- **Multiple Persons:** Shows multiple people in frame

---

## Summary

**To see violation proofs:**

1. Login as examiner
2. Click "📊 View Results" on an exam
3. Click on a student card
4. Scroll to "⚠️ Violations" section
5. Click "📷 View Evidence" link
6. Screenshot opens in new tab

**If no links appear:**
- Take a NEW exam with violations
- Make sure backend is running
- Make sure frontend is restarted
- Check evidence folder has files

---

**Need help? Check if backend and frontend are both running and restarted!** 🚀
