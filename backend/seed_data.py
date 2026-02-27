"""
Seed database with test data
"""
from app import create_app
from database import db
from models import User, Exam, ExamQuestion
from datetime import datetime, timedelta

def seed_database():
    """Seed database with test data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("🌱 Seeding database...")
        
        # Create test users
        student1 = User(
            name='John Doe',
            email='student1@example.com',
            role='student'
        )
        student1.set_password('Student@123')
        
        student2 = User(
            name='Jane Smith',
            email='student2@example.com',
            role='student'
        )
        student2.set_password('Student@123')
        
        examiner = User(
            name='Prof. Adams',
            email='examiner@example.com',
            role='examiner'
        )
        examiner.set_password('Examiner@123')
        
        db.session.add_all([student1, student2, examiner])
        db.session.commit()
        
        print("✅ Users created")
        
        # Create test exam
        exam = Exam(
            title='Python Programming Test',
            description='Basic Python programming concepts',
            instructions='Answer all questions. Exam duration: 30 minutes',
            examiner_id=examiner.id,
            duration=30,
            total_marks=100,
            passing_marks=40,
            negative_marking=0.25,
            is_published=True
        )
        
        db.session.add(exam)
        db.session.commit()
        
        print("✅ Exam created")
        
        # Create test questions
        questions = [
            {
                'question_text': 'What is the output of print(2 ** 3)?',
                'option_a': '5',
                'option_b': '8',
                'option_c': '6',
                'option_d': '9',
                'correct_answer': 'b',
                'marks': 1
            },
            {
                'question_text': 'Which of these is a mutable data type?',
                'option_a': 'Tuple',
                'option_b': 'String',
                'option_c': 'List',
                'option_d': 'Integer',
                'correct_answer': 'c',
                'marks': 1
            },
            {
                'question_text': 'What does len() function do?',
                'option_a': 'Returns length of object',
                'option_b': 'Creates a new list',
                'option_c': 'Converts to string',
                'option_d': 'Removes duplicates',
                'correct_answer': 'a',
                'marks': 1
            }
        ]
        
        for q in questions:
            question = ExamQuestion(
                exam_id=exam.id,
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_answer=q['correct_answer'],
                marks=q['marks'],
                question_type='mcq'
            )
            db.session.add(question)
        
        db.session.commit()
        
        print("✅ Questions created")
        print("✅ Database seeded successfully!")
        print("\n📋 Test Credentials:")
        print(f"Student: student1@example.com / Student@123")
        print(f"Student: student2@example.com / Student@123")
        print(f"Examiner: examiner@example.com / Examiner@123")

if __name__ == '__main__':
    seed_database()