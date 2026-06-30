from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL, TOP_K

client = Groq(api_key=GROQ_API_KEY)

def answer_question(vectorstore, query, k=TOP_K):
    results = vectorstore.similarity_search(query, k=k)
    context = "\n\n".join([doc.page_content for doc in results])
    sources = [doc.metadata.get("source", "unknown") for doc in results]

    prompt = f"""You are answering questions based on the document context below. Be direct and specific. If the context contains relevant information, use it confidently to answer. Only say you don't have enough information if the context truly doesn't address the question.

Context:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources,
        "context_used": context
    }