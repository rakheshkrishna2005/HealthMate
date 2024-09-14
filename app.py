import os
import time
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Healthcare ChatBot - Powered by Gemini 1.5 Pro!",
    page_icon=":hospital:",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;  /* Set the width to 100% */
        padding: 10px 0;  /* Increase padding for better appearance */
    }
    </style>
    """,
    unsafe_allow_html=True
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini 1.5 Pro model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-pro')
vision_model = gen_ai.GenerativeModel('vision-x-model')

# Function to translate roles between Gemini-1.5 Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session and other session state variables
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.user_prompts = []
    st.session_state.greeting_done = False
    st.session_state.questions_asked = False

# Main content
st.markdown("<h1 style='text-align: center;'>🏥 Healthcare ChatBot!</h1>", unsafe_allow_html=True)

# Feature cards
col1, col2 = st.columns(2)
with col1:
    st.success("📊 Analyses patient-reported symptoms and provide preliminary diagnoses or suggest possible conditions.")
    st.info("📈 Assess symptoms and provides preliminary insights to guide your next steps in seeking medical care.")
with col2:
    st.warning("📄 This data can help in identifying trends, and making more informed decisions about treatment plans.")
    st.error("💡 Receive tailored health recommendations based on your symptoms, including preventive measures and treatments.")

# Chat interface
chat_placeholder = st.empty()

# Initial greeting and questions
if not st.session_state.greeting_done:
    with chat_placeholder.chat_message("assistant"):
        st.write("Hello! I'm your Healthcare ChatBot. How can I assist you today?")
    time.sleep(2)
    st.session_state.greeting_done = True

if st.session_state.greeting_done and not st.session_state.questions_asked:
    questions = [
        "What is your current health condition?",
        "Do you have any specific health concerns or symptoms?",
        "Are you currently taking any medications?",
        "Do you have any chronic diseases or conditions?",
        "Have you had any recent changes in your health or lifestyle?"
    ]
    
    for question in questions:
        with chat_placeholder.chat_message("assistant"):
            st.write(question)
        user_response = st.chat_input(f"Your answer to: {question}")
        if user_response:
            with chat_placeholder.chat_message("user"):
                st.write(user_response)
            st.session_state.user_prompts.append(f"Q: {question}\nA: {user_response}")
        else:
            break
    
    st.session_state.questions_asked = True

# Regular chat interaction
if st.session_state.greeting_done and st.session_state.questions_asked:
    for message in st.session_state.chat_session.history:
        with chat_placeholder.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Enter your health-related question here...")
    if user_prompt:
        with chat_placeholder.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.user_prompts.append(user_prompt)

        # Display a spinner in the center of the page to indicate prompt generation
        with st.spinner("Generating response..."):
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            time.sleep(2)  # Simulate some processing time (optional)
        
        with chat_placeholder.chat_message("assistant"):
            st.markdown(gemini_response.text)