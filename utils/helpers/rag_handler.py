import logging
from typing import List, Dict
from utils.helpers.chroma_db import ChromaVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalRAG:
    def __init__(self):
        self.store = ChromaVectorStore()

    async def search(self, query: str, top_k: int = 6) -> List[Dict]:
        print(f"RAG Query ===> {query}")
        results = self.store.get_documents(query=query, k=top_k)
        print(f" RAG DATA ===> {results}")
        formatted = []
        for r in results:
            content = r.get("document", "") or r.get("text", "")
            score = r.get("score") or r.get("distance")
            formatted.append({"content": content, "score": score})
        return formatted

    @staticmethod
    def format_for_llm(results: List[Dict]) -> str:
        if not results:
            return "No relevant information found in the knowledge base."
        parts = []
        for i, r in enumerate(results, 1):
            parts.append(f"Reference {i}:\n{r['content']}\n")
        return "\n".join(parts)

_local_rag = LocalRAG()

async def search_knowledge_base(query: str, max_results: int = 6) -> str:
    try:
        hits = await _local_rag.search(query, top_k=max_results)
        return _local_rag.format_for_llm(hits)
    except Exception as e:
        logger.error(f"RAG error: {e}")
        return "I’m having trouble accessing the knowledge base right now."
