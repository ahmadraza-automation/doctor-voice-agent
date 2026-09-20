"""
Simple knowledge base.
In production, replace with vector database (Chroma, Pinecone, FAISS + embeddings).
"""

import os
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

def load_knowledge() -> str:
    """Load all text files from knowledge folder."""
    texts = []
    if KNOWLEDGE_DIR.exists():
        for file in KNOWLEDGE_DIR.glob("*.txt"):
            try:
                texts.append(f"=== {file.name} ===\n{file.read_text(encoding='utf-8')}")
            except Exception:
                pass
    return "\n\n".join(texts) if texts else "No knowledge base documents found."


def query_knowledge_base(query: str) -> str:
    """
    Very simple keyword search over knowledge base.
    Replace with proper RAG later.
    """
    content = load_knowledge()
    if "No knowledge base" in content:
        return content

    # Simple relevance: return full content for now (small KB)
    # In production: embed query + documents and retrieve top chunks
    return f"Knowledge base content relevant to '{query}':\n\n{content[:3000]}"
