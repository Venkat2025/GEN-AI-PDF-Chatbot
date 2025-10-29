import os
import json
import numpy as np
from typing import List, Dict, Any

# Try to import FAISS
try:
    import faiss
    _HAS_FAISS = True
except Exception:
    _HAS_FAISS = False

class VectorStore:
    def __init__(self, index_path: str = "faiss_index.bin", metadata_path: str = "metadata.json"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.metadata: List[Dict[str, Any]] = []
        self.id_counter = 0
        self.embeddings = None  # used for in-memory fallback
        self.dim = None
        self.use_faiss = _HAS_FAISS and os.path.exists(self.index_path)
        if self.use_faiss:
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, "r") as f:
                    self.metadata = json.load(f)
                self.id_counter = len(self.metadata)
                self.dim = self.index.d
            except Exception:
                self.use_faiss = False
                self.index = None
        else:
            self.index = None
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, "r") as f:
                    self.metadata = json.load(f)
                    self.id_counter = len(self.metadata)

    def _save_metadata(self):
        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def add_document(self, chunks: List[str], embeddings: np.ndarray, doc_metadata: Dict[str, Any]) -> str:
        # embeddings: shape (n_chunks, dim)
        if embeddings is None or len(chunks) == 0:
            raise ValueError("Embeddings and chunks required")

        n, dim = embeddings.shape
        if self.index is None and _HAS_FAISS:
            # create faiss index
            self.index = faiss.IndexFlatIP(dim)
            self.use_faiss = True

        if self.use_faiss:
            self.index.add(embeddings.astype("float32"))
        else:
            if self.embeddings is None:
                self.embeddings = embeddings.astype("float32")
            else:
                self.embeddings = np.vstack([self.embeddings, embeddings.astype("float32")])

        doc_id = str(self.id_counter)
        self.id_counter += 1
        for i, chunk in enumerate(chunks):
            meta = {
                "id": f"{doc_id}_{i}",
                "document_id": doc_id,
                "chunk_index": i,
                "text": chunk,
                **doc_metadata
            }
            self.metadata.append(meta)

        self._save_metadata()
        # if using faiss, save index file if possible
        if self.use_faiss and _HAS_FAISS:
            try:
                faiss.write_index(self.index, self.index_path)
            except Exception:
                pass
        return doc_id

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        if self.use_faiss and self.index is not None:
            q = query_embedding / np.linalg.norm(query_embedding)
            q = q.reshape(1, -1).astype("float32")
            scores, indices = self.index.search(q, min(top_k, self.index.ntotal))
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx != -1:
                    meta = dict(self.metadata[idx])
                    meta["similarity_score"] = float(score)
                    results.append(meta)
            results.sort(key=lambda x: x["similarity_score"], reverse=True)
            return results
        else:
            if self.embeddings is None or len(self.metadata) == 0:
                return []
            q = query_embedding / np.linalg.norm(query_embedding)
            emb = self.embeddings
            emb_norms = np.linalg.norm(emb, axis=1)
            emb_norms[emb_norms == 0] = 1e-9
            emb_normalized = emb / emb_norms[:, None]
            scores = emb_normalized.dot(q)
            idxs = np.argsort(scores)[::-1][:min(top_k, len(scores))]
            results = []
            for idx in idxs:
                results.append({**self.metadata[idx], "similarity_score": float(scores[idx])})
            return results

    def list_documents(self) -> List[Dict[str, Any]]:
        if not self.metadata:
            return []
        docs = {}
        for meta in self.metadata:
            doc_id = meta["document_id"]
            if doc_id not in docs:
                docs[doc_id] = {"id": doc_id, "filename": meta.get("filename", "Unknown"), "chunks_count": 0}
            docs[doc_id]["chunks_count"] += 1
        return list(docs.values())

    def clear_all(self):
        self.metadata = []
        self.embeddings = None
        self.index = None
        self.id_counter = 0
        if os.path.exists(self.index_path):
            try:
                os.remove(self.index_path)
            except Exception:
                pass
        if os.path.exists(self.metadata_path):
            try:
                os.remove(self.metadata_path)
            except Exception:
                pass
