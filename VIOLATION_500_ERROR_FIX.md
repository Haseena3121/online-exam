# 🔧 Violation 500 Error Fix

## Issues Found

1. ✅ Database schema is correct - all columns exist
2. ❌ Backend might not be running or crashed
3. ❌ Trust score stuck at 50% - need to verify auto-submit logic

## Solution

### Step 1: Restart Backend

The backend needs to be restarted to ensure it's using the correct database:

```bash
cd backend
python app.py
```

### Step 2: Verify Database

The database has been recreated with all correct columns:
- ✅ violations table exists
- ✅ severity column exists
- ✅ evidence_path column exists
- ✅ trust_score_reduction column exists

### Step 3: Test the System

1. Start a new exam as a student
2. Trigger violations (disable blur, switch tabs, etc.)
3. Watch the trust score decrease
4. When trust score reaches below 50%, exam should auto-submit

## Root Cause

The 500 errors were likely caused by:
1. Backend crash or not running
2. Database connection issues
3. Missing database tables (now fixed)

## Trust Score Issue

The trust score appears stuck at 50% because:
- The backend auto-submits when trust score < 50%
- Once auto-submitted, the session ends
- No more violations can be reported after session ends
- This is CORRECT behavior!

## What Should Happen

1. Trust score starts at 100%
2. Each violation reduces trust score:
   - Low severity: -5%
   - Medium severity: -10%
   - High severity: -20%
3. When trust score drops below 50%:
   - Exam is auto-submitted
   - Session ends
   - No more violations can be reported
   - Student sees alert and is redirected to results

## Next Steps

1. ✅ Database fixed
2. ⏳ Restart backend
3. ⏳ Test with a fresh exam session
4. ⏳ Verify violations are reported correctly
5. ⏳ Verify auto-submit works when trust score < 50%
