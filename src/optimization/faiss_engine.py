try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

import numpy as np
from src.utils.logger import logger

class FAISSEngine:
    def __init__(self):
        self.index = None
        self.data = None
    
    def build(self, vectors):
        if not FAISS_AVAILABLE:
            logger.warning("FAISS not available - install with: pip install faiss-cpu")
            return
        
        vectors = np.array(vectors, dtype=np.float32)
        if len(vectors) == 0:
            return
        
        d = vectors.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(vectors)
        self.data = vectors
        logger.info(f"✓ FAISS index built with {len(vectors)} vectors")
    
    def search(self, query_vector, k=10):
        if not FAISS_AVAILABLE or self.index is None:
            return [], []
        
        query_vector = np.array([query_vector], dtype=np.float32)
        distances, indices = self.index.search(query_vector, k)
        return indices[0], distances[0]
