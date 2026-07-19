# 🏦 AI Loan Advisory Chatbot

An AI-powered chatbot that allows users to upload policy PDFs, ask natural language questions, and receive accurate answers grounded in the uploaded documents using **Retrieval-Augmented Generation (RAG)**.

The application also includes a **Premium Calculator** for instant premium estimation, and a **Compare** tool to check answers across multiple uploaded documents.

🔗 **Live Demo:** https://ai-loan-advisory-chatbot-jrvuyaazfpvunn8jibwxhm.streamlit.app/

> Note: the backend runs on Render's free tier, so it may take 30–60 seconds to wake up on the first request after a period of inactivity.

---

## 📸 Project Preview

### Chat Interface

[![Chat](screenshots/chat.png)](https://github.com/Jatinkhandelwal29/AI-Loan-Advisory-Chatbot/blob/20b1e8d22ed9962489e9d9a554704d977973e517/Screenshot%202026-07-19%20011603.png)

### Premium Calculator

https://github.com/Jatinkhandelwal29/AI-Loan-Advisory-Chatbot/blob/04f8eda138ce1b238e64f6cc0fa14504d25ee53a/Screenshot%202026-07-19%20011620.png

### Compare Policies

![Compare](screenshots/compare.png)

### Upload Policies

![Upload](screenshots/upload.png)

---

# ✨ Features

- 📄 Upload one or multiple policy PDFs
- 🤖 AI-powered Question Answering using Groq (Llama 3.1)
- 📚 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic Search using FAISS
- 🧠 Lightweight local embeddings via fastembed (ONNX, no PyTorch, no API key)
- 📑 Source Citation (PDF + Page Number)
- 🧮 Premium Calculator
- 🔍 Compare tool — ask the same question across multiple uploaded documents
- 💬 Interactive Chat Interface
- ⚡ FastAPI Backend
- 🎨 Streamlit Frontend
- 🐳 Docker Support
- 🔒 Environment Variable Support (.env)

---

# 🛠 Tech Stack

### Frontend

- Streamlit

### Backend

- FastAPI
- Uvicorn

### AI & RAG

- Groq API (`llama-3.1-8b-instant`)
- LangChain
- FAISS
- fastembed (`BAAI/bge-small-en-v1.5`, ONNX-based, runs locally — no API key, low memory)

### PDF Processing

- PyMuPDF (fitz)

### Programming Language

- Python 3.11+

---

# 📂 Project Structure

```text
AI-Loan-Advisory-Chatbot
│
├── backend
│   ├── chatbot.py
│   ├── config.py
│   ├── insurance_utils.py
│   ├── main.py
│   ├── models.py
│   ├── pdf_processor.py
│   └── rag.py
│
├── frontend
│   ├── app.py
│   ├── api.py
│   └── __init__.py
│
├── documents
├── faiss_index
├── screenshots
│
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Loan-Advisory-Chatbot.git

cd AI-Loan-Advisory-Chatbot
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Get a free Groq API key at https://console.groq.com/keys

---

# ▶️ Running the Application

## Start Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

Swagger API

```
http://127.0.0.1:8000/docs
```

---

## Start Frontend

Open another terminal

```bash
streamlit run frontend/app.py
```

Frontend

```
http://localhost:8501
```

---

# 🐳 Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

Stop

```bash
docker compose down
```

---

# 🚀 Workflow

```text
Upload PDF
      │
      ▼
Extract Text (PyMuPDF)
      │
      ▼
Chunk Documents (LangChain)
      │
      ▼
Generate Local Embeddings (fastembed / ONNX)
      │
      ▼
Store in FAISS
      │
      ▼
Semantic Retrieval
      │
      ▼
Groq LLM (Llama 3.1)
      │
      ▼
Answer + Source Citation
```

---

# 📚 API Endpoints

| Method | Endpoint     | Description                      |
| ------ | ------------ | -------------------------------- |
| GET    | `/health`    | Backend Health                   |
| POST   | `/upload`    | Upload & Index PDFs              |
| POST   | `/chat`      | Ask Questions                    |
| POST   | `/premium`   | Calculate Premium                |
| POST   | `/compare`   | Compare Answers Across Documents |
| GET    | `/documents` | List Uploaded Documents          |
| POST   | `/reindex`   | Rebuild Vector Database          |

---

# ☁️ Deployment

## Backend on Render

1. Push this repo to your own GitHub account.
2. On [render.com](https://render.com), create a **New Web Service** and connect your repo.
3. Render auto-detects the `Dockerfile`. Choose the **Free** plan.
4. Add environment variable `GROQ_API_KEY` with your real key under **Environment**.
5. Deploy. Copy the live URL, e.g. `https://ai-loan-advisory-chatbot-backend.onrender.com`.
6. Verify at `https://ai-loan-advisory-chatbot-backend.onrender.com/health`.

## Frontend on Streamlit Community Cloud

1. On [share.streamlit.io](https://share.streamlit.io), click **New app**.
2. Select this repo, branch `main`, main file path `frontend/app.py`.
3. Under **Advanced settings → Secrets**, add:
   ```toml
   BACKEND_URL = "https://ai-loan-advisory-chatbot-backend.onrender.com"
   ```
4. Click **Deploy**.

---

# 📈 Future Improvements

- Conversation Memory
- Eligibility / Risk Pre-screening
- OCR Support for Scanned PDFs
- Voice Input
- Multilingual Support
- Admin Dashboard
- Authentication
- Multi-user Document Isolation

---

# 📄 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Never upload your real API key to GitHub.

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork this repository and submit a pull request.

---

# 👨‍💻 Author

**JATIN KHANDELWAL**

Add your background, e.g.: B.Tech CSE | AI/ML | Python | FastAPI | LangChain

GitHub: https://github.com/Jatinkhandelwal29

LinkedIn: www.linkedin.com/in/khandelwal-jatin

---

# ⭐ If you like this project

Please consider giving it a ⭐ on GitHub.
