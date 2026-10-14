import pytest
from fastapi.testclient import TestClient

from agent.main import REPLY_PREFIX, app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("message", ["Hello", "", "2 + 2", "echo demo"])
def test_chat(message):
    response = client.post("/chat", json={"message": message})
    assert response.status_code == 200
    assert response.json() == {"reply": f"{REPLY_PREFIX}{message}"}


@pytest.mark.parametrize("payload", [{}, {"message": 123}, {"message": None}])
def test_chat_rejects_invalid_payload(payload):
    response = client.post("/chat", json=payload)
    assert response.status_code == 422
