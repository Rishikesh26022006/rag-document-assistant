import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings


from src.config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, CHROMA_DIR, DATA_DIR

def load_and_chunk(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    return chunks

def build_vectorstore(file_paths):
    """Takes a list of PDF paths, chunks them all, embeds, and stores in ChromaDB."""
    all_chunks = []
    for path in file_paths:
        chunks = load_and_chunk(path)
        all_chunks.extend(chunks)
        print(f"Loaded {len(chunks)} chunks from {os.path.basename(path)}")

    embeddings = HuggingFaceEndpointEmbeddings(
        model=EMBEDDING_MODEL,
        huggingfacehub_api_token=os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    vectorstore = Chroma.from_documents(
        all_chunks, embeddings, persist_directory=CHROMA_DIR
    )
    print(f"Vector store built with {len(all_chunks)} total chunks")
    return vectorstore

def load_existing_vectorstore():
    """Loads a previously-built vectorstore instead of rebuilding from scratch."""
    embeddings = HuggingFaceEndpointEmbeddings(
        model=EMBEDDING_MODEL,
        huggingfacehub_api_token=os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)