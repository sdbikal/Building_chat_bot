import streamlit as st
from dotenv import load_dotenv
from functions import *
from html_templates import bot_template,css,user_template
import os 
import imghdr


openai.api_key = os.getenv("OPENAI_API_KEY")

def heandle_userinput(user_input):
    response = st.session_state.conversation({'question':user_input})
    st.session_state.chat_history = response['chat_history']

    for i , message in enumerate(st.session_state.chat_history):
        if i%2==0:
            st.write(user_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple data type ",page_icon=":books:")
    st.write(css,unsafe_allow_html=True)
     
    if "conversation" not in st.session_state:
        st.session_state.conversation = None 
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    st.header("Chat with multiple data type :books: ")
    user_question = st.text_input("As a question about your document")
    if user_question:
        heandle_userinput(user_question)

     
    
    # with st.sidebar:
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs =st.file_uploader("Upload your data",accept_multiple_files=True)
        st.subheader("You tuube or web site link")
        link =  st.text_input("Link")

        if st.button("Procress"):
            with st.spinner("Procressing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # get text from url 
                url_text = load_url(link)
                # merge  url text and raw text
                raw_text+=url_text# get chunks
                chunks = get_text_chunks(raw_text)
                # get vectorstore 
                vectorstore = get_vectorstore(chunks=chunks)
                # get conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
            
            
             

        





if __name__ == "__main__":
    main()
          