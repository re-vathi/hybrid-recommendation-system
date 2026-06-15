import networkx as nx


class GraphRecommender:

    def __init__(self):

        self.graph = nx.Graph()

    def build_graph(
        self,
        ratings
    ):

        for row in ratings.itertuples():

            user_node = f"U_{row.userId}"

            movie_node = f"M_{row.movieId}"

            self.graph.add_edge(
                user_node,
                movie_node,
                weight=row.rating
            )

    def recommend_movies(
        self,
        user_id,
        top_n=10
    ):

        user_node = f"U_{user_id}"

        if user_node not in self.graph:

            return []

        watched = set(
            self.graph.neighbors(
                user_node
            )
        )

        scores = {}

        for movie in watched:

            for other_user in self.graph.neighbors(
                movie
            ):

                if other_user == user_node:
                    continue

                for candidate_movie in (
                    self.graph.neighbors(
                        other_user
                    )
                ):

                    if candidate_movie in watched:
                        continue

                    scores[
                        candidate_movie
                    ] = scores.get(
                        candidate_movie,
                        0
                    ) + 1

        recommendations = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return recommendations[
            :top_n
        ]