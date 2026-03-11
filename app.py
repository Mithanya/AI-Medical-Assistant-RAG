"""
app.py
------
Streamlit web interface for the AI Medical Assistant.
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv(override=True)

import streamlit as st

st.set_page_config(
    page_title="AI Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a6b4a, #2e9e70);
        color: white;
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .main-header h1 { margin: 0; font-size: 1.9rem; }
    .main-header p  { margin: 4px 0 0; opacity: 0.88; font-size: 0.95rem; }
    .answer-box {
        background: #f0faf5;
        border-left: 4px solid #2e9e70;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 12px 0;
    }
    .disclaimer {
        background: #fff8e1;
        border-left: 4px solid #f9a825;
        padding: 10px 16px;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #5d4037;
        margin-top: 12px;
    }
    .example-pill {
        display: inline-block;
        background: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #a5d6a7;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.82rem;
        margin: 3px;
    }
    .user-msg {
        background: #e3f2fd;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        font-weight: 500;
    }
    .bot-msg {
        background: #f1f8e9;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="🔬 Loading AI Medical Assistant... (first load may take ~30s)")
def get_rag_engine(api_key: str):
    os.environ["GROQ_API_KEY"] = api_key
    from rag_engine import MedicalRAGEngine
    return MedicalRAGEngine()


with st.sidebar:
    st.image("https://img.icons8.com/color/96/caduceus.png", width=70)
    st.title("⚙️ Settings")
    st.markdown("---")

    st.subheader("🔑 API Configuration")
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Leave blank to use GROQ_API_KEY from .env file",
    )

    active_api_key = api_key_input.strip() if api_key_input.strip() else os.environ.get("GROQ_API_KEY", "")

    if active_api_key:
        st.success("✅ API key loaded.")
    else:
        st.error("❌ No API key found. Add to .env or enter above.")

    st.markdown("---")

    st.subheader("📄 Upload Medical Documents")
    uploaded_files = st.file_uploader(
        "Add .txt or .pdf files to the knowledge base",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        os.makedirs("medical_docs", exist_ok=True)
        saved = []
        for f in uploaded_files:
            save_path = os.path.join("medical_docs", f.name)
            with open(save_path, "wb") as out:
                out.write(f.getbuffer())
            saved.append(f.name)
        st.success(f"✅ Saved: {', '.join(saved)}")

        if st.button("🔄 Rebuild Knowledge Index"):
            with st.spinner("Rebuilding FAISS index..."):
                try:
                    engine = get_rag_engine(active_api_key)
                    engine.rebuild_index()
                    st.cache_resource.clear()
                    st.success("✅ Index rebuilt! Refresh the page.")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    st.subheader("ℹ️ About")
    st.markdown("""
    **AI Medical Assistant** uses RAG (Retrieval-Augmented Generation) to answer medical questions 
    grounded in a curated knowledge base.

    **Tech Stack:**
    - 🤖 Groq (Llama 3.3)
    - 🔍 FAISS Vector DB
    - 🧠 HuggingFace Embeddings
    - 🦜 LangChain
    - 🌐 Streamlit

    ---
    ⚠️ *For informational purposes only. Always consult a qualified healthcare provider.*
    """)


st.markdown("""
<div class="main-header">
    <h1>🏥 AI Medical Assistant</h1>
    <p>Ask medical questions and receive AI-generated answers grounded in medical literature.</p>
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("**💡 Example questions you can ask:**")
example_queries = [
    "What are the symptoms of diabetes?",
    "How is hypertension treated?",
    "What is the difference between Type 1 and Type 2 diabetes?",
    "What medications are used for high blood pressure?",
    "What are the side effects of Metformin?",
    "How do I perform CPR?",
    "What are common drug interactions I should know about?",
]
st.markdown(" ".join([f'<span class="example-pill">{q}</span>' for q in example_queries]), unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([5, 1])
with col1:
    user_query = st.text_input(
        "Ask a medical question:",
        placeholder="e.g., What are the early signs of a heart attack?",
        key="query_input",
        label_visibility="collapsed",
    )
with col2:
    ask_button = st.button("🔍 Ask", use_container_width=True, type="primary")

if ask_button and user_query.strip():
    if not active_api_key:
        st.error("❌ Please provide your Groq API key in the sidebar or .env file.")
    else:
        with st.spinner("🤔 Analyzing medical knowledge base..."):
            try:
                engine = get_rag_engine(active_api_key)
                result = engine.generate_answer(user_query.strip())
                st.session_state.chat_history.append({
                    "question": user_query.strip(),
                    "answer": result["answer"],
                    "sources": result["sources"],
                    "chunks": result["context_chunks"],
                })
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                logger.error(f"App error: {e}")

elif ask_button and not user_query.strip():
    st.warning("⚠️ Please enter a question before clicking Ask.")

if st.session_state.chat_history:
    latest = st.session_state.chat_history[-1]

    st.markdown("### 🩺 Answer")
    st.markdown(f'<div class="answer-box">{latest["answer"]}</div>', unsafe_allow_html=True)

    if latest["sources"]:
        st.markdown(f"📚 **Sources used:** `{'` | `'.join(latest['sources'])}`")

    with st.expander("🔍 View Retrieved Context Chunks", expanded=False):
        for i, chunk in enumerate(latest["chunks"], 1):
            st.markdown(f"**Chunk {i}:**")
            st.text(chunk[:600] + ("..." if len(chunk) > 600 else ""))
            st.markdown("---")

    st.markdown("""
    <div class="disclaimer">
    ⚠️ <strong>Medical Disclaimer:</strong> This information is for educational purposes only and is not a substitute 
    for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider 
    for personal medical concerns.
    </div>
    """, unsafe_allow_html=True)

    if len(st.session_state.chat_history) > 1:
        st.markdown("---")
        st.markdown("### 💬 Conversation History")
        for entry in reversed(st.session_state.chat_history[:-1]):
            with st.expander(f"Q: {entry['question'][:80]}...", expanded=False):
                st.markdown(f'<div class="user-msg">🧑 {entry["question"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="bot-msg">🤖 {entry["answer"]}</div>', unsafe_allow_html=True)

        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.rerun()

else:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px; color: #666;">
        <div style="font-size: 4rem">🏥</div>
        <h3>Welcome to the AI Medical Assistant</h3>
        <p>Type a medical question above and click <strong>Ask</strong> to get started.</p>
        <p style="font-size:0.85rem;">Powered by Groq + RAG + FAISS</p>
    </div>
    """, unsafe_allow_html=True)