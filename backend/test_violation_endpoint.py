#!/usr/bin/env python3
"""Test violation endpoint to diagnose 500 errors"""

import sys
import traceback
from app import app, db
from models import ViolationLog, ProctoringSession, ExamResult
from datetime import datetime

def test_violation_logic():
    """Test the violation reporting logic"""
    with app.app_context():
        try:
            # Find an active session
            session = ProctoringSession.query.filter_by(status='active').first()
            
            if not session:
                print("❌ No active session found")
                return
            
            print(f"✅ Found active session: ID={session.id}, Student={session.student_id}")
            print(f"   Current trust score: {session.current_trust_score}%")
            
            # Test creating a violation
            violation_type = "test_violation"
            severity = "high"
            trust_score_reduction = 20
            
            print(f"\n📝 Creating test violation...")
            print(f"   Type: {violation_type}")
            print(f"   Severity: {severity}")
            print(f"   Reduction: {trust_score_reduction}")
            
            violation = ViolationLog(
                student_id=session.student_id,
                exam_id=session.exam_id,
                session_id=session.id,
                violation_type=violation_type,
                trust_score_reduction=trust_score_reduction,
                created_at=datetime.utcnow()
            )
            
            # Update trust score
            old_score = session.current_trust_score
            session.current_trust_score -= trust_score_reduction
            if session.current_trust_score < 0:
                session.current_trust_score = 0
            
            print(f"   Trust score: {old_score}% → {session.current_trust_score}%")
            
            db.session.add(violation)
            db.session.commit()
            
            print(f"✅ Violation created successfully: ID={violation.id}")
            
            # Check if auto-submit should trigger
            if session.current_trust_score < 50:
                print(f"\n⚠️  Trust score below 50%! Checking auto-submit...")
                
                existing_result = ExamResult.query.filter_by(
                    student_id=session.student_id,
                    exam_id=session.exam_id
                ).first()
                
                if existing_result:
                    print(f"   ℹ️  Result already exists: ID={existing_result.id}")
                else:
                    print(f"   ⚠️  No result exists - auto-submit should trigger")
            
            # Rollback the test
            db.session.rollback()
            print(f"\n✅ Test completed successfully (rolled back)")
            
        except Exception as e:
            print(f"\n❌ Error during test:")
            print(f"   {str(e)}")
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    test_violation_logic()
