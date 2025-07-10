#!/bin/bash
# Voice Chatbot - Docker Setup Script
# This script makes it easy for anyone to run your chatbot

set -e  # Exit if any command fails

# Colors for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Voice Chatbot - Docker Setup${NC}"
echo "================================="
echo ""

# Function to print colored messages
print_step() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
print_step "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed!"
    echo ""
    echo "Please install Docker first:"
    echo "- Visit: https://docs.docker.com/get-docker/"
    echo "- Or run: curl -fsSL https://get.docker.com | sh"
    echo ""
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not available!"
    echo ""
    echo "Please install Docker Compose:"
    echo "- It's usually included with Docker Desktop"
    echo "- Or install separately: https://docs.docker.com/compose/install/"
    echo ""
    exit 1
fi

print_success "Docker and Docker Compose are installed!"

# Check if Docker daemon is running
print_step "Checking if Docker is running..."
if ! docker info &> /dev/null; then
    print_error "Docker daemon is not running!"
    echo ""
    echo "Please start Docker:"
    echo "- On Linux: sudo systemctl start docker"
    echo "- On Mac/Windows: Start Docker Desktop application"
    echo ""
    exit 1
fi

print_success "Docker is running!"

# Check if .env file exists
print_step "Setting up environment configuration..."
if [ ! -f .env ]; then
    print_warning "No .env file found. Creating from template..."
    cp .env.example .env
    echo ""
    print_warning "IMPORTANT: You need to edit .env file!"
    echo ""
    echo "1. Open .env file in your text editor"
    echo "2. Replace 'your_gemini_api_key_here' with your actual API key"
    echo "3. Get your free API key from: https://aistudio.google.com/"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

# Validate GEMINI_API_KEY
print_step "Validating configuration..."
if ! grep -q "GEMINI_API_KEY=.*[^[:space:]]" .env || grep -q "your_gemini_api_key_here" .env; then
    print_error "GEMINI_API_KEY is not properly set in .env file!"
    echo ""
    echo "Please edit .env file and add your real API key:"
    echo "GEMINI_API_KEY=your_actual_api_key_here"
    echo ""
    echo "Get your API key from: https://aistudio.google.com/"
    exit 1
fi

print_success "Configuration looks good!"

# Create necessary directories
print_step "Creating required directories..."
mkdir -p logs static/audio instance audio_files
print_success "Directories created!"

# Build Docker images
print_step "Building Docker images... (this may take a few minutes)"
if docker-compose build; then
    print_success "Docker images built successfully!"
else
    print_error "Failed to build Docker images!"
    echo ""
    echo "Common solutions:"
    echo "1. Check your internet connection"
    echo "2. Make sure you have enough disk space"
    echo "3. Try running: docker system prune -f"
    echo ""
    exit 1
fi

# Start the services
print_step "Starting Voice Chatbot services..."
if docker-compose up -d; then
    print_success "Services started!"
else
    print_error "Failed to start services!"
    echo ""
    echo "Check logs with: docker-compose logs"
    exit 1
fi

# Wait for services to be ready
print_step "Waiting for services to start..."
sleep 5

# Check if the application is responding
print_step "Testing application health..."
max_attempts=12
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f -s http://localhost:5000/api/health > /dev/null 2>&1; then
        print_success "Voice Chatbot is running successfully!"
        break
    else
        if [ $attempt -eq $max_attempts ]; then
            print_error "Application failed to start properly."
            echo ""
            echo "Troubleshooting:"
            echo "1. Check logs: docker-compose logs"
            echo "2. Check if port 5000 is free: lsof -i :5000"
            echo "3. Restart: docker-compose restart"
            echo ""
            exit 1
        fi
        echo "Waiting... (attempt $attempt/$max_attempts)"
        sleep 5
        ((attempt++))
    fi
done

echo ""
echo "🎉====================================🎉"
echo "   Voice Chatbot is Ready!"
echo "🎉====================================🎉"
echo ""
echo -e "${GREEN}🌐 Open your browser and go to: http://localhost:5000${NC}"
echo ""
echo "📱 Useful commands:"
echo "   View logs:           docker-compose logs -f"
echo "   Stop application:    docker-compose down"
echo "   Restart:            docker-compose restart"
echo "   Update application:  docker-compose build && docker-compose up -d"
echo "   Open app shell:      docker-compose exec chatbot bash"
echo ""
echo "🔧 Management script:"
echo "   Use ./chatbot.sh for easy management commands"
echo ""
echo "📚 Documentation:"
echo "   README.md - Main documentation"
echo "   DOCKER_GUIDE.md - Learn more about Docker"
echo ""
print_success "Setup complete! Enjoy your voice chatbot! 🎤🤖"
