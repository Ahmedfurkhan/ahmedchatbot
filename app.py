import streamlit as st
from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Hugging Face model
hf_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
if not hf_token:
    st.error("Hugging Face API token not found. Please set the HUGGINGFACEHUB_API_TOKEN in your .env file.")
    st.stop()

llm = HuggingFaceHub(
    repo_id="tiiuae/falcon-7b-instruct",
    model_kwargs={"temperature": 0.5, "max_length": 128}
)

# Streamlit UI configuration
st.set_page_config(page_title="Q&A Chatbot")
st.markdown("<h1 style='text-align: center;'>Ahmed ChatBot</h1>", unsafe_allow_html=True)
st.header("Ask Me Anything!")

def get_model_response(question):
    prompt = f"Human: {question}\nAI: "
    try:
        response = llm(prompt)
        return response.strip()
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