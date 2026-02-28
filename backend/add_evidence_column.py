#!/usr/bin/env python3
"""Add evidence_path column to violations table"""
import sqlite3
import os

db_path = os.path.join('instance', 'exam_proctoring.db')

if not os.path.exists(db_path):
    print(f"❌ Database not found at: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("🔧 ADDING EVIDENCE_PATH COLUMN")
print("=" * 60)

# Check if column already exists
cursor.execute("PRAGMA table_info(violations)")
columns = [row[1] for row in cursor.fetchall()]

if 'evidence_path' in columns:
    print("\n✅ evidence_path column already exists!")
else:
    print("\n📝 Adding evidence_path column...")
    try:
        cursor.execute("""
            ALTER TABLE violations 
            ADD COLUMN evidence_path VARCHAR(255)
        """)
        conn.commit()
        print("✅ Column added successfully!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        conn.rollback()

# Verify
cursor.execute("PRAGMA table_info(violations)")
print("\n📋 Current violations table structure:")
for row in cursor.fetchall():
    print(f"   {row[1]} ({row[2]})")

conn.close()

print("\n" + "=" * 60)
print("✅ Done!")
print("=" * 60)
