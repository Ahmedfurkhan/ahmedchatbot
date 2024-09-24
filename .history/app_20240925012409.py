import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Groq client
groq_token = os.getenv('GROQ_API_TOKEN')
if not groq_token:
    st.error("Groq API token not found. Please set the GROQ_API_TOKEN in your .env file.")
    st.stop()

groq_client = Groq(
    api_key=groq_token,
)

# Streamlit UI configuration
st.set_page_config(page_title="Ahmed Chatbot")
st.markdown("<h1 style='text-align: center;'>Ahmed Chatbot</h1>", unsafe_allow_html=True)
st.header("Ask Me Anything")

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are Ahmed Assistant, an AI assistant that helps with coding and answering questions on a variety of topics."
        }
    ]

user_input = st.chat_input("You:")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    chat_completion = groq_client.chat.completions.create(
        messages=st.session_state.messages,
        model="llama-3.1-70b-versatile",  # You can change this to llama3_Groq70B if needed
    )

    result = chat_completion.choices[0].message.content

    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": result})
    with st.chat_message("assistant"):
        st.markdown(result)

if st.button("Reset Conversation"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are Ahmed Assistant, an AI assistant that helps with coding and answering questions on a variety of topics."
        }
    ]
    st.experimental_rerun()