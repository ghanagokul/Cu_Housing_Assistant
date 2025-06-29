from llm1_router import decide_query_route
from llm2_1_rewriter import rewrite_query_llm2_1
from llm2_2_non_sql import respond_to_non_sql_query
from sql_generator_and_runner import generate_sql_from_prompt, execute_sql_query
from final_llm_answer import generate_final_response

print("\n🎓 CU Boulder Housing Chatbot — Ask me anything about student housing!\n")

conversation_history = []

while True:
    user_input = input("👤 You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break

    # Step 1: Decide whether SQL is needed
    route = decide_query_route(user_input)
    print(f"\n🔀 Routing decision: {route}")

    if route == "SQL":
        # Step 2A: Rewrite the query using LLM2_1
        rewritten_prompt = rewrite_query_llm2_1(user_input)
        print(f"\n📝 Rewritten Prompt: {rewritten_prompt}")

        # Step 3A: Generate SQL
        sql_query = generate_sql_from_prompt(rewritten_prompt)
        print(f"\n🧾 SQL Query: {sql_query}")

        # Step 4A: Execute SQL
        results_df = execute_sql_query(sql_query)

        # Step 5A: Final LLM to explain results
        if results_df.empty:
            final_reply = "Sorry, I couldn't find any matching results for your query."
        else:
            final_reply = generate_final_response(user_input, rewritten_prompt, results_df)

    else:
        # Step 2B: Direct reply for non-SQL queries
        final_reply = respond_to_non_sql_query(user_input)

    print(f"\n🤖 Assistant: {final_reply}\n")
    conversation_history.append((user_input, final_reply))
