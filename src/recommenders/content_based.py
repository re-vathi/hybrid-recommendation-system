import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:

    def __init__(self):

        self.similarity_matrix = None

        self.movies = None

    def fit(self, movies):

        self.movies = movies.copy()

        self.movies["genres"] = (
            self.movies["genres"]
            .fillna("")
            .str.replace("|", " ")
        )

        tfidf = TfidfVectorizer()

        tfidf_matrix = tfidf.fit_transform(
            self.movies["genres"]
        )

        self.similarity_matrix = cosine_similarity(
            tfidf_matrix
        )

    def recommend(
        self,
        movie_title,
        top_n=10
    ):

        idx = self.movies[
            self.movies["title"] == movie_title
        ].index[0]

        scores = list(
            enumerate(
                self.similarity_matrix[idx]
            )
        )

        scores = sorted(
            scores,
            key=lambda x: x[1],
            reverse=True
        )

        scores = scores[1:top_n+1]

        movie_indices = [
            i[0]
            for i in scores
        ]

        return self.movies.iloc[
            movie_indices
        ]["title"]