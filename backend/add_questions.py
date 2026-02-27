"""
Add sample questions to existing exams
"""
from app import create_app
from database import db
from models import Exam, ExamQuestion

def add_questions_to_exam(exam_id):
    """Add sample questions to an exam"""
    app = create_app()
    
    with app.app_context():
        exam = Exam.query.get(exam_id)
        
        if not exam:
            print(f"❌ Exam with ID {exam_id} not found")
            return
        
        print(f"📝 Adding questions to exam: {exam.title}")
        
        # Sample questions
        questions = [
            {
                'question_text': 'What is the capital of France?',
                'option_a': 'London',
                'option_b': 'Berlin',
                'option_c': 'Paris',
                'option_d': 'Madrid',
                'correct_answer': 'c',
                'marks': 5
            },
            {
                'question_text': 'Which programming language is known for web development?',
                'option_a': 'Python',
                'option_b': 'JavaScript',
                'option_c': 'C++',
                'option_d': 'Java',
                'correct_answer': 'b',
                'marks': 5
            },
            {
                'question_text': 'What does HTML stand for?',
                'option_a': 'Hyper Text Markup Language',
                'option_b': 'High Tech Modern Language',
                'option_c': 'Home Tool Markup Language',
                'option_d': 'Hyperlinks and Text Markup Language',
                'correct_answer': 'a',
                'marks': 5
            },
            {
                'question_text': 'Which of the following is a database management system?',
                'option_a': 'HTML',
                'option_b': 'CSS',
                'option_c': 'MySQL',
                'option_d': 'JavaScript',
                'correct_answer': 'c',
                'marks': 5
            },
            {
                'question_text': 'What is the result of 10 + 20 * 2?',
                'option_a': '60',
                'option_b': '50',
                'option_c': '40',
                'option_d': '30',
                'correct_answer': 'b',
                'marks': 5
            }
        ]
        
        for idx, q in enumerate(questions, 1):
            question = ExamQuestion(
                exam_id=exam.id,
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_answer=q['correct_answer'],
                marks=q['marks'],
                question_type='mcq',
                order=idx
            )
            db.session.add(question)
        
        db.session.commit()
        
        print(f"✅ Added {len(questions)} questions to exam")
        print(f"📊 Total marks: {sum(q['marks'] for q in questions)}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python add_questions.py <exam_id>")
        print("Example: python add_questions.py 1")
    else:
        exam_id = int(sys.argv[1])
        add_questions_to_exam(exam_id)
