import os
import qdrant_client
import openai
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = qdrant_client.QdrantClient(
    os.getenv("QDRANT_HOST"),
    api_key = os.getenv("QDRANT_API_KEY")
)

embeddings = OpenAIEmbeddings()

vectorstore = Qdrant(
        client=client,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        embeddings=embeddings
    )

def qa_dev(user_query:str):
    llm = ChatOpenAI(model='gpt-4-1106-preview')
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
        )
    result = qa.invoke({'query':user_query})
    return result['result']