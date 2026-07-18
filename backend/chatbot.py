from langchain_groq import ChatGroq

from backend.config import GROQ_API_KEY, LLM_MODEL
from backend.rag import get_relevant_chunks

_llm = ChatGroq(
    model=LLM_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0.2,
)

PROMPT_TEMPLATE = """You are an AI Loan Advisor. Answer the user's question
ONLY using the context below, which comes from uploaded insurance policy documents.
If the answer is not contained in the context, say you don't have enough information
in the uploaded documents and suggest the user upload the relevant policy document.

Context:
{context}

Question: {question}

Give a clear, concise answer in plain language suitable for a non-expert customer.
"""


def answer_question(question: str):
    chunks = get_relevant_chunks(question)

    if not chunks:
        return {
            "answer": "I don't have any indexed policy documents yet. Please upload a policy PDF first.",
            "sources": [],
        }

    context = "\n\n".join(
        f"[{c.metadata.get('source')} - page {c.metadata.get('page')}]\n{c.page_content}"
        for c in chunks
    )

    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    response = _llm.invoke(prompt)

    sources = [
        {
            "document": c.metadata.get("source", "unknown"),
            "page": c.metadata.get("page"),
            "snippet": c.page_content[:220],
        }
        for c in chunks
    ]

    return {"answer": response.content, "sources": sources}
