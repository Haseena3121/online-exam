# 🎥 Copy/Paste Detection & Live Monitoring Guide

## New Features Added

### 1. ✅ Copy/Paste Detection for Students
Students can no longer copy, paste, or cut text during exams. Any attempt triggers:
- Immediate warning message
- Violation logged to database
- Trust score reduction
- Evidence recorded

### 2. ✅ Real-Time Monitoring Dashboard for Examiners
Examiners can now monitor active exams in real-time:
- See all students currently taking exams
- View trust scores live
- See violations as they happen
- Auto-refresh every 5 seconds
- Detailed session information

---

## 🚀 How to Use

### For Students (Copy/Paste Detection)

When taking an exam:

1. **Copying Text (Ctrl+C):**
   - ❌ Blocked
   - ⚠️ Warning: "COPYING IS NOT ALLOWED!"
   - 📊 Trust Score: -20%
   - 📝 Violation Type: `copy_attempt`

2. **Pasting Text (Ctrl+V):**
   - ❌ Blocked
   - ⚠️ Warning: "PASTING IS NOT ALLOWED!"
   - 📊 Trust Score: -20%
   - 📝 Violation Type: `paste_attempt`

3. **Cutting Text (Ctrl+X):**
   - ❌ Blocked
   - ⚠️ Warning: "CUTTING TEXT IS NOT ALLOWED!"
   - 📊 Trust Score: -10%
   - 📝 Violation Type: `cut_attempt`

**Warning Display:**
- Shows for 5 seconds
- Red banner at top of screen
- Cannot be dismissed early
- Violation is logged immediately

### For Examiners (Live Monitoring)

1. **Access Monitoring Dashboard:**
   ```
   Login as examiner → Examiner Dashboard → Click "🎥 Live Monitoring"
   ```

2. **Dashboard Features:**
   - **Active Sessions List:** See all students currently taking exams
   - **Auto-Refresh:** Updates every 5 seconds automatically
   - **Manual Refresh:** Click "🔄 Refresh Now" button
   - **Session Details:** Click any session to see full details

3. **Information Displayed:**
   - Student name and email
   - Exam title and duration
   - Current trust score (color-coded)
   - Elapsed time
   - Camera/mic status
   - Violation count
   - Recent violations list

4. **Trust Score Colors:**
   - 🟢 Green (80-100%): Good
   - 🟠 Orange (50-79%): Warning
   - 🔴 Red (0-49%): Critical

---

## 📊 Violation Types & Penalties

| Violation Type | Severity | Trust Score Reduction | Icon |
|---------------|----------|----------------------|------|
| Copy Attempt | High | -20% | 📋 |
| Paste Attempt | High | -20% | 📌 |
| Cut Attempt | Medium | -10% | ✂️ |
| Tab Switch | High | -20% | 🔄 |
| Blur Disabled | Low | -5% | 🟪 |
| Multiple Persons | High | -20% | 👥 |
| Face Not Visible | Medium | -10% | 👤 |
| Suspicious Behavior | High | -20% | ⚠️ |

---

## 🔧 Setup Instructions

### Step 1: Restart Backend

```powershell
cd C:\Projects\online-exam\backend
python clean_start.py
python run.py
```

**Expected output:**
```
🎓 Online Exam Proctoring System
Server running at http://localhost:5000
```

### Step 2: Restart Frontend

```powershell
cd C:\Projects\online-exam\frontend
# Press Ctrl+C to stop
npm start
```

**Expected output:**
```
Compiled successfully!
Local: http://localhost:3000
```

### Step 3: Clear Browser Cache

Press `Ctrl + Shift + R` for hard refresh

---

## 🧪 Testing

### Test Copy/Paste Detection

1. **Login as Student:**
   ```
   Email: skhaseena009@gmail.com
   Password: password123
   ```

2. **Start Exam:**
   - Go to Exam List
   - Take exam #2 or #3
   - Accept terms and start

3. **Try to Copy:**
   - Select any text on the page
   - Press `Ctrl+C`
   - ✅ Should see warning message
   - ✅ Trust score should decrease

4. **Try to Paste:**
   - Press `Ctrl+V` anywhere
   - ✅ Should see warning message
   - ✅ Trust score should decrease

5. **Check Console (F12):**
   ```
   📊 Reporting violation: copy_attempt (high)
   ✅ Violation reported. New trust score: 80%
   ```

### Test Live Monitoring

1. **Open Two Browser Windows:**
   - Window 1: Student taking exam
   - Window 2: Examiner monitoring

2. **Window 1 - Student:**
   ```
   Login: skhaseena009@gmail.com / password123
   Start exam #2 or #3
   ```

3. **Window 2 - Examiner:**
   ```
   Login: skhaseena0@gmail.com / password123
   Go to Examiner Dashboard
   Click "🎥 Live Monitoring"
   ```

4. **Verify Monitoring:**
   - ✅ Student session appears in list
   - ✅ Trust score shows 100%
   - ✅ Camera/mic status visible
   - ✅ Elapsed time counting

5. **Trigger Violations (Window 1):**
   - Try to copy text
   - Switch tabs
   - Turn off blur

6. **Watch Monitoring (Window 2):**
   - ✅ Trust score decreases in real-time
   - ✅ Violations appear in list
   - ✅ Click session to see details
   - ✅ Auto-refreshes every 5 seconds

---

## 📁 Files Created/Modified

### Backend
1. `backend/routes/proctoring.py`
   - Added `/api/proctoring/monitor/active-sessions` endpoint
   - Added `/api/proctoring/monitor/session/<id>/details` endpoint

### Frontend
1. `frontend/src/pages/ExamInterface.js`
   - Added copy/paste/cut detection
   - Added warning messages

2. `frontend/src/pages/LiveMonitoring.js` (NEW)
   - Real-time monitoring dashboard
   - Auto-refresh functionality
   - Session details view

3. `frontend/src/styles/LiveMonitoring.css` (NEW)
   - Monitoring dashboard styles
   - Responsive design

4. `frontend/src/App.js`
   - Added `/live-monitoring` route

5. `frontend/src/pages/ExaminarDashboard.js`
   - Added "Live Monitoring" button

---

## 🎯 Expected Behavior

### During Exam (Student View)

1. **Normal Typing:** ✅ Works fine
2. **Copy (Ctrl+C):** ❌ Blocked + Warning
3. **Paste (Ctrl+V):** ❌ Blocked + Warning
4. **Cut (Ctrl+X):** ❌ Blocked + Warning
5. **Right-click:** ❌ Blocked
6. **Tab Switch:** ⚠️ Warning + Violation

### Monitoring Dashboard (Examiner View)

1. **No Active Exams:**
   - Shows "No Active Exams" message
   - Explains that sessions will appear here

2. **Active Exams:**
   - List of all active sessions
   - Real-time trust scores
   - Violation counts
   - Auto-refresh every 5 seconds

3. **Session Details:**
   - Click any session card
   - See full student info
   - See exam details
   - See all violations with timestamps
   - See trust score history

---

## 🔍 Troubleshooting

### Issue: Copy/paste still works

**Solution:**
1. Hard refresh browser: `Ctrl + Shift + R`
2. Check console for errors
3. Verify frontend restarted

### Issue: Monitoring shows no sessions

**Possible Reasons:**
1. No students currently taking exams
2. Backend not running
3. Examiner not logged in
4. Student's session ended

**Solution:**
1. Start a new exam as student
2. Check backend is running
3. Click "Refresh Now" button

### Issue: Violations not showing in monitoring

**Solution:**
1. Restart backend: `python clean_start.py && python run.py`
2. Check backend terminal for errors
3. Verify violations table exists: `python fix_violations_table.py`

### Issue: Auto-refresh not working

**Solution:**
1. Check "Auto-refresh (5s)" checkbox is enabled
2. Check browser console for errors
3. Manually click "Refresh Now"

---

## 📊 Database Tables

### Violations Table
Stores all violation attempts:
- `id`: Unique violation ID
- `student_id`: Student who violated
- `exam_id`: Exam being taken
- `session_id`: Proctoring session
- `violation_type`: Type of violation
- `trust_score_reduction`: Points deducted
- `created_at`: Timestamp

### Proctoring Sessions Table
Tracks active exams:
- `id`: Session ID
- `student_id`: Student taking exam
- `exam_id`: Exam ID
- `status`: active/ended
- `current_trust_score`: Current score
- `start_time`: When exam started
- `end_time`: When exam ended

---

## 🎉 Success Indicators

### Copy/Paste Detection Working:
- ✅ Warning message appears
- ✅ Console shows violation log
- ✅ Trust score decreases
- ✅ Violation saved to database

### Live Monitoring Working:
- ✅ Active sessions appear in list
- ✅ Trust scores update in real-time
- ✅ Violations appear immediately
- ✅ Auto-refresh works
- ✅ Session details load correctly

---

## 📝 Next Steps

### Enhancements You Can Add:

1. **Screenshot Capture:**
   - Capture screenshot when violation occurs
   - Store as evidence
   - Display in monitoring dashboard

2. **Email Alerts:**
   - Send email to examiner on critical violations
   - Daily violation summary

3. **Export Reports:**
   - Download violation reports as PDF
   - Export session data as CSV

4. **Video Recording:**
   - Record exam session
   - Store video evidence
   - Playback in monitoring

5. **WebSocket Integration:**
   - Real-time push notifications
   - Instant violation alerts
   - Live chat with student

---

**Ready to test? Follow the Setup Instructions above!** 🚀
