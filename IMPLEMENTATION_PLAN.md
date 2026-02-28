# 📋 Implementation Plan - Complete Proctoring System

## Requirements Summary

1. ✅ **Violation Evidence (Screenshots/Videos)**
   - Capture screenshot when violation occurs
   - Store in backend for 24 hours
   - Display in examiner dashboard

2. ✅ **Fix Auto-Submit Error**
   - Fix error when trust score < 50%
   - Ensure smooth auto-submission

3. ✅ **Warning Messages for Students**
   - Show warning when trust score decreases
   - Display current trust score
   - Show violation type

4. ✅ **Results Page for Examiners**
   - View student marks
   - See violation history with evidence
   - View trust scores
   - Filter by exam/student

---

## Current Status

### What's Working ✅
- Violation detection (copy/paste, tab switch, blur, etc.)
- Trust score calculation
- Database storage of violations
- Live monitoring dashboard

### What Needs Implementation 🔨
1. Screenshot capture on violation
2. Evidence storage and retrieval
3. Auto-submit fix
4. Enhanced warning messages
5. Examiner results page

---

## Implementation Steps

### Phase 1: Evidence Capture & Storage

**Frontend Changes:**
- Modify `ProctorCamera.js` to capture screenshot on violation
- Convert canvas to blob
- Send screenshot with violation report

**Backend Changes:**
- Update violation endpoint to accept file upload
- Store screenshots in `uploads/evidence/`
- Add evidence_path to violations table
- Create cleanup job for 24-hour deletion

### Phase 2: Fix Auto-Submit

**Backend Changes:**
- Fix `auto_submit_exam` function
- Handle missing enrollment gracefully
- Create result even without enrollment

**Frontend Changes:**
- Better error handling
- Show proper message on auto-submit

### Phase 3: Enhanced Warnings

**Frontend Changes:**
- Improve `ViolationWarning` component
- Show trust score in warning
- Add sound alert (optional)
- Persistent warning for critical violations

### Phase 4: Examiner Results Page

**Backend Changes:**
- Create `/api/exams/<id>/results` endpoint
- Return student marks, violations, evidence
- Include trust scores

**Frontend Changes:**
- Create `ExamResults.js` page
- Display student list with marks
- Show violation details with screenshots
- Add filters and search

---

## File Structure

```
backend/
├── routes/
│   ├── proctoring.py (update violation endpoint)
│   └── exam.py (add results endpoint)
├── uploads/
│   └── evidence/ (screenshots stored here)
└── cleanup_evidence.py (new - 24hr cleanup)

frontend/
├── pages/
│   ├── ExamInterface.js (update warnings)
│   ├── ExamResults.js (new - examiner results)
│   └── LiveMonitoring.js (add evidence view)
├── components/
│   ├── ProctorCamera.js (add screenshot capture)
│   └── ViolationWarning.js (enhance)
└── styles/
    └── ExamResults.css (new)
```

---

## Database Schema Updates

### violations table (already exists)
```sql
- id
- student_id
- exam_id
- session_id
- violation_type
- trust_score_reduction
- evidence_path (NEW - path to screenshot)
- created_at
```

### exam_results table (check if exists)
```sql
- id
- student_id
- exam_id
- obtained_marks
- total_marks
- percentage
- violation_count
- final_trust_score
- status (completed/auto_submitted)
- submitted_at
```

---

## API Endpoints

### Existing (to update)
- `POST /api/proctoring/violation` - Add file upload support

### New
- `GET /api/exams/<id>/results` - Get all results for exam
- `GET /api/exams/<id>/results/<student_id>` - Get specific student result
- `GET /api/evidence/<filename>` - Serve evidence files
- `DELETE /api/evidence/cleanup` - Cleanup old evidence (cron job)

---

## Implementation Priority

### High Priority (Must Have)
1. ✅ Screenshot capture on violation
2. ✅ Evidence storage
3. ✅ Fix auto-submit error
4. ✅ Enhanced warning messages
5. ✅ Basic results page

### Medium Priority (Should Have)
1. Evidence cleanup (24 hours)
2. Results filtering
3. Evidence viewer in monitoring
4. Export results as PDF

### Low Priority (Nice to Have)
1. Video recording
2. Sound alerts
3. Email notifications with evidence
4. Analytics dashboard

---

## Testing Plan

### Test 1: Screenshot Capture
1. Start exam
2. Trigger violation (copy text)
3. Check backend logs for screenshot save
4. Verify file in `uploads/evidence/`

### Test 2: Evidence Display
1. Login as examiner
2. Go to results page
3. View student results
4. Click violation to see screenshot

### Test 3: Auto-Submit
1. Start exam
2. Trigger violations until trust < 50%
3. Verify auto-submit works
4. Check results are saved

### Test 4: Warnings
1. Start exam
2. Trigger violation
3. Verify warning shows trust score
4. Verify warning is visible

---

## Estimated Implementation Time

- Phase 1 (Evidence): 2-3 hours
- Phase 2 (Auto-submit fix): 30 minutes
- Phase 3 (Warnings): 1 hour
- Phase 4 (Results page): 2-3 hours

**Total: 6-8 hours of development**

---

## Next Steps

Would you like me to:

1. **Implement everything at once** (complete solution)
2. **Implement phase by phase** (step-by-step with testing)
3. **Focus on specific features first** (you choose priority)

Please confirm and I'll start implementation!

---

## Notes

- Screenshots will be JPEG format (smaller size)
- Evidence stored for 24 hours then auto-deleted
- Results page accessible only to examiners
- All evidence paths stored in database
- Cleanup can be manual or automated (cron job)

