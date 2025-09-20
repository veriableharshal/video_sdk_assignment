import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from utils.helpers.gemini_embedding import GeminiEmbedding
from dotenv import load_dotenv

load_dotenv()

class ChromaVectorStore:
    def __init__(self):
        self.db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        self.collection_name = os.getenv("COLLECTION_NAME", "documents_collection")
        self.client = chromadb.PersistentClient(path=self.db_path, settings=Settings(allow_reset=True))
        self.embedding_function = GeminiEmbedding()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Document embeddings for RAG"}
        )

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        try:
            embeddings = self.embedding_function.embed_batch(documents)
            if not embeddings:
                return False
            if not ids:
                ids = [f"doc_{i}" for i in range(len(documents))]
            if not metadatas:
                metadatas = [{"source": f"document_{i}"} for i in range(len(documents))]
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
            return False

    def get_documents(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.embedding_function.embed_text(query)
            if not query_embedding:
                return []
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
            )
            print(results)
            out: List[Dict[str, Any]] = []
            docs = results.get("documents", [[]])[0] if results.get("documents") else []
    
            for i in range(len(docs)):
                out.append({
                    "document": docs[i],
                })
            return out
        except Exception as e:
            print(f"Error searching in ChromaDB: {e}")
            return []

    def delete_collection(self):
        try:
            self.client.delete_collection(name=self.collection_name)
            return True
        except Exception as e:
            print(f"Error deleting collection: {e}")
            return False

    def get_collection_info(self):
        try:
            count = self.collection.count()
            return {
                "name": self.collection_name,
                "document_count": count,
                "db_path": self.db_path
            }
        except Exception as e:
            print(f"Error getting collection info: {e}")
            return None

  
    def info(self):
        return self.get_collection_info()
