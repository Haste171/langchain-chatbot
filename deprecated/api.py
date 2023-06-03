# import necessary packages
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from werkzeug.utils import secure_filename

# import packages for natural language processing
import tempfile
import os
from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
import pinecone

# import prompts
from templates.qa_prompt import QA_PROMPT
from templates.condense_prompt import CONDENSE_PROMPT

# import environment variables
from dotenv import load_dotenv
load_dotenv()
openai_api_key_env = os.environ.get('OPENAI_API_KEY')
pinecone_api_key_env = os.environ.get('PINECONE_API_KEY')
pinecone_environment_env = os.environ.get('PINECONE_ENVIRONMENT')
pinecone_index_env = os.environ.get('PINECONE_INDEX')

# set up Pinecone namespace
pinecone_namespace = 'testing-pdf-2389203901'

# set up Flask app
app = Flask("L-ChatBot")
UPLOAD_FOLDER = 'documents'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

parser = reqparse.RequestParser()

# add commentary to get_answer function
def get_answer(message, temperature=0.7, source_amount=4):
    """
    Retrieve the answer given a message using conversational retrieval and Pinecone vectorstore.

    Parameters:
    message (str): the message to retrieve the answer for
    temperature (float): the temperature to use for generating responses (default 0.7)
    source_amount (int): the number of sources to use for the response (default 4)

    Returns:
    dict: a dictionary object containing the answer and relevant metadata
    """
    chat_history = []
    embeddings = OpenAIEmbeddings(
        model='text-embedding-ada-002', openai_api_key=openai_api_key_env)

    pinecone.init(api_key=pinecone_api_key_env,
                  environment=pinecone_environment_env)
    vectorstore = Pinecone.from_existing_index(
        index_name=pinecone_index_env, embedding=embeddings, text_key='text', namespace=pinecone_namespace)
    model = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=temperature,
                       openai_api_key=openai_api_key_env, streaming=False)  # max temperature is 2 least is 0
    retriever = vectorstore.as_retriever(search_kwargs={
        "k": source_amount},  qa_template=QA_PROMPT, question_generator_template=CONDENSE_PROMPT)  # 9 is the max sources
    qa = ConversationalRetrievalChain.from_llm(
        llm=model, retriever=retriever, return_source_documents=True)
    result = qa({"question": message, "chat_history": chat_history})
    print("Cevap Geldi")
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

    # return answer and metadata as dictionary
    return {
        "answer": answer,
        "meta": parsed_documents
    }

# add commentary to Ask class
class Ask(Resource):

    def get(self):
        """
        Retrieve the response to a GET request containing a question.

        Returns:
        dict: a dictionary matching the response from get_answer() containing the answer and relevant metadata
        """
        question = request.args.get("question")
        temp = request.args.get("temp", default=0.7)
        sources = request.args.get("sources", default=4)
        return get_answer(question, float(temp), int(sources))

# add commentary to Ingest class
class Ingest(Resource):

    def allowed_file(self, filename):
        """
        Check if a file with the given filename is allowed to be uploaded.

        Parameters:
        filename (str): the name of the file to check

        Returns:
        bool: True if the file is allowed, False otherwise
        """
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        """
        Retrieve the PDF file from a request and ingest it into Pinecone vectorstore.

        Returns:
        str: a message indicating that the file has been uploaded successfully
        """
        # Get Text type fields
        if 'file' not in request.files:
            return 'No file part'

        file = request.files.get("file")
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            loader = DirectoryLoader(
                app.config['UPLOAD_FOLDER'], glob="**/*.pdf", loader_cls=PyMuPDFLoader)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=100)
            documents = text_splitter.split_documents(documents)

            pinecone.init(
                api_key=pinecone_api_key_env,  # find at app.pinecone.io
                environment=pinecone_environment_env  # next to api key in console
            )
            embeddings = OpenAIEmbeddings(
                model='text-embedding-ada-002', openai_api_key=openai_api_key_env)
            Pinecone.from_documents(
                documents, embeddings, index_name=pinecone_index_env, namespace=pinecone_namespace)
            return 'File uploaded and ingested successfully'

# add resources to API
api.add_resource(Ask, "/ask")
api.add_resource(Ingest, "/ingest")

# run Flask app
if __name__ == "__main__":
    app.run()