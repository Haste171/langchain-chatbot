from fastapi import APIRouter
from pydantic import BaseModel
from handlers.base import BaseHandler

router = APIRouter()
handler = BaseHandler()

class ChatModel(BaseModel):
    query: str
    chat_history: list[str] = []
    namespace: str = None

@router.post("/chat")
async def chat():
    pass