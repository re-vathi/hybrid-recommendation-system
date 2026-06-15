import numpy as np

from src.optimization.faiss_engine import (
    FaissEngine
)

vectors = np.random.rand(
    100,
    20
)

engine = FaissEngine(
    dimension=20
)

engine.add_vectors(
    vectors
)

query = vectors[0]

D, I = engine.search(
    query,
    5
)

print(I)