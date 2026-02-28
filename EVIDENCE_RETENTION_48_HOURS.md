# 📸 Evidence Retention - 48 Hours Configuration

## ✅ What's Been Fixed

Evidence files are now configured to be kept for **48 hours (2 days)** after exam completion.

---

## 🔧 Configuration Changes

### 1. Evidence Retention Period
- **Previous**: 24 hours
- **New**: 48 hours (2 days)
- **Location**: `backend/config_evidence.py`

### 2. Auto-Cleanup Disabled
- **Status**: DISABLED by default
- **Reason**: Prevents accidental deletion
- **Manual cleanup**: Run script when needed

---

## 📁 Files Modified

### 1. `backend/config_evidence.py` (NEW)
Central configuration for evidence retention:
```python
EVIDENCE_RETENTION_HOURS = 48  # Keep for 48 hours
AUTO_CLEANUP_ENABLED = False   # Manual cleanup only
```

### 2. `backend/cleanup_evidence.py` (UPDATED)
Now uses config file and keeps evidence for 48 hours:
```python
MAX_AGE_HOURS = 48  # From config
```

---

## 🎯 How It Works

### Evidence Lifecycle

```
Violation Detected
       ↓
Screenshot Captured
       ↓
Saved to: backend/uploads/evidence/
       ↓
Filename: {uuid}_{timestamp}.jpg
       ↓
Stored in Database: violations.evidence_path
       ↓
Available for 48 HOURS
       ↓
Manual Cleanup (when you run script)
       ↓
Deleted after 48 hours
```

### Timeline Example

```
Day 1, 10:00 AM - Exam starts
Day 1, 10:30 AM - Violation detected, screenshot saved
Day 1, 11:00 AM - Exam ends
Day 1, 11:30 AM - Examiner views evidence ✅
Day 2, 10:00 AM - Evidence still available ✅
Day 2, 11:00 PM - Evidence still available ✅
Day 3, 10:30 AM - Evidence still available ✅
Day 3, 10:31 AM - 48 hours passed
Day 3, 11:00 AM - Run cleanup script
Day 3, 11:01 AM - Evidence deleted ❌
```

---

## 🔍 Verify Evidence is Being Saved

### Check Evidence Folder
```bash
cd backend
ls -la uploads/evidence/
```

You should see files like:
```
abc123-def456_20240227_103015.jpg
xyz789-ghi012_20240227_103542.jpg
```

### Check Database
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT id, violation_type, evidence_path, created_at FROM violations WHERE evidence_path IS NOT NULL ORDER BY created_at DESC LIMIT 5')
for row in cursor.fetchall():
    print(f'ID: {row[0]}, Type: {row[1]}, Path: {row[2]}, Time: {row[3]}')
conn.close()
"
```

---

## 🧹 Manual Cleanup

### When to Run Cleanup
- After 48 hours have passed
- When storage space is low
- Before archiving old exams

### How to Run Cleanup
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
Deleted: abc123_20240225_080000.jpg (age: 2 days, 2:00:00, size: 245678 bytes)
Deleted: xyz789_20240225_090000.jpg (age: 2 days, 1:00:00, size: 189234 bytes)
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

## ⚙️ Configuration Options

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

### Enable Auto-Cleanup (Not Recommended)

Edit `backend/config_evidence.py`:

```python
AUTO_CLEANUP_ENABLED = True  # Enable automatic cleanup
AUTO_CLEANUP_INTERVAL_HOURS = 24  # Run every 24 hours
```

**Warning**: Auto-cleanup requires setting up a cron job or task scheduler.

---

## 📊 Storage Management

### Check Storage Usage
```bash
cd backend
python -c "
import os
total_size = 0
count = 0
for filename in os.listdir('uploads/evidence'):
    filepath = os.path.join('uploads/evidence', filename)
    if os.path.isfile(filepath):
        total_size += os.path.getsize(filepath)
        count += 1
print(f'Files: {count}')
print(f'Total size: {total_size / 1024 / 1024:.2f} MB')
"
```

### Set Storage Limits

Edit `backend/config_evidence.py`:

```python
MAX_EVIDENCE_SIZE_MB = 1000  # 1 GB total
MAX_FILE_SIZE_MB = 10  # 10 MB per file
```

---

## 🔐 Evidence Security

### File Permissions
Evidence files are only accessible to:
- ✅ Examiners (via authenticated API)
- ❌ Students (cannot access)
- ❌ Public (not exposed)

### Access Control
```python
@proctoring_bp.route('/evidence/<path:filename>', methods=['GET'])
@jwt_required()
def serve_evidence(filename):
    user = User.query.get(int(get_jwt_identity()))
    
    # Only examiners can view evidence
    if user.role != 'examiner':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Serve file...
```

---

## 📋 Best Practices

### 1. Regular Cleanup
Run cleanup script weekly:
```bash
# Windows Task Scheduler
schtasks /create /tn "Evidence Cleanup" /tr "python C:\Projects\online-exam\backend\cleanup_evidence.py" /sc weekly /d SUN /st 02:00

# Linux Cron
0 2 * * 0 cd /path/to/backend && python cleanup_evidence.py
```

### 2. Backup Before Cleanup
```bash
# Backup evidence folder
cd backend
tar -czf evidence_backup_$(date +%Y%m%d).tar.gz uploads/evidence/

# Or on Windows
Compress-Archive -Path uploads\evidence -DestinationPath evidence_backup_$(Get-Date -Format 'yyyyMMdd').zip
```

### 3. Monitor Storage
```bash
# Check storage weekly
cd backend
python -c "
import os
total = sum(os.path.getsize(os.path.join('uploads/evidence', f)) for f in os.listdir('uploads/evidence') if os.path.isfile(os.path.join('uploads/evidence', f)))
print(f'Evidence storage: {total / 1024 / 1024:.2f} MB')
if total > 1000 * 1024 * 1024:
    print('⚠️ WARNING: Storage exceeds 1 GB!')
"
```

### 4. Archive Important Evidence
Before cleanup, archive evidence for important exams:
```bash
# Archive specific exam evidence
cd backend
mkdir -p archives/exam_123
cp uploads/evidence/*exam_123* archives/exam_123/
```

---

## 🐛 Troubleshooting

### Issue: Evidence Disappearing Immediately

**Possible Causes**:
1. Cleanup script running automatically
2. Evidence not being saved properly
3. File permissions issue

**Solutions**:
```bash
# 1. Check if cleanup is scheduled
# Windows
schtasks /query | findstr "Evidence"

# Linux
crontab -l | grep cleanup

# 2. Check evidence folder
cd backend
ls -la uploads/evidence/

# 3. Check file permissions
chmod 755 uploads/evidence/
```

### Issue: Evidence Not Saving

**Check**:
1. Folder exists and is writable
2. Disk space available
3. Backend logs for errors

**Fix**:
```bash
cd backend
mkdir -p uploads/evidence
chmod 755 uploads/evidence
python -c "
import os
test_file = 'uploads/evidence/test.txt'
with open(test_file, 'w') as f:
    f.write('test')
print('✅ Can write to evidence folder')
os.remove(test_file)
"
```

### Issue: Can't View Evidence

**Check**:
1. Logged in as examiner
2. Evidence path in database
3. File exists on disk

**Fix**:
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('instance/exam_proctoring.db')
cursor = conn.cursor()
cursor.execute('SELECT evidence_path FROM violations WHERE evidence_path IS NOT NULL LIMIT 1')
path = cursor.fetchone()
if path:
    import os
    full_path = 'uploads/evidence/' + path[0].split('/')[-1]
    print(f'Checking: {full_path}')
    print('✅ File exists' if os.path.exists(full_path) else '❌ File missing')
conn.close()
"
```

---

## ✅ Verification Steps

### 1. Check Configuration
```bash
cd backend
python -c "from config_evidence import EVIDENCE_RETENTION_HOURS; print(f'Retention: {EVIDENCE_RETENTION_HOURS} hours ({EVIDENCE_RETENTION_HOURS/24} days)')"
```

Expected: `Retention: 48 hours (2.0 days)`

### 2. Test Evidence Saving
1. Start an exam as student
2. Trigger a violation
3. Check evidence folder:
```bash
cd backend
ls -lt uploads/evidence/ | head -5
```

### 3. Test Evidence Viewing
1. Login as examiner
2. View exam results
3. Click "📷 View Evidence"
4. Screenshot should open

### 4. Test Cleanup Script
```bash
cd backend
python cleanup_evidence.py
```

Should show: "Files deleted: 0" (if all files are < 48 hours old)

---

## 📈 Monitoring

### Daily Check
```bash
cd backend
python -c "
import os
from datetime import datetime, timedelta

evidence_dir = 'uploads/evidence'
now = datetime.now()
cutoff = now - timedelta(hours=48)

total = 0
old = 0
for f in os.listdir(evidence_dir):
    if f == '.gitkeep':
        continue
    filepath = os.path.join(evidence_dir, f)
    if os.path.isfile(filepath):
        total += 1
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        if mtime < cutoff:
            old += 1

print(f'Total files: {total}')
print(f'Files > 48 hours: {old}')
print(f'Files < 48 hours: {total - old}')
"
```

---

## 🎯 Summary

✅ Evidence retention: **48 hours (2 days)**
✅ Auto-cleanup: **DISABLED** (manual only)
✅ Configuration file: `backend/config_evidence.py`
✅ Cleanup script: `backend/cleanup_evidence.py`
✅ Evidence folder: `backend/uploads/evidence/`

**Evidence will NOT be deleted automatically!**
**You must run cleanup script manually after 48 hours.**

---

**Last Updated**: February 27, 2026
**Version**: 2.0
**Retention Period**: 48 hours
