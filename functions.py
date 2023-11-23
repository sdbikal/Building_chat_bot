from dotenv import load_dotenv
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

    
client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
embeddings = OpenAIEmbeddings()

vector_store = Qdrant(
        client=client, 
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"), 
        embeddings=embeddings,
    )
    
  
def qa_model(question):
    

    prompt_template = """
    Use the context pieces below to answer
    question at the end. If you don't know the answer, say you don't know.
    don't try to answer.
    if they say you are someone, your answer is I'm MOJ chat bot 

    {context}

    Question: {question}
    Answer:
    """
    PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), chain_type="stuff", retriever=vector_store.as_retriever(), chain_type_kwargs=chain_type_kwargs)
    answer = qa.run(question)
    return answer