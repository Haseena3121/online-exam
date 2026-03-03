"""
Clean up old proctoring sessions
Run this to fix trust score issues
"""
from app import create_app
from database import db
from models import ProctoringSession

app = create_app()

with app.app_context():
    print("\n" + "=" * 60)
    print("CLEANING OLD PROCTORING SESSIONS")
    print("=" * 60)
    
    # Get all active sessions
    active_sessions = ProctoringSession.query.filter_by(status='active').all()
    
    print(f"\nFound {len(active_sessions)} active sessions")
    
    if active_sessions:
        print("\nActive sessions:")
        for session in active_sessions:
            print(f"  - Student {session.student_id}, Exam {session.exam_id}, Trust Score: {session.current_trust_score}%")
        
        response = input("\nClose all active sessions? (yes/no): ")
        
        if response.lower() == 'yes':
            for session in active_sessions:
                session.status = 'ended'
            
            db.session.commit()
            print(f"\n✅ Closed {len(active_sessions)} sessions")
        else:
            print("\n❌ Cancelled")
    else:
        print("\n✅ No active sessions to clean")
    
    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    print("\nNow students can start fresh exams with 100% trust score!")
