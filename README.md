# 🏡 CU Housing Assistant (RAG-Based)

This project is an intelligent Housing Assistant powered by **Retrieval-Augmented Generation (RAG)**, designed to help students and newcomers find housing near universities in Colorado.

It provides:

* Natural language query support
* Housing data retrieval from PostgreSQL and vector stores
* Friendly explanations of housing terms (e.g., lease, subletting)
* Query rewriting and structured SQL generation using LLMs

---

## 🎓 Universities Covered

* University of Colorado Boulder

---

## 🛠️ Tech Stack

* **Python**, **LangChain**, **OpenAI GPT-4**
* **PostgreSQL** (for structured housing data)
* **FAISS** (for semantic search)
* **Streamlit** (frontend UI)
* **FastAPI** (backend for APIs and LLM processing)
* **Docker** (for local development)
* **GitHub Actions** (CI/CD)
* **Render.com** (deployment)

---

## 📁 Project Structure

```bash
RAG1/
│
├── app/                       # Streamlit frontend
├── main.py                    # FastAPI app entry
├── llm1_router.py             # Determines if SQL is needed
├── llm2_1_rewriter.py         # SQL-specific query rewriting
├── llm2_2_non_sql.py          # Handles conversational queries
├── sql_generator_and_runner.py
├── final_llm_answer.py        # Converts SQL result to user-friendly output
├── final_housing_dataset_with_links.csv   # Stored in PostgreSQL DB
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

Clone the repo:

```bash
git clone https://github.com/ghanagokul/RAG1.git
cd RAG1
```

Set environment variables:

```bash
OPENAI_API_KEY=your-key   # Put directly into files or create .env
POSTGRES_URI=postgresql://user:pass@host/dbname
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
# Frontend
streamlit run app.py

# Backend
python main.py
```

---

## 📌 Features

This chatbot assists with housing-related questions:

✅ Ask: *"Which apartments are near CU Boulder?"*
✅ Understands vague queries like: *"Any cheap and furnished place?"*
✅ Fetches structured info like rent, deposit, distance to bus stops, etc.

---

## 🔐 Security Note

Ensure that sensitive keys (OpenAI API, PostgreSQL URI) are kept in `.env` files and not hardcoded directly in the source code.

---

## 🏗️ Architecture

Below is the architecture diagram of the CU Housing Assistant:

https://github.com/ghanagokul/Cu_Housing_Assistant/blob/main/Architecture.png

---

## 🙌 Contribution

Feel free to open issues or submit pull requests!

---

## 📜 License

MIT License – See LICENSE
