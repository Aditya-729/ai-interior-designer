"""
Vector memory service using Qdrant for semantic search.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from app.core.config import settings
from typing import List, Dict, Any, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class VectorMemory:
    """Vector memory service for design references and style memory."""

    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
            self.available = True
            logger.info("Vector memory initialized with sentence-transformers")
        else:
            self.encoder = None
            self.available = False
            logger.warning("sentence-transformers not available. Vector search will be disabled.")
        
        self.collection_name = "design_memory"
        if self.available:
            self._ensure_collection()

    def _ensure_collection(self):
        """Ensure collection exists."""
        try:
            self.client.get_collection(self.collection_name)
            logger.info(f"Qdrant collection '{self.collection_name}' exists")
        except Exception:
            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,  # all-MiniLM-L6-v2 dimension
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Qdrant collection '{self.collection_name}' created")

    def store_design_reference(
        self,
        project_id: str,
        user_prompt: str,
        edit_plan: Dict[str, Any],
        room_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Store a design reference in vector memory.

        Returns:
            Reference ID
        """
        if not self.available:
            raise RuntimeError("Vector memory is not available. Please install sentence-transformers.")
        
        # Create text representation
        text = f"{user_prompt} {room_type} {edit_plan}"
        vector = self.encoder.encode(text).tolist()

        reference_id = str(uuid.uuid4())

        point = PointStruct(
            id=reference_id,
            vector=vector,
            payload={
                "project_id": project_id,
                "user_prompt": user_prompt,
                "edit_plan": edit_plan,
                "room_type": room_type,
                **(metadata or {}),
            },
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

        logger.info(f"Design reference stored: {reference_id}")
        return reference_id

    def search_similar_designs(
        self,
        query: str,
        room_type: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar designs.

        Returns:
            List of similar designs with scores
        """
        if not self.available:
            logger.warning("Vector search not available. Returning empty results.")
            return []
        
        # Encode query
        query_vector = self.encoder.encode(query).tolist()

        # Build filter
        filter_dict = None
        if room_type:
            filter_dict = {
                "must": [
                    {
                        "key": "room_type",
                        "match": {"value": room_type},
                    }
                ]
            }

        # Search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=filter_dict,
            limit=limit,
        )

        return [
            {
                "id": result.id,
                "score": result.score,
                "project_id": result.payload.get("project_id"),
                "user_prompt": result.payload.get("user_prompt"),
                "edit_plan": result.payload.get("edit_plan"),
                "room_type": result.payload.get("room_type"),
            }
            for result in results
        ]

    def get_user_style_profile(
        self, user_id: str, limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get user's style profile from their past designs.

        Returns:
            Style profile with preferred colors, materials, etc.
        """
        # Search user's past projects
        # This would require storing user_id in payload
        # For now, return empty profile
        return {
            "preferred_colors": [],
            "preferred_materials": [],
            "preferred_styles": [],
        }


vector_memory = VectorMemory()
