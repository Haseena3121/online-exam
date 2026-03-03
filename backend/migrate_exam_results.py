"""
Migration script to add missing columns to exam_results table
"""
from app import create_app
from database import db
import sqlite3

app = create_app()

def migrate_exam_results():
    """Add missing columns to exam_results table"""
    with app.app_context():
        print("=" * 60)
        print("MIGRATING EXAM_RESULTS TABLE")
        print("=" * 60)
        
        # Get database path
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        print(f"\nDatabase: {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get existing columns
        cursor.execute("PRAGMA table_info(exam_results)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        print(f"\nExisting columns: {len(existing_columns)}")
        for col in existing_columns:
            print(f"  - {col}")
        
        # Define new columns to add
        new_columns = [
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
        skipped = 0
        
        for col_name, col_type in new_columns:
            if col_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE exam_results ADD COLUMN {col_name} {col_type}"
                    cursor.execute(sql)
                    print(f"  ✅ Added: {col_name} ({col_type})")
                    added += 1
                except Exception as e:
                    print(f"  ❌ Error adding {col_name}: {str(e)}")
            else:
                print(f"  ⏭️  Skipped: {col_name} (already exists)")
                skipped += 1
        
        conn.commit()
        conn.close()
        
        print(f"\n" + "=" * 60)
        print(f"MIGRATION COMPLETE")
        print(f"=" * 60)
        print(f"  Added: {added} columns")
        print(f"  Skipped: {skipped} columns")
        print(f"  Total: {len(existing_columns) + added} columns")
        
        # Verify
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(exam_results)")
        final_columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        
        print(f"\nFinal columns: {len(final_columns)}")
        for col in final_columns:
            print(f"  - {col}")
        
        print(f"\n✅ Migration successful!")

if __name__ == '__main__':
    migrate_exam_results()
