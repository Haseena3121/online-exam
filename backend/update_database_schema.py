#!/usr/bin/env python3
"""
Update database schema to add missing columns for violation evidence
"""
import sqlite3
import os

db_path = os.path.join('instance', 'exam_proctoring.db')

if not os.path.exists(db_path):
    print(f"❌ Database not found at: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 70)
print("🔧 UPDATING DATABASE SCHEMA FOR VIOLATION EVIDENCE")
print("=" * 70)

# Check and add columns to violations table
print("\n📋 Updating violations table...")
cursor.execute("PRAGMA table_info(violations)")
columns = {col[1]: col[2] for col in cursor.fetchall()}

updates_made = []

if 'evidence_path' not in columns:
    cursor.execute("ALTER TABLE violations ADD COLUMN evidence_path VARCHAR(255)")
    updates_made.append("✅ Added evidence_path column")
    
if 'severity' not in columns:
    cursor.execute("ALTER TABLE violations ADD COLUMN severity VARCHAR(20) DEFAULT 'medium'")
    updates_made.append("✅ Added severity column")
    
if 'description' not in columns:
    cursor.execute("ALTER TABLE violations ADD COLUMN description TEXT")
    updates_made.append("✅ Added description column")

# Check and add columns to exam_results table
print("\n📋 Updating exam_results table...")
cursor.execute("PRAGMA table_info(exam_results)")
columns = {col[1]: col[2] for col in cursor.fetchall()}

if 'final_trust_score' not in columns:
    cursor.execute("ALTER TABLE exam_results ADD COLUMN final_trust_score INTEGER DEFAULT 100")
    updates_made.append("✅ Added final_trust_score column to exam_results")
    
if 'status' not in columns:
    cursor.execute("ALTER TABLE exam_results ADD COLUMN status VARCHAR(50) DEFAULT 'completed'")
    updates_made.append("✅ Added status column to exam_results")
    
if 'submitted_at' not in columns:
    cursor.execute("ALTER TABLE exam_results ADD COLUMN submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    updates_made.append("✅ Added submitted_at column to exam_results")

# Check and add columns to examiner_notifications table
print("\n📋 Updating examiner_notifications table...")
cursor.execute("PRAGMA table_info(examiner_notifications)")
columns = {col[1]: col[2] for col in cursor.fetchall()}

if 'student_id' not in columns:
    cursor.execute("ALTER TABLE examiner_notifications ADD COLUMN student_id INTEGER")
    updates_made.append("✅ Added student_id column to examiner_notifications")
    
if 'exam_id' not in columns:
    cursor.execute("ALTER TABLE examiner_notifications ADD COLUMN exam_id INTEGER")
    updates_made.append("✅ Added exam_id column to examiner_notifications")
    
if 'severity_level' not in columns:
    cursor.execute("ALTER TABLE examiner_notifications ADD COLUMN severity_level VARCHAR(20) DEFAULT 'medium'")
    updates_made.append("✅ Added severity_level column to examiner_notifications")

conn.commit()

print("\n📊 Updates Summary:")
if updates_made:
    for update in updates_made:
        print(f"   {update}")
else:
    print("   ✅ All columns already exist - no updates needed")

# Show final structure
print("\n📋 Final violations table structure:")
cursor.execute("PRAGMA table_info(violations)")
for col in cursor.fetchall():
    print(f"   {col[1]} ({col[2]})")

print("\n📋 Final exam_results table structure:")
cursor.execute("PRAGMA table_info(exam_results)")
for col in cursor.fetchall():
    print(f"   {col[1]} ({col[2]})")

conn.close()

print("\n" + "=" * 70)
print("✅ DATABASE SCHEMA UPDATED SUCCESSFULLY!")
print("=" * 70)
print("\nNext steps:")
print("1. Restart backend: python backend/app.py")
print("2. Test violation evidence capture")
print("3. Check examiner dashboard for violation proofs")
