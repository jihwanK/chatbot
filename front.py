import os

from dotenv import load_dotenv
load_dotenv(override=True)

import streamlit as st
from chatbot.chatbot import Chatbot

def init_session_state():
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = Chatbot(llm_platform="openai")
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

def main():
    # st.title("🍯   푸와   친구들의   고민상담   🍯")
    st.title("🍯 푸와 친구들의 고민상담 🍯")
    st.divider()

    init_session_state()

    if not st.session_state.username:
        username_input = st.text_input("이름을 입력해 주세요")
        if username_input:
            st.session_state.username = username_input.strip()
            st.rerun()

    else:
        messages = st.container()

        # Display conversation messages
        for chat in st.session_state.conversation:
            messages.chat_message("user").write(chat['user'])
            messages.chat_message("assistant").write(chat['bot'])

        # Chat input box at the bottom of the page
        prompt = st.chat_input("메시지를 입력해 주세요")
        if prompt:
            try:
                response = st.session_state.chatbot._chat(prompt, st.session_state.username)
                st.session_state.conversation.append({"user": prompt, "bot": response})
                # st.experimental_rerun()  # Rerun the app to update the conversation display
                st.rerun()  # Rerun the app to update the conversation display
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
