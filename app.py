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

        st.markdown(f"**You:** {user_prompt}")
        st.markdown(f"**AI:** {response}")

if st.session_state.conversation:
    st.subheader("Conversation History")
    for role, text in st.session_state.conversation:
        st.markdown(f"**{role}:** {text}")
