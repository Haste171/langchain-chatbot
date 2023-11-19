from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "langchain-chatbot is running!"}

from api.router import router
app.include_router(router, prefix="/api/v1")