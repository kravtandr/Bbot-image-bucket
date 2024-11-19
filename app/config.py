from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Настройки приложения, читаемые из переменных окружения
    """
    # FastAPI настройки
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8011

    # MinIO настройки
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_BUCKET_NAME: str
    MINIO_USE_SSL: bool = False

    # Настройки загрузки файлов
    MAX_FILE_SIZE: int = 5_242_880  # 5MB в байтах
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif"}

    class Config:
        env_file = ".env"

settings = Settings()