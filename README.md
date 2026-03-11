# 🏥 AI Medical Assistant – RAG Healthcare Chatbot

An **AI-powered Medical Question Answering System** built using **Retrieval-Augmented Generation (RAG)**.
The system retrieves relevant information from medical documents and generates reliable answers using an AI model.

⚠️ *This project is for educational purposes only and does not replace professional medical advice.*

---

## 📸 Project Demo

![Demo](Screenshot 2026-03-11 174048.png)

![Demo](Screenshot 2026-03-11 174204.png)

![Demo](Screenshot 2026-03-11 174238.png)

---

## 🚀 Features

* Ask medical-related questions
* Upload medical documents (PDF / TXT)
* AI answers grounded in medical knowledge
* Retrieval-Augmented Generation (RAG) pipeline
* Source citation for reliable responses
* Interactive web interface using Streamlit

---

## 🧠 How It Works

1. User asks a medical question
2. Question is converted into embeddings
3. FAISS vector database retrieves relevant document chunks
4. Context is sent to the AI model
5. AI generates an answer based on retrieved knowledge

This reduces hallucination and improves answer reliability.

---

## 🛠 Tech Stack

* Python
* Streamlit
* LangChain
* FAISS Vector Database
* HuggingFace Embeddings
* Claude API

---

## 📂 Project Structure

```
AI-Medical-Assistant-RAG
│
├── app.py
├── rag_engine.py
├── data_loader.py
├── main.py
├── requirements.txt
│
├── medical_docs/
└── faiss_index/
```

---

## ⚙️ Installation & Run

Clone the repository:

```
git clone https://github.com/Mithanya/AI-Medical-Assistant-RAG.git
cd AI-Medical-Assistant-RAG
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 💬 Example Questions

* What are the symptoms of diabetes?
* How is hypertension treated?
* What are the side effects of Metformin?
* How do I perform CPR?

---

## 👩‍💻 Author

**Mithanya Murugesan**
Engineering Student | Python Developer | AI Enthusiast

⭐ If you like this project, consider starring the repository.
