def chunk_text(text: str, max_chars: int = 1200, overlap: int = 120) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []
    if max_chars <= overlap:
        raise ValueError("max_chars must be greater than overlap")
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start + max_chars // 2:
                end = boundary
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks
