import os
import time
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiEmbedding:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is required")
        self.client = genai.Client(api_key=api_key)
        self.model = os.getenv("GEMINI_EMBED_MODEL")

  

    def embed_text(self, text: str) -> List[float]:
        resp = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(task_type="QUESTION_ANSWERING", output_dimensionality=1536),
        )
        emb = resp.embeddings[0].values
        print(f"EMBEDDINGS  {emb}")
        return emb

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        output = []
        for text in texts:
            time.sleep(5)
            resp = self.embed_text(
            text=text,
          
        )
            output.append(resp)
        print(output)
    
        return output