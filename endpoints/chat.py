from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from handlers.base import BaseHandler
from typing import Optional

router = APIRouter()

class ChatModel(BaseModel):
    query: str
    model: str = "gpt-3.5-turbo"
    temperature: float
    vector_fetch_k: Optional[int] = 5 # Number of vectors to fetch from Pinecone as source documents
    chat_history: list[str] = [] # Example input: [("You are a helpful assistant.", "What is your name?")]
    namespace: Optional[str] = None 

@router.post("/chat")
async def chat( 
    chat_model: ChatModel,
):
    available_models = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k", "gpt-4-1106-preview", "claude-3-sonnet-20240229", "claude-3-opus-20240229"]

    if chat_model.model not in available_models:
        raise HTTPException(status_code=400, detail=f"Invalid model name. Please select a valid model from the list of available models: \n{str(available_models)}")
    
    if chat_model.temperature < 0.0 or chat_model.temperature > 2.0:
        raise HTTPException(status_code=400, detail="Invalid temperature value. Please select a value between 0.0 and 2.0")

    handler = BaseHandler(chat_model=chat_model.model, openai_chat_temperature=chat_model.temperature)
    response = handler.chat(
        chat_model.query, 
        chat_model.chat_history,
        namespace=(chat_model.namespace or None),
        search_kwargs=({"k": chat_model.vector_fetch_k} or {"k": 5})
    )
    return {"response": response}
    