# Use Python 3.12 slim image as the base
# "slim" means it has fewer unnecessary packages = smaller image
FROM python:3.12-slim

# Set metadata for the image (optional but good practice)
LABEL maintainer="Voice Chatbot Project"
LABEL description="AI-powered voice chatbot with speech recognition"
LABEL version="1.0"

# Set environment variables
# These make Python work better in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Set the working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

# Install system dependencies needed for audio processing
# This is crucial for voice features to work!
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    ffmpeg \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for better Docker layer caching)
# Docker caches layers, so if requirements don't change, 
# it won't reinstall packages
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
# The . means "copy everything from current directory"
COPY . .

# Create necessary directories for the application
RUN mkdir -p /app/logs /app/static/audio /app/instance /app/audio_files

# Create a non-root user for security
# Running as root in containers is a security risk
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose port 5000 (the port our Flask app uses)
# This is just documentation - doesn't actually open the port
EXPOSE 5000

# Add a health check to make sure the container is working
# Docker will periodically check if the app is responding
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')" || exit 1

# Define the command to run when the container starts
# This starts our Flask application
CMD ["python", "app.py"]
