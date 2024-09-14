import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is available
if not api_key:
    st.error("GEMINI_API_KEY not found in .env file. Please add it and restart the app.")
    st.stop()

# Configure the Google AI SDK
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="First when the user says that he is suffering from some health issues. You should reply the user in this format:\n1. Reply the causes\n2. Tell the user why it is caused\n3. Cross reference with some databases and suggest potential diagnosis.\n4. Provide recommendations or next steps for seeking medical care.\n\nYou should not reply that you are an AI and cannot assist on real-time problems and also if the user asks something beyond healthcare or human well-being you should say that you don't have info beyond healthcare.",
)

# Streamlit app
st.title("Healthcare Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Initialize chat session if it doesn't exist
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Generate response
    response = st.session_state.chat_session.send_message(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.text)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Add a sidebar with information about the chatbot
st.sidebar.title("About")
st.sidebar.info("This is a healthcare chatbot powered by Google's Gemini AI. It can answer questions related to health issues and provide general health advice. Please note that this bot is not a substitute for professional medical advice.")
