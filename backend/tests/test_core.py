from fastapi.testclient import TestClient

from app.ingestion.chunker import chunk_text
from app.ingestion.normalizer import normalize_record
from app.main import app
from app.models.common import Source


def test_chunker_preserves_content():
    chunks = chunk_text("alpha " * 500, max_chars=100, overlap=10)
    assert len(chunks) > 1
    assert "alpha" in " ".join(chunks)


def test_search_chat_and_graph():
    app.state.repository.clear()
    app.state.repository.upsert(normalize_record({"id": "decision", "title": "OAuth decision", "text": "The team chose OAuth for authentication.", "url": "https://example.test/oauth"}, Source.google))
    client = TestClient(app)
    assert client.get("/api/search", params={"q": "Why OAuth?"}).status_code == 200
    response = client.post("/api/chat", json={"question": "Why OAuth?"})
    assert response.status_code == 200
    assert response.json()["grounded"] is True
    assert response.json()["citations"][0]["id"] == "google:decision"
    assert client.get("/api/graph").json()["nodes"]
