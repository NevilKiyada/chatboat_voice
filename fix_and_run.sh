#!/bin/bash
# fix_and_run.sh - Fix database issues and run the application

# Exit on error
set -e

# Display banner
echo "===================================================="
echo "🚀 Voice Chatbot - Fix and Run Script"
echo "===================================================="

# Create needed directories
echo -n "Creating required directories... "
mkdir -p instance audio_files static/audio logs
chmod -R 755 instance audio_files static/audio logs
echo "✓ Done"

# Set environment variables
echo -n "Setting environment variables... "
export SDL_AUDIODRIVER=dummy  # Use dummy audio driver to avoid ALSA warnings
echo "✓ Done"

# Fix SQLite database
echo -n "Testing SQLite database connection... "
python3 - << EOF
import sqlite3
import os

# Create a test database connection
conn = sqlite3.connect('instance/chatbot.db')
cursor = conn.cursor()

# Create a test table
cursor.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)')
cursor.execute('INSERT INTO test (name) VALUES (?)', ('Test Entry',))
conn.commit()

# Query the test data
cursor.execute('SELECT * FROM test')
print('Database test successful!')

# Close the connection
conn.close()

# Set permissions
os.chmod('instance/chatbot.db', 0o666)
EOF

if [ $? -eq 0 ]; then
    echo "✓ Done"
else
    echo "✗ Failed"
    echo "Error creating database. Check permissions and try again."
    exit 1
fi

# Update .env file if it exists
if [ -f .env ]; then
    echo -n "Updating .env file... "
    # Add DATABASE_URL and SDL_AUDIODRIVER if not already present
    grep -q "DATABASE_URL" .env || echo "DATABASE_URL=sqlite:///instance/chatbot.db" >> .env
    grep -q "SDL_AUDIODRIVER" .env || echo "SDL_AUDIODRIVER=dummy" >> .env
    echo "✓ Done"
fi

echo "===================================================="
echo "✅ All fixes applied successfully!"
echo ""
echo "Running the application..."
echo "===================================================="

# Run the application
SDL_AUDIODRIVER=dummy python app.py

# Exit
exit 0
