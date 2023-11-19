from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from api.utils.chains import AIHandler
from lanarky.responses import StreamingResponse


ai_handler = AIHandler()
router = APIRouter()

class ChatInput(BaseModel):
    prompt: str
    collection: str = Field(None, example="my_documents")
    model: Optional[str] = Field(None, example="gpt-3.5-turbo")
    temperature: Optional[float] = Field(None, example=0.8)
    search_k : Optional[int] = Field(None, example=2)

@router.post("/chat")
async def root(input: ChatInput):
    """Chat with the AI. Returns a StreamingResponse with a chain of tokens and source documents."""
    chain = ai_handler.retrieve(collection_name=input.collection, 
                                search_k=input.search_k,
                                model=input.model,
                                temperature=input.temperature,
                                return_sources=True)

    # TODO: Add compartmentalization for chat history and collections per user in DB, add identification Bearer requirement per user
    # TODO: Add chat history to chain_dict and store in DB for each user
    hist = []
    chain_dict = {"question": input.prompt, "chat_history": hist}

    return StreamingResponse.from_chain(chain, chain_dict, as_json=True)