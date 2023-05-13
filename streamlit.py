# The following code imports necessary libraries and modules
import streamlit as st
import tempfile
import os 
from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
import pinecone
from templates.qa_prompt import QA_PROMPT
from templates.condense_prompt import CONDENSE_PROMPT

# The following code loads environment variables from an external file
from dotenv import load_dotenv
load_dotenv()

# The following code defines a namespace
pinecone_namespace ='testing-pdf-2389203901'

# The following code defines the main function that runs the Streamlit app
def main():
    # Set Streamlit app title and header
    st.title('Langchain Chat')
    st.header('PDF Mode')

    # The following code defines four columns to input API keys and Pinecone indexing details
    col1, col2, col3, col4 = st.columns(4)

    # Input OpenAI API Key
    with col1:
        openai_api_key = st.text_input("OpenAI API Key", type="password")

    # Input Pinecone API Key
    with col2:
        pinecone_api_key = st.text_input("Pinecone API Key", type="password")

    # Input Pinecone Environment
    with col3:
        pinecone_environment = st.text_input("Pinecone Environment")

    # Input Pinecone Index Name
    with col4:
        pinecone_index = st.text_input("Pinecone Index Name")

    # Upload PDF files
    uploaded_files = st.file_uploader("Upload multiple files", accept_multiple_files=True, type="pdf")

    if uploaded_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                file_content = uploaded_file.read()
                st.write("Filename: ", file_name)

                # Write the content of the PDF files to a temporary directory
                with open(os.path.join(tmpdir, file_name), "wb") as file:
                    file.write(file_content)

            # Load the PDF files from the temporary directory
            loader = DirectoryLoader(tmpdir, glob="**/*.pdf", loader_cls=PyMuPDFLoader)
            documents = loader.load()

            # Split the PDF files into smaller chunks of text
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
            documents = text_splitter.split_documents(documents)

            # Initialize Pinecone with API keys and environment variables
            pinecone.init(
                api_key=pinecone_api_key,  # find at app.pinecone.io
                environment=pinecone_environment  # next to api key in console
            )

            # Initialize the OpenAI embeddings model
            embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)

            # Add the documents to Pinecone index
            Pinecone.from_documents(documents, embeddings, index_name=pinecone_index, namespace=pinecone_namespace)
            st.success("Ingested File!")

    # The following code takes user input, sets the temperature and determines the number of sources for the retrieval chain
    message = st.text_input('User Input:')
    temperature = st.slider('Temperature', 0.0, 2.0, 0.7)
    source_amount = st.slider('Sources', 1, 8, 4)

    if message:
        chat_history = []

        # Initialize the OpenAI Chat model
        embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)
        model = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=temperature, openai_api_key=openai_api_key, streaming=True)

        # Use Pinecone to retrieve documents relevant to user query
        pinecone.init(api_key=pinecone_api_key,environment=pinecone_environment)
        vectorstore = Pinecone.from_existing_index(index_name=pinecone_index, embedding=embeddings, text_key='text', namespace=pinecone_namespace)
        retriever = vectorstore.as_retriever(search_kwargs={"k": source_amount},  qa_template=QA_PROMPT, question_generator_template=CONDENSE_PROMPT)
        qa = ConversationalRetrievalChain.from_llm(llm=model, retriever=retriever, return_source_documents=True)
        result = qa({"question": message, "chat_history": chat_history})
        answer = result["answer"]
        source_documents = result['source_documents']

        parsed_documents = []
        for doc in source_documents:
            parsed_doc = {
                "page_content": doc.page_content,
                "metadata": {
                    "author": doc.metadata.get("author", ""),
                    "creationDate": doc.metadata.get("creationDate", ""),
                    "creator": doc.metadata.get("creator", ""),
                    "file_path": doc.metadata.get("file_path", ""),
                    "format": doc.metadata.get("format", ""),
                    "keywords": doc.metadata.get("keywords", ""),
                    "modDate": doc.metadata.get("modDate", ""),
                    "page_number": doc.metadata.get("page_number", 0),
                    "producer": doc.metadata.get("producer", ""),
                    "source": doc.metadata.get("source", ""),
                    "subject": doc.metadata.get("subject", ""),
                    "title": doc.metadata.get("title", ""),
                    "total_pages": doc.metadata.get("total_pages", 0),
                    "trapped": doc.metadata.get("trapped", "")
                }
            }
            parsed_documents.append(parsed_doc)
        
        # Display the response in the Streamlit app
        st.write('AI:')
        st.write(answer)
        for doc in parsed_documents:
            st.write(f"Source:", doc["metadata"]["source"])
            st.write(f"Page Number:", doc["metadata"]["page_number"])

if __name__ == '__main__':
    try:
        main()
    except:
        st.write('Fatal Error!')