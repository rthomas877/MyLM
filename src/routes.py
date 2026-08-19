from fastapi import APIRouter 

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello"}

@router.get("/status")
async def status():
    return {"running": True}

# TODO implement post endpoint for chat completions
@router.post("/chat")
async def chat():
    return {"response": ""}