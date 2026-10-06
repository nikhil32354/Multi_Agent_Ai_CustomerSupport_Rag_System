from fastapi.testclient import TestClient

from app.main import app
from app.services.agents import IntentAgent


client = TestClient(app)


def test_chat_accepts_session_and_content_without_role():
    response = client.post(
        "/api/chat",
        json={"session_id": "sess-123", "content": "hello"},
    )

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["intent"] in {"general", "faq", "ticket"}
    assert payload["answer"] or payload["ticket"]


def test_intent_routing_matches_business_rules():
    assert IntentAgent.route("Hi") == "general"
    assert IntentAgent.route("hello") == "general"
    assert IntentAgent.route("What is your refund policy?") == "faq"
    assert IntentAgent.route("My refund hasn't arrived") == "ticket"
    assert IntentAgent.route("I need a refund") == "ticket"
    assert IntentAgent.route("I need help with my refund") == "ticket"
