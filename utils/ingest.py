from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.vectorstores import Pinecone
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


def ingest(openai_api_key, pinecone_api_key, pinecone_environment, pinecone_index, pinecone_namespace, use_pinecone):
    loader = DirectoryLoader('docs', glob="**/*.pdf", loader_cls=PyMuPDFLoader)
    documents = loader.load()

#reduce chunc size to 100 and overlap to 10
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, chunk_overlap=20)
    documents = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(
        model='text-embedding-ada-002', openai_api_key=openai_api_key)
    if use_pinecone:
        pinecone.init(
            api_key=pinecone_api_key,  # find at app.pinecone.io
            environment=pinecone_environment  # next to api key in console
        )

        Pinecone.from_documents(
            documents, embeddings, index_name=pinecone_index, namespace=pinecone_namespace)
        return 'Finished Ingesting, stored at Pinecone'
    else:
        vectorstore = Chroma.from_documents(
            documents, embeddings, collection_name="my_collection", persist_directory="./vectorstore")
        return 'Finished Ingesting, stored at ./vectorstore'
