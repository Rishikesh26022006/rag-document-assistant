import streamlit as st
import glob
import os
from src.ingest import build_vectorstore, load_existing_vectorstore
from src.rag import answer_question
from src.config import CHROMA_DIR, DATA_DIR

st.set_page_config(page_title="Intelligent Document Research Assistant", layout="wide")
st.title("📄 Intelligent Document Research Assistant")
st.caption("Ask questions about your documents, grounded in RAG (Retrieval-Augmented Generation)")

# Sidebar: upload + index management
with st.sidebar:
    st.header("Documents")
    uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        os.makedirs(DATA_DIR, exist_ok=True)
        for file in uploaded_files:
            save_path = os.path.join(DATA_DIR, file.name)
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"Saved {len(uploaded_files)} file(s)")

    if st.button("🔄 Rebuild Index"):
        with st.spinner("Building vector store..."):
            pdf_files = glob.glob(f"{DATA_DIR}/*.pdf")
            build_vectorstore(pdf_files)
        st.success("Index rebuilt!")

    existing_pdfs = glob.glob(f"{DATA_DIR}/*.pdf")
    st.write("Current documents:")
    for pdf in existing_pdfs:
        st.write(f"- {os.path.basename(pdf)}")

# Main area: Q&A
st.divider()
query = st.text_input("Ask a question about your documents:")

if query:
    if not os.path.exists(CHROMA_DIR):
        st.error("No index found. Please upload documents and click 'Rebuild Index' first.")
    else:
        with st.spinner("Thinking..."):
            vectorstore = load_existing_vectorstore()
            result = answer_question(vectorstore, query)

        st.subheader("Answer")
        st.write(result["answer"])

        with st.expander("📚 Sources used"):
            for src in set(result["sources"]):
                st.write(f"- {src}")

        with st.expander("🔍 Retrieved context (for debugging)"):
            st.text(result["context_used"])