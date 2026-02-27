# 🚀 RESTART GUIDE - Fix Exam Auto-Submit Issue

## ✅ What Was Fixed

The exam was auto-submitting immediately with 0 marks because `timeLeft` was initialized to `0`. This has been fixed in `frontend/src/pages/ExamInterface.js`.

## 📋 Steps to Restart (Follow Exactly)

### Step 1: Restart Backend (if not running)

Open PowerShell in `backend` folder:

```powershell
cd C:\Projects\online-exam\backend
```

Run the restart script:

```powershell
.\RESTART_BACKEND.bat
```

OR manually:

```powershell
python clean_start.py
python run.py
```

You should see:
```
🎓 Online Exam Proctoring System
Server running at http://localhost:5000
```

### Step 2: Restart Frontend

Open a NEW PowerShell window in `frontend` folder:

```powershell
cd C:\Projects\online-exam\frontend
```

Stop the current server (if running): Press `Ctrl + C`

Start fresh:

```powershell
npm start
```

Wait for:
```
Compiled successfully!
You can now view frontend in the browser.
Local: http://localhost:3000
```

### Step 3: Clear Browser Cache

In your browser (Chrome/Edge):
- Press `Ctrl + Shift + R` (hard refresh)
- Or press `F12` → Right-click refresh button → "Empty Cache and Hard Reload"

### Step 4: Test the Exam

1. Go to: http://localhost:3000

2. Login as STUDENT:
   - Email: `skhaseena009@gmail.com`
   - Password: `password123`

3. Click "View Available Exams"

4. Find "test_2" exam (should be published)

5. Click "Take Exam"

6. Accept all terms and conditions

7. Click "Accept & Start Exam"

### ✅ Expected Results

You should now see:

- ✅ Camera feed appears
- ✅ Timer shows "30:00" and starts counting down
- ✅ Question 1 of 3 is visible
- ✅ Can select answers (A, B, C, D options)
- ✅ Can navigate between questions
- ✅ Progress shows "0 of 3 answered"
- ✅ Trust score shows "100%"
- ✅ NO immediate auto-submit
- ✅ NO "0 marks" result

### 🎯 What You Can Do

- Answer questions by clicking radio buttons
- Navigate with "Previous" and "Next" buttons
- Click question numbers on the right to jump to any question
- Submit manually with "Submit Exam" button
- Exam will auto-submit only when:
  - Timer reaches 0:00
  - Trust score falls below 50%

## ❌ If Still Having Issues

### Issue: Backend won't start

```powershell
cd C:\Projects\online-exam\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Issue: Frontend won't start

```powershell
cd C:\Projects\online-exam\frontend
npm install
npm start
```

### Issue: Exam still auto-submits

1. Make sure you restarted frontend (Step 2)
2. Clear browser cache (Step 3)
3. Check browser console (F12) for errors
4. Check backend terminal for errors

### Issue: "No routes matched location /result/2"

This is normal - it happens after exam submits. The result page should still load.

### Issue: 404 on /api/proctoring/submit

Backend needs restart:
```powershell
cd C:\Projects\online-exam\backend
python clean_start.py
python run.py
```

## 📊 Test Accounts

### Student Account
- Email: `skhaseena009@gmail.com`
- Password: `password123`

### Examiner Account
- Email: `skhaseena0@gmail.com`
- Password: `password123`

## 🎉 Success Indicators

When everything works:

1. Backend shows: `Server running at http://localhost:5000`
2. Frontend shows: `Compiled successfully!`
3. Exam loads without auto-submitting
4. Timer counts down from 30:00
5. Can answer all 3 questions
6. Can submit manually

## 📝 Notes

- Backend must run on port 5000
- Frontend must run on port 3000
- Both must be running simultaneously
- Clear browser cache after frontend restart
- Check both terminal windows for errors

---

**Ready to test? Follow Steps 1-4 above!** 🚀
