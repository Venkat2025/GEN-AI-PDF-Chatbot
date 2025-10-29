# GenAI PDF Chatbot

This repository contains a minimal, working GenAI PDF Chatbot backend and a small static frontend to test uploads and chat. The backend extracts text from PDFs, chunks text, computes embeddings (mock if no API key), and stores vectors. FAISS is optional — the project includes a pure numpy fallback so it runs on Windows.

## What I changed / provided
- Fixed `pdf_processor.py` to handle edge cases and None from PyPDF2
- Added FAISS fallback in `vector_store.py` so the app works if `faiss` isn't available
- Made FAISS optional in `requirements.txt` (won't be installed on Windows by default)
- Kept `chat_handler.py`'s mock fallback; it will use DeepSeek if `DEEPSEEK_API_KEY` is set
- Added a minimal static frontend in `simple_frontend/` to upload PDFs and ask chat queries
- Updated `main.py` to allow `BACKEND_PORT` override and print startup info

## Quick Start (Windows PowerShell)

1) Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2) Install Python dependencies

```powershell
pip install -r requirements.txt
```

3) (Optional) Add your DeepSeek API key to `.env` (create `.env` from `.env.example`)

```powershell
copy .env.example .env
# Edit .env and set DEEPSEEK_API_KEY
```

4) Start the backend

```powershell
# Optionally change port: set BACKEND_PORT environment variable
$env:BACKEND_PORT = '8000'
python main.py
```

Visit the health endpoint in your browser (use localhost or 127.0.0.1, not 0.0.0.0):

http://127.0.0.1:8000/

5) Run the simple frontend

Open `simple_frontend/index.html` in your browser (you can double-click the file) or serve it with a simple static server:

```powershell
# from project root
python -m http.server 8080
# then open http://127.0.0.1:8080/simple_frontend/
```

6) Upload a PDF and ask questions

Use the simple UI to upload `Bank-Policy-Development-pol-fin.pdf` (or any PDF). Then type queries and click Ask.

## Notes & Troubleshooting
- Do not use `http://0.0.0.0:8000` in the browser — use `http://127.0.0.1:8000` or `http://localhost:8000`.
- On Windows, installing `faiss-cpu` via pip may fail. The code has a numpy fallback; you can skip installing FAISS. If you want FAISS, install it separately on a supported platform and set `sys_platform` accordingly.
- If the backend can't bind to port 8000, another process is using it. Find and kill it:

```powershell
netstat -a -n -o | findstr :8000
taskkill /PID <pid> /F
```

## Files of interest
- `main.py` — FastAPI backend
- `pdf_processor.py` — PDF extraction and chunking
- `vector_store.py` — Vector store with FAISS fallback
- `chat_handler.py` — Embeddings and chat integration (mock if no API key)
- `simple_frontend/` — Minimal UI to test upload and chat

If you want, I can:
- Add a small unit test suite and CI workflow
- Implement a full React frontend that matches the original design
- Add Dockerfile / containerized setup

Tell me which of these you'd like next, or paste any errors you still see and I'll fix them.

---
Built with helpful automation and the provided project files.
# GenAI PDF Chatbot

A modern, end-to-end Generative AI chatbot that extracts content from PDFs, stores and indexes information using vector databases, and provides an interactive web UI for querying.

## Features

- 📄 **PDF Upload & Processing**: Upload PDF documents and automatically extract text
- 🔍 **Intelligent Text Chunking**: Split documents into contextual chunks for better retrieval
- 🧠 **Vector Search**: FAISS-based vector database for semantic search
- 🤖 **AI-Powered Responses**: DeepSeek AI integration for natural language responses
- 💬 **Modern Chat Interface**: Beautiful, responsive React-based UI
- 📱 **Mobile Friendly**: Responsive design that works on all devices
- ⚡ **Real-time Processing**: Fast PDF processing and query responses

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│◄──►│  FastAPI Backend│◄──►│   Vector Store  │
│                 │    │                 │    │   (FAISS)       │
│ - Chat UI       │    │ - PDF Processing│    │                 │
│ - File Upload   │    │ - Embeddings    │    │ - Similarity    │
│ - Responsive    │    │ - Chat API      │    │ - Search        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   DeepSeek API  │
                       │                 │
                       │ - Embeddings    │
                       │ - Chat Models   │
                       └─────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- DeepSeek API Key (get one from [DeepSeek](https://platform.deepseek.com/api-keys))

### 1. Backend Setup

```bash
# Navigate to project directory
cd d:/Project/edukron/Genai

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your DeepSeek API key:
# DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Run the backend server
python main.py
```

The backend will start on `http://localhost:8000`

### 2. Frontend Setup

```bash
# Install Node.js dependencies
npm install

# Start the development server
npm start
```

The frontend will start on `http://localhost:3000`

### 3. Usage

1. Open your browser and go to `http://localhost:3000`
2. Upload a PDF document using the file picker
3. Wait for the document to be processed (you'll see a success message)
4. Start chatting by typing questions about your PDF content
5. The AI will provide answers based on the document content with source citations

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload and process PDF files
- `POST /chat` - Send chat messages
- `GET /documents` - List processed documents

## Project Structure

```
├── main.py              # FastAPI backend application
├── pdf_processor.py     # PDF text extraction and chunking
├── vector_store.py      # FAISS vector database management
├── chat_handler.py      # DeepSeek API integration
├── requirements.txt     # Python dependencies
├── package.json         # Node.js dependencies
├── README.md           # This file
├── src/                # React frontend
│   ├── App.js         # Main React component
│   ├── index.js       # React entry point
│   ├── index.css      # Global styles
│   └── App.css        # Component-specific styles
└── public/             # Static assets
    └── index.html     # HTML template
```

## Key Components

### Backend Components

#### PDFProcessor (`pdf_processor.py`)
- Extracts text from PDF files using PyPDF2
- Supports OCR for scanned documents (with Tesseract)
- Intelligently chunks text into contextual segments
- Cleans and normalizes extracted text

#### VectorStore (`vector_store.py`)
- Manages vector embeddings using FAISS
- Provides similarity search functionality
- Handles document metadata and indexing
- Persistent storage of vectors and metadata

#### ChatHandler (`chat_handler.py`)
- Generates embeddings using DeepSeek's API
- Manages chat interactions with DeepSeek models
- Provides context-aware response generation
- Includes fallback to open-source alternatives

### Frontend Components

#### Professional React Chat Interface
- **Modern Glassmorphism Design** with backdrop blur effects and gradient backgrounds
- **Professional Header** with animated status indicators and branding
- **Advanced Upload System** with progress bars, file validation, and drag-and-drop support
- **Document Management Panel** showing processed PDFs with metadata and status badges
- **Enhanced Chat Experience** with avatars, timestamps, and message actions
- **Interactive Welcome Screen** with feature highlights and animations
- **Real-time Feedback System** with thumbs up/down buttons and copy functionality
- **Responsive Design** optimized for desktop, tablet, and mobile devices
- **PWA Support** with manifest file for installable app experience
- **Error Handling** with elegant error banners and user-friendly messages
- **Loading States** with custom spinners and progress indicators
- **Smooth Animations** including fade-ins, slide-ins, and hover effects

## Customization

### Using Open-Source Alternatives

For a completely free setup, you can modify `chat_handler.py` to use:

1. **Hugging Face Transformers** for embeddings:
   ```bash
   pip install transformers torch
   ```

2. **Local LLM models** for chat responses (requires more setup)

### Adjusting Chunk Size

Modify the chunk size in `pdf_processor.py`:

```python
def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200)
```

### Customizing UI

The frontend uses CSS custom properties and can be easily themed by modifying `src/index.css`.

## Performance Considerations

- **Chunk Size**: Smaller chunks (500-800 tokens) provide more precise answers
- **Vector Dimensions**: OpenAI embeddings use 1536 dimensions for good performance
- **Search Results**: Top 3-5 chunks usually provide sufficient context
- **Caching**: Consider implementing response caching for frequently asked questions

## Security Best Practices

1. **API Key Security**: Never commit API keys to version control
2. **Input Validation**: Validate file types and sizes on upload
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **CORS**: Configure CORS properly for production deployment
5. **Authentication**: Add user authentication for multi-user scenarios

## Deployment

### Backend Deployment

```bash
# Using Gunicorn for production
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Serve with any static file server
npx serve -s build
```

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **DeepSeek API Errors**: Check your API key and account status
2. **PDF Processing Failures**: Ensure PDF files are not password-protected
3. **Memory Issues**: Large PDFs may require chunk size adjustment
4. **CORS Errors**: Check CORS configuration in production

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export DEBUG=true
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Create an issue in the repository

---

Built with ❤️ using FastAPI, React, FAISS, and DeepSeek AI
