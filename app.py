import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import time
from typing import List, Dict, Any

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
st.set_page_config(page_title="Ahmed Chatbot", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1a73e8;'>Ahmedus AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Your Technical AI Companion</h3>", unsafe_allow_html=True)

# Initialize chat history in session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Hello! I am *Ahmedus*, your AI assistant. I specialize in providing comprehensive support "
                "across a wide range of technical domains, including software development, data science, and AI. "
                "My goal is to assist you in tackling complex challenges efficiently, offering precise solutions, "
                "and guiding you through technical queries with clarity and professionalism."
            )
        }
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input from chat interface
user_input = st.chat_input("You:")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f"You: {user_input} 📱")

    # Show typing indicator
    with st.chat_message("assistant"):
        st.markdown("AI is thinking... ⏳")
        st.stop()

    try:
        # Get bot response using Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=st.session_state.messages,
            model="deepseek-r1-distill-llama-70b",  # Model used for chat completion
        )

        result = chat_completion.choices[0].message.content

        # Append bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})

        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(f"AI: {result} 💡")

    except Exception as e:
        # Handle any errors
        with st.chat_message("assistant"):
            st.markdown("Sorry, there was an error processing your request. Please try again. 🤔")
            st.error(str(e))

# Additional features
with st.sidebar:
    st.header("Settings")

    # Model selection
    models = {
        "deepseek-r1-distill-llama-70b": "LLAMA 70B Distill",
        "mixtral-8x7b-32768": "Mixtral 8x7B",
        "llama2-70b-4096": "LLAMA 2 70B"
    }

    selected_model = st.selectbox(
        "Choose Model",
        options=list(models.keys()),
        format_func=lambda x: models[x]
    )

    # Character limit
    max_length = st.slider(
        "Max Response Length",
        min_value=100,
        max_value=1000,
        value=500
    )

    # Clear chat history
    if st.button("Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "Hello! I am *Ahmedus*, your AI assistant. I specialize in providing comprehensive support "
                    "across a wide range of technical domains, including software development, data science, and AI. "
                    "My goal is to assist you in tackling complex challenges efficiently, offering precise solutions, "
                    "and guiding you through technical queries with clarity and professionalism."
                )
            }
        ]
        st.experimental_rerun()

# Loading spinner
with st.spinner("Processing your request..."):
    pass

# Typing indicator
def typing_indicator():
    with st.chat_message("assistant"):
        st.markdown("AI is thinking... ⏳")

# Error handling
def handle_error(error):
    with st.chat_message("assistant"):
        st.markdown(f"Error: {error}")
