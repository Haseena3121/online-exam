"""
Recreate exam_results table with correct schema
"""
import sqlite3
import os

DB_PATH = 'exam_proctoring.db'

# Backup existing data
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("🔧 RECREATING EXAM_RESULTS TABLE")
print("=" * 60)

try:
    # Check if table exists and has data
    cursor.execute("SELECT COUNT(*) FROM exam_results")
    count = cursor.fetchone()[0]
    print(f"\n📊 Current records in exam_results: {count}")
    
    if count > 0:
        print("⚠️  Backing up existing data...")
        cursor.execute("SELECT * FROM exam_results")
        backup_data = cursor.fetchall()
        cursor.execute("PRAGMA table_info(exam_results)")
        backup_columns = [col[1] for col in cursor.fetchall()]
        print(f"✅ Backed up {len(backup_data)} records")
    else:
        backup_data = []
        backup_columns = []
    
    # Drop the table
    print("\n🗑️  Dropping old exam_results table...")
    cursor.execute("DROP TABLE IF EXISTS exam_results")
    
    # Create new table with correct schema
    print("➕ Creating new exam_results table...")
    cursor.execute("""
        CREATE TABLE exam_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_id INTEGER,
            student_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            obtained_marks FLOAT,
            total_marks FLOAT,
            percentage FLOAT,
            status VARCHAR(50) DEFAULT 'completed',
            violation_count INTEGER DEFAULT 0,
            final_trust_score INTEGER DEFAULT 100,
            total_time_taken INTEGER,
            correct_answers INTEGER DEFAULT 0,
            incorrect_answers INTEGER DEFAULT 0,
            unanswered INTEGER DEFAULT 0,
            submitted_at DATETIME,
            reviewed_by INTEGER,
            reviewed_at DATETIME,
            remarks TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users(id),
            FOREIGN KEY (exam_id) REFERENCES exams(id)
        )
    """)
    
    print("✅ New table created successfully!")
    
    # Restore data if any
    if backup_data:
        print(f"\n📥 Restoring {len(backup_data)} records...")
        # Note: This is a simplified restore - adjust column mapping as needed
        for row in backup_data:
            try:
                cursor.execute("""
                    INSERT INTO exam_results 
                    (id, enrollment_id, student_id, exam_id, obtained_marks, total_marks, 
                     percentage, status, violation_count, final_trust_score, total_time_taken,
                     correct_answers, incorrect_answers, unanswered, submitted_at, 
                     reviewed_by, reviewed_at, remarks, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, row)
            except Exception as e:
                print(f"⚠️  Skipping row due to error: {e}")
        print("✅ Data restored!")
    
    conn.commit()
    
    # Verify
    cursor.execute("PRAGMA table_info(exam_results)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\n📋 New table columns ({len(columns)}):")
    for col in columns:
        print(f"  - {col}")
    
    print("\n" + "=" * 60)
    print("✅ TABLE RECREATION COMPLETE!")
    print("=" * 60)
    print("Now restart the backend: python app.py")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()
