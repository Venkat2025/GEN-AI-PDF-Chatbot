import os
import numpy as np
import requests
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class DeepSeekChatHandler:
    """Handles DeepSeek API integration for embeddings and chat"""

    def __init__(self, api_key: str = None):
        """Initialize with optional API key override"""
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            logger.warning("⚠️ No DeepSeek API key found. Using mock responses.")
            self.api_available = False
        else:
            self.api_available = True
            logger.info("✅ DeepSeek API key loaded")

        # API configuration
        self.base_url = "https://api.deepseek.com/v1"
        self.embedding_model = "deepseek-base"  # Change to your model
        self.chat_model = "deepseek-chat"       # Change to your model

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings using DeepSeek API or fallback to mock"""
        if not self.api_available:
            return self._generate_mock_embeddings(texts)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json={
                    "input": texts,
                    "model": self.embedding_model
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                embeddings = [data["embedding"] for data in result["data"]]
                return np.array(embeddings)
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._generate_mock_embeddings(texts)
                
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {str(e)}")
            return self._generate_mock_embeddings(texts)

    def _generate_mock_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate deterministic mock embeddings for testing"""
        import hashlib
        
        def text_to_embedding(text: str, dim: int = 384) -> np.ndarray:
            h = hashlib.sha256(text.encode()).digest()
            arr = np.frombuffer(h, dtype=np.uint8)
            # Expand to desired dimensions
            if len(arr) < dim:
                arr = np.pad(arr, (0, dim - len(arr)), mode='wrap')
            else:
                arr = arr[:dim]
            # Normalize to unit vector
            emb = arr.astype(np.float32) / 255.0
            if np.linalg.norm(emb) > 0:
                emb = emb / np.linalg.norm(emb)
            return emb
            
        embeddings = [text_to_embedding(t) for t in texts]
        return np.vstack(embeddings)

    def generate_query_embedding(self, text: str) -> np.ndarray:
        return self._text_to_embedding(text).astype(np.float32)

    def generate_response(self, query: str, relevant_chunks: List[Dict[str, Any]]) -> str:
        """Generate response using DeepSeek API with context from chunks"""
        if not self.api_available:
            return self._generate_mock_response(query, relevant_chunks)

        if not relevant_chunks:
            return "I don't have any relevant context from the documents to answer your question."

        try:
            # Prepare context from relevant chunks
            context = "\n\n".join([chunk["text"] for chunk in relevant_chunks])
            
            # Create system and user messages
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on the provided document context. Always be accurate and concise."
                },
                {
                    "role": "user",
                    "content": f"Context from documents:\n\n{context}\n\nQuestion: {query}\n\nAnswer the question based only on the provided context."
                }
            ]
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.chat_model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"DeepSeek chat API error: {response.status_code} - {response.text}")
                return self._generate_mock_response(query, relevant_chunks)
                
        except Exception as e:
            logger.error(f"Error calling DeepSeek chat API: {str(e)}")
            return self._generate_mock_response(query, relevant_chunks)

    def _generate_mock_response(self, query: str, relevant_chunks: List[Dict[str, Any]]) -> str:
        """Generate a simple mock response using the chunks directly"""
        if not relevant_chunks:
            return "I don't have any relevant context from the documents to answer your question."

        # Use the most relevant chunks to construct a response
        top_chunks = relevant_chunks[:2]  # Use top 2 chunks
        context = "\n\n".join(chunk["text"] for chunk in top_chunks)
        
        response = (
            f"Based on the documents, here's what I found:\n\n{context}\n\n"
            "(Note: This is a mock response. Add your DeepSeek API key for AI-powered answers.)"
        )
        return response
