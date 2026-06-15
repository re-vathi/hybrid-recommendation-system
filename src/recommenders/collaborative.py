import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


class CollaborativeFiltering:

    def __init__(self):

        self.user_item_matrix = None

        self.user_similarity = None

    def build_matrix(self, ratings):

        self.user_item_matrix = ratings.pivot_table(
            index="userId",
            columns="movieId",
            values="rating"
        ).fillna(0)

        return self.user_item_matrix

    def compute_similarity(self):

        self.user_similarity = cosine_similarity(
            self.user_item_matrix
        )

        return self.user_similarity