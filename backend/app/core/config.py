from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TMDB_API_KEY: str = ""
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    TMDB_IMAGE_BASE: str = "https://image.tmdb.org/t/p/w500"
    MOVIELENS_PATH: str = "data/ml-latest-small"
    # Comma-separated list of origins allowed to call the API
    CORS_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()
