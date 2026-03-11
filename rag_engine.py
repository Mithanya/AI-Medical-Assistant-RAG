import os
import logging
from typing import Optional, List
from groq import Groq

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from data_loader import load_and_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX_PATH = "faiss_index"
DATA_DIR = "medical_docs"
TOP_K_RESULTS = 5

SYSTEM_PROMPT = """You are a knowledgeable and empathetic AI Medical Assistant. 
Answer based ONLY on the context provided. Use clear, simple language.
Always recommend consulting a qualified healthcare professional for personal medical advice.
"""

class MedicalRAGEngine:
    def __init__(self):
        self.embeddings: Optional[HuggingFaceEmbeddings] = None
        self.vectorstore: Optional[FAISS] = None
        self.client = None
        self._initialize()

    def _initialize(self):
        logger.info("Initializing Medical RAG Engine...")
        self._load_embedding_model()
        if os.path.exists(FAISS_INDEX_PATH):
            self._load_vectorstore()
        else:
            self._build_vectorstore()
        self._init_llm_client()
        logger.info("RAG Engine initialized successfully.")

    def _load_embedding_model(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def _build_vectorstore(self):
        chunks = load_and_split(DATA_DIR)
        if not chunks:
            raise ValueError(f"No document chunks found in '{DATA_DIR}'.")
        self.vectorstore = FAISS.from_documents(documents=chunks, embedding=self.embeddings)
        self.vectorstore.save_local(FAISS_INDEX_PATH)

    def _load_vectorstore(self):
        try:
            self.vectorstore = FAISS.load_local(
                FAISS_INDEX_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            logger.warning(f"Failed to load FAISS index: {e}. Rebuilding...")
            self._build_vectorstore()

    def _init_llm_client(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY not found.")
        else:
            logger.info(f"GROQ_API_KEY loaded: {api_key[:8]}...")
        self.client = Groq(api_key=api_key)
        logger.info("Groq client initialized.")

    def retrieve_context(self, query: str, k: int = TOP_K_RESULTS) -> List[Document]:
        if not self.vectorstore:
            raise ValueError("Vector store not initialized.")
        return self.vectorstore.similarity_search(query, k=k)

    def generate_answer(self, query: str) -> dict:
        relevant_docs = self.retrieve_context(query)
        if not relevant_docs:
            return {"answer": "No relevant info found. Consult a doctor.", "sources": [], "context_chunks": []}

        context_text = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
        sources = list({os.path.basename(doc.metadata.get("source", "Unknown")) for doc in relevant_docs})

        user_prompt = f"""QUESTION: {query}

MEDICAL CONTEXT:
{context_text}

Please provide a clear, accurate answer based only on the above context.
"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=1024,
            )
            answer = response.choices[0].message.content

        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                answer = "⚠️ Rate limit hit. Wait a moment and try again."
            elif "api_key" in error_msg.lower() or "auth" in error_msg.lower():
                answer = "❌ Invalid Groq API key. Check your .env file."
            else:
                answer = f"❌ Error: {error_msg}"
            logger.error(f"Groq error: {e}")

        return {
            "answer": answer,
            "sources": sources,
            "context_chunks": [doc.page_content for doc in relevant_docs],
        }

    def rebuild_index(self):
        import shutil
        if os.path.exists(FAISS_INDEX_PATH):
            shutil.rmtree(FAISS_INDEX_PATH)
        self._build_vectorstore()