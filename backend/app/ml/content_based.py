# Content-based filtering — "because you liked Inception..."
# Similarity measured by cosine distance on genre vectors
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class ContentFilter:
    def __init__(self):
        self.genre_matrix = None
        self.movie_ids = None

    def fit(self, genre_df: pd.DataFrame):
        """
        Store genre vectors only. A full movie x movie similarity matrix
        (~9.7k^2 floats ≈ 760 MB) won't fit on small hosts, so similarity
        is computed per request instead — one row at a time.
        """
        self.movie_ids = genre_df["movieId"].tolist()
        genre_cols = [c for c in genre_df.columns if c not in ["movieId", "title"]]
        self.genre_matrix = genre_df[genre_cols].values

    def similar_to(self, movie_id: int, n: int = 10) -> list[dict]:
        """Return n most genre-similar movies to a given film."""
        if movie_id not in self.movie_ids:
            return []
        idx = self.movie_ids.index(movie_id)
        scores = cosine_similarity(self.genre_matrix[idx:idx+1], self.genre_matrix)[0]
        scores[idx] = -1  # exclude the movie itself
        top = np.argsort(scores)[::-1][:n]
        return [{"movie_id": self.movie_ids[i], "score": float(scores[i])} for i in top]

    def recommend_from_profile(self, rated_movies: dict, n: int = 10) -> list[dict]:
        """
        Build weighted genre fingerprint from user's ratings
        (higher rated movies contribute more to the profile),
        then score all movies against that fingerprint.
        """
        profile = np.zeros(self.genre_matrix.shape[1])
        for mid, rating in rated_movies.items():
            if mid in self.movie_ids:
                profile += self.genre_matrix[self.movie_ids.index(mid)] * rating

        norm = np.linalg.norm(profile)
        if norm > 0:
            profile /= norm

        scores = self.genre_matrix @ profile
        results = [(mid, s) for mid, s in zip(self.movie_ids, scores)
                   if mid not in rated_movies]
        results.sort(key=lambda x: x[1], reverse=True)
        return [{"movie_id": mid, "score": float(s)} for mid, s in results[:n]]
