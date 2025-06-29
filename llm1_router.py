# ---------------------------------------------------------
# Imports and Environment Setup
# ---------------------------------------------------------
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

# ---------------------------------------------------------
# Load API Keys
# ---------------------------------------------------------
# (You can use a .env file to load the key securely in production)
OPENAI_API_KEY = ""

# ---------------------------------------------------------
# Initialize LLM (GPT-4 via LangChain)
# ---------------------------------------------------------
llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-4",
    openai_api_key=OPENAI_API_KEY
)

# ---------------------------------------------------------
# Define Prompt Template with Few-Shot Examples
# ---------------------------------------------------------
prompt = PromptTemplate(
    input_variables=["chat_history", "query"],
    template="""
You are a smart assistant working for a student housing company. Your job is to decide whether a user's query requires a SQL query to the housing database or if it can be answered with general knowledge.

---

### What does "rewriting a query" mean?

It means converting the user's raw input into a **complete, grammatically correct, and context-aware** question. This rewritten query should:
- Clarify vague or incomplete phrases
- Leverage chat history for context
- Be cleanly formatted for a second LLM or SQL engine to interpret

---

### Your Task:

1. If the query **requires data from the housing database**, respond with:
    **SQL_NEEDED: <rewritten_query>**

2. If the query **can be answered without accessing the database**, respond with:
    **NO_SQL_NEEDED: <rewritten_query>**

---

### Chat history:
{chat_history}

### ❓ User query:
{query}

---

### Few-shot examples:

#### Example 1:
Chat history:
User: Show me apartments near Target  
User: Which one is cheapest?

User query: which of them  
Response: SQL_NEEDED: Retrieve the cheapest apartment among those near Target.

---

#### Example 2:
User query: least rent?  
Response: SQL_NEEDED: Retrieve the property with the lowest monthly rent from the database.

---

#### Example 3:
User query: Can u help?  
Response: NO_SQL_NEEDED: Yes, I can help you find student housing. Please share your requirements.

---

#### Example 4:
User query: What is the lease clause?  
Response: SQL_NEEDED: Retrieve the lease termination clause from the housing database.

---

#### Example 5:
User query: Where to pay rent?  
Response: NO_SQL_NEEDED: Rent is typically paid via online portals or checks, depending on the landlord.

---

Only output one line:  
SQL_NEEDED: <rewritten_query>  
or  
NO_SQL_NEEDED: <rewritten_query>
"""
)

# ---------------------------------------------------------
# Initialize Chat Memory
# ---------------------------------------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="query"
)

# ---------------------------------------------------------
# Routing Function to Decide if SQL is Needed
# ---------------------------------------------------------
def decide_query_route(query: str, memory: ConversationBufferMemory) -> dict:
    """
    Determines whether a user's query should be answered via SQL or not.
    Returns:
        {
            "route": "SQL" or "NO_SQL",
            "cleaned_query": rewritten query string
        }
    """
    rewriter_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )

    # Run the query through the chain
    result = rewriter_chain.invoke({"query": query})
    raw_response = result["text"].strip()

    # Parse result and determine route
    if raw_response.startswith("SQL_NEEDED:"):
        return {
            "route": "SQL",
            "cleaned_query": raw_response.replace("SQL_NEEDED:", "").strip()
        }
    else:
        return {
            "route": "NO_SQL",
            "cleaned_query": raw_response.replace("NO_SQL_NEEDED:", "").strip()
        }

# ---------------------------------------------------------
# Debug Helper (Optional)
# ---------------------------------------------------------
def print_chat_memory():
    """Prints current memory buffer for debugging."""
    print("\nMemory so far:\n" + memory.buffer)
