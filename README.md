# 🎤🤖 AI Voice Chatbot

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![AI](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

**A modern voice-enabled AI chatbot with speech recognition and natural language processing**

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

## ✨ Features

� **Voice Recognition** - Real-time speech-to-text conversion  
🤖 **AI Conversations** - Powered by Google Gemini AI  
� **Text-to-Speech** - Natural voice responses  
💾 **Chat History** - Persistent conversation storage  
🌐 **Modern Web UI** - Beautiful, responsive interface  
 **Mobile Friendly** - Works on all devices  
🔒 **Production Ready** - Security, monitoring, and more

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/NevilKiyada/chatboat_voice.git
cd chatboat_voice

# 2. Run the setup script
./setup.sh

# 3. Add your Gemini API key
# Edit the .env file and add your API key from https://aistudio.google.com/
# GEMINI_API_KEY=your_key_here

# 4. Start the application
./start.sh

# 5. Open in your browser
# http://localhost:5000
```

### Manual Setup (Alternative)

```bash
# 1. Clone repository
git clone https://github.com/NevilKiyada/chatboat_voice.git
cd chatboat_voice

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your Gemini API key

# 5. Run the application
python app.py
```

### Windows-Specific Setup

```powershell
# 1. Clone repository
git clone https://github.com/NevilKiyada/chatboat_voice.git
cd chatboat_voice

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with your Gemini API key
# GEMINI_API_KEY=your_key_here
# FLASK_ENV=development
# DEBUG=True

# 5. Run the application
python app.py
```

## 📋 Requirements

- **Python 3.11+**
- **Google Gemini API key** - Free from [Google AI Studio](https://aistudio.google.com/)
- **Microphone access** - For voice input features
- **Modern web browser** - Chrome, Firefox, Safari, Edge

## 🎬 How It Works

1. **🎤 Speak or Type** - Use voice input or text chat
2. **🧠 AI Processing** - Google Gemini understands your message  
3. **� Get Response** - Intelligent, contextual replies
4. **🔊 Listen** - Hear responses with text-to-speech
5. **💾 Continue** - Chat history is saved automatically

## 🏗️ Project Structure

```
chatboat_voice/
├── 🚀 Application
│   ├── app.py                  # Main Flask application
│   ├── setup.sh                # Easy setup script
│   ├── start.sh                # Start the application
│   └── requirements.txt        # All dependencies
├── 🧠 Source Code
│   └── src/
│       ├── api/                # AI integration with Gemini
│       ├── voice/              # Speech recognition & TTS
│       ├── database/           # Database management
│       ├── models/             # Data models
│       └── utils/              # Utilities and logging
├── 🗃️ Data
│   ├── instance/               # SQLite database
│   └── logs/                   # Application logs
├── 🌐 Web
│   ├── static/                 # Static assets
│   │   └── audio/              # Generated audio files
│   └── templates/              # HTML templates
│       ├── api/                # AI integration
│       ├── voice/              # Speech processing
│       ├── database/           # Data management
│       ├── models/             # Database models
│       └── utils/              # Utilities
├── 🌐 Frontend
│   ├── templates/              # HTML templates
│   └── static/                 # CSS, JS, assets
├── 🛠️ Management
│   ├── setup-docker.sh         # Easy deployment
│   ├── chatbot.sh              # Management script
│   └── validate_setup.py       # Health checker
└── 📖 Documentation
    ├── README_PRODUCTION.md     # Detailed docs
    ├── DOCKER_GUIDE.md         # Docker tutorial
    └── GITHUB_SETUP.md         # Publication guide
```

## 📖 Documentation

- **[📚 Production Guide](README_PRODUCTION.md)** - Comprehensive documentation
- **[🐳 Docker Learning](DOCKER_GUIDE.md)** - Docker concepts and commands  
- **[🐙 GitHub Setup](GITHUB_SETUP.md)** - Publishing and sharing guide
- **[🏥 API Documentation](docs/API.md)** - REST API reference

## 🛠️ Management Commands

```bash
# Quick management with the included script
./chatbot.sh start      # Start the chatbot
./chatbot.sh stop       # Stop the chatbot  
./chatbot.sh logs       # View logs
./chatbot.sh status     # Check health
./chatbot.sh update     # Update to latest
./chatbot.sh backup     # Backup data
```

## 🌐 Deployment Options

### 🏠 Local Development
```bash
python app.py  # Development server
```

### 🐳 Docker (Production)
```bash
./setup-docker.sh  # One-command deployment
```

### ☁️ Cloud Platforms
- **AWS ECS/Fargate** - Container service
- **Google Cloud Run** - Serverless containers
- **Azure Container Instances** - Managed containers
- **DigitalOcean App Platform** - Platform-as-a-Service
- **Heroku** - With Docker deployment

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/voice-chatbot.git
cd voice-chatbot

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Validate setup
python validate_setup.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - For powerful language processing
- **Flask Community** - For the excellent web framework
- **Docker** - For containerization made simple
- **Open Source Community** - For inspiration and tools

## 🆘 Support

- 📖 **Documentation**: Check [README_PRODUCTION.md](README_PRODUCTION.md)
- 🐛 **Bug Reports**: [Open an issue](https://github.com/YOUR-USERNAME/voice-chatbot/issues)
- 💬 **Questions**: [Start a discussion](https://github.com/YOUR-USERNAME/voice-chatbot/discussions)
- 📧 **Email**: your.email@example.com

## ⭐ Show Your Support

If this project helped you, please consider:
- ⭐ **Starring** the repository
- 🐛 **Reporting** issues you find  
- 💡 **Suggesting** new features
- 🤝 **Contributing** code improvements
- 📢 **Sharing** with others who might benefit

---

<div align="center">

**Made with ❤️ by [Your Name](https://github.com/YOUR-USERNAME)**

*Transforming conversations with AI and voice technology*

</div>
│   └── utils/
│       └── logger.py          # Logging utilities
├── templates/
│   └── index.html             # Web interface
├── static/
│   └── audio/                 # Generated audio files
├── audio_files/               # Temporary audio storage
└── logs/                      # Application logs
```

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd /path/to/chatboat_voice

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit the `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `GEMINI_MODEL` | Gemini model to use | `gemini-pro` |
| `DATABASE_URL` | Database connection URL | `sqlite:///./chatbot.db` |
| `FLASK_ENV` | Flask environment | `development` |
| `DEBUG` | Enable debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5000` |
| `LOG_LEVEL` | Logging level | `INFO` |

## API Endpoints

### Chat
- `POST /api/chat` - Send a text message
- `GET /api/sessions/{id}/history` - Get chat history

### Voice
- `POST /api/voice/record` - Upload and transcribe audio
- `POST /api/voice/speak` - Convert text to speech

### Utility
- `GET /api/health` - Health check endpoint

## Usage

### Text Chat
1. Open the web interface at `http://localhost:5000`
2. Type your message in the input field
3. Click "Send" or press Enter
4. The AI will respond with a text message

### Voice Chat
1. Click the microphone button (🎤)
2. Speak your message clearly
3. Click the stop button (⏹️) when finished
4. Your speech will be transcribed and sent to the AI
5. The AI response will appear as text

### Voice Features
- **Speech-to-Text**: Uses Google Speech Recognition
- **Text-to-Speech**: Uses Google Text-to-Speech (gTTS)
- **Real-time Recording**: Live audio capture from microphone
- **Audio Processing**: Automatic format conversion and optimization

## Database Schema

### ChatSession
- `id`: Unique session identifier
- `user_id`: User identifier (default: 'anonymous')
- `created_at`: Session creation timestamp
- `last_activity`: Last activity timestamp
- `is_active`: Session status

### Message
- `id`: Message identifier
- `session_id`: Associated session
- `sender`: Message sender ('user' or 'bot')
- `content`: Message content
- `timestamp`: Message timestamp
- `message_type`: Type of message ('text' or 'voice')

## Development

### Adding New Features

1. **New API Endpoints**: Add routes in `app.py`
2. **Voice Processing**: Extend `src/voice/speech_processor.py`
3. **AI Integration**: Modify `src/api/gemini_client.py`
4. **Database Operations**: Update `src/database/db_manager.py`

### Testing

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Logging

Logs are written to:
- Console (colored output)
- File: `logs/chatbot.log` (with rotation)

Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check browser permissions
   - Ensure microphone is connected
   - Try refreshing the page

2. **Gemini API errors**
   - Verify API key is correct
   - Check internet connection
   - Ensure API quota is not exceeded

3. **Audio playback issues**
   - Check browser audio settings
   - Ensure speakers/headphones are connected

4. **Installation issues**
   - For PyAudio: `sudo apt-get install portaudio19-dev python3-pyaudio`
   - For system dependencies: Check requirements for your OS

### Browser Compatibility

- Chrome/Chromium: Full support
- Firefox: Full support
- Safari: Partial support (some voice features may not work)
- Edge: Full support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for intelligent responses
- Google Speech APIs for voice processing
- Flask framework for web application
- All open-source contributors

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs in `logs/chatbot.log`
3. Create an issue on GitHub

---

Made with ❤️ and AI
