import React, { useState } from "react";

const API = "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [documentId, setDocumentId] = useState(null);
  const [chunksCount, setChunksCount] = useState(0);
  const [query, setQuery] = useState("");
  const [chatResponse, setChatResponse] = useState("");
  const [sources, setSources] = useState([]);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const upload = async () => {
    if (!file) return alert("Choose a PDF first");
    setStatus("Uploading...");
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await fetch(API + "/upload", { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || JSON.stringify(data));
      setStatus("Uploaded");
      setDocumentId(data.document_id);
      setChunksCount(data.chunks_count);
    } catch (e) {
      setStatus("Error: " + e.message);
      console.error(e);
    }
  };

  const ask = async () => {
    if (!query) return;
    setChatResponse("Thinking...");
    try {
      const res = await fetch(API + "/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || JSON.stringify(data));
      setChatResponse(data.response);
      setSources(data.sources || []);
    } catch (e) {
      setChatResponse("Error: " + e.message);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>GenAI PDF Chatbot (local)</h2>
        <p>Upload a PDF and ask about its content.</p>

        <div style={{ marginBottom: 12 }}>
          <input type="file" accept="application/pdf" onChange={onFileChange} />
          <button onClick={upload} style={{ marginLeft: 8 }}>
            Upload
          </button>
        </div>

        <div>
          <strong>Status:</strong> {status} &nbsp;
          {documentId && <span>• Document ID: {documentId} • Chunks: {chunksCount}</span>}
        </div>
      </div>

      <div className="card" style={{ marginTop: 18 }}>
        <h3>Ask a question</h3>
        <input
          style={{ width: "80%", padding: 8, borderRadius: 6, border: "none" }}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Write your question here..."
        />
        <button onClick={ask} style={{ marginLeft: 8 }}>
          Ask
        </button>

        <div style={{ marginTop: 12 }}>
          <h4>Response</h4>
          <div style={{ whiteSpace: "pre-wrap", background: "rgba(255,255,255,0.02)", padding: 12, borderRadius: 6 }}>
            {chatResponse}
          </div>

          {sources.length > 0 && (
            <>
              <h5>Sources</h5>
              <ul>
                {sources.map((s, i) => (
                  <li key={i}>
                    <strong>{s.filename || "Unknown"}</strong> — chunk {s.chunk_index} (score: {s.similarity_score?.toFixed(3)})
                    <div style={{ fontSize: 13, opacity: 0.9 }}>{s.text?.slice(0, 200)}{s.text && s.text.length>200 ? "..." : ""}</div>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
