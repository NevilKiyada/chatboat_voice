# Setup Instructions

## 🎯 Quick Setup

### 1. Create Python Virtual Environment
```bash
# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

### 3. Configure Your API Key
Create an environment file and add your Gemini API key:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_gemini_api_key_here
```

**Get your API key**: https://aistudio.google.com/

### 4. Create Required Directories
```bash
# Create necessary directories for the application
mkdir -p audio_files static/audio logs instance
```

### 5. Install System Dependencies (if needed)

#### For Linux:
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

#### For macOS:
```bash
brew install portaudio
```

#### For Windows:
If you encounter issues with PyAudio:
```powershell
pip install pipwin
pipwin install pyaudio
```

### 6. Start the Application
```bash
python app.py
```

### 7. Open in Browser
Navigate to: http://localhost:5000

## 🎤 Using the Voice Chatbot

1. **Text Chat**: Type your message and press Enter
2. **Voice Chat**: Click the microphone button and speak
3. **Settings**: Configure voice preferences in the interface

## 🔧 Configuration Options

Edit `.env` file for:
- **API Keys**: Gemini, Azure Speech, ElevenLabs
- **Database**: Switch from SQLite to PostgreSQL/MySQL
- **Voice Settings**: Change TTS/STT providers
- **Server Settings**: Host, port, debug mode

## 📱 Browser Support

**Recommended**: Chrome/Chromium for full voice features
**Supported**: Firefox, Edge, Safari (limited voice support)

## 🐛 Troubleshooting

### Common Issues:
1. **No microphone access**: Check browser permissions
2. **PyAudio errors**: Install system audio libraries
3. **API errors**: Verify API keys and internet connection
4. **Import errors**: Ensure all packages are installed

### Debug Mode:
Set `DEBUG=True` in `.env` for detailed error messages

## 🎉 You're Ready!

Your voice chatbot is now set up and ready to use. Enjoy chatting with AI using both text and voice!
