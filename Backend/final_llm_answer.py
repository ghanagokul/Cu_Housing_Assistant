from openai import OpenAI

OPENAI_API_KEY = ""

# ✅ Initialize the OpenAI client correctly
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_final_response(original_query: str, rewritten_prompt: str, df) -> str:
    table_text = df.to_markdown(index=False)

    prompt = f"""
You are a helpful assistant providing natural language summaries of database query results.

Original User Query:
{original_query}

Rewritten Instruction:
{rewritten_prompt}

SQL Result Table:
{table_text}

Now explain the result to the user in a concise, friendly way.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You summarize housing data results clearly and informatively."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
