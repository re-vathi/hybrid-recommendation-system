import pandas as pd


class PopularityRecommender:

    def fit(
        self,
        ratings
    ):

        self.popularity = ratings.groupby(
            "movieId"
        )["rating"].count()

    def score(
        self,
        movie_id
    ):

        if movie_id in self.popularity.index:

            return self.popularity[
                movie_id
            ]

        return 0