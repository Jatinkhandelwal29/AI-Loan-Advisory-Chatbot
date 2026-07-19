import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "documents")
INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

LLM_MODEL = "llama-3.1-8b-instant"

TOP_K = 4

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not set. Set it in your .env file or environment variables.")
