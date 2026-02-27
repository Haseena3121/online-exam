# How to Create an Exam Using the UI

## Complete Step-by-Step Guide

### Prerequisites
1. Make sure both servers are running:
   - Backend: `cd backend && python run.py`
   - Frontend: `cd frontend && npm start`
2. Login as an examiner account

### Step 1: Access Create Exam Page

1. Login with examiner credentials:
   - Email: `examiner@test.com`
   - Password: `password123`

2. You'll be redirected to the Examiner Dashboard

3. Click the "Create New Exam" button (or navigate to `/create-exam`)

### Step 2: Fill Exam Details (Step 1 of 2)

You'll see a form with the following fields:

#### Required Fields:
- **Exam Title**: Give your exam a clear name
  - Example: "Mathematics Final Exam 2024"
  
- **Duration (minutes)**: How long students have to complete the exam
  - Example: 60 (for 1 hour)
  
- **Total Marks**: Maximum marks for the entire exam
  - Example: 100
  
- **Passing Marks**: Minimum marks needed to pass
  - Example: 40

#### Optional Fields:
- **Description**: Brief overview of the exam
  - Example: "Final examination covering all topics from Semester 1"
  
- **Instructions**: Specific instructions for students
  - Example: "Answer all questions. No calculators allowed."

#### Actions:
- Click "Cancel" to go back to dashboard
- Click "Next: Add Questions →" to proceed to Step 2

### Step 3: Add Questions (Step 2 of 2)

After creating the exam, you'll see:
- A summary showing questions added and total marks
- A form to add new questions
- A list of all added questions

#### Adding a Question:

1. **Question Text**: Enter your question
   - Example: "What is the capital of France?"

2. **Options A, B, C, D**: Enter four answer choices
   - Option A: "London"
   - Option B: "Berlin"
   - Option C: "Paris"
   - Option D: "Madrid"

3. **Correct Answer**: Select which option is correct
   - Select: "Option C"

4. **Marks**: Points awarded for this question
   - Example: 5

5. Click "➕ Add Question" button

The question will appear in the "Added Questions" list below.

#### Managing Questions:

- **View Questions**: All added questions are displayed with:
  - Question number (Q1, Q2, etc.)
  - Marks value
  - Question text
  - All options (correct answer highlighted in green)
  
- **Remove Question**: Click the "🗑️ Remove" button on any question

- **Add More**: Keep adding questions until you reach your total marks

#### Completing the Exam:

You have two options:

1. **Skip for Now**: 
   - Creates the exam without questions
   - You can add questions later using the Python script:
     ```bash
     cd backend
     python add_questions.py <exam_id>
     ```

2. **Create Exam with Questions**:
   - Click "✓ Create Exam with X Questions"
   - All questions will be saved
   - You'll be redirected to Examiner Dashboard

### Step 4: Publish the Exam

After creating the exam:

1. Go to Examiner Dashboard
2. Find your newly created exam
3. Click the "Publish" button
4. The exam status will change to "Published"
5. Students can now see and take the exam

## Example: Creating a Sample Exam

### Exam Details:
- Title: "Python Programming Quiz"
- Description: "Basic Python concepts"
- Instructions: "Answer all questions. Time limit: 30 minutes"
- Duration: 30 minutes
- Total Marks: 20
- Passing Marks: 10

### Sample Questions:

**Question 1:**
- Text: "What is the output of print(2 ** 3)?"
- A: "5"
- B: "8" ✓
- C: "6"
- D: "9"
- Marks: 5

**Question 2:**
- Text: "Which of these is a mutable data type?"
- A: "Tuple"
- B: "String"
- C: "List" ✓
- D: "Integer"
- Marks: 5

**Question 3:**
- Text: "What does len() function do?"
- A: "Returns length of object" ✓
- B: "Creates a new list"
- C: "Converts to string"
- D: "Removes duplicates"
- Marks: 5

**Question 4:**
- Text: "Which keyword is used to define a function?"
- A: "function"
- B: "def" ✓
- C: "func"
- D: "define"
- Marks: 5

Total: 4 questions, 20 marks

## Tips for Creating Good Exams

### Question Writing:
- ✅ Make questions clear and unambiguous
- ✅ Ensure all options are plausible
- ✅ Avoid trick questions
- ✅ Test understanding, not just memorization
- ✅ Distribute marks appropriately

### Exam Settings:
- ✅ Set realistic time limits (1-2 minutes per mark)
- ✅ Set passing marks at 40-50% for fair assessment
- ✅ Provide clear instructions
- ✅ Test the exam yourself before publishing

### After Creation:
- ✅ Review all questions for errors
- ✅ Check that total marks match your questions
- ✅ Publish only when ready
- ✅ Monitor students during the exam

## Troubleshooting

### "Failed to create exam" error:
- Check that you're logged in as an examiner
- Verify all required fields are filled
- Check browser console for specific errors

### Questions not saving:
- Ensure all question fields are filled
- Check that correct answer is selected
- Verify marks are positive numbers

### Can't see the exam:
- Make sure you clicked "Publish" in Examiner Dashboard
- Students only see published exams
- Refresh the page

### Total marks don't match:
- The system calculates total marks from questions
- If you set total marks to 100 but add questions worth 80, that's okay
- Students will be graded based on actual question marks

## Features of the New UI

### Visual Progress:
- Two-step process with clear indicators
- See which step you're on
- Can't skip steps

### Real-time Summary:
- See how many questions you've added
- Track total marks vs target marks
- Know when you have enough questions

### Question Preview:
- See all questions before submitting
- Correct answers highlighted in green
- Easy to spot mistakes

### Flexible Workflow:
- Add questions one by one
- Remove questions if needed
- Skip questions and add later
- No pressure to complete in one session

## Next Steps After Creating Exam

1. **Publish the Exam**: Make it visible to students
2. **Share with Students**: They can find it in "Available Exams"
3. **Monitor Progress**: Watch students take the exam in real-time
4. **Review Violations**: Check proctoring alerts
5. **Grade Results**: View student performance

## Need Help?

- Check `QUICK_FIX_GUIDE.md` for technical issues
- See `TESTING_GUIDE.md` for complete testing workflow
- Run `python check_db.py` to verify exam was created
- Check backend logs for error messages

---

**Congratulations!** You now know how to create exams using the UI. The two-step process makes it easy to create professional exams with multiple-choice questions.
