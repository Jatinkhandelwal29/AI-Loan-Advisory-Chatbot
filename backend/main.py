import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import DOCS_DIR
from backend.models import (
    ChatRequest, ChatResponse,
    PremiumRequest, PremiumResponse,
    CompareRequest, CompareResponse,
    UploadResponse, DocumentInfo,
)
from backend.pdf_processor import chunk_pdf
from backend.rag import build_or_update_index, rebuild_index_from_scratch, index_is_ready
from backend.chatbot import answer_question
from backend.insurance_utils import calculate_premium

app = FastAPI(
    title="AI Loan Advisory Chatbot",
    description="RAG-powered API for answering insurance policy questions and estimating premiums.",
    version="1.0.0",
)

# Allow the Streamlit frontend (any origin) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "index_ready": index_is_ready()}


@app.post("/upload", response_model=UploadResponse)
async def upload_documents(files: list[UploadFile] = File(...)):
    doc_infos = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"{file.filename} is not a PDF")

        save_path = os.path.join(DOCS_DIR, file.filename)
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        chunks = chunk_pdf(save_path, file.filename)
        build_or_update_index(chunks)
        doc_infos.append(DocumentInfo(filename=file.filename, chunks_indexed=len(chunks)))

    return UploadResponse(message="Documents uploaded and indexed successfully", documents=doc_infos)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = answer_question(request.question)
    return ChatResponse(**result)


@app.post("/premium", response_model=PremiumResponse)
def premium(request: PremiumRequest):
    result = calculate_premium(
        age=request.age,
        sum_assured=request.sum_assured,
        term_years=request.term_years,
        plan_type=request.plan_type,
        smoker=request.smoker,
    )
    return PremiumResponse(**result)


@app.post("/compare", response_model=CompareResponse)
def compare(request: CompareRequest):
    """Ask the same question(s) and return grounded answers side by side, useful for comparing policies."""
    results = [ChatResponse(**answer_question(q)) for q in request.questions]
    return CompareResponse(comparison=results)


@app.get("/documents")
def list_documents():
    files = [f for f in os.listdir(DOCS_DIR) if f.lower().endswith(".pdf")]
    return {"documents": files, "count": len(files)}


@app.post("/reindex")
def reindex():
    all_docs = []
    files = [f for f in os.listdir(DOCS_DIR) if f.lower().endswith(".pdf")]
    if not files:
        raise HTTPException(status_code=400, detail="No documents found to reindex")

    for filename in files:
        path = os.path.join(DOCS_DIR, filename)
        all_docs.extend(chunk_pdf(path, filename))

    rebuild_index_from_scratch(all_docs)
    return {"message": f"Reindexed {len(files)} documents into {len(all_docs)} chunks"}
