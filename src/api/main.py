from fastapi import FastAPI
from pydantic import BaseModel

from src.crew import run_crew

app = FastAPI(title="Amar Passport AI Agent")


class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.get("/")
def health() -> dict:
    return {"status": "ok", "message": "Amar Passport AI Agent is running"}


@app.post("/chat")
def chat(req: ChatRequest) -> dict:
    return run_crew(req.message, req.session_id)
