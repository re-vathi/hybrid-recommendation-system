from src.data.data_loader import DataLoader

from src.data.preprocessing import Preprocessor

from src.recommenders.collaborative import CollaborativeFiltering

from src.optimization.sparse_matrix import SparseOptimizer


loader = DataLoader("data/raw")

ratings = loader.load_ratings()

pre = Preprocessor()

ratings = pre.clean_ratings(ratings)

ratings = pre.filter_active_users(ratings)

ratings = pre.filter_popular_movies(ratings)

cf = CollaborativeFiltering()

matrix = cf.build_matrix(ratings)

print(matrix.shape)

sparse = SparseOptimizer.convert(matrix)

print(sparse.shape)

similarity = cf.compute_similarity()

print(similarity.shape)