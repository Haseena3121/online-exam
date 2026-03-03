# Backend Server Not Running - Quick Fix

## The Issue

The error shows:
```
Access to fetch at 'http://localhost:5000/api/results/all' from origin 'http://localhost:3000' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

This means: **Backend server is NOT running or crashed**

## Good News ✅

The auto-submit is working! Trust score went: 55% → 50% → 45% → 40%

The exam was auto-submitted when it hit 45% (below 50%).

## Quick Fix

### Step 1: Check if Backend is Running

Open a terminal and check:
```bash
# Windows
netstat -ano | findstr :5000

# If nothing shows, backend is not running
```

### Step 2: Start Backend Server

```bash
cd backend
python app.py
```

You should see:
```
============================================================
🚀 BACKEND SERVER STARTING
============================================================
📍 URL: http://127.0.0.1:5000
📍 Frontend should connect to: http://localhost:5000
============================================================
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

### Step 3: Verify Backend is Working

Open browser and go to:
```
http://localhost:5000/
```

Should see:
```json
{"message": "Backend Running Successfully 🚀"}
```

### Step 4: Test Results API

```
http://localhost:5000/api/results/all
```

Should see either:
- Results data (if logged in)
- `{"error": "Missing authorization header"}` (if not logged in - this is OK)

### Step 5: Refresh Frontend

Once backend is running:
1. Go back to frontend (http://localhost:3000)
2. Refresh the page (F5)
3. Results should load now

## Common Issues

### Issue 1: Port 5000 Already in Use
```
Error: Address already in use
```

**Fix:**
```bash
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Then start backend again
python app.py
```

### Issue 2: Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```

**Fix:**
```bash
pip install -r requirements.txt
```

### Issue 3: Database Connection Error
```
Error connecting to database
```

**Fix:**
```bash
# Check MySQL is running
mysql -u root -p

# If not running, start MySQL service
# Windows: Services → MySQL → Start
```

## What's Working Now ✅

Based on your logs:
1. ✅ Violations are being detected
2. ✅ Trust score is decreasing correctly
3. ✅ Auto-submit triggered at 45% (below 50%)
4. ✅ Proctoring stopped automatically
5. ❌ Results page can't load (backend not running)

## Next Steps

1. **Start backend server** (see Step 2 above)
2. **Refresh frontend**
3. **Check results page** - should show the auto-submitted exam with marks

## Expected Result

After starting backend, you should see:
- Results page loads successfully
- Shows the auto-submitted exam
- Displays marks for questions answered
- Shows trust score: 40%
- Shows violations count
- Shows "AUTO-SUBMITTED" status

## Quick Test Command

Run this in one command:
```bash
cd backend && python app.py
```

Keep this terminal open - don't close it!

## Status

- Auto-submit logic: ✅ Working
- Violation detection: ✅ Working  
- Trust score calculation: ✅ Working
- Backend server: ❌ Not running
- Results display: ⏳ Waiting for backend

**Just start the backend server and everything will work!** 🚀
