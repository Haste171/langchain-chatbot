from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"detail": "Langchain Chatbot is Running!"}

from endpoints import (
    ingest,
    chat,
)

for endpoint in [ingest, chat]:
    app.include_router(endpoint.router)

if __name__ == "__main__":
    uvicorn.run('app:app', port=9091, reload=True)