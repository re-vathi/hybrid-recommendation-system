from src.data.data_loader import DataLoader
from src.data.preprocessing import Preprocessor

def main():
    loader = DataLoader("data/raw")
    ratings = loader.load_ratings()

    pre = Preprocessor()
    ratings = pre.clean_ratings(ratings)
    ratings = pre.filter_active_users(ratings)
    ratings = pre.filter_popular_movies(ratings)

    pre.save_processed_data(
        ratings,
        "data/processed/ratings_cleaned.csv"
    )

    print(ratings.head())

if __name__ == "__main__":
    main()
