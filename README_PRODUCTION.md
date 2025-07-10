# 🎤 Voice Chatbot - AI Assistant

<div align="center">

![Voice Chatbot](https://img.shields.io/badge/Voice-Chatbot-blue?style=for-the-badge&logo=microphone)
![AI Powered](https://img.shields.io/badge/AI-Powered-green?style=for-the-badge&logo=brain)
![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)

**A modern voice-enabled AI chatbot with speech recognition and natural language responses**

</div>

## 🚀 Quick Start (One Command!)

```bash
# 1. Clone this repository
git clone https://github.com/your-username/voice-chatbot-ai.git
cd voice-chatbot-ai

# 2. Run the setup script
./setup-docker.sh

# 3. Open http://localhost:5000 in your browser
# 4. Start talking to your AI assistant! 🎉
```

## ✨ Features

🎯 **Voice Recognition** - Real-time speech-to-text conversion  
🤖 **AI Responses** - Powered by Google Gemini AI  
🔊 **Text-to-Speech** - Natural voice responses  
💾 **Chat History** - Persistent conversation storage  
🌐 **Modern Web UI** - Beautiful, responsive interface  
🐳 **Docker Ready** - One-command deployment  
📱 **Mobile Friendly** - Works on phones and tablets  

## 🎬 How It Works

1. **Click the microphone** button in the web interface
2. **Speak your message** (or type it)
3. **AI processes** your input with Google Gemini
4. **Get intelligent responses** via text and voice
5. **Continue the conversation** naturally

## 📋 Requirements

### Option 1: Docker (Recommended)
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker)
- Google Gemini API key (free from [Google AI Studio](https://aistudio.google.com/))

### Option 2: Local Development
- Python 3.8+ installed
- System audio libraries (portaudio, ffmpeg)
- Google Gemini API key

## 🔑 Getting Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

## 🐳 Docker Setup (Recommended)

```bash
# Quick setup - everything automated!
./setup-docker.sh

# Manual setup if you prefer:
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
docker-compose up -d
```

### Management Commands

```bash
./chatbot.sh start    # Start the chatbot
./chatbot.sh stop     # Stop the chatbot  
./chatbot.sh logs     # View logs
./chatbot.sh status   # Check health
./chatbot.sh update   # Update and restart
```

## 🔧 Local Development Setup

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install portaudio19-dev ffmpeg python3-pip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the application
python app.py
```

## 📁 Project Structure

```
voice-chatbot-ai/
├── 🎯 app.py                    # Main Flask application
├── 🐳 docker-compose.yml       # Docker orchestration
├── 📋 requirements.txt         # Python dependencies
├── ⚙️ .env.example             # Environment template
├── 🧠 src/                     # Source code modules
│   ├── api/                    # AI integration
│   ├── voice/                  # Speech processing
│   ├── database/               # Data management
│   └── utils/                  # Utilities
├── 🎨 templates/               # Web interface
├── 📊 static/                  # Static assets
└── 📚 docs/                    # Documentation
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/chat` | POST | Send text message |
| `/api/voice/record` | POST | Upload voice recording |
| `/api/voice/speak` | POST | Generate speech audio |
| `/api/health` | GET | Health check |

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional customization
FLASK_ENV=production
PORT=5000
LOG_LEVEL=INFO
SESSION_TIMEOUT_HOURS=24
```

## 🐛 Troubleshooting

### Voice Not Working?
- ✅ Grant microphone permissions in browser
- ✅ Check if ffmpeg is installed
- ✅ Verify internet connection

### Docker Issues?
```bash
# Check Docker status
docker --version
docker-compose --version

# View logs
./chatbot.sh logs

# Restart services
./chatbot.sh restart
```

### API Key Problems?
- ✅ Verify key is in `.env` file
- ✅ Check API quota at [Google AI Studio](https://aistudio.google.com/)
- ✅ Ensure no extra spaces in key

## 🚀 Deployment Options

### Development
```bash
python app.py  # Local development server
```

### Production (Docker)
```bash
docker-compose up -d  # Production-ready deployment
```

### Cloud Deployment
Works on any platform supporting Docker:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean Apps
- Heroku

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: Check the `docs/` folder
- 🐛 **Issues**: Open a GitHub issue
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Email**: Contact the maintainers

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for the intelligent responses
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for voice processing
- [Docker](https://www.docker.com/) for containerization

---

<div align="center">

**Made with ❤️ and AI**

[⭐ Star this repo](https://github.com/your-username/voice-chatbot-ai) if you found it helpful!

</div>
