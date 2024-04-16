import streamlit as st
from agent import qa_dev

st.title("CS GPT")
st.image("dialogXR_Typography.jpg")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Hello and welcome to dialogXR, your dedicated AI assistant for child welfare services. I’m here to help you efficiently gather and manage information for your investigations. How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = qa_dev(question)
        
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
