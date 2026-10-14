from app.graph.repository import KnowledgeRepository
from app.ingestion.normalizer import normalize_record
from app.models.common import Source


def seed(repository: KnowledgeRepository) -> None:
    examples = [
        {"id": "oauth-decision", "title": "Authentication decision", "text": "The team chose OAuth 2.0 for the authentication service because it supports delegated access and established provider integrations.", "url": "https://example.invalid/docs/oauth"},
        {"id": "auth-project", "title": "Authentication service", "text": "The authentication service project owns login, token exchange, and identity provider integration.", "url": "https://example.invalid/projects/auth"},
    ]
    for item in examples:
        repository.upsert(normalize_record(item, Source.google, kind="decision"))


if __name__ == "__main__":
    seed(KnowledgeRepository())
    print("Seeded demo records")
