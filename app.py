import streamlit as st
from openai import OpenAI

# 1. Page Setup
st.set_page_config(page_title="My AI Assistant", page_icon="🤖")
st.title("🤖AI Chatbot")

# 2. Get API Key from the secrets file we just made
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("Key missing! Did you create .streamlit/secrets.toml?")
    st.stop()

client = OpenAI(api_key=api_key)

# 3. Session State (The "Memory")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# 4. Display Chat History
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 5. Handle User Input
if prompt := st.chat_input("Say something..."):
    # Show user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o", 
            messages=st.session_state["messages"],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Save AI response
    st.session_state["messages"].append({"role": "assistant", "content": response})