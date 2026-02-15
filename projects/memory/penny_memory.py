#!/usr/bin/env python3
"""Penny Memory System - Qdrant vector memory for context retention"""
import json
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    print("⚠️ qdrant-client not installed. Run: pip3 install qdrant-client")

class PennyMemory:
    def __init__(self, host="localhost", port=6333, collection="penny_memory"):
        self.collection = collection
        self.client = None
        
        if QDRANT_AVAILABLE:
            try:
                self.client = QdrantClient(host=host, port=port)
                self._ensure_collection()
                print(f"✅ Connected to Qdrant at {host}:{port}")
            except Exception as e:
                print(f"⚠️ Qdrant connection failed: {e}")
                self.client = None
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                print(f"✅ Created collection: {self.collection}")
        except Exception as e:
            print(f"⚠️ Collection setup error: {e}")
    
    def embed_text(self, text: str) -> List[float]:
        """Simple embedding using sentence-transformers or fallback"""
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            return model.encode(text).tolist()
        except ImportError:
            # Fallback: simple hash-based encoding (not semantic, but works for demo)
            print("⚠️ sentence-transformers not installed. Using fallback embedding.")
            # Create a 384-dim vector from text hash
            hash_val = hashlib.md5(text.encode()).hexdigest()
            vec = [int(hash_val[i:i+2], 16) / 255.0 for i in range(0, min(len(hash_val), 768), 2)]
            # Pad to 384 dimensions
            vec = (vec * 10)[:384]
            return vec
    
    def remember(self, text: str, metadata: Optional[Dict] = None) -> bool:
        """Store a memory"""
        if not self.client:
            print("⚠️ Qdrant not available. Memory not stored.")
            return False
        
        try:
            embedding = self.embed_text(text)
            point_id = hashlib.md5(f"{text}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
            
            self.client.upsert(
                collection_name=self.collection,
                points=[PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text": text,
                        "timestamp": datetime.now().isoformat(),
                        **(metadata or {})
                    }
                )]
            )
            return True
        except Exception as e:
            print(f"⚠️ Remember failed: {e}")
            return False
    
    def recall(self, query: str, limit: int = 5) -> List[Dict]:
        """Search memories by semantic similarity"""
        if not self.client:
            print("⚠️ Qdrant not available.")
            return []
        
        try:
            embedding = self.embed_text(query)
            results = self.client.search(
                collection_name=self.collection,
                query_vector=embedding,
                limit=limit
            )
            
            memories = []
            for result in results:
                memories.append({
                    "text": result.payload.get("text", ""),
                    "score": result.score,
                    "timestamp": result.payload.get("timestamp"),
                    **{k: v for k, v in result.payload.items() if k not in ["text", "timestamp"]}
                })
            return memories
        except Exception as e:
            print(f"⚠️ Recall failed: {e}")
            return []
    
    def get_recent(self, hours: int = 24) -> List[Dict]:
        """Get recent memories by time"""
        if not self.client:
            return []
        
        try:
            from datetime import timedelta
            cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
            
            results = self.client.scroll(
                collection_name=self.collection,
                scroll_filter={
                    "must": [
                        {"key": "timestamp", "range": {"gte": cutoff}}
                    ]
                },
                limit=100
            )[0]
            
            return [r.payload for r in results]
        except Exception as e:
            print(f"⚠️ Recent fetch failed: {e}")
            return []

# Quick test
if __name__ == "__main__":
    memory = PennyMemory()
    
    # Test store
    print("\nStoring test memories...")
    memory.remember("BONK position is 45% of portfolio", {"type": "portfolio", "token": "BONK"})
    memory.remember("Research x402 protocol for SolanaFloor video", {"type": "task", "project": "content"})
    memory.remember("SKRmaxing submitted to dApp Store on Feb 13", {"type": "milestone", "project": "SKRmaxing"})
    
    # Test recall
    print("\nRecalling 'portfolio' memories:")
    results = memory.recall("portfolio allocation", limit=3)
    for r in results:
        print(f"  - {r['text'][:60]}... (score: {r['score']:.3f})")
    
    print("\n✅ Memory system ready!")
