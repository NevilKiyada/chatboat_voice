#!/usr/bin/env python3
"""
SQLite Database Fix Script
Fixes issues with database access in the Voice Chatbot project
"""

import os
import sys
import sqlite3
from pathlib import Path
import shutil

def create_fresh_instance():
    """Create a fresh instance directory with proper permissions"""
    print("Creating a fresh instance directory...")
    
    # Path to instance directory
    instance_path = Path("instance")
    
    # Remove old directory if it exists
    if instance_path.exists():
        print("Removing old instance directory...")
        try:
            shutil.rmtree(instance_path)
            print("Old instance directory removed.")
        except Exception as e:
            print(f"Warning: Could not remove old instance directory: {e}")
    
    # Create fresh directory
    try:
        print("Creating new instance directory...")
        instance_path.mkdir(mode=0o777, parents=True, exist_ok=True)
        print(f"Fresh instance directory created at: {instance_path.absolute()}")
    except Exception as e:
        print(f"Error creating instance directory: {e}")
        return False
    
    return True

def create_test_database():
    """Create a test database to verify connection"""
    print("Testing database connection...")
    
    db_path = Path("instance/chatbot.db")
    
    try:
        # Try to create and connect to database
        conn = sqlite3.connect(str(db_path))
        
        # Create a simple test table
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO test (name) VALUES (?)", ("Test Entry",))
        conn.commit()
        
        # Verify the data was written
        cursor.execute("SELECT * FROM test")
        data = cursor.fetchall()
        print(f"Test data written and retrieved: {data}")
        
        # Close the connection
        conn.close()
        
        # Set generous permissions on the db file
        try:
            os.chmod(str(db_path), 0o666)
            print(f"Database permissions set to 666")
        except Exception as e:
            print(f"Warning: Could not set database permissions: {e}")
        
        print(f"✅ Database test successful! Created file: {db_path.absolute()}")
        return True
    except sqlite3.Error as e:
        print(f"❌ SQLite Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def setup_env_file():
    """Set up the environment file with proper database path"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ Error: .env file not found. Please create a .env file.")
        return False
    
    try:
        # Read the current .env file
        with open(env_path, "r") as f:
            env_content = f.readlines()
        
        # Check and update database URL
        has_db_url = False
        new_content = []
        
        for line in env_content:
            if line.startswith("DATABASE_URL="):
                has_db_url = True
                new_content.append("DATABASE_URL=sqlite:///instance/chatbot.db\n")
            else:
                new_content.append(line)
        
        # Add DATABASE_URL if not present
        if not has_db_url:
            new_content.append("DATABASE_URL=sqlite:///instance/chatbot.db\n")
            new_content.append("SDL_AUDIODRIVER=dummy\n")  # Also add audio driver fix
        
        # Write back the updated content
        with open(env_path, "w") as f:
            f.writelines(new_content)
        
        print("✅ .env file updated with correct database path")
        return True
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def main():
    """Main function to fix database issues"""
    print("=== Voice Chatbot Database Fix ===")
    
    # Create fresh instance directory
    if not create_fresh_instance():
        print("❌ Failed to create fresh instance directory.")
        return 1
    
    # Create test database
    if not create_test_database():
        print("❌ Failed to create test database.")
        return 1
    
    # Update environment file
    if not setup_env_file():
        print("❌ Failed to update environment file.")
        return 1
    
    print("\n=== All fixes applied successfully! ===")
    print("Try running the application now with:")
    print("SDL_AUDIODRIVER=dummy python app.py")
    return 0

if __name__ == "__main__":
    sys.exit(main())
