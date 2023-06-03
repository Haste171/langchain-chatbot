# Import necessary modules
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
import pinecone
from templates.qa_prompt import QA_PROMPT
from templates.condense_prompt import CONDENSE_PROMPT
from langchain.vectorstores import Chroma


# Define the function with necessary inputs
def query(openai_api_key, pinecone_api_key, pinecone_environment, pinecone_index, pinecone_namespace, temperature, sources, use_pinecone):
    
    # Retrieve embeddings from OpenAI
    embeddings = OpenAIEmbeddings(
        model='text-embedding-ada-002', openai_api_key=openai_api_key)

    # Check if Pinecone should be used to store vector embeddings
    if use_pinecone:
        pinecone.init(api_key=pinecone_api_key,
                      environment=pinecone_environment)
        vectorstore = Pinecone.from_existing_index(
            index_name=pinecone_index, embedding=embeddings, text_key='text', namespace=pinecone_namespace)
    else:

        # Load vector embeddings from Chroma database
        persist_directory = "./vectorstore"
        vectorstore = Chroma(
            persist_directory=persist_directory, embedding_function=embeddings, collection_name="my_collection")

    # Retrieve chat model from OpenAI
    model = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=temperature,
                       openai_api_key=openai_api_key, streaming=True)  # max temperature is 2 least is 0
    
    # Retrieve document retriever using Pinecone or Chroma vectorstore
    retriever = vectorstore.as_retriever(search_kwargs={
                                         "k": sources},  qa_template=QA_PROMPT, question_generator_template=CONDENSE_PROMPT)  # 9 is the max sources
    
    # Create ConversationalRetrievalChain from chat model and document retriever
    qa = ConversationalRetrievalChain.from_llm(
        llm=model, retriever=retriever, return_source_documents=True)
    
    # Return ConversationalRetrievalChain object for further use
    return qa