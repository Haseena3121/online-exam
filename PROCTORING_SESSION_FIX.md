# 🔧 Proctoring Session & Violation Fix

## Issues Found

### 1. ❌ 404 Error: "No active session"
**Problem:** Violations can't be reported because no active proctoring session exists

**Root Cause:** Sessions are being created but immediately closed when exam is submitted

**Evidence from logs:**
```
Session ID: 19
Student ID: 5, Exam ID: 3
Status: ended
Start: 2026-02-27 10:08:59
End: 2026-02-27 10:09:09  ← Only 10 seconds!
```

### 2. ❌ Missing `violations` Table
**Problem:** Database missing the violations table  
**Solution:** Created with `db.create_all()`

### 3. ❌ Examiner Not Getting Updates
**Problem:** No notification system implemented for real-time updates

---

## Solutions Applied

### Fix 1: Ensured Tables Exist
```bash
cd backend
python -c "from app import create_app; from database import db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Fix 2: Clean Backend Cache
```bash
cd backend
python clean_start.py
```

### Fix 3: Need to Restart Backend
The backend MUST be restarted for changes to take effect.

---

## How to Fix Now

### Step 1: Stop Backend
In the backend terminal, press `Ctrl+C`

### Step 2: Clean and Restart
```powershell
cd C:\Projects\online-exam\backend
python clean_start.py
python run.py
```

### Step 3: Test Again
1. Login as student
2. Take a NEW exam (don't resume old one)
3. Open console (F12)
4. Switch tabs to trigger violation
5. Check console for:
   ```
   📊 Reporting violation: tab_switch (high)
   ✅ Violation reported. New trust score: 80%
   ```

### Step 4: Check Backend Terminal
You should see:
```
WARNING:root:Violation: tab_switch for student X, Trust Score: 80%
```

---

## Why Sessions Were Ending Immediately

The old auto-submit bug was causing exams to submit right away, which closed the proctoring session. Now that we fixed the auto-submit issue, new sessions should stay active.

---

## Testing Checklist

### Before Testing
- [ ] Backend restarted with clean cache
- [ ] Frontend restarted
- [ ] Browser cache cleared (Ctrl+Shift+R)
- [ ] Logged in as student

### During Test
- [ ] Start a NEW exam (not old session)
- [ ] Console open (F12)
- [ ] Camera shows (not blurred)
- [ ] Trust score shows 100%

### Trigger Violations
- [ ] Switch tabs → Should see -20% trust score
- [ ] Turn off blur → Should see -5% trust score
- [ ] Switch tabs 5 times → Should auto-submit at <50%

### Expected Console Output
```
Fetching exam details for exam ID: X
Exam data received: Object
🚨 Violation detected: tab_switch (high)
📊 Reporting violation: tab_switch (high)
✅ Violation reported. New trust score: 80%
```

### Expected Backend Output
```
WARNING:root:Violation: tab_switch for student X, Trust Score: 80%
```

---

## Examiner Notifications

Currently, the examiner dashboard doesn't show real-time updates. To see exam results:

1. Login as examiner: `skhaseena0@gmail.com` / `password123`
2. Go to Examiner Dashboard
3. Click "View Results" on completed exams
4. See violations and trust scores

**Note:** Real-time notifications require WebSocket implementation (not currently implemented).

---

## Common Issues

### Issue: Still getting 404 on violation
**Solution:** 
1. Make sure you started a NEW exam (not resumed old one)
2. Check backend terminal for session creation log
3. Run `python check_sessions.py` to verify active session exists

### Issue: Session shows as 'ended' immediately
**Solution:**
1. This was the old auto-submit bug
2. Make sure frontend has the fix (timeLeft: null)
3. Hard refresh browser (Ctrl+Shift+R)
4. Start a completely new exam

### Issue: Backend shows "No such table: violations"
**Solution:**
```powershell
cd backend
python -c "from app import create_app; from database import db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## Files Created

1. `backend/check_sessions.py` - Check proctoring sessions and violations
2. `PROCTORING_SESSION_FIX.md` - This file

---

## Next Steps

1. **Restart backend** (CRITICAL!)
2. **Start a NEW exam** (don't resume)
3. **Test violations** (tab switch)
4. **Check console logs**
5. **Check backend logs**
6. **Report results**

---

**IMPORTANT:** You MUST restart the backend for the violations table to be available!

```powershell
cd C:\Projects\online-exam\backend
python clean_start.py
python run.py
```

Then test with a fresh exam session.
