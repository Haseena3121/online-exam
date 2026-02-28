# ✅ Complete Solution - Evidence & Examiner Access

## 🎯 Two Issues to Fix

### Issue 1: 403 Forbidden (Can't Access Examiner Dashboard)
**Problem**: You're logged in as student, not examiner
**Solution**: Login as examiner

### Issue 2: No Evidence in Violations
**Problem**: 93 violations recorded but 0 have evidence
**Solution**: Fix evidence saving and test with NEW exam

---

## 🚀 Step 1: Login as Examiner

### Available Examiner Accounts
```
ID: 2, Name: sindhu, Email: skhaseena0@gmail.com, Role: examiner
ID: 6, Name: Bhavya, Email: haseena009@gmail.com, Role: examiner  
ID: 12, Name: Shaik Haseena, Email: harini1@gmail.com, Role: examiner
```

### How to Login as Examiner
1. **Logout** from current account
2. **Login** with one of these examiner emails:
   - `skhaseena0@gmail.com` (sindhu)
   - `haseena009@gmail.com` (Bhavya)
   - `harini1@gmail.com` (Shaik Haseena)
3. Use the password you set for that account

---

## 🔧 Step 2: Fix Evidence Saving

The evidence isn't being saved because the old violations were created before we fixed the session issue.

### Test with NEW Exam
1. **Login as student** (different browser/incognito)
2. **Start a FRESH exam** (not old ones)
3. **Trigger violations** during exam
4. **Check evidence is saved**
5. **View as examiner**

---

## 📋 Complete Testing Process

### Phase 1: Login as Examiner
```
1. Go to http://localhost:3000
2. Logout if needed
3. Login with: skhaseena0@gmail.com (or other examiner)
4. Should see "Examiner Dashboard" (no 403 error)
5. Click "📊 View Results" on any exam
6. See list of students who took exams
```

### Phase 2: Test Evidence Saving (New Exam)
```
1. Open incognito/private browser window
2. Go to http://localhost:3000
3. Login as student (e.g., skhaseena009@gmail.com)
4. Start a NEW exam attempt
5. During exam:
   - Look away from camera
   - Have someone else in frame
   - Turn camera away
6. Watch trust score decrease
7. Submit exam or let it auto-submit
```

### Phase 3: View Evidence as Examiner
```
1. Back to examiner browser
2. Refresh results page
3. Click on the student who just took exam
4. Should see violations with evidence
5. Click "📷 View Evidence" links
```

---

## 🔍 Verification Commands

### Check if New Session Created
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT id, student_id, exam_id, status, start_time FROM proctoring_sessions ORDER BY id DESC LIMIT 3')
print('Recent sessions:')
for row in cursor.fetchall():
    print(f'  ID: {row[0]}, Student: {row[1]}, Exam: {row[2]}, Status: {row[3]}, Time: {row[4]}')
conn.close()
"
```

### Check New Violations with Evidence
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT id, violation_type, evidence_path, created_at FROM violations ORDER BY id DESC LIMIT 5')
print('Recent violations:')
for row in cursor.fetchall():
    evidence = 'YES' if row[2] else 'NO'
    print(f'  ID: {row[0]}, Type: {row[1]}, Evidence: {evidence}, Time: {row[3]}')
conn.close()
"
```

### Check Evidence Files
```bash
cd backend
ls -la uploads/evidence/
```

---

## 🎯 Expected Results

### After Logging as Examiner
- ✅ No 403 errors
- ✅ Can see examiner dashboard
- ✅ Can view exam results
- ✅ Can see student list

### After New Exam with Violations
- ✅ New proctoring session created
- ✅ Violations saved with evidence_path
- ✅ Evidence files in uploads/evidence/
- ✅ Examiner can see "📷 View Evidence" links
- ✅ Evidence screenshots open when clicked

---

## 🐛 If Still Not Working

### Issue: Still Getting 403 Errors
**Check**: Are you really logged in as examiner?
```javascript
// In browser console (F12):
console.log(localStorage.getItem('access_token'));
// Should show a JWT token

// Check user role:
fetch('http://localhost:5000/api/auth/me', {
  headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
}).then(r => r.json()).then(console.log);
// Should show role: "examiner"
```

### Issue: Evidence Still Not Saving
**Check**: Is new session being created?
- Look at backend terminal for: "✅ Proctoring session created successfully"
- If not, check backend logs for errors

### Issue: Can't See Evidence Links
**Check**: Do violations have evidence_path?
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT id, violation_type, evidence_path FROM violations WHERE evidence_path IS NOT NULL ORDER BY id DESC LIMIT 3')
for row in cursor.fetchall():
    print(f'Violation {row[0]}: {row[1]} -> {row[2]}')
conn.close()
"
```

---

## 📊 Current Status Summary

### What We Know
- ✅ Backend is running
- ✅ Database has exams and results
- ✅ 93 violations recorded (but no evidence)
- ✅ Examiner accounts exist
- ✅ Session creation fix applied

### What to Do
1. **Login as examiner** (fix 403 error)
2. **Test with NEW exam** (evidence will be saved)
3. **View evidence as examiner**

### Why Old Violations Have No Evidence
- Old violations were created before session fix
- No proctoring session = no evidence saving
- New exams will have evidence

---

## 🎉 Quick Action Plan

### Right Now (5 minutes)
1. **Logout** and **login as examiner**
2. **Check** you can access examiner dashboard
3. **View** existing results (no evidence yet)

### Test Evidence (10 minutes)
1. **Open incognito window**
2. **Login as student**
3. **Start NEW exam**
4. **Trigger violations**
5. **Check evidence is saved**

### Verify Success (2 minutes)
1. **Refresh examiner results**
2. **Click on new student**
3. **See violations with evidence**
4. **Click evidence links**

---

**The fix is ready - just need to login as examiner and test with a new exam!** 🎉