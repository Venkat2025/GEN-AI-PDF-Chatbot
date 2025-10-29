import PyPDF2
import re
from typing import List

class PDFProcessor:
    """Handles PDF text extraction and chunking"""

    def __init__(self):
        pass

    def extract_text(self, pdf_path: str) -> str:
        """Extract text from a PDF file safely."""
        text = ""
        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"❌ Error extracting text from '{pdf_path}': {e}")
        return text.strip()

    def _clean_text(self, text: str) -> str:
        """Clean text by removing extra spaces, numbers, and newlines."""
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        return text.strip()

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for better context retrieval."""
        if not text:
            return []

        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current = ""

        for sentence in sentences:
            if len(current) + len(sentence) > chunk_size and current:
                chunks.append(current.strip())

                # keep a small overlap
                words = current.split()[-(overlap // 10):] if overlap > 0 else []
                current = " ".join(words) + " " + sentence
            else:
                current += " " + sentence

        if current:
            chunks.append(current.strip())

        return chunks
    