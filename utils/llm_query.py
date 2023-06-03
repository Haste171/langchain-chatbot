import interactions, pinecone
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.prompt import PromptTemplate
from interactions import Client, CommandContext
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.chains.llm import LLMChain
from langchain.llms import OpenAI
from utils.mongo_db import MongoDBHandler
from dotenv import load_dotenv
import os
import sys

pinecone_api_key = os.environ.get('pinecone_api_key')
pinecone_env = os.environ.get('pinecone_env')
pinecone_index = os.environ.get('pinecone_index')

def llm_query(namespace, openai_api_key):
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    # streaming_llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0, openai_api_key=OPENAI_API_KEY)
    streaming_llm = ChatOpenAI(streaming=True, model_name='gpt-4', openai_api_key=openai_api_key, temperature=0, verbose=True)

    QA_V2 = """You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
Very Important: If the question is about writing code use backticks (```) at the front and end of the code snippet and include the language use after the first ticks.
If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
Use as much detail when as possible when responding.

{context}

Question: {question}
All answers should be in MARKDOWN (.md) Format:"""

    qap = PromptTemplate(template=QA_V2, input_variables=["context", "question"])

    CD_V2 = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    All answers should be in MARKDOWN (.md) Format:
    Standalone question:"""

    cdp = PromptTemplate.from_template(CD_V2)

    question_generator = LLMChain(llm=llm, prompt=cdp)
    doc_chain = load_qa_chain(streaming_llm, chain_type="stuff", prompt=qap)

    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)
    vectorstore = Pinecone.from_existing_index(index_name=pinecone_index, embedding=embeddings, text_key='text', namespace=namespace)

    qa = ConversationalRetrievalChain(retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6}), combine_docs_chain=doc_chain, return_source_documents=True, question_generator=question_generator, verbose=True)
    return qa