import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq

# Step 1: Load environment variables (your API key)
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Step 2: Load the PDF
loader = PyPDFLoader("data/sample_document.pdf")  # replace with your actual filename
documents = loader.load()
print(f"Loaded {len(documents)} pages")

# Step 3: Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks")

# Step 4: Create embeddings and store in ChromaDB
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
print("Vector store created")

# Step 5: Function to answer a question
def answer_question(query):
    results = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in results])

    prompt = f"""Answer the question based only on the context below. If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {query}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Step 6: Test it
if __name__ == "__main__":
    question = input("Ask a question about your document: ")
    answer = answer_question(question)
    print("\nAnswer:", answer)