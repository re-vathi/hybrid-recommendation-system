import heapq


class TopKOptimizer:

    @staticmethod
    def get_top_k(
        scores,
        k=10
    ):

        return heapq.nlargest(
            k,
            scores.items(),
            key=lambda x: x[1]
        )