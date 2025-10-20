#!/bin/bash

# Flask Backend Startup Script for Retell AI Integration
# This script starts the Flask backend server

echo "🚀 Starting Flask Backend for Retell AI Integration"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the flask_backend directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "⚠️  Warning: Virtual environment not found. Creating one..."
    python3 -m venv ../venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f "../.env" ]; then
    echo "⚠️  Warning: .env file not found in parent directory."
    echo "   Please create a .env file with GROQ_API_KEY and SERP_API_KEY"
    echo "   Example:"
    echo "   GROQ_API_KEY=your_groq_api_key_here"
    echo "   SERP_API_KEY=your_serp_api_key_here"
    echo ""
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Start the server
echo "🌐 Starting Flask server..."
echo "📞 Webhook endpoint: http://localhost:5000/retell/webhook"
echo "🔍 Test endpoint: http://localhost:5000/test-agent"
echo "❤️  Health check: http://localhost:5000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="

python run_server.py
