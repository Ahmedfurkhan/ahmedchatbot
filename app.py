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
st.set_page_config(page_title="LLaMA 3.1 70B Chatbot")
st.markdown("<h1 style='text-align: center;'>LLaMA 3.1 70B Chatbot</h1>", unsafe_allow_html=True)
st.header("Chat with the LLaMA 3.1 70B Model")

def get_model_response(prompt):
    try:
        response = groq_client.query(
            query=f"{{llama3 = $llama3, result: llama3(prompt='{prompt}', max_tokens=256, temperature=0.7, top_p=0.95)}}",
            variables={
                "llama3": "llama-3.1-70b-versatile"
            }
        )
        return response['result'].strip()
    except Exception as e:
        st.error(f"Error in generating response: {e}")
        return "Sorry, I couldn't process your request."

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

input_text = st.text_area("Your message:", height=100, key="input")
submit = st.button("Send")

if submit:
    if input_text.strip():
        with st.spinner("Thinking..."):
            user_prompt = input_text.strip()
            st.session_state.conversation.append(("You", user_prompt))
            response = get_model_response(user_prompt)
            st.session_state.conversation.append(("AI", response))

        st.write("**You:** " + user_prompt)
        st.write("**AI:** " + response)

if st.session_state.conversation:
    st.subheader("Conversation History")
    for role, text in st.session_state.conversation:
        st.write(f"**{role}:** {text}")import streamlit as st
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
st.set_page_config(page_title="Q&A Chatbot")
st.markdown("<h1 style='text-align: center;'>Ahmed ChatBot</h1>", unsafe_allow_html=True)
st.header("Ask Me Anything!")

def get_model_response(question):
    prompt = f"Human: {question}\nAI: "
    try:
        response = groq_client.query(
            query=f"{{llama3 = $llama3, result: llama3(prompt='{prompt}', max_tokens=128, temperature=0.5)}}",
            variables={
                "llama3": "llama3-groq-70b-8192-tool-use-preview"
            }
        )
        return response['result'].strip()
    except Exception as e:
        st.error(f"Error in generating response: {e}")
        return "Sorry, I couldn't process your request."

input_text = st.text_input("Ask a question:", key="input")
submit = st.button("Get Answer")

if submit:
    if input_text.strip():
        with st.spinner("Thinking..."):
            response = get_model_response(input_text)
        st.subheader("Answer:")
        st.write(response)
    else:
        st.warning("Please enter a question before submitting.")

# Display conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if submit and input_text.strip():
    st.session_state.conversation.append(("You", input_text))
    st.session_state.conversation.append(("AI", response))

if st.session_state.conversation:
    st.subheader("Conversation History")
    for role, text in st.session_state.conversation:
        st.write(f"**{role}:** {text}")
