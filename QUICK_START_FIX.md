# ⚡ Quick Start - Fix Violation Evidence (2 Minutes)

## 🎯 What This Fixes
- ✅ Examiners can now see violation proofs (screenshots)
- ✅ Student marks display correctly
- ✅ Auto-submit works at trust score < 50%
- ✅ Students see violation warnings

---

## 🚀 Run This Now

### Windows Users
```bash
# Just run this:
setup_violation_evidence.bat
```

### Mac/Linux Users
```bash
# Run these 3 commands:
cd backend
python update_database_schema.py
mkdir -p uploads/evidence
```

---

## ✅ Then Restart

### Terminal 1 (Backend)
```bash
cd backend
python app.py
```

### Terminal 2 (Frontend)
```bash
cd frontend
npm start
```

---

## 🧪 Test It

1. **Login as Examiner** → http://localhost:3000
2. **Go to any exam** → Click "📊 View Results"
3. **Click on a student** → See violations section
4. **Look for** → "📷 View Evidence" links
5. **Click evidence link** → Screenshot opens!

---

## ✅ Success Indicators

You'll see:
- ✅ Marks: 18/20 (90%)
- ✅ Trust Score: 85%
- ✅ Violations with severity badges (🟡🟠🔴)
- ✅ "📷 View Evidence" links
- ✅ Timestamps for each violation

---

## 🐛 If Something's Wrong

### Error: "Column not found"
```bash
cd backend
python update_database_schema.py
python app.py
```

### Error: Evidence link 404
```bash
cd backend
mkdir -p uploads/evidence
python app.py
```

### Error: No violations showing
- Check browser console (F12)
- Check backend logs
- Restart both servers

---

## 📚 More Info

- **COMPLETE_FIX_SUMMARY.md** - What was fixed
- **SETUP_VIOLATION_EVIDENCE.md** - Detailed setup
- **VIOLATION_EVIDENCE_GUIDE.md** - How to use
- **EXAMINER_FEATURES_COMPLETE.md** - All features

---

## 💡 Quick Tips

1. **Evidence is stored for 24 hours** - Review promptly
2. **Severity colors matter**:
   - 🟡 Yellow = Low (5% reduction)
   - 🟠 Orange = Medium (10% reduction)
   - 🔴 Red = High (20% reduction)
3. **Auto-submit happens at < 50% trust** - Shows orange badge
4. **Students see warnings** - They know when trust score drops

---

**That's it! You're done. 🎉**

Total time: ~2 minutes
