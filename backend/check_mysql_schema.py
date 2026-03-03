#!/usr/bin/env python3
"""Check MySQL violations table schema"""

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def check_schema():
    try:
        # Connect to MySQL
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='online_exam_proctoring'
        )
        cursor = conn.cursor()
        
        # Check if violations table exists
        cursor.execute("SHOW TABLES LIKE 'violations'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ Violations table does NOT exist!")
            print("\n📋 Available tables:")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            for table in tables:
                print(f"   - {table[0]}")
            conn.close()
            return
        
        print("✅ Violations table exists")
        
        # Get violations table schema
        cursor.execute("DESCRIBE violations")
        columns = cursor.fetchall()
        
        print(f"\n📋 Violations table columns ({len(columns)} total):")
        for col in columns:
            print(f"   {col[0]} ({col[1]})")
        
        # Check for required columns
        column_names = [col[0] for col in columns]
        
        required_columns = ['severity', 'evidence_path', 'trust_score_reduction']
        missing = [col for col in required_columns if col not in column_names]
        
        if missing:
            print(f"\n❌ Missing columns: {', '.join(missing)}")
        else:
            print("\n✅ All required columns exist")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_schema()
