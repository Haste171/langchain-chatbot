from fastapi import APIRouter
from typing import List
from fastapi import UploadFile, Form
from handlers.base import BaseHandler
from typing import Optional

router = APIRouter()

@router.post("/ingest")
async def ingest_documents(
    files: List[UploadFile],
    namespace: Optional[str] = Form(None), 
):
    handler = BaseHandler(
        #embeddings_model='text-embedding-3-large' # Uncomment this kwarg to use the large embeddings model if you have Pinecone configured to that dimension size
    )
    documents = handler.load_documents(files, namespace)
    handler.ingest_documents(documents)
    return {"message": "Documents ingested"}