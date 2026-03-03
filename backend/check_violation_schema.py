#!/usr/bin/env python3
"""Check violations table schema"""

import sqlite3

def check_schema():
    try:
        conn = sqlite3.connect('proctoring.db')
        cursor = conn.cursor()
        
        # Check if violations table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='violations'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ Violations table does NOT exist!")
            print("\n📋 Available tables:")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for table in tables:
                print(f"   - {table[0]}")
            conn.close()
            return
        
        print("✅ Violations table exists")
        
        # Get violations table schema
        cursor.execute("PRAGMA table_info(violations)")
        columns = cursor.fetchall()
        
        print(f"📋 Violations table columns ({len(columns)} total):")
        if columns:
            for col in columns:
                print(f"   {col[1]} ({col[2]})")
        else:
            print("   ⚠️ No columns found!")
        
        # Check if severity column exists
        column_names = [col[1] for col in columns]
        if 'severity' not in column_names:
            print("\n❌ Missing 'severity' column!")
        else:
            print("\n✅ 'severity' column exists")
        
        if 'evidence_path' not in column_names:
            print("❌ Missing 'evidence_path' column!")
        else:
            print("✅ 'evidence_path' column exists")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_schema()
