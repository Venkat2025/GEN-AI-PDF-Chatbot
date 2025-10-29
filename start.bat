@echo off
REM GenAI PDF Chatbot Startup Script for Windows
echo 🚀 Starting GenAI PDF Chatbot...

REM Check if .env file exists
if not exist .env (
    echo ⚠️  Warning: .env file not found!
    echo    Copy .env.example to .env and add your OPENAI_API_KEY
    echo    Example: copy .env.example .env
)

REM Function to check if port is in use
:check_port
netstat -an | findstr :%1 >nul
if %errorlevel% equ 0 (
    echo ❌ Port %1 is already in use
    exit /b 1
) else (
    echo ✅ Port %1 is available
    exit /b 0
)

REM Check ports
echo 🔍 Checking ports...
call :check_port 8000
set BACKEND_PORT_OK=%errorlevel%
call :check_port 3000
set FRONTEND_PORT_OK=%errorlevel%

if %BACKEND_PORT_OK% equ 0 (
    if %FRONTEND_PORT_OK% equ 0 (
        echo ✅ All ports are available
    ) else (
        echo ❌ Some ports are in use. Please free them up or modify the configuration.
        pause
        exit /b 1
    )
) else (
    echo ❌ Some ports are in use. Please free them up or modify the configuration.
    pause
    exit /b 1
)

REM Install backend dependencies if needed
echo 📦 Checking backend dependencies...
if not exist venv (
    echo    Creating virtual environment...
    python -m venv venv
)

echo    Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Install frontend dependencies if needed
echo 📦 Checking frontend dependencies...
if not exist node_modules (
    echo    Installing frontend dependencies...
    npm install
)

REM Start backend in background
echo 🔧 Starting backend server...
start "Backend" cmd /c "python main.py"
set BACKEND_PID=%errorlevel%

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Test backend
echo 🧪 Testing backend...
curl -s http://localhost:8000/ >nul
if %errorlevel% equ 0 (
    echo ✅ Backend started successfully
) else (
    echo ❌ Backend failed to start
    taskkill /f /im python.exe >nul 2>&1
    pause
    exit /b 1
)

REM Start frontend
echo 🎨 Starting frontend development server...
start "Frontend" cmd /c "npm start"

echo.
echo 🎉 GenAI PDF Chatbot is starting up!
echo.
echo 📋 Services:
echo    • Backend API: http://localhost:8000
echo    • Frontend UI: http://localhost:3000 (will open automatically)
echo.
echo 📖 Usage:
echo    1. Wait for the frontend to load in your browser
echo    2. Upload a PDF document
echo    3. Start chatting with AI about your document content
echo.
echo 🛑 To stop:
echo    • Close both command windows
echo    • Or press Ctrl+C in each window
echo.
echo Press any key to continue...
pause >nul

echo.
echo 🛑 Shutting down servers...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo ✅ Servers stopped
