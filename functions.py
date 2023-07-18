from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
_ = load_dotenv(find_dotenv()) 




openai.api_key = os.getenv("OPENAI_API_KEY")

def get_pdf_text(pdf_docs):
    """
    PDF documents are converted to text format
    input : PDF documnts
    output : text 
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text 


def get_text_chunks(raw_text,chunk_size=1000,chunk_overlap=200):
    """
    divides the given text into chunks
    """
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size =chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len
        )
    chunks = splitter.split_text(raw_text)
    return chunks

def get_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=chunks,embedding=embeddings)

    return vectorstore 

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain 


def load_url(url):
    url = str(url)
    loader = WebBaseLoader(url)
    data = loader.load()
    text = ""
    for i in range(len(data)):
        text+=data[i].page_content
    return str(text)
