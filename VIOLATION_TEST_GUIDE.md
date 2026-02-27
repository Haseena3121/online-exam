# 🚨 Violation Testing Guide

## Changes Made

### 1. Camera Blur Fixed
- **Before:** Camera was blurred by default
- **After:** Camera shows clear video feed
- **Toggle:** Click "Blur ON/OFF" button to test

### 2. Violation Detection Enabled
- Added actual violation detection logic
- Added console logging for debugging
- Added cooldown (10 seconds between same violation type)

### 3. Violations That Now Work

#### Tab Switch (Already Working)
- Switch to another tab/window
- **Severity:** High
- **Trust Score:** -20%
- **Test:** Press `Alt+Tab` during exam

#### Blur Disabled
- Turn off background blur
- **Severity:** Low  
- **Trust Score:** -5%
- **Test:** Click "Blur OFF" button

#### Face Not Visible
- Camera detects very dark/no face
- **Severity:** Medium
- **Trust Score:** -10%
- **Test:** Cover camera or turn off lights

#### Multiple Persons (Simulated)
- Detects more than one person
- **Severity:** High
- **Trust Score:** -20%
- **Test:** Random 5% chance every 2 seconds

---

## 🧪 How to Test

### Step 1: Start Exam
1. Login as student: `skhaseena009@gmail.com` / `password123`
2. Take exam #2
3. Accept terms and start exam

### Step 2: Open Browser Console
- Press `F12`
- Go to "Console" tab
- You should see logs like:
  ```
  Fetching exam details for exam ID: 2
  Exam data received: Object
  ```

### Step 3: Test Violations

#### Test 1: Tab Switch
1. Switch to another tab: `Alt+Tab`
2. Switch back to exam
3. **Expected:**
   - Console: `📊 Reporting violation: tab_switch (high)`
   - Console: `✅ Violation reported. New trust score: 80%`
   - Warning message appears on screen
   - Trust score changes from 100% to 80%

#### Test 2: Blur Toggle
1. Click "Blur OFF" button
2. **Expected:**
   - Console: `🚨 Blur disabled - reporting violation`
   - Console: `📊 Reporting violation: blur_disabled (medium)`
   - Trust score decreases by 10%

#### Test 3: Multiple Tab Switches
1. Switch tabs 5 times
2. **Expected:**
   - Trust score: 100% → 80% → 60% → 40% → 20% → 0%
   - After 5th switch (trust < 50%):
     - Alert: "Trust score below 50%. Exam will be auto-submitted!"
     - Exam auto-submits
     - Redirects to results page

---

## 📊 Trust Score Breakdown

| Violation Type | Severity | Score Reduction |
|---------------|----------|-----------------|
| Tab Switch | High | -20% |
| Multiple Persons | High | -20% |
| Face Not Visible | Medium | -10% |
| Blur Disabled | Low | -5% |
| Suspicious Behavior | High | -20% |

---

## 🔍 Debugging

### If Trust Score Not Decreasing

1. **Check Console Logs:**
   - Look for: `📊 Reporting violation:`
   - Look for: `✅ Violation reported. New trust score:`
   - If you see these, violation is being sent

2. **Check Backend Terminal:**
   - Look for: `WARNING:root:Violation: tab_switch for student X, Trust Score: 80%`
   - If you see this, backend received it

3. **Check for Errors:**
   - Console errors in red
   - Backend errors in terminal
   - 404 or 500 errors

### Common Issues

#### Issue: No console logs when switching tabs
**Solution:** Make sure you're on the exam page, not another tab

#### Issue: Console shows error 404
**Solution:** Backend not running or wrong URL
```powershell
cd backend
python run.py
```

#### Issue: Console shows error 401
**Solution:** Not logged in or token expired
- Logout and login again

#### Issue: Trust score shows but doesn't change
**Solution:** Check backend terminal for errors
- Look for database errors
- Check proctoring_sessions table exists

---

## 🎯 Expected Behavior

### Normal Flow
1. Start exam → Trust score: 100%
2. Switch tab → Trust score: 80%
3. Switch tab → Trust score: 60%
4. Switch tab → Trust score: 40%
5. Switch tab → Trust score: 20%
6. Switch tab → Trust score: 0% → Auto-submit

### With Multiple Violation Types
1. Start exam → Trust score: 100%
2. Switch tab → Trust score: 80% (high)
3. Turn off blur → Trust score: 75% (low)
4. Switch tab → Trust score: 55% (high)
5. Switch tab → Trust score: 35% (high) → Warning shown
6. Switch tab → Trust score: 15% (high) → Auto-submit

---

## 📝 What to Report

### If Working:
✅ "Trust score decreases when I switch tabs"
✅ "Exam auto-submitted after 5 tab switches"
✅ "Console shows violation logs"

### If Not Working:
❌ "Trust score stays at 100% even after violations"
❌ "Console shows: [paste error message]"
❌ "Backend shows: [paste error message]"

---

## 🔄 Restart Instructions

If you made changes, restart frontend:

```powershell
cd C:\Projects\online-exam\frontend
# Press Ctrl+C to stop
npm start
```

Then:
1. Hard refresh browser: `Ctrl + Shift + R`
2. Login again
3. Take exam #2
4. Open console (F12)
5. Test violations

---

**Ready to test?** Follow Step 1-3 above! 🚀
