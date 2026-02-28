#!/usr/bin/env python3
"""Check proctoring sessions"""
import sqlite3
import os

db_path = os.path.join('instance', 'exam_proctoring.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("🎥 PROCTORING SESSIONS")
print("=" * 60)

# Get all sessions
cursor.execute("""
    SELECT id, student_id, exam_id, status, current_trust_score, 
           start_time, end_time, camera_active, mic_active
    FROM proctoring_sessions
    ORDER BY id DESC
    LIMIT 10
""")

sessions = cursor.fetchall()

if not sessions:
    print("\n❌ No sessions found!")
else:
    print(f"\n📊 Last 10 Sessions:")
    for s in sessions:
        print(f"\n   Session ID: {s[0]}")
        print(f"   Student ID: {s[1]}")
        print(f"   Exam ID: {s[2]}")
        print(f"   Status: {s[3]}")
        print(f"   Trust Score: {s[4]}%")
        print(f"   Start: {s[5]}")
        print(f"   End: {s[6]}")
        print(f"   Camera: {s[7]}, Mic: {s[8]}")

# Check active sessions
cursor.execute("""
    SELECT id, student_id, exam_id, current_trust_score
    FROM proctoring_sessions
    WHERE status = 'active'
""")

active = cursor.fetchall()

print(f"\n🟢 Active Sessions: {len(active)}")
if active:
    for a in active:
        print(f"   Session {a[0]}: Student {a[1]}, Exam {a[2]}, Trust: {a[3]}%")

# Check violations
cursor.execute("""
    SELECT COUNT(*) FROM violations
""")
violation_count = cursor.fetchone()[0]
print(f"\n⚠️ Total Violations Logged: {violation_count}")

if violation_count > 0:
    cursor.execute("""
        SELECT id, student_id, exam_id, violation_type, trust_score_reduction, created_at
        FROM violations
        ORDER BY id DESC
        LIMIT 5
    """)
    violations = cursor.fetchall()
    print(f"\n📋 Last 5 Violations:")
    for v in violations:
        print(f"   ID: {v[0]}, Student: {v[1]}, Exam: {v[2]}, Type: {v[3]}, Reduction: -{v[4]}%, Time: {v[5]}")

conn.close()

print("\n" + "=" * 60)
