# 🏥 AI Medical Assistant – GenAI Healthcare Chatbot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?logo=streamlit)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20DB-orange)
![Claude](https://img.shields.io/badge/Claude-Anthropic-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📋 Project Description

**AI Medical Assistant** is an intelligent healthcare chatbot powered by **Retrieval-Augmented Generation (RAG)**. It answers medical questions by retrieving relevant information from a curated medical knowledge base and generating grounded, context-aware responses using **Claude** (Anthropic's LLM).

Unlike generic chatbots, this assistant **does not hallucinate** — every answer is based only on the verified documents in the knowledge base, making it a trustworthy tool for general health information.

> ⚠️ **Disclaimer:** This tool is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Document Ingestion** | Load medical knowledge from `.txt` and `.pdf` files |
| 🧠 **Local Embeddings** | Uses `sentence-transformers` — no extra API key needed |
| 🔍 **FAISS Vector Search** | Fast semantic search over embedded document chunks |
| 🦜 **LangChain RAG Pipeline** | Structured retrieval + prompt engineering |
| 🤖 **Claude LLM** | Accurate, empathetic answers via Anthropic's Claude |
| 💬 **Streamlit Chat UI** | Clean, intuitive web interface with chat history |
| 📁 **Dynamic Uploads** | Add new medical documents via the sidebar |
| 🔄 **Index Rebuilding** | Rebuild the FAISS index after adding new documents |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Claude (Anthropic) via `anthropic` SDK |
| **Orchestration** | LangChain |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **UI** | Streamlit |
| **PDF Parsing** | PyPDF via LangChain |
| **Language** | Python 3.10+ |

---

## 🏗️ Project Structure

```
ai_medical_assistant/
│
├── app.py                  # Streamlit frontend — UI and user interaction
├── rag_engine.py           # Core RAG pipeline (embed → store → retrieve → generate)
├── data_loader.py          # Document loading and text chunking utilities
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md               # This file
│
├── medical_docs/           # 📁 Knowledge base — add your files here
│   ├── general_medicine.txt
│   └── medications_and_safety.txt
│
└── faiss_index/            # 📁 Auto-generated — persisted vector index
    ├── index.faiss
    └── index.pkl
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- An Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/ai-medical-assistant.git
cd ai-medical-assistant
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up your API key
```bash
cp .env.example .env
```
Open `.env` and replace the placeholder with your actual Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### Step 5 — Add medical documents (optional)
Place any `.txt` or `.pdf` medical reference files in the `medical_docs/` folder.  
Two sample files are already included to get you started.

---

## 🚀 How to Run

```bash
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**

**First launch note:** The embedding model (`all-MiniLM-L6-v2`, ~80MB) will be downloaded on first run. The FAISS index is then built and saved — subsequent launches are much faster.

---

## 💬 Example Queries

Try asking the assistant these questions:

```
What are the symptoms of Type 2 diabetes?
How is hypertension diagnosed and treated?
What is the difference between Type 1 and Type 2 diabetes?
What are the side effects of Metformin?
How do I perform CPR on an adult?
What medications are commonly used for high blood pressure?
What are dangerous drug interactions I should be aware of?
What vaccines should adults get?
What are the warning signs of a heart attack in women?
How is asthma treated?
```

---

## 🔄 Adding New Documents

1. Place new `.txt` or `.pdf` files in the `medical_docs/` folder  
   **OR** upload them directly via the sidebar in the app.

2. Click **"Rebuild Knowledge Index"** in the sidebar to re-embed the new documents.

3. The FAISS index will be updated and saved automatically.

---

## 🧠 How RAG Works (Architecture)

```
User Question
     │
     ▼
[Query Embedding]          ← sentence-transformers model
     │
     ▼
[FAISS Similarity Search]  ← finds top-5 most relevant document chunks
     │
     ▼
[Context Assembly]         ← combines retrieved chunks into a prompt
     │
     ▼
[Claude LLM]               ← generates grounded answer from context
     │
     ▼
[Streamlit UI]             ← displays answer + sources to user
```

**Why RAG instead of fine-tuning?**
- ✅ No expensive GPU training required
- ✅ Knowledge base can be updated without retraining
- ✅ Answers are grounded — no hallucinations from irrelevant data
- ✅ Sources are transparent and auditable

---

## 🔐 Security Notes

- Never commit your `.env` file to version control (it's already in `.gitignore`).
- The app does not store any user queries or personal health data.
- API calls to Anthropic are subject to their [privacy policy](https://www.anthropic.com/privacy).

---

## 📈 Future Improvements

- [ ] Add multi-language support
- [ ] Integrate real-time medical databases (PubMed, WHO)
- [ ] Add symptom checker decision tree
- [ ] Implement user authentication
- [ ] Deploy to cloud (AWS / GCP / Streamlit Cloud)
- [ ] Add voice input/output
- [ ] Support for DICOM/medical imaging analysis

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

Built as an AI portfolio project demonstrating RAG, vector databases, and LLM integration for healthcare applications.

---

*⭐ If you found this useful, please star the repository!*
