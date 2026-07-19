import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
# Never hardcode real keys here. Set GROQ_API_KEY in a local .env file
# (which is git-ignored) or as an environment variable / secret on your
# hosting platform (Render, Streamlit Cloud, etc).
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "documents")
INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# --- RAG settings ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# Local, free embedding model (no API key needed) run via sentence-transformers.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Groq-hosted Llama model for answer generation.
LLM_MODEL = "llama-3.1-8b-instant"

TOP_K = 4

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not set. Set it in your .env file or environment variables.")
