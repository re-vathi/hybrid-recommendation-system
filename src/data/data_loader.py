import pandas as pd

class DataLoader:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_ratings(self):
        return pd.read_csv(f"{self.data_path}/ratings.csv")

    def load_movies(self):
        return pd.read_csv(f"{self.data_path}/movies.csv")

    def load_tags(self):
        return pd.read_csv(f"{self.data_path}/tags.csv")

    def load_links(self):
        return pd.read_csv(f"{self.data_path}/links.csv")
