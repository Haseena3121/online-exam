"""
Check backend status and database state
"""
from database import db
from models import ExamResult, ProctoringSession, ViolationLog
from app import create_app

app = create_app()

with app.app_context():
    print("=" * 60)
    print("🔍 BACKEND DATABASE STATUS CHECK")
    print("=" * 60)
    
    # Check proctoring sessions
    active_sessions = ProctoringSession.query.filter_by(status='active').all()
    print(f"\n📊 Active Sessions: {len(active_sessions)}")
    for session in active_sessions:
        print(f"  - Student {session.student_id}, Exam {session.exam_id}, Trust: {session.current_trust_score}%")
    
    # Check exam results
    results = ExamResult.query.all()
    print(f"\n📝 Total Exam Results: {len(results)}")
    for result in results[-5:]:  # Show last 5
        print(f"  - Student {result.student_id}, Exam {result.exam_id}, Score: {result.obtained_marks}/{result.total_marks}, Status: {result.status}")
    
    # Check violations
    violations = ViolationLog.query.all()
    print(f"\n⚠️  Total Violations: {len(violations)}")
    
    print("\n" + "=" * 60)
    print("If you see active sessions with trust score < 50%,")
    print("run: python clean_old_sessions.py")
    print("=" * 60)
