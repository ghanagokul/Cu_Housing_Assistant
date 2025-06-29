import streamlit as st
import requests

st.set_page_config(page_title="CU Boulder Housing Chatbot", page_icon="🏠")

st.title("🏠 CU Boulder Housing Chatbot")
st.markdown("Ask me anything about housing, rent, lease terms, location, and more!")

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Input from user
if user_input := st.chat_input("Type your message here..."):
    # Show and store user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 🔁 Send the query to Flask backend
    try:
        response = requests.post("http://localhost:5000/chat", json={"query": user_input})  # ✅ fixed key
        response.raise_for_status()
        bot_reply = response.json().get("response", "❌ Bot returned no response.")
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    # Show and store assistant reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
