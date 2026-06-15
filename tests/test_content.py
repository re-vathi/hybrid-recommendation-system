from src.data.data_loader import DataLoader

from src.recommenders.content_based import (
    ContentBasedRecommender
)

loader = DataLoader("data/raw")

movies = loader.load_movies()

cb = ContentBasedRecommender()

cb.fit(movies)

recommendations = cb.recommend(
    "Toy Story (1995)"
)

print(recommendations)