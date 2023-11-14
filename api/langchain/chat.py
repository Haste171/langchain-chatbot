from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def root():
    pass

@router.post("/chat/retrieval")
async def root(namespace: str):
    pass