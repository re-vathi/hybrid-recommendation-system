from src.optimization.topk import (
    TopKOptimizer
)

scores = {

    "movie1": 20,

    "movie2": 35,

    "movie3": 10,

    "movie4": 90
}

print(
    TopKOptimizer.get_top_k(
        scores,
        2
    )
)