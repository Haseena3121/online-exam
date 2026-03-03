"""
Fix exam_results table - Add ALL missing columns
Run this ONCE to fix the database
"""
import sqlite3
import os

def fix_table():
    db_path = 'exam_proctoring.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        print("Creating new database...")
        # Database will be created when we connect
    
    print("\n" + "=" * 60)
    print("FIXING EXAM_RESULTS TABLE")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='exam_results'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("\n❌ exam_results table doesn't exist!")
        print("Creating table with all columns...")
        
        # Create the table with ALL columns
        cursor.execute('''
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
                submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                reviewed_by INTEGER,
                reviewed_at DATETIME,
                remarks TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("✅ Table created successfully!")
    else:
        print("\n✅ exam_results table exists")
        
        # Get existing columns
        cursor.execute("PRAGMA table_info(exam_results)")
        existing_columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        print(f"\nExisting columns ({len(existing_columns)}):")
        for col, col_type in existing_columns.items():
            print(f"  - {col} ({col_type})")
        
        # Define ALL columns that should exist
        required_columns = {
            'enrollment_id': 'INTEGER',
            'violation_count': 'INTEGER DEFAULT 0',
            'total_time_taken': 'INTEGER',
            'correct_answers': 'INTEGER DEFAULT 0',
            'incorrect_answers': 'INTEGER DEFAULT 0',
            'unanswered': 'INTEGER DEFAULT 0',
            'reviewed_at': 'DATETIME',
            'remarks': 'TEXT'
        }
        
        print(f"\nAdding missing columns...")
        added = 0
        
        for col_name, col_type in required_columns.items():
            if col_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE exam_results ADD COLUMN {col_name} {col_type}"
                    cursor.execute(sql)
                    print(f"  ✅ Added: {col_name}")
                    added += 1
                except Exception as e:
                    print(f"  ❌ Error adding {col_name}: {str(e)}")
            else:
                print(f"  ⏭️  Skipped: {col_name} (already exists)")
        
        conn.commit()
        print(f"\n✅ Added {added} columns")
    
    # Verify final structure
    cursor.execute("PRAGMA table_info(exam_results)")
    final_columns = cursor.fetchall()
    
    print(f"\n" + "=" * 60)
    print(f"FINAL TABLE STRUCTURE ({len(final_columns)} columns)")
    print("=" * 60)
    for col in final_columns:
        print(f"  {col[1]} ({col[2]})")
    
    conn.close()
    
    print(f"\n✅ Database fixed successfully!")
    print(f"\nNow restart the backend server:")
    print(f"  1. Stop backend (CTRL+C)")
    print(f"  2. Run: python app.py")
    print(f"  3. Refresh browser")

if __name__ == '__main__':
    fix_table()
