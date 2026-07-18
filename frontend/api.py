import os
import requests
import streamlit as st

# Resolution order for the backend URL:
# 1. Streamlit secrets (set on Streamlit Community Cloud)
# 2. Environment variable (set locally or in Docker)
# 3. Local FastAPI default (for local dev)
def get_backend_url() -> str:
    try:
        if "BACKEND_URL" in st.secrets:
            return st.secrets["BACKEND_URL"].rstrip("/")
    except Exception:
        pass
    return os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


BASE_URL = get_backend_url()


def check_health():
    resp = requests.get(f"{BASE_URL}/health", timeout=15)
    resp.raise_for_status()
    return resp.json()


def upload_documents(files):
    """files: list of (filename, bytes, content_type) tuples from Streamlit uploader."""
    multipart = [("files", (name, data, "application/pdf")) for name, data in files]
    resp = requests.post(f"{BASE_URL}/upload", files=multipart, timeout=120)
    resp.raise_for_status()
    return resp.json()


def ask_question(question: str):
    resp = requests.post(f"{BASE_URL}/chat", json={"question": question}, timeout=60)
    resp.raise_for_status()
    return resp.json()


def get_premium(age, sum_assured, term_years, plan_type, smoker):
    payload = {
        "age": age,
        "sum_assured": sum_assured,
        "term_years": term_years,
        "plan_type": plan_type,
        "smoker": smoker,
    }
    resp = requests.post(f"{BASE_URL}/premium", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def compare_questions(questions):
    resp = requests.post(f"{BASE_URL}/compare", json={"questions": questions}, timeout=90)
    resp.raise_for_status()
    return resp.json()


def list_documents():
    resp = requests.get(f"{BASE_URL}/documents", timeout=15)
    resp.raise_for_status()
    return resp.json()


def reindex():
    resp = requests.post(f"{BASE_URL}/reindex", timeout=120)
    resp.raise_for_status()
    return resp.json()
