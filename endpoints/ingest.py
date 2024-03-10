from fastapi import APIRouter
from typing import List
from fastapi import UploadFile
from pydantic import BaseModel
import tempfile

router = APIRouter()

class IngestModel(BaseModel):
    files: List[UploadFile]
    namespace: str = None

@router.post("/ingest")
async def ingest_documents(
    ingest_model: IngestModel
):
    for file in ingest_model.files:
        pass