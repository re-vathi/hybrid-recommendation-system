from src.data.data_loader import DataLoader

from src.recommenders.content_based import (
    ContentBasedRecommender
)

from src.recommenders.popularity import (
    PopularityRecommender
)

from src.recommenders.hybrid import (
    HybridRecommender
)


loader = DataLoader(
    "data/raw"
)

movies = loader.load_movies()

ratings = loader.load_ratings()

content = (
    ContentBasedRecommender()
)

content.fit(
    movies
)

pop = (
    PopularityRecommender()
)

pop.fit(
    ratings
)

hybrid = (
    HybridRecommender(
        content,
        pop,
        movies
    )
)

result = hybrid.recommend(
    "Toy Story (1995)"
)

print(result)