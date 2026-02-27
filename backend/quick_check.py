#!/usr/bin/env python3
"""Quick check of database status"""
import sqlite3
import os

db_path = os.path.join('instance', 'exam_proctoring.db')

if not os.path.exists(db_path):
    print(f"❌ Database not found at: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("📊 DATABASE STATUS CHECK")
print("=" * 60)

# Check exams
cursor.execute("SELECT id, title, is_published, duration, total_marks FROM exams")
exams = cursor.fetchall()
print(f"\n✅ Total Exams: {len(exams)}")
for exam in exams:
    print(f"   ID: {exam[0]}, Title: {exam[1]}, Published: {exam[2]}, Duration: {exam[3]}min, Marks: {exam[4]}")

# Check questions for each exam
print("\n📝 Questions per Exam:")
for exam in exams:
    cursor.execute("SELECT COUNT(*) FROM exam_questions WHERE exam_id = ?", (exam[0],))
    count = cursor.fetchone()[0]
    print(f"   Exam {exam[0]} ({exam[1]}): {count} questions")

# Check users
cursor.execute("SELECT id, email, role FROM users")
users = cursor.fetchall()
print(f"\n👥 Total Users: {len(users)}")
for user in users:
    print(f"   ID: {user[0]}, Email: {user[1]}, Role: {user[2]}")

# Check proctoring sessions
cursor.execute("SELECT COUNT(*) FROM proctoring_sessions")
session_count = cursor.fetchone()[0]
print(f"\n🎥 Total Proctoring Sessions: {session_count}")

# Check active sessions
cursor.execute("SELECT COUNT(*) FROM proctoring_sessions WHERE status = 'active'")
active_count = cursor.fetchone()[0]
print(f"   Active Sessions: {active_count}")

conn.close()

print("\n" + "=" * 60)
print("✅ Check Complete!")
print("=" * 60)
