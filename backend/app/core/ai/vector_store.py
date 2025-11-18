import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from app.core.ai.config import ai_settings


class VectorStore:
    """ChromaDB vector store for knowledge management."""

    _instance: Optional["VectorStore"] = None

    def __init__(self):
        # TODO: Configure ChromaDB client for production deployment
        # For now using in-memory, should use HTTP client in production
        self.client = chromadb.Client(Settings())
        self.collection_name = ai_settings.CHROMADB_COLLECTION_NAME
        self._collection = None

    @classmethod
    def get_instance(cls) -> "VectorStore":
        """Get singleton instance of vector store."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_collection(self):
        """Get or create the ChromaDB collection."""
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "AI Gym Management knowledge base"},
            )
        return self._collection

    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str],
    ):
        """Add documents to the vector store."""
        collection = self.get_collection()
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )

    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict] = None,
    ) -> Dict:
        """Query the vector store."""
        collection = self.get_collection()
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
        )
        return results

    def delete(self, ids: List[str]):
        """Delete documents from vector store."""
        collection = self.get_collection()
        collection.delete(ids=ids)


# Global vector store instance
vector_store = VectorStore.get_instance()
