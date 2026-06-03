import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    data_dir: str = os.getenv("DATA_DIR", "data")
    uploads_dir: str = os.path.join(data_dir, "uploads")
    faiss_index_dir: str = os.path.join(data_dir, "faiss_index")
    db_path: str = os.path.join(data_dir, "learning.db")

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.uploads_dir, exist_ok=True)
os.makedirs(settings.faiss_index_dir, exist_ok=True)
