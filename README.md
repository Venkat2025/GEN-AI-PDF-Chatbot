# 🧠 GenAI PDF Chatbot

A modern, end-to-end Generative AI chatbot that extracts content from PDFs, stores and indexes information using a vector database (FAISS or NumPy fallback), and provides an interactive web UI for querying your documents.

---

## 🚀 Features

- 📄 **PDF Upload & Processing:** Extracts and cleans text using PyPDF2  
- 🧩 **Intelligent Text Chunking:** Splits long documents into contextual chunks  
- 🧠 **Vector Search:** Uses FAISS if available, falls back to NumPy on Windows  
- 🤖 **AI Responses:** Uses DeepSeek API (or mock embeddings if no API key)  
- 💬 **Simple Web UI:** Upload PDFs and chat with them in your browser  
- ⚙️ **Cross-platform:** Fully compatible with Windows, Linux, and macOS  

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend (React) │◄──►│  FastAPI Backend │◄──►│  Vector Store (FAISS) │
│   Upload & Chat UI │    │  PDF + Embeddings │    │  Semantic Search      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   DeepSeek API  │
                       │  (Optional AI)  │
                       └─────────────────┘
```

---

## ⚙️ Quick Start (Windows PowerShell)

### 1️⃣ Create & activate virtual environment

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

### 2️⃣ Install Python dependencies

```powershell
pip install -r requirements.txt
```

> 💡 `faiss` is **optional** — the app automatically falls back to NumPy if FAISS isn’t available.

---

### 3️⃣ (Optional) Add your DeepSeek API key

```powershell
copy .env.example .env
# Edit .env and set:
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

---

### 4️⃣ Start the backend

```powershell
$env:BACKEND_PORT = '8000'
python main.py
```

Backend runs at:  
👉 http://127.0.0.1:8000/  
(You’ll see `{"message":"GenAI Chatbot API","status":"running"}`)

---

### 5️⃣ Start the frontend

If you’re using the React-based UI:

```powershell
cd frontend
npm install
npm start
```

Frontend will open at:  
👉 http://localhost:3000

If you’re using the simple static HTML UI instead:

```powershell
python -m http.server 8080
# Then open: http://127.0.0.1:8080/simple_frontend/
```

---

### 6️⃣ Upload a PDF and Ask Questions

1. Upload `Bank-Policy-Development-pol-fin.pdf` (or any PDF).  
2. Wait for “Status: Uploaded” with document ID and chunk count.  
3. Ask natural questions like:  
   - “What is Development Policy Financing?”  
   - “Who is responsible for policy compliance?”  
   - “What are the eligibility criteria for Special DPF?”

---

## 📂 Project Structure

```
GENAI-MAIN/
│
├── main.py                  # FastAPI backend
├── pdf_processor.py         # Extracts and chunks PDF text
├── vector_store.py          # FAISS or NumPy vector store
├── chat_handler.py          # DeepSeek API integration / fallback
│
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── STARTUP_GUIDE.md         # Optional setup guide
│
├── uploads/                 # Uploaded PDF files (auto-created)
│   └── *.pdf
│
├── metadata.json            # Document metadata (auto-generated)
├── faiss_index.bin          # Vector index (auto-generated)
│
├── test_upload.py           # Upload route test
├── test_system.py           # Full pipeline test
│
├── start.bat                # Windows launcher
├── start.sh                 # Linux/Mac launcher
│
├── .env                     # API keys and configs
├── .env.example             # Example env template
│
└── frontend/                # React frontend
    ├── package.json
    ├── package-lock.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js
        ├── App.css
        ├── index.js
        └── index.css
```

---

## 🧠 Configuration

### Environment Variables (`.env`)
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
BACKEND_PORT=8000
```

### API Endpoints

| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload and process PDF |
| `POST` | `/chat` | Send chat message and get response |
| `GET` | `/documents` | List processed documents |

---

## 🧩 Key Components

| Component | Description |
|------------|--------------|
| **PDFProcessor** | Extracts text with PyPDF2 and chunks it for embeddings |
| **VectorStore** | Stores and searches document embeddings (FAISS or NumPy) |
| **ChatHandler** | Handles embedding and AI responses (DeepSeek or mock) |
| **Frontend** | React-based or static HTML UI for uploads and chat |

---

## 🛠️ Troubleshooting

| Issue | Fix |
|--------|-----|
| ❌ `500 Internal Server Error` | Ensure `uploads/` folder exists and PDF is valid |
| ⚠️ `faiss` import error | Ignore — app falls back to NumPy |
| ⚙️ Port 8000 in use | Run `netstat -a -n -o | findstr :8000` → `taskkill /PID <pid> /F` |
| 🔒 PowerShell script error | Run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |

---

## 🧱 Deployment

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (React)
```bash
cd frontend
npm run build
npx serve -s build
```

---

## ❤️ Built With
- [FastAPI](https://fastapi.tiangolo.com/)  
- [PyPDF2](https://pypi.org/project/PyPDF2/)  
- [FAISS](https://faiss.ai/) / NumPy fallback  
- [React](https://react.dev/)  
- [DeepSeek API](https://platform.deepseek.com/)

---
