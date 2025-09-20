# --------------------------------------------------------------
# Module: SQL Query Rewriter using OpenAI GPT-4o
# --------------------------------------------------------------

import os
from openai import OpenAI
from dotenv import load_dotenv

# --------------------------------------------------------------
# Load API Key securely from .env file
# --------------------------------------------------------------
load_dotenv()
api_key =""

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not set in environment variables!")

# Initialize OpenAI Client
client = OpenAI(api_key=api_key)

# --------------------------------------------------------------
# Few-shot Prompt Template for SQL Query Rewriting
# --------------------------------------------------------------
BASE_PROMPT = """
You are an expert **query rewriter** for a SQL assistant. Your job is to rewrite **vague, shorthand, or conversational** user queries into clear, unambiguous **natural language instructions** that help another AI write a correct SQL query.

Only include information that can be retrieved from the `lease_data` table.

---

**Schema Overview:**
[...schema truncated for brevity in this comment block...]
---

**Few-Shot Examples:**

Valid Queries:
- "Cheapest apartment?"  
  → Retrieve the property with the lowest `monthly_rent`.

- "Private room with gym?"  
  → Retrieve all properties where `room_type` = 'Private' and `gym_access` = TRUE.

- "What is the deposit for Boulder Heights?"  
  → Retrieve the `deposit_amount` from `lease_data` where `property_name` = 'Boulder Heights'.

Invalid Queries:
- "How many students live in each unit?"  
  → Not supported – no student data in schema.

- "Show me photos or 3D tours"  
  → Not possible – no media columns in the database.

---

User: {query}  
Rewrite:
"""

# --------------------------------------------------------------
# Rewrite User Query for SQL Prompt (LLM2_1)
# --------------------------------------------------------------
def rewrite_query_llm2_1(query: str) -> str:
    """
    Rewrites a user's vague or conversational query into a clear,
    schema-aware instruction for generating SQL.

    Args:
        query (str): The raw input from the user.

    Returns:
        str: A rewritten natural language query with explicit structure.
    """
    prompt = BASE_PROMPT.format(query=query)

    # Send the prompt to OpenAI GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert query rewriter for database access."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=200
    )

    # Return clean output
    return response.choices[0].message.content.strip()
