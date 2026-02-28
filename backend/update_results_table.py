#!/usr/bin/env python3
"""Add missing columns to exam_results table"""
import sqlite3
import os

db_path = os.path.join('instance', 'exam_proctoring.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("🔧 UPDATING EXAM_RESULTS TABLE")
print("=" * 60)

# Get current columns
cursor.execute("PRAGMA table_info(exam_results)")
columns = [row[1] for row in cursor.fetchall()]
print(f"\nCurrent columns: {', '.join(columns)}")

# Add missing columns
columns_to_add = [
    ('violation_count', 'INTEGER DEFAULT 0'),
    ('final_trust_score', 'INTEGER DEFAULT 100'),
    ('status', 'VARCHAR(50) DEFAULT "completed"'),
    ('submitted_at', 'DATETIME')
]

for col_name, col_type in columns_to_add:
    if col_name not in columns:
        print(f"\n📝 Adding {col_name}...")
        try:
            cursor.execute(f"ALTER TABLE exam_results ADD COLUMN {col_name} {col_type}")
            conn.commit()
            print(f"✅ Added {col_name}")
        except Exception as e:
            print(f"❌ Error adding {col_name}: {str(e)}")
    else:
        print(f"✅ {col_name} already exists")

# Verify
cursor.execute("PRAGMA table_info(exam_results)")
print("\n📋 Updated table structure:")
for row in cursor.fetchall():
    print(f"   {row[1]} ({row[2]})")

conn.close()

print("\n" + "=" * 60)
print("✅ Done!")
print("=" * 60)
