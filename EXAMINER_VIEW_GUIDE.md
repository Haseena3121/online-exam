# 👁️ Examiner View Guide - What You'll See

## 📊 Complete Visual Walkthrough

This guide shows exactly what examiners will see when viewing violation evidence.

---

## 🏠 Step 1: Examiner Dashboard

After logging in, you'll see:

```
┌─────────────────────────────────────────────────────────┐
│  👨‍🏫 Examiner Dashboard                                  │
├─────────────────────────────────────────────────────────┤
│  [➕ Create New Exam]  [🎥 Live Monitoring]             │
├─────────────────────────────────────────────────────────┤
│  📚 My Exams (5)                                        │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Python Programming Exam                           │ │
│  │ ⏱️ 60 min | ⭐ 20 marks                           │ │
│  │ ✅ Published                                      │ │
│  │ [Unpublish] [📊 View Results]                    │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │ JavaScript Basics                                 │ │
│  │ ⏱️ 45 min | ⭐ 15 marks                           │ │
│  │ ⚠️ Not Published                                  │ │
│  │ [Publish] [📊 View Results]                      │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Click**: "📊 View Results" button

---

## 📈 Step 2: Exam Results Page

You'll see the complete results overview:

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back    📊 Exam Results: Python Programming Exam             │
│  Duration: 60 min | Total Marks: 20                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │    25    │  │    20    │  │     5    │  │  78.5%   │       │
│  │  Total   │  │  Passed  │  │  Failed  │  │ Average  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
├─────────────────────────────────────────────────────────────────┤
│  🔍 Search by name or email...                                  │
│  [All (25)] [Passed (20)] [Failed (5)]                         │
├──────────────────────────┬──────────────────────────────────────┤
│  📋 Student List         │  (Select a student to view details) │
│  ┌────────────────────┐  │                                      │
│  │ John Doe           │  │                                      │
│  │ john@test.com      │  │                                      │
│  │ Score: 18/20 (90%) │  │                                      │
│  │ Trust: 85%         │  │                                      │
│  │ Violations: 2      │  │                                      │
│  │ [PASSED ✅]        │  │                                      │
│  └────────────────────┘  │                                      │
│  ┌────────────────────┐  │                                      │
│  │ Jane Smith         │  │                                      │
│  │ jane@test.com      │  │                                      │
│  │ Score: 0/20 (0%)   │  │                                      │
│  │ Trust: 30%         │  │                                      │
│  │ Violations: 8      │  │                                      │
│  │ [AUTO-SUBMIT 🟠]   │  │                                      │
│  └────────────────────┘  │                                      │
│  ┌────────────────────┐  │                                      │
│  │ Bob Wilson         │  │                                      │
│  │ bob@test.com       │  │                                      │
│  │ Score: 19/20 (95%) │  │                                      │
│  │ Trust: 95%         │  │                                      │
│  │ Violations: 1      │  │                                      │
│  │ [PASSED ✅]        │  │                                      │
│  └────────────────────┘  │                                      │
└──────────────────────────┴──────────────────────────────────────┘
```

**Click**: Any student card to see details

---

## 👤 Step 3: Student Details Panel

When you click a student, the right panel shows:

```
┌─────────────────────────────────────────────────────────┐
│  👤 John Doe                                      [✕]   │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  📊 Performance                                         │
│  ┌─────────────────────┬─────────────────────┐         │
│  │ Marks Obtained: 18  │ Total Marks: 20     │         │
│  ├─────────────────────┼─────────────────────┤         │
│  │ Percentage: 90%     │ Trust Score: 85%    │         │
│  └─────────────────────┴─────────────────────┘         │
│                                                          │
│  ⚠️ Violations (2)                                      │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 🔴 MULTIPLE PERSONS DETECTED [HIGH]              │ │
│  │ Trust Score Reduction: -20%                      │ │
│  │ 📅 Feb 27, 2024 10:30:15 AM                      │ │
│  │ 📷 View Evidence                                 │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 🟡 BACKGROUND BLUR DISABLED [LOW]                │ │
│  │ Trust Score Reduction: -5%                       │ │
│  │ 📅 Feb 27, 2024 10:35:42 AM                      │ │
│  │ 📷 View Evidence                                 │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│  📅 Submission Details                                  │
│  • Submitted At: Feb 27, 2024 11:00:00 AM              │
│  • Status: Completed                                    │
│  • Total Time: 60 minutes                               │
└─────────────────────────────────────────────────────────┘
```

**Click**: "📷 View Evidence" to see screenshot

---

## 📸 Step 4: Violation Evidence

When you click "📷 View Evidence", a new window opens:

```
┌─────────────────────────────────────────────┐
│  Violation Evidence                    [✕]  │
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │                                       │ │
│  │     [Screenshot of student's camera]  │ │
│  │                                       │ │
│  │     Shows: Multiple faces detected   │ │
│  │     Timestamp: 2024-02-27 10:30:15   │ │
│  │                                       │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  Violation Type: Multiple Persons           │
│  Severity: HIGH                             │
│  Trust Score Impact: -20%                   │
│  Captured: Feb 27, 2024 10:30:15 AM        │
└─────────────────────────────────────────────┘
```

---

## 🎨 Color Coding Guide

### Status Badges
- 🟢 **PASSED** (Green): Student passed with good trust score
- 🔴 **FAILED** (Red): Student failed or low trust score
- 🟠 **AUTO-SUBMITTED** (Orange): Exam auto-submitted due to trust score < 50%

### Severity Badges
- 🟡 **LOW** (Yellow): Minor violations, -5% trust score
- 🟠 **MEDIUM** (Orange): Moderate violations, -10% trust score
- 🔴 **HIGH** (Red): Critical violations, -20% trust score

---

## 📊 Understanding the Data

### Performance Metrics
```
┌─────────────────────────────────────────┐
│ Marks Obtained: 18                      │  ← Actual marks scored
│ Total Marks: 20                         │  ← Maximum possible marks
│ Percentage: 90%                         │  ← (18/20) × 100
│ Trust Score: 85%                        │  ← Started at 100%, reduced by violations
└─────────────────────────────────────────┘
```

### Trust Score Calculation
```
Starting Trust Score: 100%
─────────────────────────────
Violation 1 (HIGH):    -20%  → Trust Score: 80%
Violation 2 (MEDIUM):  -10%  → Trust Score: 70%
Violation 3 (LOW):      -5%  → Trust Score: 65%
─────────────────────────────
Final Trust Score: 65%
```

### Auto-Submit Trigger
```
Trust Score Timeline:
100% ──────────────────────────────────────
 90% ──────────────────────────────────────
 80% ────────────────────────────────────── ⚠️ Warning
 70% ──────────────────────────────────────
 60% ────────────────────────────────────── ⚠️ Warning
 50% ────────────────────────────────────── 🚨 Critical
 40% ────────────────────────────────────── 🔴 AUTO-SUBMIT
```

---

## 🔍 Violation Types Explained

### 🔴 HIGH Severity (-20%)
1. **Multiple Persons Detected**
   - More than one face visible in camera
   - Evidence: Screenshot showing multiple faces
   
2. **Phone Detected**
   - Mobile device detected in frame
   - Evidence: Screenshot showing phone
   
3. **Tab Switching**
   - Student switched to another browser tab
   - Evidence: System log timestamp

### 🟠 MEDIUM Severity (-10%)
1. **Eye Gaze Away**
   - Student looking away from screen
   - Evidence: Screenshot showing gaze direction
   
2. **Head Movement**
   - Excessive head movement detected
   - Evidence: Screenshot showing position
   
3. **Sound Detected**
   - Unusual sounds detected via microphone
   - Evidence: Audio level log

### 🟡 LOW Severity (-5%)
1. **Background Blur Disabled**
   - Student disabled background blur
   - Evidence: Screenshot without blur
   
2. **Face Not Visible**
   - Brief moment face not detected
   - Evidence: Screenshot showing no face

---

## 📋 Example Scenarios

### Scenario 1: Good Student
```
Student: Alice Johnson
Score: 19/20 (95%)
Trust Score: 95%
Violations: 1 (LOW - Brief face not visible)
Status: PASSED ✅

Examiner Action: Accept result, excellent performance
```

### Scenario 2: Suspicious Activity
```
Student: Bob Smith
Score: 15/20 (75%)
Trust Score: 60%
Violations: 4 (2 HIGH, 1 MEDIUM, 1 LOW)
Status: PASSED ⚠️

Examiner Action: Review evidence, consider interview
```

### Scenario 3: Auto-Submitted
```
Student: Charlie Brown
Score: 0/20 (0%)
Trust Score: 35%
Violations: 7 (4 HIGH, 2 MEDIUM, 1 LOW)
Status: AUTO-SUBMITTED 🟠

Examiner Action: Review evidence, decide on retake
```

---

## 🎯 Examiner Decision Matrix

### Trust Score > 80%
- ✅ Accept result as-is
- ✅ No additional review needed
- ✅ Minor violations acceptable

### Trust Score 50-80%
- ⚠️ Review violation evidence
- ⚠️ Check severity of violations
- ⚠️ Consider context
- ⚠️ May require interview

### Trust Score < 50%
- 🔴 Exam auto-submitted
- 🔴 Mandatory evidence review
- 🔴 Decide: Retake or Fail
- 🔴 Document decision

---

## 📱 Mobile/Responsive View

On smaller screens, the layout adapts:

```
┌─────────────────────────────┐
│  📊 Exam Results            │
├─────────────────────────────┤
│  Statistics (stacked)       │
├─────────────────────────────┤
│  Search & Filter            │
├─────────────────────────────┤
│  Student List (full width)  │
│  ┌───────────────────────┐  │
│  │ John Doe              │  │
│  │ [View Details]        │  │
│  └───────────────────────┘  │
├─────────────────────────────┤
│  Selected Student Details   │
│  (appears below list)       │
└─────────────────────────────┘
```

---

## ✅ Quick Reference

### What You Can Do
- ✅ View all student results
- ✅ See marks and percentages
- ✅ Check trust scores
- ✅ Review violation history
- ✅ Access evidence screenshots
- ✅ Filter by pass/fail
- ✅ Search students
- ✅ Identify auto-submits
- ✅ Make informed decisions

### What Evidence Shows
- 📷 Screenshot from student's camera
- 📅 Exact timestamp of violation
- 🎯 Type of violation detected
- 📊 Trust score impact
- 🎨 Severity level

### When to Review Evidence
- ⚠️ Trust score < 80%
- ⚠️ Multiple HIGH violations
- ⚠️ Auto-submitted exams
- ⚠️ Student disputes result
- ⚠️ Unusual patterns

---

## 💡 Best Practices

1. **Review Promptly**
   - Evidence stored for 24 hours
   - Review within same day
   
2. **Check All Violations**
   - Don't just look at HIGH severity
   - Pattern matters more than single event
   
3. **Consider Context**
   - Technical issues happen
   - False positives possible
   - Use judgment
   
4. **Document Decisions**
   - Keep notes on why you accepted/rejected
   - Useful for appeals
   
5. **Be Fair**
   - Evidence supports, doesn't replace judgment
   - Give benefit of doubt when appropriate

---

## 🎓 Training Checklist

For new examiners:
- [ ] Understand severity levels
- [ ] Know how to access results
- [ ] Can view violation evidence
- [ ] Understand trust score calculation
- [ ] Know auto-submit criteria
- [ ] Can make fair decisions
- [ ] Know when to review evidence
- [ ] Understand appeal process

---

**This is what you'll see when viewing violation evidence!**

All features are working and ready to use. 🎉
