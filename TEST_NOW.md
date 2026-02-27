# 🚀 TEST NOW - Quick Start

## ✅ Status Check

Both servers are running:
- ✅ Backend: http://localhost:5000
- ✅ Frontend: http://localhost:3000
- ✅ Database: Ready with 2 exams
- ✅ Fix Applied: Exam won't auto-submit

---

## 🎯 Test in 4 Steps

### 1️⃣ Open Browser
```
http://localhost:3000
```

### 2️⃣ Login as Student
```
Email: skhaseena009@gmail.com
Password: password123
```

### 3️⃣ Take Exam
- Click "View Available Exams"
- Find "test_2" (30 min, 10 marks, 3 questions)
- Click "Take Exam"
- Accept terms
- Click "Accept & Start Exam"

### 4️⃣ Verify It Works
- ✅ Exam loads (no auto-submit)
- ✅ Timer shows 30:00
- ✅ See Question 1 of 3
- ✅ Can select answers
- ✅ Can navigate questions
- ✅ Trust score: 100%

---

## ✅ What Should Happen

**GOOD:**
- Exam interface loads properly
- Camera feed appears
- Timer counts down from 30:00
- Can answer all 3 questions
- Can submit manually

**BAD (Old Bug - Now Fixed):**
- ❌ Exam auto-submits immediately
- ❌ Shows 0 marks instantly
- ❌ Never see questions

---

## 🔄 If You Need to Restart

### Frontend Only
```powershell
cd C:\Projects\online-exam\frontend
# Press Ctrl+C
npm start
```

### Backend Only
```powershell
cd C:\Projects\online-exam\backend
python run.py
```

### Both (Full Restart)
```powershell
# Terminal 1 - Backend
cd C:\Projects\online-exam\backend
python clean_start.py
python run.py

# Terminal 2 - Frontend
cd C:\Projects\online-exam\frontend
npm start
```

---

## 🎓 Test Accounts

**Student:**
- skhaseena009@gmail.com / password123

**Examiner:**
- skhaseena0@gmail.com / password123

---

## 📊 Available Exams

**Exam #1:** "test"
- ⚠️ Has 0 questions (skip this)

**Exam #2:** "test_2" ✅
- Duration: 30 minutes
- Total Marks: 10
- Questions: 3
- Status: Published

---

## 🆘 Quick Fixes

### Exam still auto-submits?
```
Press Ctrl + Shift + R (hard refresh)
```

### 404 errors?
```powershell
cd backend
python clean_start.py
python run.py
```

### Can't see exams?
- Make sure you're logged in as STUDENT
- Examiner account sees different dashboard

---

## 📞 What to Report

If it works:
✅ "Exam loaded successfully, can answer questions"

If it fails:
❌ "Still auto-submitting" or
❌ "Getting error: [error message]" or
❌ "Can't see questions"

---

**Ready? Go test now!** 🚀

Open: http://localhost:3000
