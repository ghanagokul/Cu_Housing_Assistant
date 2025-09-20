# ----------------------------------------------------------------------
# Module: SQL Generator & Executor using LLM + PostgreSQL (LangChain-Free)
# ----------------------------------------------------------------------

import os
import pandas as pd
from sqlalchemy import create_engine, text
from openai import OpenAI
from dotenv import load_dotenv

# ----------------------------------------------------------------------
# Load environment variables from .env (if used)
# ----------------------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = ""
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ghanagokulgabburi:Saibaba3123@127.0.0.1:5432/housing_db")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables!")

# ----------------------------------------------------------------------
# Initialize OpenAI client and SQLAlchemy engine
# ----------------------------------------------------------------------
client = OpenAI(api_key=OPENAI_API_KEY)
engine = create_engine(DATABASE_URL)

# ----------------------------------------------------------------------
# Step 0: Clean SQL response from LLM (remove markdown formatting)
# ----------------------------------------------------------------------
def clean_sql_query(raw_sql: str) -> str:
    """
    Strips markdown formatting like ```sql ... ``` from LLM-generated SQL.
    """
    return raw_sql.strip().replace("```sql", "").replace("```", "").strip()

# ----------------------------------------------------------------------
# Step 1: Generate SQL query using LLM from a natural language prompt
# ----------------------------------------------------------------------
def generate_sql_from_prompt(prompt: str, retry_simple: bool = False) -> str:
    """
    Converts a natural language instruction into a valid SQL query for the `lease_data` table.

    Args:
        prompt (str): The user instruction (already rewritten).
        retry_simple (bool): If True, instructs the LLM to simplify the SQL (used during fallback).

    Returns:
        str: Cleaned SQL query.
    """
    base_instruction = (
        "You are an expert SQL query generator. Generate an SQL SELECT query for a PostgreSQL database "
        "with a table called `lease_data`. Only use available columns from the schema.\n\n"
    )

    if retry_simple:
        base_instruction += (
            "Avoid complex joins, functions, or unknown columns. Use only basic SELECT with WHERE, ORDER BY, or LIMIT.\n\n"
        )

    full_prompt = f"{base_instruction}Instruction:\n{prompt}\n\nSQL:"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert SQL query generator for a PostgreSQL housing database."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.2,
        max_tokens=300
    )

    return clean_sql_query(response.choices[0].message.content.strip())

# ----------------------------------------------------------------------
# Step 2: Execute generated SQL query and return results (with retry)
# ----------------------------------------------------------------------
def execute_sql_query(prompt: str) -> pd.DataFrame:
    """
    Executes an SQL query generated from a natural language prompt.
    If the first execution fails, attempts a simplified retry.

    Args:
        prompt (str): Cleaned and rewritten instruction describing the query.

    Returns:
        pd.DataFrame: Query result (empty if both attempts fail).
    """
    initial_sql = generate_sql_from_prompt(prompt)

    try:
        with engine.connect() as conn:
            result = pd.read_sql(text(initial_sql), conn)
        return result

    except Exception as e:
        print(f"First SQL attempt failed:\n{e}")
        print("Retrying with a simplified SQL query...")

        fallback_sql = generate_sql_from_prompt(prompt, retry_simple=True)
        try:
            with engine.connect() as conn:
                result = pd.read_sql(text(fallback_sql), conn)
            return result
        except Exception as e2:
            print(f"SQL Execution Failed Again:\n{e2}")
            return pd.DataFrame()
