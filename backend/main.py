from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import glob
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingest import build_vectorstore, load_existing_vectorstore
from src.rag import answer_question
from src.config import CHROMA_DIR, DATA_DIR

app = FastAPI(title="Intelligent Document Research Assistant API")

# Allow the React frontend (running on a different port) to call this API
origins = ["http://localhost:5173", "http://localhost:3000"]
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
if allowed_origins_env:
    origins.extend([o.strip() for o in allowed_origins_env.split(",") if o.strip()])
else:
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API is running"}

@app.get("/documents")
def list_documents():
    pdfs = glob.glob(f"{DATA_DIR}/*.pdf")
    return {"documents": [os.path.basename(p) for p in pdfs]}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs(DATA_DIR, exist_ok=True)
    save_path = os.path.join(DATA_DIR, file.filename)
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"filename": file.filename, "status": "uploaded"}

@app.post("/rebuild-index")
def rebuild_index():
    pdf_files = glob.glob(f"{DATA_DIR}/*.pdf")
    if not pdf_files:
        return {"error": "No documents found"}
    build_vectorstore(pdf_files)
    return {"status": "index rebuilt", "documents": len(pdf_files)}

@app.post("/ask")
def ask_question(payload: dict):
    query = payload.get("question")
    if not query:
        return {"error": "No question provided"}
    if not os.path.exists(CHROMA_DIR):
        return {"error": "No index found. Upload documents and rebuild index first."}

    vectorstore = load_existing_vectorstore()
    result = answer_question(vectorstore, query)
    return result

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)