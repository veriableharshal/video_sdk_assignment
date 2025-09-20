from typing import AsyncIterator, Optional
from videosdk.agents import Agent, ConversationFlow, ChatRole
from utils.helpers.rag_handler import search_knowledge_base


class RAGConversationFlow(ConversationFlow):
    async def run(self, transcript: str) -> AsyncIterator[str]:
        self.agent.chat_context.add_message(role=ChatRole.USER, content=transcript)

        retrieved_context: Optional[str] = None
        try:
            retrieved_context = await search_knowledge_base(transcript, max_results=4)
        except Exception as e:
            print(f"RAG retrieval error: {e}")

        if retrieved_context:
            self.agent.chat_context.add_message(
                role=ChatRole.SYSTEM,
                content=f"Relevant KB context: \n{retrieved_context}"
            )

        async for chunk in self.process_with_llm():
            yield chunk