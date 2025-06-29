# 🏡 CU Housing Assistant (RAG-Based)

This project is an intelligent Housing Assistant powered by **Retrieval-Augmented Generation (RAG)**, designed to help students and newcomers find housing near universities in Colorado.

It provides:
- Natural language query support
- Housing data retrieval from PostgreSQL and vector stores
- Friendly explanations of housing terms (e.g., lease, subletting)
- Query rewriting and structured SQL generation using LLMs

---

## 🎓 Universities Covered

- University of Colorado Boulder

---

## 🛠️ Tech Stack

- **Python**, **LangChain**, **OpenAI GPT-4**
- **PostgreSQL** (for structured housing data)
- **ChromaDB / FAISS** (for semantic search)
- **Streamlit** (frontend UI)
- **FastAPI** (backend for APIs and LLM processing)
- **Docker** (for local development)
- **GitHub Actions** (CI/CD)
- **Render.com** (deployment)

---

## 📁 Project Structure

```bash
RAG1/


|   ├──app                       # Streamlit
│   ├── main.py                  # FastAPI app entry
│   ├── llm1_router.py           # Determines if SQL is needed
│   ├── llm2_1_rewriter.py       # SQL-specific query rewriting
│   ├── llm2_2_non_sql.py        # Handles conversational queries
│   ├── sql_generator_and_runner.py
│   └── final_llm_answer.py      # Converts SQL result to user-friendly output
├── final_housing_dataset_with_links.csv # Store it into the database                       
├── requirements.txt
└── README.md
⚙️ Setup Instructions

Clone the repo
git clone https://github.com/ghanagokul/RAG1.git
cd RAG1

OPENAI_API_KEY=your-key  #Put directly into all the fiels or create .env and modify the files accordingly
POSTGRES_URI=postgresql://user:pass@host/dbname
Install dependencies
pip install -r requirements.txt
Run the app
Frontend ->streamlit run app.py
Backend -> python main.py
📌 Features

It is basically a chatbot that helps to answers questions that arise while looking for a house 
✅ Ask "Which apartments are near CU Boulder?"
✅ Understands vague queries like "Any cheap and furnished place?"
✅ Fetches structured info like rent, deposit, distance to bus stops, etc.
🔐 Security Note

Architecture
<img width="963" alt="Screenshot 2025-06-29 at 2 15 14 AM" src="https://github.com/user-attachments/assets/bfa74e7a-9b9b-4aea-8c6d-354b400fe3e4" />



🙌 Contribution

Feel free to open issues or submit pull requests!

📜 License

MIT License – See LICENSE

