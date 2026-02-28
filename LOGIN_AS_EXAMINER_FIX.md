# 🔧 FIX: 403 Forbidden Error - Login as Examiner

## ❌ PROBLEM
You're getting 403 Forbidden errors because you're logged in as a **STUDENT** but trying to access **EXAMINER** features.

## ✅ SOLUTION

### Step 1: Logout Current User
1. Go to your browser (http://localhost:3001 or whatever port is running)
2. Click **Logout** button in the top right
3. Clear browser storage (F12 → Application → Local Storage → Clear All)

### Step 2: Login as Examiner
Use one of these examiner accounts:

**Option 1:**
- Email: `skhaseena0@gmail.com`
- Password: `password123` (or whatever you set)
- Role: examiner

**Option 2:**
- Email: `haseena009@gmail.com` 
- Password: `password123`
- Role: examiner

**Option 3:**
- Email: `harini1@gmail.com`
- Password: `password123`
- Role: examiner

### Step 3: Access Examiner Dashboard
After logging in as examiner:
1. Go to **Examiner Dashboard**
2. You should now see your exams
3. Click **"View Results"** to see violation evidence

## 🎯 WHAT TO TEST

1. **Create New Exam** - Should work
2. **View Results** - Should show violation photos/videos inline
3. **Live Monitoring** - Should work
4. **Evidence Display** - Photos and videos should appear beside violation details

## 📝 NOTES
- Evidence is kept for 30 days automatically
- Only NEW exams will have evidence (old ones won't due to previous session bug)
- Inline evidence display shows photos/videos directly in violation details

## 🚀 SERVERS RUNNING
- ✅ Backend: http://localhost:5000
- ✅ Frontend: http://localhost:3001 (or check terminal for actual port)

**Ready to test!** 🎉