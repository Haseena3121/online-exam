"""
Fix SQLite database - Add missing columns to exam_results table
"""
import sqlite3
import os

def fix_database():
    # Find the SQLite database file
    db_path = 'exam_proctoring.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    print("=" * 60)
    print("FIXING SQLITE DATABASE")
    print("=" * 60)
    print(f"\nDatabase: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(exam_results)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    print(f"\nExisting columns ({len(existing_columns)}):")
    for col in existing_columns:
        print(f"  - {col}")
    
    # Define columns to add
    columns_to_add = [
        ('enrollment_id', 'INTEGER'),
        ('violation_count', 'INTEGER DEFAULT 0'),
        ('total_time_taken', 'INTEGER'),
        ('correct_answers', 'INTEGER DEFAULT 0'),
        ('incorrect_answers', 'INTEGER DEFAULT 0'),
        ('unanswered', 'INTEGER DEFAULT 0'),
        ('reviewed_at', 'DATETIME'),
        ('remarks', 'TEXT'),
    ]
    
    print(f"\nAdding missing columns...")
    added = 0
    
    for col_name, col_type in columns_to_add:
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
    
    # Verify
    cursor.execute("PRAGMA table_info(exam_results)")
    final_columns = [row[1] for row in cursor.fetchall()]
    
    conn.close()
    
    print(f"\n" + "=" * 60)
    print(f"MIGRATION COMPLETE")
    print(f"=" * 60)
    print(f"Added: {added} columns")
    print(f"Total columns: {len(final_columns)}")
    
    print(f"\nFinal columns:")
    for col in final_columns:
        print(f"  - {col}")
    
    print(f"\n✅ Database fixed successfully!")

if __name__ == '__main__':
    fix_database()
