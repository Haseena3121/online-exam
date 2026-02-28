# ✅ Evidence Retention Fixed - 48 Hours

## 🎯 Problem Solved

**Issue**: Evidence files were disappearing immediately after exam completion
**Solution**: Configured evidence retention for 48 hours with manual cleanup only

---

## ✅ What's Been Done

### 1. Created Configuration File
**File**: `backend/config_evidence.py`
- Sets retention period to 48 hours
- Disables auto-cleanup (manual only)
- Configurable storage limits

### 2. Updated Cleanup Script
**File**: `backend/cleanup_evidence.py`
- Now uses config file
- Keeps evidence for 48 hours
- Only runs when manually executed

### 3. Created Verification Script
**File**: `backend/check_evidence.py`
- Checks evidence files
- Shows file ages
- Verifies database entries
- Provides recommendations

---

## 🚀 Quick Start

### Check Current Evidence Status
```bash
cd backend
python check_evidence.py
```

**Expected Output**:
```
======================================================================
📸 EVIDENCE RETENTION CHECK
======================================================================

⚙️ Configuration:
   Retention Period: 48 hours (2.0 days)
   Evidence Directory: uploads/evidence

✅ Evidence directory exists

📁 Files in evidence directory:
   Total files: 5

   Recent files:
   🟢 abc123_20240227_103015.jpg
      Age: 2.5 hours
      Size: 245.3 KB
      Created: 2024-02-27 10:30:15
   
   📊 Files by age:
      🟢 < 24 hours: 5
      🟡 24-48 hours: 0
      🔴 > 48 hours: 0 (ready for cleanup)

💡 Recommendations:
   ✅ All files are within retention period

======================================================================
✅ Check complete!
======================================================================
```

---

## 📋 Evidence Lifecycle

### Timeline
```
Hour 0:  Exam starts
Hour 0.5: Violation detected → Screenshot saved
Hour 1:  Exam ends
Hour 2:  Examiner views evidence ✅
Hour 24: Evidence still available ✅
Hour 47: Evidence still available ✅
Hour 48: Evidence still available ✅
Hour 49: Evidence ready for cleanup
         (Run: python cleanup_evidence.py)
Hour 50: Evidence deleted after cleanup
```

### File Indicators
- 🟢 **Green** (< 24 hours): Fresh evidence
- 🟡 **Yellow** (24-48 hours): Still available
- 🔴 **Red** (> 48 hours): Ready for cleanup

---

## 🔧 Configuration

### Current Settings
```python
# backend/config_evidence.py
EVIDENCE_RETENTION_HOURS = 48  # 2 days
AUTO_CLEANUP_ENABLED = False   # Manual only
MAX_EVIDENCE_SIZE_MB = 1000    # 1 GB total
MAX_FILE_SIZE_MB = 10          # 10 MB per file
```

### Change Retention Period

Edit `backend/config_evidence.py`:

```python
# Keep for 72 hours (3 days)
EVIDENCE_RETENTION_HOURS = 72

# Keep for 1 week
EVIDENCE_RETENTION_HOURS = 168

# Keep for 30 days
EVIDENCE_RETENTION_HOURS = 720
```

Then restart backend:
```bash
cd backend
# Stop current backend (Ctrl+C)
python app.py
```

---

## 🧹 Manual Cleanup

### When to Run
- After 48 hours have passed
- When storage is getting full
- Before archiving old exams

### How to Run
```bash
cd backend
python cleanup_evidence.py
```

### Expected Output
```
============================================================
🧹 EVIDENCE CLEANUP SCRIPT
============================================================
Directory: uploads/evidence
Max age: 48 hours
============================================================
Starting cleanup of files older than 48 hours...
Cutoff time: 2024-02-25 10:00:00
Deleted: old_file_1.jpg (age: 2 days, 5:00:00, size: 245678 bytes)
Deleted: old_file_2.jpg (age: 3 days, 1:00:00, size: 189234 bytes)
Cleanup complete!
Files deleted: 2
Space freed: 424.72 KB
============================================================
✅ Cleanup finished!
   Files deleted: 2
   Space freed: 424.72 KB
============================================================
```

---

## ✅ Verification Steps

### 1. Check Configuration
```bash
cd backend
python -c "from config_evidence import EVIDENCE_RETENTION_HOURS; print(f'Retention: {EVIDENCE_RETENTION_HOURS} hours')"
```
Expected: `Retention: 48 hours`

### 2. Check Evidence Files
```bash
cd backend
python check_evidence.py
```

### 3. Test Evidence Saving
1. Start exam as student
2. Trigger violation (look away, multiple persons, etc.)
3. Check evidence folder:
```bash
cd backend
ls -lt uploads/evidence/ | head -5
```

### 4. Test Evidence Viewing
1. Login as examiner
2. View exam results
3. Click student → See violations
4. Click "📷 View Evidence"
5. Screenshot should open

### 5. Test Cleanup (Optional)
```bash
cd backend
python cleanup_evidence.py
```
Should show: "Files deleted: 0" (if all < 48 hours)

---

## 🐛 Troubleshooting

### Issue: Evidence Still Disappearing

**Check 1**: Is cleanup script scheduled?
```bash
# Windows
schtasks /query | findstr "cleanup"

# Linux
crontab -l | grep cleanup
```

**Fix**: Remove any scheduled tasks

**Check 2**: Are files being saved?
```bash
cd backend
python check_evidence.py
```

**Fix**: Ensure folder exists and is writable

**Check 3**: Check backend logs
```bash
cd backend
tail -f logs/app.log | grep evidence
```

### Issue: Can't View Evidence

**Check**: File exists on disk
```bash
cd backend
ls uploads/evidence/
```

**Check**: Database has evidence_path
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM violations WHERE evidence_path IS NOT NULL')
print(f'Violations with evidence: {cursor.fetchone()[0]}')
conn.close()
"
```

**Fix**: Restart backend and test again

---

## 📊 Monitoring

### Daily Check Script
Create `check_evidence_daily.bat`:
```batch
@echo off
cd C:\Projects\online-exam\backend
python check_evidence.py
pause
```

Run this daily to monitor evidence status.

### Weekly Cleanup
Create `cleanup_evidence_weekly.bat`:
```batch
@echo off
echo Running weekly evidence cleanup...
cd C:\Projects\online-exam\backend
python cleanup_evidence.py
pause
```

Run this weekly to clean old evidence.

---

## 🎯 Summary

### What Changed
- ✅ Evidence retention: 24 hours → **48 hours**
- ✅ Auto-cleanup: Enabled → **DISABLED**
- ✅ Configuration: Hardcoded → **Config file**
- ✅ Verification: None → **Check script**

### Files Created/Modified
- ✅ `backend/config_evidence.py` (NEW)
- ✅ `backend/cleanup_evidence.py` (UPDATED)
- ✅ `backend/check_evidence.py` (NEW)
- ✅ `EVIDENCE_RETENTION_48_HOURS.md` (NEW)
- ✅ `EVIDENCE_48_HOURS_COMPLETE.md` (THIS FILE)

### How It Works Now
1. Violation detected → Screenshot saved
2. Evidence stored in `backend/uploads/evidence/`
3. Evidence path saved in database
4. Evidence available for **48 hours**
5. Manual cleanup removes files > 48 hours
6. Examiner can view evidence anytime within 48 hours

---

## 🎉 You're All Set!

Evidence will now be kept for **48 hours (2 days)** after exam completion.

### Next Steps
1. ✅ Configuration is done
2. ✅ Scripts are ready
3. ✅ Verification tools available
4. ⏳ Test with a real exam
5. ⏳ Run cleanup after 48 hours

### Quick Commands
```bash
# Check evidence status
cd backend && python check_evidence.py

# Run cleanup (after 48 hours)
cd backend && python cleanup_evidence.py

# Check configuration
cd backend && python -c "from config_evidence import *; print(f'Retention: {EVIDENCE_RETENTION_HOURS}h')"
```

---

**Status**: ✅ COMPLETE
**Retention Period**: 48 hours (2 days)
**Auto-Cleanup**: DISABLED (manual only)
**Last Updated**: February 27, 2026
