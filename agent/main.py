from fastapi import FastAPI
from pydantic import BaseModel

from agent.config import HOST, PORT, REPLY_PREFIX

app = FastAPI(title="Dummy Hosted Agent")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=f"{REPLY_PREFIX}{request.message}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("agent.main:app", host=HOST, port=PORT)
