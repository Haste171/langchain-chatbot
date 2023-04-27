from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.vectorstores import Pinecone
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter


def ingest(openai_api_key, pinecone_api_key, pinecone_environment, pinecone_index, pinecone_namespace):
    loader = DirectoryLoader('docs', glob="**/*.pdf", loader_cls=PyMuPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    documents = text_splitter.split_documents(documents)

    pinecone.init(
        api_key=pinecone_api_key,  # find at app.pinecone.io
        environment=pinecone_environment  # next to api key in console
    )

    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)
    Pinecone.from_documents(documents, embeddings, index_name=pinecone_index, namespace=pinecone_namespace)

    return 'Finished Ingesting'