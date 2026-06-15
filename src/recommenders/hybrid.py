import pandas as pd


class HybridRecommender:

    def __init__(
        self,
        content_model,
        popularity_model,
        movies
    ):

        self.cb = content_model
        self.pop = popularity_model
        self.movies = movies

    def recommend(
        self,
        movie_title,
        top_n=10
    ):

        content_recs = self.cb.recommend(
            movie_title,
            top_n=50
        )

        result = []

        for title in content_recs:

            movie_row = self.movies[
                self.movies["title"] == title
            ]

            if movie_row.empty:
                continue

            movie_id = movie_row[
                "movieId"
            ].values[0]

            popularity_score = (
                self.pop.score(movie_id)
            )

            result.append({
                "title": title,
                "popularity_score":
                    popularity_score,
                "final_score":
                    popularity_score
            })

        result = pd.DataFrame(result)

        result = result.sort_values(
            "final_score",
            ascending=False
        )

        return result.head(top_n)