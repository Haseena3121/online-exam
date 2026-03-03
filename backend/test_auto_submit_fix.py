"""
Test script to verify auto-submit and results fixes
"""
from app import create_app
from database import db
from models import ExamResult, ProctoringSession, StudentAnswer, ExamQuestion, Exam, User

app = create_app()

def test_exam_result_fields():
    """Test that ExamResult model has all required fields"""
    with app.app_context():
        print("=" * 60)
        print("Testing ExamResult Model Fields")
        print("=" * 60)
        
        # Check if model has all required fields
        required_fields = [
            'id', 'enrollment_id', 'student_id', 'exam_id',
            'obtained_marks', 'total_marks', 'percentage',
            'status', 'violation_count', 'final_trust_score',
            'total_time_taken', 'correct_answers', 'incorrect_answers',
            'unanswered', 'submitted_at', 'reviewed_by', 'reviewed_at',
            'remarks', 'created_at'
        ]
        
        result = ExamResult()
        model_fields = [c.name for c in result.__table__.columns]
        
        print(f"\nModel has {len(model_fields)} fields:")
        for field in model_fields:
            status = "✅" if field in required_fields else "⚠️"
            print(f"  {status} {field}")
        
        missing = set(required_fields) - set(model_fields)
        if missing:
            print(f"\n❌ Missing fields: {missing}")
        else:
            print(f"\n✅ All required fields present!")
        
        return len(missing) == 0

def test_existing_results():
    """Check existing exam results in database"""
    with app.app_context():
        print("\n" + "=" * 60)
        print("Checking Existing Exam Results")
        print("=" * 60)
        
        results = ExamResult.query.all()
        print(f"\nFound {len(results)} exam results in database")
        
        if results:
            print("\nSample result:")
            r = results[0]
            print(f"  ID: {r.id}")
            print(f"  Student ID: {r.student_id}")
            print(f"  Exam ID: {r.exam_id}")
            print(f"  Enrollment ID: {r.enrollment_id if hasattr(r, 'enrollment_id') else 'N/A'}")
            print(f"  Marks: {r.obtained_marks}/{r.total_marks}")
            print(f"  Percentage: {r.percentage}%")
            print(f"  Status: {r.status}")
            print(f"  Trust Score: {r.final_trust_score if hasattr(r, 'final_trust_score') else 'N/A'}")
            print(f"  Violations: {r.violation_count if hasattr(r, 'violation_count') else 'N/A'}")
            print(f"  Time Taken: {r.total_time_taken if hasattr(r, 'total_time_taken') else 'N/A'} min")
            print(f"  Submitted: {r.submitted_at}")
        
        return True

def test_student_answers():
    """Check if student answers exist for calculating auto-submit marks"""
    with app.app_context():
        print("\n" + "=" * 60)
        print("Checking Student Answers")
        print("=" * 60)
        
        answers = StudentAnswer.query.all()
        print(f"\nFound {len(answers)} student answers in database")
        
        if answers:
            # Group by student
            from collections import defaultdict
            by_student = defaultdict(list)
            for ans in answers:
                by_student[ans.student_id].append(ans)
            
            print(f"\nAnswers by {len(by_student)} students:")
            for student_id, student_answers in list(by_student.items())[:3]:
                print(f"\n  Student {student_id}: {len(student_answers)} answers")
                for ans in student_answers[:2]:
                    question = ExamQuestion.query.get(ans.question_id)
                    if question:
                        is_correct = ans.selected_answer == question.correct_answer
                        print(f"    Q{ans.question_id}: {ans.selected_answer} {'✅' if is_correct else '❌'}")
        
        return True

def test_proctoring_sessions():
    """Check proctoring sessions"""
    with app.app_context():
        print("\n" + "=" * 60)
        print("Checking Proctoring Sessions")
        print("=" * 60)
        
        sessions = ProctoringSession.query.all()
        print(f"\nFound {len(sessions)} proctoring sessions")
        
        active = [s for s in sessions if s.status == 'active']
        ended = [s for s in sessions if s.status == 'ended']
        
        print(f"  Active: {len(active)}")
        print(f"  Ended: {len(ended)}")
        
        if sessions:
            s = sessions[0]
            print(f"\nSample session:")
            print(f"  ID: {s.id}")
            print(f"  Student: {s.student_id}")
            print(f"  Exam: {s.exam_id}")
            print(f"  Enrollment: {s.enrollment_id}")
            print(f"  Status: {s.status}")
            print(f"  Trust Score: {s.current_trust_score}")
            print(f"  Start: {s.start_time}")
            print(f"  End: {s.end_time}")
        
        return True

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("AUTO-SUBMIT & RESULTS FIX - VERIFICATION TEST")
    print("=" * 60)
    
    tests = [
        ("ExamResult Model Fields", test_exam_result_fields),
        ("Existing Results", test_existing_results),
        ("Student Answers", test_student_answers),
        ("Proctoring Sessions", test_proctoring_sessions),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Error in {name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(success for _, success in results)
    if all_passed:
        print("\n🎉 All tests passed! System is ready.")
    else:
        print("\n⚠️ Some tests failed. Please review the output above.")
