import os
import streamlit as st
from health_model import start_chat, send_message  # Import functions from health_model
from audio_handler import speech_to_text, text_to_speech
from database import init_db, save_conversation, get_conversations, get_all_sessions  # Import new function
import uuid

# Initialize the database
init_db()

# Start a chat session
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = start_chat()
    st.session_state.session_id = str(uuid.uuid4())  # معرف فريد لكل جلسة

# User interface
st.title("🩺 Health Content Generator")
st.write("Use this app to ask health-related questions and get answers. 💬")

# Saving previous conversations
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Displaying the conversation
if st.session_state.conversation:
    for idx, (question, answer) in enumerate(st.session_state.conversation):
        # Display user question on the right
        st.markdown(f'''
            <div style="text-align: right; background-color: #e1f5fe; border-radius: 10px; padding: 10px; margin: 5px 0; display: inline-block; max-width: 80%; float: right; clear: both;">
                   {question} ؟
            </div>
        ''', unsafe_allow_html=True)

        # Display system answer on the left
        st.markdown(f'''
            <div style="text-align: left; background-color: #e8f5e9; border-radius: 10px; padding: 10px; margin: 5px 0; display: inline-block; max-width: 80%; float: left; clear: both;">
                ✅ {answer}
            
        ''', unsafe_allow_html=True)

        # Button to convert specific answer to speech next to the answer (emoji only)
        if st.button("🔊", key=f'convert_{idx}'):
            text_to_speech(answer)

# Check if the input field was updated from voice-transcribed text
if 'voice_input' in st.session_state and st.session_state.voice_input:
    st.session_state.user_input = st.session_state.voice_input
    st.session_state.voice_input = ''  # Reset after updating

if 'user_temp_input' not in st.session_state:
    st.session_state.user_temp_input = ""

# User input field
user_input = st.text_input("Enter your health question:", value=st.session_state.user_temp_input, key="user_input")

# وضع الأزرار الفعلية بجانب بعضها البعض في الجهة اليسرى
col1, col2, col3 = st.columns([1, 1, 5])

with col1:
    if st.button("🎤", key='voice'):
        question = speech_to_text()
        if question:
            st.session_state.voice_input = question  # Store the voice-transcribed text in session_state
            st.rerun()  # Rerun the app to update the field

with col2:
    if st.button("📩", key='send'):
        if user_input:
            # Send question to AI model
            response_text = send_message(st.session_state.chat_session, user_input)
            if response_text:  # Check if the response is not empty
                save_conversation(st.session_state.session_id, user_input, response_text)
                st.session_state.conversation.append((user_input, response_text))
                # تفريغ المتغير المؤقت بعد الإرسال
                st.session_state.user_temp_input = ""  
                st.rerun()  # إعادة تشغيل التطبيق لتحديث الواجهة
        else:
            st.warning("⚠️ Please enter a question.")
            

# Display previous conversations with the main question as the title in sidebar
st.sidebar.header("🗣️ Previous Conversations")

# Retrieve all stored sessions
all_sessions = get_all_sessions()

if all_sessions:
    for idx, session in enumerate(all_sessions):
        # Retrieve the conversations of the session
        conversations = get_conversations(session)
        if conversations:
            # Use the first question as the session title
            session_title = conversations[0][0] if conversations[0][0] else f"Session {idx + 1}"
            with st.sidebar.expander(session_title, expanded=False):
                for question, answer in conversations:
                    st.write(f"Question ❓: {question}")
                    st.write(f"Answer ✅: {answer}")
                # Add a button to load the conversation into the main interface
                if st.button(f"🔄 Load Session {idx + 1}", key=f'load_{idx}'):
                    st.session_state.conversation = conversations  # Load the entire conversation
                    st.rerun()
else:
    st.sidebar.write("No previous conversations found.")

# Display developers and supervisor neatly
# قسم معلومات المطورين 
st.markdown(""" 
    <div style="background-color:#F5F5F5; padding: 10px; border-radius: 10px;"> 
        <h3 style="text-align: center;">
                  <b>ENGINEERS:</b></h3> 
        <ul style="list-style-type: none; padding-left: 0;"> 
            <li>👤 <b>Eng: Raidan Al-khateeb</b></li> 
            <li>👤 <b>Eng: Jalal Al-hujary</b></li>
            <li>👤 <b>Eng: Mohmmed Al-zikry</b></li>
            <li>👤 <b>Eng: Amr Al-zikry</b></li>
        </ul> 
    </div> 
""", unsafe_allow_html=True) 
 
# قسم الإشراف 
st.markdown(""" 
    <div style="background-color:#F5F5F5; padding: 10px; border-radius: 10px; margin-top: 20px;"> 
        <h3 style="text-align: center;">👨🏽‍💻 <b>Under the Supervision of:</b></h3> 
        <p style="text-align: center;"><b>Dr. Omar Abu Sand</b></p> 
    </div> 
""", unsafe_allow_html=True)
