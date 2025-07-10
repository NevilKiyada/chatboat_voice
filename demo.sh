#!/bin/bash

# Voice Chatbot Demo Script
# Demonstrates the containerized voice chatbot capabilities

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_banner() {
    echo -e "${PURPLE}"
    echo "🎤🤖 Voice Chatbot Demo"
    echo "======================"
    echo -e "${NC}"
}

print_status() { echo -e "${BLUE}[DEMO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check Docker
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found! Please install Docker first."
        echo "See DOCKER_INSTALL.md for installation instructions."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose not found!"
        exit 1
    fi
    
    print_success "Docker environment ready"
}

# Start the application
start_chatbot() {
    print_status "Starting Voice Chatbot with Docker..."
    
    if docker-compose up -d; then
        print_success "Voice Chatbot containers started!"
    else
        print_error "Failed to start containers"
        exit 1
    fi
    
    print_status "Waiting for application to be ready..."
    sleep 10
}

# Test health endpoint
test_health() {
    print_status "Testing health endpoint..."
    
    for i in {1..30}; do
        if curl -s http://localhost:5000/health > /dev/null 2>&1; then
            print_success "✅ Health check passed!"
            return 0
        fi
        echo -n "."
        sleep 2
    done
    
    print_error "❌ Health check failed"
    return 1
}

# Test API endpoints
test_api() {
    print_status "Testing API endpoints..."
    
    # Test chat endpoint
    echo -n "Testing chat API... "
    response=$(curl -s -X POST http://localhost:5000/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello, this is a test message"}')
    
    if echo "$response" | grep -q "response"; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌${NC}"
    fi
    
    # Test TTS endpoint
    echo -n "Testing text-to-speech API... "
    tts_response=$(curl -s -X POST http://localhost:5000/api/voice/speak \
        -H "Content-Type: application/json" \
        -d '{"text": "This is a test message"}')
    
    if echo "$tts_response" | grep -q "audio_url"; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌${NC}"
    fi
}

# Show container status
show_status() {
    print_status "Container status:"
    docker-compose ps
    
    echo ""
    print_status "Resource usage:"
    docker stats --no-stream voice-chatbot 2>/dev/null || echo "Container not found"
}

# Show demo instructions
show_demo_instructions() {
    echo ""
    echo -e "${PURPLE}🎉 Demo Ready!${NC}"
    echo "=============="
    echo ""
    echo "Your Voice Chatbot is now running at:"
    echo -e "${GREEN}🌐 Web Interface: http://localhost:5000${NC}"
    echo -e "${GREEN}🏥 Health Check: http://localhost:5000/health${NC}"
    echo ""
    echo "Try these features:"
    echo "1. 💬 Text Chat - Type messages and get AI responses"
    echo "2. 🎤 Voice Input - Click microphone to speak"
    echo "3. 🔊 Voice Output - Click speaker to hear responses"
    echo "4. 📱 Mobile - Try it on your phone browser"
    echo ""
    echo "Management commands:"
    echo "• View logs: ./chatbot.sh logs"
    echo "• Stop demo: ./chatbot.sh stop"
    echo "• Restart: ./chatbot.sh restart"
    echo ""
    echo "Press Ctrl+C to stop this demo"
}

# Monitor logs
monitor_logs() {
    print_status "Monitoring application logs (Ctrl+C to stop)..."
    echo ""
    docker-compose logs -f
}

# Cleanup function
cleanup() {
    echo ""
    print_status "Stopping demo..."
    docker-compose down
    print_success "Demo stopped. Thank you for trying Voice Chatbot!"
}

# Main demo function
main() {
    print_banner
    
    # Set trap for cleanup
    trap cleanup EXIT
    
    check_prerequisites
    start_chatbot
    
    if test_health; then
        test_api
        show_status
        show_demo_instructions
        
        # Keep running and show logs
        monitor_logs
    else
        print_error "Demo failed to start properly"
        print_status "Check logs with: docker-compose logs"
        exit 1
    fi
}

# Run main function
main "$@"