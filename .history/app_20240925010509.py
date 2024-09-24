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
st.markdown("<h1 style='text-align: center;'>LLaMA 3.1 70B Chatbot</h1>", unsafe_allow_html=True)
st.header("")

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are Ahmed Assistant, an AI assistant that helps with coding and answering questions on a variety of topics."
        }
    ]

def get_model_response(messages):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama3-groq-70b-8192-tool-use-preview",
            max_tokens=256,
            temperature=0.7,
            top_p=0.95
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error in generating response: {e}")
        return "Sorry, I couldn't process your request."

user_input = st.chat_input("You:")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_model_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are Ahmed Assistant, an AI assistant that helps with coding and answering questions on a variety of topics."
        }
    ]
    st.experimental_rerun()
