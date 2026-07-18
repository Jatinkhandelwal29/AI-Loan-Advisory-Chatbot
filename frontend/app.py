import streamlit as st
from api import (
    check_health, upload_documents, ask_question,
    get_premium, compare_questions, list_documents, reindex, BASE_URL,
)

st.set_page_config(page_title="AI Loan Advisory Chatbot", page_icon="🛡️", layout="wide")

st.title("🛡️ AI Loan Advisor Chatbot")
st.caption(f"Connected backend: {BASE_URL}")

tab_chat, tab_upload, tab_premium, tab_compare = st.tabs(
    ["💬 Chat", "📄 Upload Policies", "🧮 Premium Calculator", "🔍 Compare"]
)

# --- Chat tab ---
with tab_chat:
    st.subheader("Ask about your insurance policy")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a question about your uploaded policy documents...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = ask_question(question)
                    st.markdown(result["answer"])
                    if result.get("sources"):
                        with st.expander("📚 Sources"):
                            for s in result["sources"]:
                                st.markdown(f"**{s['document']}** (page {s.get('page', '?')})")
                                st.caption(s["snippet"])
                    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
                except Exception as e:
                    st.error(f"Error reaching backend: {e}")

# --- Upload tab ---
with tab_upload:
    st.subheader("Upload policy PDFs")
    uploaded_files = st.file_uploader("Choose PDF file(s)", type=["pdf"], accept_multiple_files=True)

    if st.button("Upload & Index", type="primary", disabled=not uploaded_files):
        files_payload = [(f.name, f.getvalue()) for f in uploaded_files]
        with st.spinner("Uploading and indexing..."):
            try:
                result = upload_documents(files_payload)
                st.success(result["message"])
                for doc in result["documents"]:
                    st.write(f"- **{doc['filename']}** → {doc['chunks_indexed']} chunks indexed")
            except Exception as e:
                st.error(f"Upload failed: {e}")

    st.divider()
    st.write("**Indexed documents**")
    try:
        docs = list_documents()
        if docs["documents"]:
            for d in docs["documents"]:
                st.write(f"- {d}")
        else:
            st.info("No documents uploaded yet.")
    except Exception as e:
        st.warning(f"Could not fetch document list: {e}")

    if st.button("🔄 Rebuild index from all documents"):
        with st.spinner("Reindexing..."):
            try:
                result = reindex()
                st.success(result["message"])
            except Exception as e:
                st.error(f"Reindex failed: {e}")

# --- Premium calculator tab ---
with tab_premium:
    st.subheader("Estimate your insurance premium")
    st.caption("Illustrative estimate only — not a real quote.")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=99, value=30)
        sum_assured = st.number_input("Sum assured (₹)", min_value=100000, value=1000000, step=50000)
    with col2:
        term_years = st.number_input("Policy term (years)", min_value=1, max_value=40, value=15)
        plan_type = st.selectbox("Plan type", ["term", "endowment", "health"])
        smoker = st.checkbox("Smoker")

    if st.button("Calculate Premium", type="primary"):
        with st.spinner("Calculating..."):
            try:
                result = get_premium(age, sum_assured, term_years, plan_type, smoker)
                st.metric("Estimated Annual Premium", f"₹{result['estimated_annual_premium']:,.2f}")
                st.metric("Estimated Monthly Premium", f"₹{result['estimated_monthly_premium']:,.2f}")
                with st.expander("Breakdown"):
                    st.json(result["breakdown"])
            except Exception as e:
                st.error(f"Calculation failed: {e}")

# --- Compare tab ---
with tab_compare:
    st.subheader("Compare answers across your uploaded policies")
    st.caption("Useful when you've uploaded multiple policy documents and want the same question answered against each.")

    q1 = st.text_input("Question", value="What is the claim settlement process?")
    n = st.slider("How many times to ask (e.g. once per policy loaded)", 1, 5, 2)

    if st.button("Run Comparison", type="primary"):
        with st.spinner("Comparing..."):
            try:
                result = compare_questions([q1] * n)
                for i, item in enumerate(result["comparison"], start=1):
                    st.markdown(f"**Result {i}:**")
                    st.write(item["answer"])
                    st.divider()
            except Exception as e:
                st.error(f"Comparison failed: {e}")
