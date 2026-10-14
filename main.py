from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from banking_agent import agent

app = FastAPI(title="AI Banking Assistant using LangChain")
PAGE = Path(__file__).parent / "static" / "index.html"
conversations: dict[str, list[dict[str, str]]] = {}


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: str | None = None


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(PAGE)


@app.post("/chat")
def chat(request: ChatRequest):
    conversation_id = request.conversation_id or str(uuid4())
    history = conversations.setdefault(conversation_id, [])
    return {"answer": agent.answer(request.message, history), "conversation_id": conversation_id, "tools_used": [tool.name for tool in agent.tools]}


@app.get("/health")
def health():
    return {"status": "running", "mode": "mock training chatbot"}
