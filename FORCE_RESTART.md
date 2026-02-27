# FORCE RESTART - The 404 is Still There

## The Problem:

The backend file was updated but Flask's auto-reloader didn't pick up the change. You need to FORCE restart it.

## Solution:

### 1. STOP the Backend Completely

In the terminal running the backend:
1. Press `Ctrl + C` (might need to press twice)
2. Wait until you see the command prompt again
3. Make sure it says "PS C:\Projects\online-exam\backend>"

### 2. Verify the File is Correct

Run this to check:
```bash
findstr "Blueprint('proctoring'" routes\proctoring.py
```

You should see:
```
proctoring_bp = Blueprint('proctoring', __name__)
```

If you see `url_prefix='/api/proctoring'` in that line, the file wasn't saved correctly.

### 3. Start Backend Again

```bash
python run.py
```

Wait for it to show:
```
Server running at http://localhost:5000
```

### 4. Test the Endpoint

Open a NEW terminal and run:
```bash
cd backend
python test_submit.py
```

You should see:
```
Status: 200
Response: Exam submitted successfully
```

If you still see 404, the file change didn't save.

## Alternative: Manual Fix

If the above doesn't work, manually edit the file:

1. Open `backend/routes/proctoring.py` in your editor
2. Find line 21 (around there):
   ```python
   proctoring_bp = Blueprint('proctoring', __name__, url_prefix='/api/proctoring')
   ```
3. Change it to:
   ```python
   proctoring_bp = Blueprint('proctoring', __name__)
   ```
4. Save the file (Ctrl+S)
5. Stop backend (Ctrl+C)
6. Start backend again (`python run.py`)

## Why This Happens:

Flask's debug mode auto-reloader sometimes doesn't detect changes to imported modules. A full restart is needed.

## Verification:

After restarting, the backend terminal should show:
```
* Restarting with stat
* Debugger is active!
```

Then test with:
```bash
python test_submit.py
```

Should return Status 200, not 404.

## If Still 404:

Check the backend terminal for errors. You might see:
- Import errors
- Syntax errors  
- Module not found errors

Copy any error messages and we'll fix them.
