from src.ingest import load_existing_vectorstore
from src.rag import answer_question

vectorstore = load_existing_vectorstore()

query = input("Ask a question: ")
result = answer_question(vectorstore, query)

print("\nAnswer:", result["answer"])
print("\nSources:", result["sources"])