#!/usr/bin/env python3
"""Fix violations table"""
import sqlite3
import os

db_path = os.path.join('instance', 'exam_proctoring.db')

if not os.path.exists(db_path):
    print(f"❌ Database not found at: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("🔧 FIXING VIOLATIONS TABLE")
print("=" * 60)

# Check if violations table exists
cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='violations'
""")

if cursor.fetchone():
    print("\n✅ violations table already exists")
else:
    print("\n❌ violations table missing - creating...")
    
    # Create violations table
    cursor.execute("""
        CREATE TABLE violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            session_id INTEGER,
            violation_type VARCHAR(50) NOT NULL,
            severity VARCHAR(20),
            description TEXT,
            evidence_path VARCHAR(255),
            trust_score_reduction INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users(id),
            FOREIGN KEY (exam_id) REFERENCES exams(id),
            FOREIGN KEY (session_id) REFERENCES proctoring_sessions(id)
        )
    """)
    
    conn.commit()
    print("✅ violations table created!")

# Check structure
cursor.execute("PRAGMA table_info(violations)")
columns = cursor.fetchall()

print(f"\n📋 violations table structure:")
for col in columns:
    print(f"   {col[1]} ({col[2]})")

# Count existing violations
cursor.execute("SELECT COUNT(*) FROM violations")
count = cursor.fetchone()[0]
print(f"\n📊 Existing violations: {count}")

conn.close()

print("\n" + "=" * 60)
print("✅ Done! Backend is ready to log violations.")
print("=" * 60)
print("\nNext steps:")
print("1. Restart backend: python run.py")
print("2. Start a NEW exam")
print("3. Test violations")
