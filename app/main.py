import json

from fastapi import FastAPI
from utils.llm_query import llm_query

app = FastAPI()

@app.post("/ingest")
def ingest_data():
    from deprecated.chatbot import ingest
    ingest_response = ingest()
    return {"ingest_response": ingest_response}

@app.get("/query/{question}")
def query_data(question: str):
    from deprecated.chatbot import query
    result = query({"question": question, "chat_history": []})
    return {"answer": result["answer"]}

@app.get("/chat_history")
def get_chat_history():
    with open('chat_history.json', 'r') as json_file:
        chat_history = json.load(json_file)
    return {"chat_history": chat_history}
