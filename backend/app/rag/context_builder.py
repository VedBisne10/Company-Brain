from app.models.common import SearchResult


def build_context(results: list[SearchResult]) -> str:
    return "\n\n".join(f"[{item.id}] {item.title}\n{item.snippet}" for item in results)
