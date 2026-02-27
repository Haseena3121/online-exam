# Exam Creation - Quick Reference Card

## 🎯 Two Ways to Create Exams

### Method 1: UI (Recommended) ⭐
```
1. Login as examiner
2. Click "Create New Exam"
3. Fill exam details → Next
4. Add questions → Create
5. Publish in dashboard
```

### Method 2: Script (For bulk questions)
```bash
1. Create exam via UI (skip questions)
2. cd backend
3. python add_questions.py <exam_id>
4. Publish in dashboard
```

## 📝 UI Creation Steps

### Step 1: Exam Details
| Field | Required | Example |
|-------|----------|---------|
| Title | ✅ Yes | "Math Final Exam" |
| Description | ❌ No | "Covers chapters 1-5" |
| Instructions | ❌ No | "Answer all questions" |
| Duration | ✅ Yes | 60 (minutes) |
| Total Marks | ✅ Yes | 100 |
| Passing Marks | ✅ Yes | 40 |

### Step 2: Add Questions
| Field | Required | Example |
|-------|----------|---------|
| Question Text | ✅ Yes | "What is 2+2?" |
| Option A | ✅ Yes | "3" |
| Option B | ✅ Yes | "4" |
| Option C | ✅ Yes | "5" |
| Option D | ✅ Yes | "6" |
| Correct Answer | ✅ Yes | "B" |
| Marks | ✅ Yes | 5 |

## 🔑 Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Examiner | examiner@test.com | password123 |
| Student | student@test.com | password123 |

## 🌐 URLs

| Page | URL |
|------|-----|
| Login | http://localhost:3000/login |
| Create Exam | http://localhost:3000/create-exam |
| Examiner Dashboard | http://localhost:3000/examiner-dashboard |
| Student Dashboard | http://localhost:3000/dashboard |

## 🛠️ Useful Commands

```bash
# Check database
cd backend
python check_db.py

# Add questions via script
python add_questions.py 1

# Restart backend
python run.py

# Restart frontend
cd frontend
npm start
```

## ✅ Checklist

Before publishing an exam:
- [ ] Title is clear and descriptive
- [ ] Duration is appropriate (1-2 min per mark)
- [ ] Passing marks are fair (40-50%)
- [ ] All questions have correct answers
- [ ] Total marks match your target
- [ ] Instructions are clear
- [ ] Tested the exam yourself

## 🚨 Common Issues

| Problem | Solution |
|---------|----------|
| Can't create exam | Login as examiner |
| Questions not saving | Fill all fields |
| Students can't see exam | Click "Publish" |
| CORS errors | Restart both servers |
| User is null | Clear localStorage, login again |

## 📊 Quick Stats

After creating an exam, you'll see:
- ✅ Number of questions added
- ✅ Total marks calculated
- ✅ Exam status (Draft/Published)
- ✅ Creation timestamp

## 🎓 Example: 5-Question Exam

```
Exam: "Python Basics"
Duration: 25 minutes
Total: 25 marks
Passing: 12 marks

Q1: What is Python? (5 marks)
Q2: Variables in Python? (5 marks)
Q3: Python functions? (5 marks)
Q4: Python loops? (5 marks)
Q5: Python data types? (5 marks)
```

## 💡 Pro Tips

1. **Start small**: Create a 3-5 question test first
2. **Test yourself**: Take the exam as a student
3. **Use clear language**: Avoid ambiguous questions
4. **Balance difficulty**: Mix easy and hard questions
5. **Check marks**: Ensure they add up correctly
6. **Preview before publish**: Review all questions
7. **Monitor live**: Watch students during exam

## 🔄 Workflow

```
Create → Add Questions → Preview → Publish → Monitor → Grade
```

## 📱 Mobile Support

The UI is responsive and works on:
- ✅ Desktop (recommended)
- ✅ Tablet
- ✅ Mobile (basic support)

## 🎨 UI Features

- Two-step progress indicator
- Real-time mark calculation
- Question preview with highlighting
- Add/remove questions easily
- Validation and error messages
- Modern gradient design

## 📞 Need Help?

Read these guides:
1. `HOW_TO_CREATE_EXAM_UI.md` - Detailed walkthrough
2. `UI_EXAM_CREATION_SUMMARY.md` - Feature overview
3. `QUICK_FIX_GUIDE.md` - Troubleshooting
4. `TESTING_GUIDE.md` - Complete testing

---

**Print this card and keep it handy!** 📋
