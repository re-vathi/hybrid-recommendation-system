import pandas as pd

class Preprocessor:
    def clean_ratings(self, ratings: pd.DataFrame) -> pd.DataFrame:
        ratings = ratings.drop_duplicates()
        ratings = ratings.dropna()
        return ratings

    def filter_active_users(self, ratings: pd.DataFrame, min_ratings: int = 20) -> pd.DataFrame:
        counts = ratings["userId"].value_counts()
        active_users = counts[counts >= min_ratings].index
        return ratings[ratings["userId"].isin(active_users)]

    def filter_popular_movies(self, ratings: pd.DataFrame, min_reviews: int = 50) -> pd.DataFrame:
        counts = ratings["movieId"].value_counts()
        popular_movies = counts[counts >= min_reviews].index
        return ratings[ratings["movieId"].isin(popular_movies)]

    def save_processed_data(self, ratings: pd.DataFrame, output_path: str):
        ratings.to_csv(output_path, index=False)
