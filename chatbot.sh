#!/bin/bash
# Voice Chatbot Management Script
# Easy commands to manage your Docker-based voice chatbot

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Helper functions
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose not found!"
        echo "Please install Docker Compose first."
        exit 1
    fi
}

# Get the correct docker-compose command
get_compose_cmd() {
    if command -v docker-compose &> /dev/null; then
        echo "docker-compose"
    else
        echo "docker compose"
    fi
}

case "$1" in
    "start")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_info "Starting Voice Chatbot..."
        if $COMPOSE_CMD up -d; then
            sleep 3
            print_success "Voice Chatbot started!"
            print_info "Open your browser: http://localhost:5000"
        else
            print_error "Failed to start. Check 'docker-compose logs' for details."
        fi
        ;;
    
    "stop")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_info "Stopping Voice Chatbot..."
        if $COMPOSE_CMD down; then
            print_success "Voice Chatbot stopped!"
        else
            print_error "Failed to stop services."
        fi
        ;;
    
    "restart")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_info "Restarting Voice Chatbot..."
        $COMPOSE_CMD restart
        sleep 3
        print_success "Voice Chatbot restarted!"
        print_info "Open your browser: http://localhost:5000"
        ;;
    
    "logs")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_info "Showing logs (Ctrl+C to exit)..."
        $COMPOSE_CMD logs -f
        ;;
    
    "build")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_info "Building Voice Chatbot image..."
        if $COMPOSE_CMD build; then
            print_success "Build completed!"
        else
            print_error "Build failed!"
        fi
        ;;
    
    "update")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_info "Updating Voice Chatbot..."
        print_info "Building new image..."
        $COMPOSE_CMD build
        print_info "Restarting with new image..."
        $COMPOSE_CMD up -d
        sleep 3
        print_success "Update completed!"
        print_info "Open your browser: http://localhost:5000"
        ;;
    
    "status")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_info "Service status:"
        $COMPOSE_CMD ps
        echo ""
        print_info "Quick health check:"
        if curl -f -s http://localhost:5000/api/health > /dev/null 2>&1; then
            print_success "Application is responding!"
        else
            print_warning "Application might not be running or ready yet."
        fi
        ;;
    
    "clean")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_warning "This will remove all containers and unused images."
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Cleaning up..."
            $COMPOSE_CMD down -v
            docker system prune -f
            print_success "Cleanup completed!"
        else
            print_info "Cleanup cancelled."
        fi
        ;;
    
    "shell"|"bash")
        check_docker_compose
        COMPOSE_CMD=$(get_compose_cmd)
        print_info "Opening shell in Voice Chatbot container..."
        $COMPOSE_CMD exec chatbot bash
        ;;
    
    "health")
        print_info "Checking application health..."
        if curl -f -s http://localhost:5000/api/health > /dev/null 2>&1; then
            print_success "✨ Voice Chatbot is healthy and responding!"
            echo ""
            # Get actual health response
            response=$(curl -s http://localhost:5000/api/health 2>/dev/null)
            if [ $? -eq 0 ]; then
                echo "Response: $response"
            fi
        else
            print_error "Voice Chatbot is not responding."
            echo ""
            print_info "Troubleshooting steps:"
            echo "1. Check if containers are running: ./chatbot.sh status"
            echo "2. Check logs: ./chatbot.sh logs"
            echo "3. Restart services: ./chatbot.sh restart"
        fi
        ;;
    
    "backup")
        print_info "Creating backup of voice chatbot data..."
        timestamp=$(date +%Y%m%d_%H%M%S)
        backup_name="chatbot_backup_$timestamp.tar.gz"
        
        tar -czf "$backup_name" \
            --exclude='venv' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='.git' \
            . 2>/dev/null
        
        if [ $? -eq 0 ]; then
            print_success "Backup created: $backup_name"
        else
            print_error "Backup failed!"
        fi
        ;;
    
    *)
        echo ""
        echo "🎤 Voice Chatbot - Docker Management Commands"
        echo "=============================================="
        echo ""
        echo "Usage: ./chatbot.sh [command]"
        echo ""
        echo -e "${BLUE}📱 Basic Commands:${NC}"
        echo "  start     - Start the voice chatbot"
        echo "  stop      - Stop the voice chatbot"
        echo "  restart   - Restart the voice chatbot"
        echo "  status    - Show service status and health"
        echo ""
        echo -e "${BLUE}🔍 Monitoring Commands:${NC}"
        echo "  logs      - View application logs (live)"
        echo "  health    - Check if application is responding"
        echo ""
        echo -e "${BLUE}🔧 Maintenance Commands:${NC}"
        echo "  build     - Rebuild the Docker image"
        echo "  update    - Build and restart with new image"
        echo "  clean     - Remove containers and unused images"
        echo "  backup    - Create backup of project files"
        echo ""
        echo -e "${BLUE}🐚 Development Commands:${NC}"
        echo "  shell     - Open bash shell in container"
        echo "  bash      - Same as shell"
        echo ""
        echo -e "${BLUE}💡 Examples:${NC}"
        echo "  ./chatbot.sh start        # Start the chatbot"
        echo "  ./chatbot.sh logs         # Watch live logs"
        echo "  ./chatbot.sh update       # Update and restart"
        echo "  ./chatbot.sh health       # Check if working"
        echo ""
        echo -e "${GREEN}🌐 After starting, open: http://localhost:5000${NC}"
        echo ""
        ;;
esac
