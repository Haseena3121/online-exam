# 🎓 How to Use the Exam System - Quick Guide

## 📋 For Examiners (Teachers)

### Step 1: Create an Exam
1. Login as examiner
2. Click "Create New Exam" button
3. Fill in:
   - Title (e.g., "Math Final Exam")
   - Description (e.g., "Final exam for Math 101")
   - Instructions (e.g., "Answer all questions carefully")
   - Duration (e.g., 60 minutes)
   - Total Marks (e.g., 100)
   - Passing Marks (e.g., 40)
4. Click "Create Exam"

### Step 2: Publish the Exam
1. Go to Examiner Dashboard
2. You'll see your exam with "⚠️ Not Published" status
3. Click the "Publish" button
4. The status will change to "✅ Published"
5. Now students can see and take this exam!

### Step 3: Unpublish (if needed)
- Click "Unpublish" button to hide the exam from students
- Useful when you want to edit or temporarily disable an exam

---

## 📝 For Students

### Step 1: View Available Exams
1. Login as student
2. Go to "Exam List" or "Available Exams"
3. You'll see all published exams

### Step 2: Take an Exam
1. Click "Take Exam" button on any exam
2. Accept terms and conditions
3. Allow camera and microphone permissions
4. Start the exam

### Step 3: During the Exam
- Your camera will monitor you
- AI will detect violations:
  - Looking away
  - Multiple people
  - Phone usage
  - Tab switching
  - Unusual sounds
- Answer all questions
- Submit when done

---

## 🎯 Quick Workflow

### Examiner Workflow:
```
Create Exam → Publish Exam → Students can see it
```

### Student Workflow:
```
View Exams → Take Exam → Camera Monitoring → Submit
```

---

## ⚠️ Important Notes

### For Examiners:
- ❌ Unpublished exams are NOT visible to students
- ✅ Published exams appear in student's exam list
- You can publish/unpublish anytime
- You can only publish your own exams

### For Students:
- You can only see PUBLISHED exams
- Camera must be enabled during exam
- Violations will reduce your trust score
- Tab switching is detected

---

## 🔧 Testing the System

### Test as Examiner:
1. Create an exam
2. Check it shows "Not Published"
3. Click "Publish"
4. Verify status changes to "Published"

### Test as Student:
1. Login as student
2. Go to Exam List
3. You should see the published exam
4. Click "Take Exam" to start

---

## 📱 URLs

- **Examiner Dashboard**: http://localhost:3000/examiner-dashboard
- **Create Exam**: http://localhost:3000/create-exam
- **Student Exam List**: http://localhost:3000/exam-list
- **Camera Test**: http://localhost:3000/camera-test

---

## ✅ Checklist

### Before Students Can Take Exam:
- [ ] Exam created
- [ ] Exam published (green checkmark)
- [ ] Student logged in
- [ ] Student can see exam in list

### Before Taking Exam:
- [ ] Camera working
- [ ] Microphone working
- [ ] Good lighting
- [ ] Quiet environment
- [ ] No distractions

---

**That's it! The system is ready to use!** 🎉
