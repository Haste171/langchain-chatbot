from fastapi import APIRouter

router = APIRouter()

from api.chat import retrieval

router.include_router(retrieval.router, tags=["chat"])