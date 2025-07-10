#!/bin/bash
# run_with_fixes.sh - Run the Voice Chatbot with common fixes applied

# Exit on error
set -e

# Display help message
show_help() {
  echo "Usage: ./run_with_fixes.sh [options]"
  echo ""
  echo "Options:"
  echo "  --help, -h         Show this help message"
  echo "  --fix-only         Only run the fix script without starting the app"
  echo "  --debug            Run with debug mode enabled"
  echo "  --port PORT        Specify the port to run on (default: 5000)"
  echo "  --host HOST        Specify the host to bind to (default: 0.0.0.0)"
  echo ""
  echo "Examples:"
  echo "  ./run_with_fixes.sh                # Run with default settings"
  echo "  ./run_with_fixes.sh --port 8000    # Run on port 8000"
  echo "  ./run_with_fixes.sh --fix-only     # Only fix issues, don't run app"
}

# Default values
PORT=5000
HOST="0.0.0.0"
DEBUG=true
FIX_ONLY=false

# Process command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      show_help
      exit 0
      ;;
    --fix-only)
      FIX_ONLY=true
      shift
      ;;
    --debug)
      DEBUG=true
      shift
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --host)
      HOST="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Display banner
echo "===================================================="
echo "🚀 Voice Chatbot Launcher with Automatic Fixes"
echo "===================================================="

# Check Python and virtualenv
echo -n "Checking Python environment... "
if command -v python3 &>/dev/null; then
  echo "✓ Python found"
else
  echo "❌ Python not found. Please install Python 3.8 or higher."
  exit 1
fi

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "⚠️  Not running in a virtual environment."
  echo "    It's recommended to use a virtual environment."
  
  # Check if venv directory exists
  if [[ -d "venv" ]]; then
    echo -n "    Activating existing virtual environment... "
    source venv/bin/activate || { echo "❌ Failed"; exit 1; }
    echo "✓ Done"
  else
    echo "    No 'venv' directory found. Running with system Python."
  fi
else
  echo "✓ Running in virtual environment: $(basename "$VIRTUAL_ENV")"
fi

# Run fix script
echo -n "Running database and directory fixes... "
python fix_setup.py &>/dev/null || { echo "❌ Failed"; exit 1; }
echo "✓ Done"

# Exit if fix-only mode
if [[ "$FIX_ONLY" = true ]]; then
  echo "✓ Fixes completed. Exiting without starting app."
  exit 0
fi

# Start the app with proper environment variables
echo -n "Setting up environment variables... "
# Use dummy audio driver to avoid ALSA issues
export SDL_AUDIODRIVER=dummy
# Set Flask variables
export HOST=$HOST
export PORT=$PORT
export DEBUG=$DEBUG
echo "✓ Done"

# Start the application
echo "===================================================="
echo "🎤 Starting Voice Chatbot on http://$HOST:$PORT"
if [[ "$DEBUG" = true ]]; then
  echo "🐛 Debug mode is ON"
fi
echo "===================================================="
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python app.py

# Script end
exit 0
