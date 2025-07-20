import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# streamlit page configuration
st.set_page_config(
    page_title="LLAMA 3.1. ChatBot",
    layout="centered"
)

client = Groq(
    api_key=os.getenv("GROQ_API"),
)

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# streamlit page title
st.title("Chatbot with Groq API -LLAMA 3.1. Chat")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message:
user_prompt = st.chat_input("Ask LLAMA...")

if user_prompt:

    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # sens user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are an average helpful assistant. Also, everytime I ask for help, you're very non-chalant and basically give the bare minimum. Sometimes, barely."},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
