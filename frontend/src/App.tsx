import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function App() {
  const [documents, setDocuments] = useState<string[]>([]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [rebuilding, setRebuilding] = useState(false);
  const [rebuildMsg, setRebuildMsg] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const fetchDocuments = async () => {
    const res = await axios.get(`${API_URL}/documents`);
    setDocuments(res.data.documents);
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      await axios.post(`${API_URL}/upload`, formData);
      setFile(null);
      await fetchDocuments();
      setRebuildMsg(
        "File uploaded. Click 'Rebuild Index' to make it searchable.",
      );
    } catch (err) {
      setRebuildMsg("Upload failed.");
    }
    setUploading(false);
  };

  const handleRebuild = async () => {
    setRebuilding(true);
    setRebuildMsg("");
    try {
      const res = await axios.post(`${API_URL}/rebuild-index`);
      setRebuildMsg(`Index rebuilt with ${res.data.documents} document(s)`);
    } catch (err) {
      setRebuildMsg("Failed to rebuild index");
    }
    setRebuilding(false);
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer("");
    setSources([]);
    try {
      const res = await axios.post(`${API_URL}/ask`, { question });
      setAnswer(res.data.answer);
      setSources([...new Set(res.data.sources as string[])]);
    } catch (err) {
      setAnswer(
        "Something went wrong. Make sure documents are uploaded and indexed.",
      );
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center px-4 py-10">
      <div className="w-full max-w-3xl">
        <h1 className="text-3xl font-bold mb-1">
          Intelligent Document Research Assistant
        </h1>
        <p className="text-slate-400 mb-8">
          RAG-powered Q&A over your documents
        </p>

        {/* Document management */}
        <div className="bg-slate-900 rounded-xl p-5 mb-6 border border-slate-800">
          <h2 className="text-lg font-semibold mb-3">Documents</h2>

          <div className="flex gap-3 mb-4 items-center">
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="text-sm text-slate-300 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-indigo-600 file:text-white file:cursor-pointer"
            />
            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 px-4 py-2 rounded-lg text-sm font-medium"
            >
              {uploading ? "Uploading..." : "Upload"}
            </button>
          </div>

          <button
            onClick={handleRebuild}
            disabled={rebuilding}
            className="bg-slate-800 hover:bg-slate-700 disabled:opacity-40 px-4 py-2 rounded-lg text-sm font-medium mb-3"
          >
            {rebuilding ? "Rebuilding index..." : "Rebuild Index"}
          </button>

          {rebuildMsg && (
            <p className="text-sm text-emerald-400 mb-3">{rebuildMsg}</p>
          )}

          <div className="text-sm text-slate-400">
            {documents.length === 0 ? (
              <p>No documents uploaded yet.</p>
            ) : (
              <ul className="list-disc list-inside">
                {documents.map((doc) => (
                  <li key={doc}>{doc}</li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* Q&A */}
        <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
          <h2 className="text-lg font-semibold mb-3">Ask a Question</h2>
          <div className="flex gap-3 mb-4">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAsk()}
              placeholder="What is RAG?"
              className="flex-1 bg-slate-800 rounded-lg px-4 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              onClick={handleAsk}
              disabled={loading}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 px-5 py-2 rounded-lg text-sm font-medium"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>

          {answer && (
            <div className="mt-4">
              <h3 className="text-sm font-semibold text-slate-400 mb-1">
                Answer
              </h3>
              <p className="text-slate-100 leading-relaxed mb-3">{answer}</p>

              {sources.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-slate-400 mb-1">
                    Sources
                  </h3>
                  <ul className="text-sm text-slate-400 list-disc list-inside">
                    {sources.map((src, i) => (
                      <li key={i}>{src}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
