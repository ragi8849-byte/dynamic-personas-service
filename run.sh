#!/bin/bash

echo "Starting Dynamic Persona Generator..."
echo "======================================="
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "Building Docker image..."
    docker build -t persona-generator .

    echo ""
    echo "Starting server on http://localhost:8080"
    echo "Press Ctrl+C to stop"
    echo ""

    docker run -p 8080:8080 persona-generator
else
    echo "Docker not found. Trying local Python..."

    # Check if uvicorn is installed
    if python3 -c "import uvicorn" 2>/dev/null; then
        echo "Starting server on http://localhost:8000"
        echo "Press Ctrl+C to stop"
        echo ""
        python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    else
        echo "Error: Neither Docker nor Python environment is properly set up."
        echo ""
        echo "Please either:"
        echo "1. Install Docker and run: ./run.sh"
        echo "2. Or install Python dependencies: pip install -r requirements.txt"
        exit 1
    fi
fi
