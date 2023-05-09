from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from werkzeug.utils import secure_filename

########################################################################
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

from dotenv import load_dotenv
load_dotenv()
openai_api_key_env = os.environ.get('OPENAI_API_KEY')
pinecone_api_key_env = os.environ.get('PINECONE_API_KEY')
pinecone_environment_env = os.environ.get('PINECONE_ENVIRONMENT')
pinecone_index_env = os.environ.get('PINECONE_INDEX')

pinecone_namespace = 'testing-pdf-2389203901'

app = Flask("L-ChatBot")
UPLOAD_FOLDER = 'documents'
ALLOWED_EXTENSIONS = {'pdf'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

parser = reqparse.RequestParser()


def get_answer(message, temperature=0.7, source_amount=4):
    chat_history = []
    embeddings = OpenAIEmbeddings(
        model='text-embedding-ada-002', openai_api_key=openai_api_key_env)

    pinecone.init(api_key=pinecone_api_key_env,
                  environment=pinecone_environment_env)
    vectorstore = Pinecone.from_existing_index(
        index_name=pinecone_index_env, embedding=embeddings, text_key='text', namespace=pinecone_namespace)
    model = ChatOpenAI(model_name='gpt-4', temperature=temperature,
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

    # Display the response in the Streamlit app
    return {
        "answer": answer,
        "meta": parsed_documents
    }
########################################################################


class Ask(Resource):

    def get(self):
        question = request.args.get("question")
        temp = request.args.get("temp", default=0.7)
        sources = request.args.get("sources", default=4)
        return get_answer(question, float(temp), int(sources))


class Ingest(Resource):

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
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
                chunk_size=200, chunk_overlap=20)
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


api.add_resource(Ask, "/ask")
api.add_resource(Ingest, "/ingest")

if __name__ == "__main__":
    app.run()
