from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import shutil
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from pdf_processor import PDFProcessor
from vector_store import VectorStore
from chat_handler import DeepSeekChatHandler

app = FastAPI(title="GenAI PDF Chatbot API", description="PDF-based chatbot (local)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_processor = PDFProcessor()
vector_store = VectorStore()
chat_handler = DeepSeekChatHandler()

@app.get("/")
async def root():
    return {"message": "GenAI Chatbot API", "status": "running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        text = pdf_processor.extract_text(tmp_path)
        chunks = pdf_processor.chunk_text(text)

        embeddings = chat_handler.generate_embeddings(chunks)
        doc_id = vector_store.add_document(chunks, embeddings, {"filename": file.filename})

        os.unlink(tmp_path)

        return {"message": "PDF processed successfully", "document_id": doc_id, "chunks_count": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(payload: dict):
    try:
        user_query = payload.get("message")
        if not user_query:
            raise HTTPException(status_code=400, detail="message is required")

        query_emb = chat_handler.generate_query_embedding(user_query)
        relevant = vector_store.search(query_emb, top_k=5)
        response = chat_handler.generate_response(user_query, relevant)
        return {"response": response, "sources": relevant}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    try:
        return {"documents": vector_store.list_documents()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Use 127.0.0.1 so browser can open localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
