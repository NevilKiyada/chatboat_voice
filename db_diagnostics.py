"""
Database Diagnostics Script
Check SQLite database access and file permissions
"""

import os
import sys
from pathlib import Path
import sqlite3

def check_path_permissions(path):
    """Check if the path exists and has write permissions"""
    p = Path(path)
    
    # Check if the directory exists
    if not p.parent.exists():
        print(f"ISSUE: Parent directory {p.parent} does not exist")
        return False
        
    # Check if the directory is writable
    if not os.access(p.parent, os.W_OK):
        print(f"ISSUE: Parent directory {p.parent} is not writable")
        return False
        
    print(f"SUCCESS: Path {p.parent} exists and is writable")
    return True

def check_sqlite_connection(db_path):
    """Try to connect to SQLite database"""
    try:
        # Remove sqlite:/// prefix if present
        if db_path.startswith('sqlite:///'):
            db_path = db_path[10:]
            
        # Make path absolute if it's relative
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(db_path)
            
        print(f"Trying to connect to SQLite database at: {db_path}")
        
        # Check directory permissions
        check_path_permissions(db_path)
        
        # Try to connect
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()
        conn.close()
        
        print(f"SUCCESS: Connected to SQLite version: {version[0]}")
        return True
    except sqlite3.Error as e:
        print(f"ERROR: SQLite connection failed: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR: Unknown error: {str(e)}")
        return False

def create_instance_directory():
    """Create the instance directory if it doesn't exist"""
    instance_dir = "instance"
    try:
        if not os.path.exists(instance_dir):
            print(f"Creating instance directory: {instance_dir}")
            os.makedirs(instance_dir)
            print(f"SUCCESS: Created instance directory")
        else:
            print(f"Instance directory already exists: {instance_dir}")
            
        # Check permissions
        if not os.access(instance_dir, os.W_OK):
            print(f"WARNING: Instance directory is not writable")
    except Exception as e:
        print(f"ERROR: Failed to create instance directory: {str(e)}")

def run_diagnostics():
    """Run database diagnostics"""
    print("=== Database Diagnostics ===")
    
    # Check environment variable
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        print(f"DATABASE_URL from environment: {db_url}")
    else:
        print("DATABASE_URL not set in environment")
        db_url = "sqlite:///instance/chatbot.db"
        print(f"Using default: {db_url}")
    
    # Check instance directory
    create_instance_directory()
    
    # Check database connection
    if 'sqlite' in db_url:
        check_sqlite_connection(db_url)
        
    # Try to create an empty database file
    test_db_path = "instance/test.db"
    try:
        conn = sqlite3.connect(test_db_path)
        conn.close()
        print(f"SUCCESS: Created test database at {test_db_path}")
        
        # Clean up
        os.remove(test_db_path)
        print(f"Removed test database")
    except Exception as e:
        print(f"ERROR: Failed to create test database: {str(e)}")
        
    print("=== Diagnostics Complete ===")

if __name__ == "__main__":
    run_diagnostics()
