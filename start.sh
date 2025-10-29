#!/bin/bash

# GenAI PDF Chatbot Startup Script
echo "🚀 Starting GenAI PDF Chatbot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Copy .env.example to .env and add your OPENAI_API_KEY"
    echo "   Example: cp .env.example .env"
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use"
        return 1
    else
        echo "✅ Port $1 is available"
        return 0
    fi
}

# Check ports
echo "🔍 Checking ports..."
check_port 8000
BACKEND_PORT_OK=$?
check_port 3000
FRONTEND_PORT_OK=$?

if [ $BACKEND_PORT_OK -eq 0 ] && [ $FRONTEND_PORT_OK -eq 0 ]; then
    echo "✅ All ports are available"
else
    echo "❌ Some ports are in use. Please free them up or modify the configuration."
    exit 1
fi

# Install backend dependencies if needed
echo "📦 Checking backend dependencies..."
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python -m venv venv
fi

echo "   Activating virtual environment and installing dependencies..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
pip install -r requirements.txt

# Install frontend dependencies if needed
echo "📦 Checking frontend dependencies..."
if [ ! -d "node_modules" ]; then
    echo "   Installing frontend dependencies..."
    npm install
fi

# Start backend in background
echo "🔧 Starting backend server..."
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Test backend
echo "🧪 Testing backend..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend development server..."
npm start &
FRONTEND_PID=$!

echo ""
echo "🎉 GenAI PDF Chatbot is starting up!"
echo ""
echo "📋 Services:"
echo "   • Backend API: http://localhost:8000"
echo "   • Frontend UI: http://localhost:3000 (will open automatically)"
echo ""
echo "📖 Usage:"
echo "   1. Wait for the frontend to load in your browser"
echo "   2. Upload a PDF document"
echo "   3. Start chatting with AI about your document content"
echo ""
echo "🛑 To stop:"
echo "   • Press Ctrl+C to stop both servers"
echo "   • Or run: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup INT TERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
