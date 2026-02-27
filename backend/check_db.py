"""
Check database status and display current data
"""
from app import create_app
from database import db
from models import User, Exam, ExamQuestion

def check_database():
    """Display current database status"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("📊 DATABASE STATUS")
        print("="*60)
        
        # Check users
        users = User.query.all()
        print(f"\n👥 USERS ({len(users)} total):")
        print("-" * 60)
        for user in users:
            print(f"  ID: {user.id} | Name: {user.name}")
            print(f"  Email: {user.email} | Role: {user.role}")
            print("-" * 60)
        
        # Check exams
        exams = Exam.query.all()
        print(f"\n📝 EXAMS ({len(exams)} total):")
        print("-" * 60)
        for exam in exams:
            examiner = User.query.get(exam.examiner_id)
            question_count = len(exam.questions)
            print(f"  ID: {exam.id} | Title: {exam.title}")
            print(f"  Examiner: {examiner.name if examiner else 'Unknown'}")
            print(f"  Duration: {exam.duration} min | Marks: {exam.total_marks}")
            print(f"  Published: {'✅ Yes' if exam.is_published else '❌ No'}")
            print(f"  Questions: {question_count}")
            print("-" * 60)
        
        # Check questions
        questions = ExamQuestion.query.all()
        print(f"\n❓ QUESTIONS ({len(questions)} total):")
        print("-" * 60)
        
        if questions:
            for q in questions:
                exam = Exam.query.get(q.exam_id)
                print(f"  Q{q.id} (Exam: {exam.title if exam else 'Unknown'})")
                print(f"  {q.question_text}")
                print(f"  Marks: {q.marks} | Type: {q.question_type}")
                print("-" * 60)
        else:
            print("  No questions found in database")
            print("-" * 60)
        
        print("\n" + "="*60)
        print("✅ DATABASE CHECK COMPLETE")
        print("="*60 + "\n")
        
        # Provide recommendations
        if len(users) == 0:
            print("⚠️  No users found. Run: python seed_data.py")
        
        if len(exams) == 0:
            print("⚠️  No exams found. Create one via the UI or run seed_data.py")
        
        if len(questions) == 0 and len(exams) > 0:
            print("⚠️  Exams exist but no questions found.")
            print(f"   Run: python add_questions.py <exam_id>")
            print(f"   Available exam IDs: {', '.join(str(e.id) for e in exams)}")

if __name__ == '__main__':
    check_database()
