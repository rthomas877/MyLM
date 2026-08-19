from fastapi import APIRouter 
from pydantic import BaseModel
from chat import Chat

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.get("/")
async def root():
    return {"message": "Hello"}

@router.get("/status")
async def status():
    return {"running": True}

# TODO implement post endpoint for chat completions
@router.post("/chat")
async def chat(request: ChatRequest):
    chat_object = Chat()
    query = request.query
    response = await chat_object.chat_completion(query)
    return {"response": response}