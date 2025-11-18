import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import logging
from app.core.ai.config import ai_settings

logger = logging.getLogger(__name__)


class VectorStore:
    """
    ChromaDB vector store for knowledge management.

    Supports multiple modes:
    - http: Connect to ChromaDB server (production)
    - persistent: Local persistent storage
    - memory: In-memory (development only)
    """

    _instance: Optional["VectorStore"] = None

    def __init__(self):
        self.collection_name = ai_settings.CHROMADB_COLLECTION_NAME
        self._collection = None

        # Initialize client based on mode
        mode = ai_settings.CHROMADB_MODE.lower()

        if mode == "http":
            # HTTP client for production deployment
            try:
                self.client = chromadb.HttpClient(
                    host=ai_settings.CHROMADB_HOST,
                    port=ai_settings.CHROMADB_PORT,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=False
                    )
                )
                logger.info(
                    f"ChromaDB HTTP client initialized: {ai_settings.CHROMADB_HOST}:{ai_settings.CHROMADB_PORT}"
                )
            except Exception as e:
                logger.error(f"Failed to initialize ChromaDB HTTP client: {e}")
                logger.warning("Falling back to in-memory client")
                self.client = chromadb.Client(Settings(anonymized_telemetry=False))

        elif mode == "persistent":
            # Persistent local storage
            self.client = chromadb.PersistentClient(
                path=ai_settings.CHROMADB_PERSIST_DIRECTORY,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=False
                )
            )
            logger.info(
                f"ChromaDB persistent client initialized: {ai_settings.CHROMADB_PERSIST_DIRECTORY}"
            )

        else:
            # In-memory client (development only)
            self.client = chromadb.Client(Settings(anonymized_telemetry=False))
            logger.warning(
                "ChromaDB in-memory client initialized - data will be lost on restart!"
            )

    @classmethod
    def get_instance(cls) -> "VectorStore":
        """Get singleton instance of vector store."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_collection(self):
        """Get or create the ChromaDB collection."""
        if self._collection is None:
            try:
                self._collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={
                        "description": "AI Gym Management knowledge base",
                        "created_at": str(__import__('datetime').datetime.utcnow())
                    },
                )
                logger.info(f"ChromaDB collection ready: {self.collection_name}")
            except Exception as e:
                logger.error(f"Failed to get/create collection: {e}")
                raise
        return self._collection

    def get_collection_info(self) -> Dict:
        """Get information about the collection."""
        try:
            collection = self.get_collection()
            count = collection.count()
            return {
                "name": self.collection_name,
                "count": count,
                "metadata": collection.metadata
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {"error": str(e)}

    def health_check(self) -> bool:
        """Check if ChromaDB is healthy."""
        try:
            self.client.heartbeat()
            return True
        except Exception as e:
            logger.error(f"ChromaDB health check failed: {e}")
            return False

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
