# 🛡️ AI Loan Advisory Chatbot

A RAG-powered chatbot that answers questions about **insurance policy PDFs** you upload, plus a
**premium calculator** and a **policy comparison** tool.

This project is a variant of a Loan Advisory Chatbot pattern, adapted with a few changes:

|               | Original Loan idea             | This project                                |
| ------------- | ------------------------------ | ------------------------------------------- |
| Domain        | Loan policies + EMI calculator | Insurance policies + Premium calculator     |
| Vector store  | ChromaDB                       | FAISS                                       |
| Embeddings    | Google Gemini embeddings       | Local HuggingFace embeddings (free, no key) |
| LLM           | Google Gemini                  | Groq (Llama 3.1, very fast inference)       |
| Extra feature | —                              | `/compare` endpoint + Compare tab in UI     |

---

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **Frontend:** Streamlit
- **LLM:** Groq API (`llama-3.1-8b-instant`)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (runs locally, free)
- **Vector store:** FAISS
- **PDF parsing:** PyMuPDF

## Project Structure

```
AI-Loan-Advisory-Chatbot
├── backend
│   ├── config.py
│   ├── models.py
│   ├── pdf_processor.py
│   ├── rag.py
│   ├── insurance_utils.py
│   ├── chatbot.py
│   └── main.py
├── frontend
│   ├── app.py
│   └── api.py
├── documents/
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── .env.example
└── .gitignore
```

## API Endpoints

| Method | Endpoint     | Description                       |
| ------ | ------------ | --------------------------------- |
| GET    | `/health`    | Backend health check              |
| POST   | `/upload`    | Upload & index PDFs               |
| POST   | `/chat`      | Ask a question                    |
| POST   | `/premium`   | Estimate insurance premium        |
| POST   | `/compare`   | Ask same question across policies |
| GET    | `/documents` | List uploaded documents           |
| POST   | `/reindex`   | Rebuild vector index from scratch |

---

## 🔑 Get a Groq API Key

1. Go to https://console.groq.com/keys
2. Sign in and click **Create API Key**.
3. Copy it — you'll paste it into `.env` (local) and into Render's dashboard (deployed).
   **Never commit this key to GitHub.**

---

## 💻 Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/AI-Insurance-Advisor-Chatbot.git
cd AI-Insurance-Advisor-Chatbot

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# open .env and paste your real GROQ_API_KEY

# Terminal 1 — backend
uvicorn backend.main:app --reload
# → http://127.0.0.1:8000/docs

# Terminal 2 — frontend
cd frontend
streamlit run app.py
# → http://localhost:8501
```

---

## 🚀 Step-by-Step: Deploy Backend on Render

1. **Push this project to your own GitHub repo** (make sure `.env` is in `.gitignore` — it already is).

2. **Sign in to Render:** https://render.com → sign up/login with GitHub.

3. **Create a new Web Service:**
   - Dashboard → **New +** → **Web Service**
   - Connect your GitHub account and select your repo.

4. **Configure the service:**
   - **Name:** `ai-insurance-advisor-backend`
   - **Runtime:** Docker (Render auto-detects the `Dockerfile` at the repo root)
   - **Region:** closest to you
   - **Instance type:** Free (fine for testing)

5. **Add the environment variable:**
   - Under **Environment** → **Add Environment Variable**
   - Key: `GROQ_API_KEY`
   - Value: _your real Groq key_ (paste it here, not in any file)

6. **Deploy:** click **Create Web Service**. Render will build the Docker image and start the container.
   Wait for the log to show `Uvicorn running on http://0.0.0.0:8000`.

7. **Copy your live backend URL**, shown at the top of the Render dashboard, e.g.:

   ```
   https://ai-insurance-advisor-backend.onrender.com
   ```

8. **Verify it's working:** open `https://ai-insurance-advisor-backend.onrender.com/health`
   in your browser — you should see `{"status": "ok", ...}`.
   You can also browse the interactive API docs at `/docs`.

> **Free tier note:** Render's free web services spin down after ~15 minutes of inactivity
> and take ~30–60 seconds to "wake up" on the next request. This is normal, not a bug.

---

## 🚀 Step-by-Step: Deploy Frontend on Streamlit Community Cloud

1. Make sure your GitHub repo (same one) also contains `frontend/app.py`, `frontend/api.py`,
   and `requirements.txt` at the root.

2. **Go to** https://share.streamlit.io → sign in with GitHub.

3. **Click "New app"**:
   - **Repository:** select your `AI-Insurance-Advisor-Chatbot` repo
   - **Branch:** `main`
   - **Main file path:** `frontend/app.py`

4. **Before deploying, open "Advanced settings" → Secrets**, and add:

   ```toml
   BACKEND_URL = "https://ai-insurance-advisor-backend.onrender.com"
   ```

   (Use the exact Render URL you copied earlier, no trailing slash.)

5. Click **Deploy**. Streamlit installs `requirements.txt` and starts your app.

6. Once live, your app URL will look like:

   ```
   https://your-app-name.streamlit.app
   ```

7. **Test it end-to-end:**
   - Upload a sample insurance PDF in the "Upload Policies" tab.
   - Ask a question in the "Chat" tab.
   - Try the Premium Calculator tab.

### If something doesn't connect

- Check the Render service logs for errors (missing `GROQ_API_KEY` is the most common one).
- Confirm the `BACKEND_URL` secret in Streamlit exactly matches your Render URL (https, no trailing slash).
- Remember the free Render instance may need ~30–60s to wake up on first request after idling.

---

## Security Notes

- `GROQ_API_KEY` is read from environment variables only — it is never hardcoded in source.
- `.env`, `faiss_index/`, and uploaded PDFs are git-ignored so secrets and user data aren't committed.
- If a real key is ever pasted into a chat, commit, or shared file by mistake, **rotate it immediately**
  from the Groq console — treat it as compromised.

---

## Future Improvements

- Conversation memory across turns
- Insurance eligibility / risk pre-screening
- OCR support for scanned PDFs
- Multilingual Q&A
- User authentication for multi-user document isolation
