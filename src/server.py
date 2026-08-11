from fastapi import FastAPI
import uvicorn
from routes import router

app = FastAPI()

app.include_router(router)

def start_server():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )