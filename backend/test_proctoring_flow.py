"""
Test if proctoring sessions are being created and violations are being recorded
"""
from database import db
from models import ProctoringSession, ViolationLog, ExamResult
from app import create_app

app = create_app()

with app.app_context():
    print("=" * 60)
    print("🔍 PROCTORING FLOW CHECK")
    print("=" * 60)
    
    # Check active sessions
    sessions = ProctoringSession.query.filter_by(status='active').all()
    print(f"\n📊 Active Proctoring Sessions: {len(sessions)}")
    for session in sessions:
        print(f"  - Student {session.student_id}, Exam {session.exam_id}")
        print(f"    Trust Score: {session.current_trust_score}%")
        print(f"    Status: {session.status}")
        print(f"    Started: {session.start_time}")
    
    # Check recent violations
    violations = ViolationLog.query.order_by(ViolationLog.created_at.desc()).limit(10).all()
    print(f"\n⚠️  Recent Violations: {len(violations)}")
    for v in violations:
        print(f"  - Student {v.student_id}, Type: {v.violation_type}, Reduction: {v.trust_score_reduction}%")
    
    # Check exam results
    results = ExamResult.query.all()
    print(f"\n📝 Exam Results: {len(results)}")
    for r in results:
        print(f"  - Student {r.student_id}, Exam {r.exam_id}, Score: {r.obtained_marks}/{r.total_marks}, Status: {r.status}")
    
    print("\n" + "=" * 60)
    if len(sessions) == 0:
        print("⚠️  NO ACTIVE SESSIONS - Start an exam to create a session")
    elif len(violations) == 0:
        print("⚠️  NO VIOLATIONS RECORDED - Check if proctoring is detecting violations")
    else:
        print("✅ Proctoring system is working!")
    print("=" * 60)
