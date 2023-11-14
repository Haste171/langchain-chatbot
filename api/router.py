from fastapi import APIRouter

router = APIRouter()

@router.get("/router")
async def root():
    return {"message": "Routing Manager is running!"}

