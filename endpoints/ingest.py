from fastapi import APIRouter
from typing import List
from fastapi import UploadFile, Form
from pydantic import BaseModel, Field
import tempfile
from handlers.base import BaseHandler
from typing import Optional

handler = BaseHandler()
router = APIRouter()


@router.post("/ingest")
async def ingest_documents(
    files: List[UploadFile],
    namespace: Optional[str] = Form(None), 
):
    documents = handler.load_documents(files, namespace)
    handler.ingest_documents(documents)
    return {"message": "Documents ingested"}