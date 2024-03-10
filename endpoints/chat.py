from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatModel(BaseModel):
    query: str
    chat_history: list[str] = []
    namespace: str = None

@router.post("/chat")
async def chat():
    pass