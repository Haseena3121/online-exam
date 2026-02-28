# ✅ Evidence Automatically Kept - No Commands Needed!

## 🎉 Simple Solution

**Evidence files are now kept automatically for 30 days!**

You don't need to run any commands - everything is automatic.

---

## 📋 How It Works

### When Violation Occurs
1. Student triggers violation (multiple persons, phone, etc.)
2. Screenshot is automatically captured
3. File is saved to `backend/uploads/evidence/`
4. Path is saved in database
5. **Evidence stays there for 30 days automatically**

### No Manual Work Required
- ❌ No commands to run
- ❌ No cleanup scripts
- ❌ No maintenance needed
- ✅ Evidence just stays there!

---

## 🎯 Evidence Timeline

```
Day 1:  Exam happens → Evidence saved ✅
Day 2:  Evidence available ✅
Day 3:  Evidence available ✅
...
Day 29: Evidence available ✅
Day 30: Evidence available ✅
Day 31: Evidence still there (until you manually delete)
```

**Evidence will NOT be deleted automatically!**

---

## 📊 View Evidence Anytime

### As Examiner
1. Login at http://localhost:3000
2. Go to "Examiner Dashboard"
3. Click "📊 View Results" on any exam
4. Click on a student
5. See violations with "📷 View Evidence" links
6. Click to view screenshots

**Evidence will be there whenever you need it!**

---

## ⚙️ Configuration

Current settings in `backend/config_evidence.py`:

```python
EVIDENCE_RETENTION_HOURS = 720  # 30 days
AUTO_CLEANUP_ENABLED = False    # No automatic deletion
```

### Want to Keep Evidence Longer?

Edit `backend/config_evidence.py`:

```python
# Keep for 60 days
EVIDENCE_RETENTION_HOURS = 1440

# Keep for 90 days
EVIDENCE_RETENTION_HOURS = 2160

# Keep for 1 year
EVIDENCE_RETENTION_HOURS = 8760
```

Then restart backend:
```bash
# Stop backend (Ctrl+C in backend terminal)
# Start again
cd backend
python app.py
```

---

## 💾 Storage Management

### Check How Much Space Evidence Uses

```bash
cd backend
python -c "
import os
total = sum(os.path.getsize(os.path.join('uploads/evidence', f)) for f in os.listdir('uploads/evidence') if os.path.isfile(os.path.join('uploads/evidence', f)))
print(f'Evidence storage: {total / 1024 / 1024:.2f} MB')
"
```

### If Storage Gets Full

Only if you need to free space (optional):

```bash
cd backend
python cleanup_evidence.py
```

This will delete files older than 30 days.

---

## 🔍 Verify Evidence is Being Saved

### Quick Check
```bash
cd backend
ls uploads/evidence/
```

You should see files like:
```
abc123_20240227_103015.jpg
xyz789_20240227_104532.jpg
```

### Detailed Check
```bash
cd backend
python check_evidence.py
```

Shows:
- How many evidence files exist
- How old they are
- Total storage used
- Database status

---

## ✅ Summary

### What You Need to Know
- ✅ Evidence is saved automatically
- ✅ Evidence stays for 30 days (or longer if you configure)
- ✅ No commands needed
- ✅ No manual cleanup required
- ✅ View evidence anytime in examiner dashboard

### What You DON'T Need to Do
- ❌ Run cleanup scripts
- ❌ Schedule tasks
- ❌ Worry about evidence disappearing
- ❌ Do any maintenance

### If You Want to Delete Old Evidence
Only if needed (optional):
```bash
cd backend
python cleanup_evidence.py
```

---

## 🎯 Quick Reference

**Evidence Location**: `backend/uploads/evidence/`
**Retention Period**: 30 days (configurable)
**Auto-Cleanup**: DISABLED
**Manual Cleanup**: Optional (only if you want)

**View Evidence**: 
1. Login as examiner
2. Exam Results → Student → Violations
3. Click "📷 View Evidence"

---

## 💡 Tips

1. **Evidence is safe** - It won't be deleted automatically
2. **Check storage occasionally** - Run `python check_evidence.py`
3. **Clean up when needed** - Run `python cleanup_evidence.py` if storage is full
4. **Configure retention** - Edit `config_evidence.py` to keep longer

---

**Status**: ✅ AUTOMATIC
**Retention**: 30 days
**Cleanup**: Manual only (optional)
**Commands Needed**: NONE

Everything is automatic! Evidence is saved and kept for 30 days without any commands. 🎉
