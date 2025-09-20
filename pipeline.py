import asyncio
import os

import requests

from agent import RAGAgent
from rag_conversational_flow import RAGConversationFlow
from utils.helpers.chroma_db import ChromaVectorStore
from utils.agent_utils.agent_instruction import RAG_AGENT_PROMPT

from videosdk.agents import JobContext, CascadingPipeline, AgentSession
from videosdk.plugins.google import GoogleLLM
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.sarvamai import SarvamAISTT, SarvamAITTS
from videosdk.plugins.turn_detector import TurnDetector
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
chroma_db = ChromaVectorStore()


async def start_agent(context: JobContext):

    agent = RAGAgent(
        instructions=RAG_AGENT_PROMPT,

    )
    conversation_flow = RAGConversationFlow(agent)

    pipeline = CascadingPipeline(
       stt=SarvamAISTT(
        model="saarika:v2.5",              
        language="en-IN",
        silence_threshold=0.001,        
        silence_duration=1.2            
    ),
    llm=GoogleLLM(
        model="gemini-2.0-flash-001",
        temperature=0.3,                
        max_output_tokens=512,          
        top_p=0.8,
        presence_penalty=0.1            
    ),
    tts=SarvamAITTS(
        model="bulbul:v2",            
        pace=0.9,                      
        loudness=1.0                   
    ),
    vad=SileroVAD(
        threshold=0.5,                  
        min_speech_duration=0.2,        
        min_silence_duration=0.8      
    ),
        turn_detector=TurnDetector(
            threshold=0.4
        )
    )

    session = AgentSession(
        agent=agent,
        conversation_flow=conversation_flow,
        pipeline=pipeline
    )

    try:
        await context.connect()
        print("Waiting for participant...")
        print("Participant joined")
        await session.start()
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        await session.close()
        await context.shutdown()
