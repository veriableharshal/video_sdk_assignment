from videosdk.agents import Agent


class RAGAgent(Agent):
    def init(self):
        super().__init__()
    
    async def on_enter(self) -> None:
        await self.session.say(
            "Hello! I'm your RAG-enabled voice assistant. I can answer questions using my knowledge base "
            "or provide general assistance. How can I help you today?"
        )
    
    async def on_exit(self) -> None:
        
        await self.session.say("Thank you for using the RAG voice assistant. Goodbye!")

        

    


    
