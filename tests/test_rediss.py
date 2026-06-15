from src.cache.cache import cache

cache.set(
    "movie_1",
    "Toy Story"
)

print(
    cache.get(
        "movie_1"
    )
)