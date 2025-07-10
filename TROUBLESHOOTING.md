# Troubleshooting Guide

## Common Issues and Solutions

### Missing Dependencies

#### ModuleNotFoundError: No module named 'pygame'

If you see this error, pygame is missing from your installation:

```bash
pip install pygame==2.5.2
```

#### ModuleNotFoundError: No module named 'pyaudio'

PyAudio installation often requires system libraries:

**Linux Solution:**
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio==0.2.14
```

**macOS Solution:**
```bash
brew install portaudio
pip install pyaudio==0.2.14
```

**Windows Solution:**
```powershell
pip install pipwin
pipwin install pyaudio
```

#### Other Missing Modules

Make sure you installed all requirements:

```bash
pip install -r requirements.txt
```

### Environment Setup Issues

If you're missing dependencies after installation, try installing packages one by one:

```bash
pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install Flask-SQLAlchemy==3.0.5
pip install google-generativeai==0.3.2
pip install SpeechRecognition==3.10.0
pip install gtts==2.4.0
pip install PyAudio==0.2.14
pip install pydub==0.25.1
pip install pygame==2.5.2
pip install python-dotenv==1.0.0
```

### Runtime Issues

#### Microphone Not Working

1. Check browser permissions - allow microphone access
2. Try a different browser (Chrome works best)
3. Ensure your microphone is properly connected
4. Try running with `FLASK_ENV=development` to see detailed errors

#### No Response from Gemini AI

1. Verify your API key in the `.env` file
2. Check your internet connection
3. Ensure you haven't exceeded your Gemini API quota
4. Check the logs in `logs/chatbot.log` for specific errors

#### Audio Playback Issues

1. Make sure your browser supports audio playback
2. Check if your speakers/headphones are properly connected
3. Try refreshing the page
4. Check the `static/audio` folder to see if files are being generated

#### Database Errors

1. Ensure the `instance` directory exists and is writable
2. Try deleting the database file `instance/chatbot.db` and restarting

### Port Conflicts

If you see errors about port 5000 being in use:

1. Change the port in your `.env` file: `PORT=5001`
2. Kill any processes using port 5000:
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill the process
   kill -9 <PID>
   ```

## Getting Help

If you encounter issues not covered here:

1. Check the logs in `logs/chatbot.log`
2. Run with debug mode enabled in `.env`: `DEBUG=True`
3. Create an issue on GitHub with:
   - Error messages
   - Steps to reproduce
   - Your operating system and Python version
   - Screenshots if applicable
