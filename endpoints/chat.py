from fastapi import APIRouter
from pydantic import BaseModel
from handlers.base import BaseHandler
from typing import Optional

router = APIRouter()
handler = BaseHandler()

class ChatModel(BaseModel):
    query: str
    chat_history: list[str] = []
    namespace: Optional[str] = None 

@router.post("/chat")
async def chat( 
    chat_model: ChatModel
):
    response = handler.chat(
        chat_model.query, 
        chat_model.chat_history,
        namespace=(chat_model.namespace or None)
    )
    return {"response": response}
    