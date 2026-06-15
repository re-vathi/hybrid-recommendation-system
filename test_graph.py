from src.data.data_loader import DataLoader

from src.recommenders.graph_based import (
    GraphRecommender
)


loader = DataLoader(
    "data/raw"
)

ratings = loader.load_ratings()

graph = GraphRecommender()

graph.build_graph(
    ratings
)

result = graph.recommend_movies(
    user_id=1
)

print(result)