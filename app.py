import streamlit as st
from llama_inference import LLMInference
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the LLaMA model
llama_token = os.getenv('LLAMA_API_TOKEN')
if not llama_token:
    st.error("LLaMA API token not found. Please set the LLAMA_API_TOKEN in your .env file.")
    st.stop()

llm = LLMInference(
    model_name="llama-3.1-70b-versatile",
    api_key=llama_token
)

# Streamlit UI configuration
st.set_page_config(page_title="LLaMA 3.1 70B Chatbot")
st.markdown("<h1 style='text-align: center;'>LLaMA 3.1 70B Chatbot</h1>", unsafe_allow_html=True)
st.header("Chat with the LLaMA 3.1 70B Model")

def get_model_response(prompt):
    try:
        response = llm.generate_text(
            prompt=prompt,
            max_length=256,
            temperature=0.7,
            top_p=0.95
        )
        return response.strip()
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

        st.markdown(f"**You:** {user_prompt}")
        st.markdown(f"**AI:** {response}")

if st.session_state.conversation:
    st.subheader("Conversation History")
    for role, text in st.session_state.conversation:
        st.markdown(f"**{role}:** {text}")
