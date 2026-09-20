"""
Simple web search tool.
You can replace Serper with Tavily, Brave, or any other search API.
"""

import os
import httpx
from typing import Optional

async def search_web(query: str, num_results: int = 5) -> str:
    """
    Search the web for general medical information (non-diagnostic).
    """
    api_key = os.getenv("SERPER_API_KEY")
    
    if not api_key:
        return (
            "Web search is currently not configured. "
            "Please answer using general knowledge only and remind the caller "
            "to consult a licensed doctor for personal medical advice."
        )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
                json={"q": query, "num": num_results},
                timeout=10.0
            )
            data = response.json()

        results = []
        for item in data.get("organic", [])[:num_results]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            results.append(f"- {title}: {snippet} ({link})")

        if not results:
            return "No relevant results found."

        return "Search results:\n" + "\n".join(results)
    except Exception as e:
        return f"Search failed: {str(e)}. Please answer carefully using general knowledge."
