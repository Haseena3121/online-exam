#!/usr/bin/env python3
"""Check if exam_results table exists"""
import sqlite3
import os

db_path = os.path.join('instance', 'exam_proctoring.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("🔍 CHECKING EXAM_RESULTS TABLE")
print("=" * 60)

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='exam_results'")
exists = cursor.fetchone() is not None

if exists:
    print("\n✅ exam_results table exists!")
    cursor.execute("PRAGMA table_info(exam_results)")
    print("\n📋 Table structure:")
    for row in cursor.fetchall():
        print(f"   {row[1]} ({row[2]})")
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM exam_results")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total records: {count}")
else:
    print("\n❌ exam_results table does NOT exist!")
    print("   Creating table...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            obtained_marks INTEGER DEFAULT 0,
            total_marks INTEGER DEFAULT 0,
            percentage FLOAT DEFAULT 0.0,
            violation_count INTEGER DEFAULT 0,
            final_trust_score INTEGER DEFAULT 100,
            status VARCHAR(50) DEFAULT 'completed',
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users(id),
            FOREIGN KEY (exam_id) REFERENCES exams(id)
        )
    """)
    conn.commit()
    print("✅ Table created!")

conn.close()

print("\n" + "=" * 60)
