# 📸 Violation Evidence & Proof Viewing Guide

## Overview
This guide explains how examiners can view violation evidence (screenshots/videos) captured during student exams.

---

## 🔧 Setup Required

### 1. Update Database Schema
First, run the database migration to add evidence columns:

```bash
cd backend
python update_database_schema.py
```

This will add:
- `evidence_path` column to violations table
- `severity` and `description` columns to violations table
- `final_trust_score`, `status`, `submitted_at` columns to exam_results table
- Additional columns to examiner_notifications table

### 2. Restart Backend
After updating the database:

```bash
cd backend
python app.py
```

---

## 📊 How to View Violation Evidence

### Step 1: Login as Examiner
1. Go to http://localhost:3000
2. Login with examiner credentials

### Step 2: Access Examiner Dashboard
1. Click on "Examiner Dashboard" in the navigation
2. You'll see a list of all your exams

### Step 3: View Exam Results
1. Find the exam you want to review
2. Click the "📊 View Results" button
3. You'll see a list of all students who took the exam

### Step 4: View Student Details
1. Click on any student card in the results list
2. The right panel will show detailed information:
   - **Performance**: Marks obtained, percentage, trust score
   - **Violations**: List of all violations with evidence
   - **Submission Details**: When the exam was submitted

### Step 5: View Violation Evidence
For each violation, you'll see:
- **Violation Type**: e.g., "MULTIPLE PERSONS", "BLUR DISABLED"
- **Severity Badge**: LOW (yellow), MEDIUM (orange), HIGH (red)
- **Trust Score Reduction**: How much the trust score was reduced
- **Timestamp**: When the violation occurred
- **📷 View Evidence Button**: Click to see the screenshot/video proof

---

## 🎯 Understanding Violation Evidence

### Evidence Types
1. **Screenshots**: Captured when violations are detected
2. **Videos**: Recorded during critical violations (if enabled)

### Severity Levels
- **🟡 LOW**: Minor violations (5% trust score reduction)
  - Background blur disabled
  - Brief face not visible
  
- **🟠 MEDIUM**: Moderate violations (10% trust score reduction)
  - Eye gaze away from screen
  - Head movement warnings
  
- **🔴 HIGH**: Critical violations (20% trust score reduction)
  - Multiple persons detected
  - Phone detected
  - Tab switching

### Evidence Storage
- Evidence files are stored in `backend/uploads/evidence/`
- Files are kept for 24 hours by default
- Automatic cleanup runs daily (configurable)

---

## 🚨 Auto-Submit Feature

### When Does Auto-Submit Happen?
When a student's trust score falls below 50%, the exam is automatically submitted.

### What Happens During Auto-Submit?
1. Exam is immediately submitted
2. Student receives 0 marks
3. Status is marked as "AUTO-SUBMITTED"
4. Examiner receives a notification
5. All violations and evidence are preserved

### Viewing Auto-Submitted Exams
- Auto-submitted exams show an orange "AUTO-SUBMITTED" badge
- All violation evidence is available for review
- Trust score history shows the decline

---

## 📱 Live Monitoring

### Real-Time Monitoring
Examiners can monitor students in real-time:

1. Click "🎥 Live Monitoring" button on dashboard
2. See all active exam sessions
3. View current trust scores
4. See recent violations as they happen

### Monitoring Features
- **Active Sessions**: See who's currently taking exams
- **Trust Score**: Real-time trust score updates
- **Recent Violations**: Last 5 violations per student
- **Camera Status**: Check if camera/mic is active

---

## 🔍 Troubleshooting

### Evidence Not Showing?
1. **Check Database**: Run `python update_database_schema.py`
2. **Check Uploads Folder**: Ensure `backend/uploads/evidence/` exists
3. **Check Permissions**: Folder must be writable
4. **Restart Backend**: After any changes

### Evidence Link Not Working?
1. **Check Backend URL**: Should be `http://localhost:5000`
2. **Check File Exists**: Look in `backend/uploads/evidence/`
3. **Check Browser Console**: Look for 404 errors
4. **Verify JWT Token**: Ensure you're logged in as examiner

### No Violations Recorded?
1. **Check Frontend**: Violations should be logged in browser console
2. **Check Backend Logs**: Look for violation recording errors
3. **Check Database**: Query violations table directly
4. **Test Camera**: Ensure camera permissions are granted

---

## 📋 Database Queries (For Debugging)

### Check Violations
```sql
SELECT * FROM violations WHERE exam_id = YOUR_EXAM_ID;
```

### Check Evidence Paths
```sql
SELECT id, violation_type, evidence_path, created_at 
FROM violations 
WHERE evidence_path IS NOT NULL;
```

### Check Results
```sql
SELECT * FROM exam_results WHERE exam_id = YOUR_EXAM_ID;
```

---

## 🎨 UI Features

### Results Page Features
- **Search**: Filter students by name or email
- **Filter Tabs**: View All / Passed / Failed
- **Statistics**: Total students, pass/fail counts, average score
- **Color Coding**:
  - 🟢 Green: Passed
  - 🔴 Red: Failed
  - 🟠 Orange: Auto-submitted

### Violation Display
- **Chronological Order**: Most recent violations first
- **Visual Indicators**: Color-coded severity badges
- **Evidence Preview**: Click to open in new window
- **Detailed Info**: Type, time, trust score impact

---

## 🔐 Security & Privacy

### Access Control
- Only examiners can view violation evidence
- Students cannot access other students' evidence
- JWT authentication required for all evidence requests

### Data Retention
- Evidence stored for 24 hours by default
- Automatic cleanup via `cleanup_evidence.py`
- Can be configured in backend settings

### Privacy Compliance
- Evidence only captured during exam time
- Clear consent required before exam starts
- Students informed about monitoring

---

## 📞 Support

### Common Issues
1. **"No active session" error**: Student needs to restart exam
2. **"Unauthorized" error**: Check examiner role in database
3. **Evidence not loading**: Check file permissions and paths

### Need Help?
- Check backend logs: `backend/logs/app.log`
- Check browser console for frontend errors
- Verify database schema is up to date

---

## ✅ Quick Checklist

Before viewing violation evidence:
- [ ] Database schema updated
- [ ] Backend restarted
- [ ] Uploads folder exists and is writable
- [ ] Logged in as examiner
- [ ] Student has completed exam
- [ ] Violations were actually triggered during exam

---

## 🎯 Best Practices

1. **Review Evidence Promptly**: Evidence may be auto-deleted after 24 hours
2. **Check All Violations**: Don't just look at high-severity ones
3. **Consider Context**: Some violations may be false positives
4. **Document Decisions**: Keep notes on why you accepted/rejected evidence
5. **Fair Evaluation**: Use evidence to support, not replace, judgment

---

## 📈 Future Enhancements

Planned features:
- Video recording of entire exam session
- AI-powered violation analysis
- Bulk evidence download
- Evidence retention policy configuration
- Student appeal system

---

**Last Updated**: February 2026
**Version**: 1.0
