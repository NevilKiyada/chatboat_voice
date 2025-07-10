"""
Database Connectivity Test Script
Test SQLite database creation and basic operations
"""

import os
import sys
import sqlite3
from pathlib import Path

def ensure_instance_directory():
    """Create the instance directory if it doesn't exist"""
    instance_dir = Path("instance")
    if not instance_dir.exists():
        print(f"Creating instance directory: {instance_dir}")
        instance_dir.mkdir(parents=True, exist_ok=True)
        
    print(f"Instance directory path: {instance_dir.absolute()}")
    print(f"Instance directory exists: {instance_dir.exists()}")
    print(f"Instance directory is writable: {os.access(instance_dir, os.W_OK)}")

def test_sqlite_connection():
    """Test SQLite connection and basic operations"""
    db_path = Path("instance/test_db.db")
    db_uri = f"sqlite:///{db_path}"
    
    print(f"Testing SQLite connection to: {db_path.absolute()}")
    
    try:
        # Create a connection
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create a test table
        cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)")
        
        # Insert some test data
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("Test entry",))
        conn.commit()
        
        # Query the data
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        print(f"Rows in test table: {rows}")
        
        # Clean up
        cursor.execute("DROP TABLE test_table")
        conn.commit()
        conn.close()
        
        print("SQLite test SUCCESSFUL! Database operations completed.")
        return True
    except sqlite3.Error as e:
        print(f"SQLite ERROR: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== Database Connectivity Test ===")
    ensure_instance_directory()
    success = test_sqlite_connection()
    sys.exit(0 if success else 1)
