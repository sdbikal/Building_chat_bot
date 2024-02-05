import streamlit as st
from agent import qa_dev,translatorAgent

st.title("MOJ demo")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Savolingizni kiriting?"):
    en_question = translatorAgent(question,'english')
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        en_response = qa_dev(en_question)
        full_response = translatorAgent(en_response,"uzbek")
        
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})