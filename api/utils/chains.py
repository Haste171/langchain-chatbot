import qdrant_client
from langchain.vectorstores.pinecone import Pinecone
from langchain.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatAnthropic
from langchain.chains.conversational_retrieval.prompts import QA_PROMPT, CONDENSE_QUESTION_PROMPT
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from decouple import config
from fastapi import HTTPException


class AIHandler(): 
    def __init__(self):
        self.openai_api_key = config("OPENAI_API_KEY")
        self.qdrant_url = config("QDRANT_URL")
        self.qdrant_api_key = config("QDRANT_API_KEY")
        self.qdrant_client = qdrant_client.QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)

    def ingest_documents(self, documents, collection_name, **kwargs):
        if kwargs.get("chunk_size"):
            chunk_size = kwargs.get("chunk_size")
        else:
            chunk_size = 4000

        if kwargs.get("chunk_overlap"):
            chunk_overlap = kwargs.get("chunk_overlap")
        else: 
            chunk_overlap = 400

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        split_docs = text_splitter.split_documents(documents)
        Qdrant.from_documents(
            split_docs,
            self.embeddings,
            url=config('QDRANT_URL'),
            prefer_grpc=True,
            api_key=config('QDRANT_API_KEY'),
            collection_name=collection_name,
        )

    def check_collection_exists(self, collection_name):
        collections = self.qdrant_client.get_collections()
        print(collections)
        if collection_name in collections:
            pass
        else:
            print(f"The collection '{collection_name}' does not exist.")
            raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' does not exist in Qdrant.")

    def retrieve(self, collection_name, **kwargs):
        """Retrieve Params:

        collection_name: str
        search_k: int
        model: str
        temperature: float
        return_sources: bool
        """

        if kwargs.get("search_k"):
            search_k = kwargs.get("search_k")
        else:    
            search_k = 2

        if kwargs.get("model"):
            model_name = kwargs.get("model")
        else: 
            model_name = "gpt-3.5-turbo"

        if kwargs.get("temperature"):
            if kwargs.get("temperature") >= 0.0 and kwargs.get("temperature") <= 2.0:
                temperature = kwargs.get("temperature")
        else:
            temperature = 0

        if kwargs.get("return_sources") != None:
            return_sources = kwargs.get("return_sources")
        else:
            return_sources = True


        # TODO: Add Check for if provided collection is in Qdrant --> Ref: chec.py
        # TODO: Add Check if model is in OpenAI
    
        llm = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=self.openai_api_key, streaming=True)
        qdrant = Qdrant(client=self.qdrant_client, collection_name=collection_name, embeddings=self.embeddings)
        retriever = qdrant.as_retriever(search_kwargs={"k": search_k}, qa_template=QA_PROMPT, question_generator_template=CONDENSE_QUESTION_PROMPT)
        return ConversationalRetrievalChain.from_llm(retriever=retriever, llm=llm, return_source_documents=return_sources)
