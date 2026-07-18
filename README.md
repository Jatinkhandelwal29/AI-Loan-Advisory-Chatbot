# 🏦 AI Loan Advisory Chatbot

An AI-powered Loan Advisory Chatbot that allows users to upload policy PDFs, ask natural language questions, and receive accurate answers grounded in the uploaded documents using **Retrieval-Augmented Generation (RAG)**.

The application also includes a **Premium Calculator** for instant premium estimation, and a **Compare** tool to check answers across multiple documents.

> **Note:** this project's name has been set to "AI Loan Advisory Chatbot," but the underlying
> features (Premium Calculator, policy comparison) are still built around insurance-style documents,
> since that's the domain the code was implemented for. Let me know if you'd also like the internal
> feature names (e.g. Premium Calculator → EMI Calculator) relabeled to fully match loan terminology.

> Adapted from the AI Loan Advisory Chatbot concept — vector store swapped to FAISS, and the LLM swapped to Groq (Llama 3.1) with free local embeddings.

---

## 📸 Project Preview

### Chat Interface

![Chat](screenshots/chat.png)

### Premium Calculator

![Premium Calculator](screenshots/premium_calculator.png)

### Compare Policies

![Compare](screenshots/compare.png)

### Upload Policies

![Upload](screenshots/upload.png)

---

# ✨ Features

- 📄 Upload one or multiple Insurance Policy PDFs
- 🤖 AI-powered Question Answering using Groq (Llama 3.1)
- 📚 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic Search using FAISS
- 🧠 Local HuggingFace Embeddings (free, no API key needed)
- 📑 Source Citation (PDF + Page Number)
- 🧮 Premium Calculator
- 🔍 Compare Policies tool
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

- Groq API (Llama 3.1)
- LangChain
- FAISS
- HuggingFace Embeddings (sentence-transformers/all-MiniLM-L6-v2)

### PDF Processing

- PyMuPDF (fitz)

### Programming Language

- Python 3.11+

---

# 📂 Project Structure

```
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

```
git clone https://github.com/YOUR_USERNAME/AI-Loan-Advisory-Chatbot.git

cd AI-Loan-Advisory-Chatbot
```

---

## 2. Create Virtual Environment

Windows

```
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

---

# ▶️ Running the Application

## Start Backend

```
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

```
streamlit run frontend/app.py
```

Frontend

```
http://localhost:8501
```

---

# 🐳 Docker

Build

```
docker compose build
```

Run

```
docker compose up
```

Stop

```
docker compose down
```

---

# 🚀 Workflow

```
Upload PDF
      │
      ▼
Extract Text (PyMuPDF)
      │
      ▼
Chunk Documents (LangChain)
      │
      ▼
Generate Local Embeddings (HuggingFace)
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

| Method | Endpoint     | Description                        |
| ------ | ------------ | ----------------------------------- |
| GET    | `/health`    | Backend Health                     |
| POST   | `/upload`    | Upload & Index PDFs                |
| POST   | `/chat`      | Ask Questions                      |
| POST   | `/premium`   | Calculate Insurance Premium        |
| POST   | `/compare`   | Compare Answers Across Policies    |
| GET    | `/documents` | List Uploaded Documents            |
| POST   | `/reindex`   | Rebuild Vector Database            |

---

# ☁️ Deployment

## Backend on Render

1. Push this repo to your own GitHub account.
2. On [render.com](https://render.com), create a **New Web Service** and connect your repo.
3. Render auto-detects the `Dockerfile`. Choose the **Free** plan.
4. Add environment variable `GROQ_API_KEY` with your real key under **Environment**.
5. Deploy. Copy the live URL, e.g. `https://your-app.onrender.com`.
6. Verify at `https://your-app.onrender.com/health`.

## Frontend on Streamlit Community Cloud

1. On [share.streamlit.io](https://share.streamlit.io), click **New app**.
2. Select this repo, branch `main`, main file path `frontend/app.py`.
3. Under **Advanced settings → Secrets**, add:
   ```
   BACKEND_URL = "https://your-app.onrender.com"
   ```
4. Click **Deploy**.

---

# 📈 Future Improvements

- Conversation Memory
- Insurance Eligibility / Risk Pre-screening
- OCR Support for Scanned PDFs
- Voice Input
- Multilingual Support
- Admin Dashboard
- Authentication
- Multi-user Document Isolation

---

# 📄 Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Never upload your real API key to GitHub.

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork this repository and submit a pull request.

---

# 👨‍💻 Author

**Your Name Here**

Add your background, e.g.: B.Tech CSE | AI/ML | Python | FastAPI | LangChain

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://linkedin.com/in/YOUR_USERNAME

---

# ⭐ If you like this project

Please consider giving it a ⭐ on GitHub.
