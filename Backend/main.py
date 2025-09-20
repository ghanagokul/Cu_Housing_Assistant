from flask import Flask, request, jsonify
from flask_cors import CORS

# LangChain and custom logic imports
from langchain.memory import ConversationBufferMemory
from llm1_router import decide_query_route
from llm2_1_rewriter import rewrite_query_llm2_1
from llm2_2_non_sql import respond_to_non_sql_query
from sql_generator_and_runner import generate_sql_from_prompt, execute_sql_query
from final_llm_answer import generate_final_response

# -------------------------------------
# Initialize Flask App and CORS
# -------------------------------------
app = Flask(__name__)
CORS(app)

# -------------------------------------
# Initialize Conversation Memory
# (shared across the session)
# -------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# -------------------------------------
# Chat Endpoint
# -------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Step 1: Receive user input from frontend
        user_input = request.json.get("query")
        if not user_input:
            return jsonify({"error": "Missing 'query' field in request"}), 400

        # Step 2: Decide routing — does the query require SQL or not?
        route_info = decide_query_route(user_input, memory)
        route = route_info["route"]
        cleaned_query = route_info["cleaned_query"]

        # Step 3: Process based on route
        if route == "SQL":
            # Rewrite query for clarity
            rewritten_prompt = rewrite_query_llm2_1(cleaned_query)

            # Generate and execute SQL query
            sql_query = generate_sql_from_prompt(rewritten_prompt)
            results_df = execute_sql_query(sql_query)

            # Format the SQL results into a natural-language reply
            if results_df.empty:
                final_reply = "Sorry, I couldn't find any matching results for your query."
            else:
                final_reply = generate_final_response(user_input, rewritten_prompt, results_df)

        else:
            # Non-SQL query: handle general conversation
            final_reply = respond_to_non_sql_query(cleaned_query)

        # Return structured response
        return jsonify({
            "query": user_input,
            "route": route,
            "response": final_reply
        })

    except Exception as e:
        # Catch any server-side errors
        return jsonify({"error": str(e)}), 500

# -------------------------------------
# Run Flask app
# -------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
