from minio import Minio
from minio.error import S3Error
from fastapi import UploadFile
import os
import io
from datetime import timedelta
from ..config import settings
import logging
import time
import json

logger = logging.getLogger(__name__)

class MinioService:
    def __init__(self):
        """Инициализация подключения к MinIO"""
        retries = 5
        while retries > 0:
            try:
                self.client = Minio(
                    f"{settings.MINIO_HOST}:{settings.MINIO_PORT}",
                    access_key=settings.MINIO_ROOT_USER,
                    secret_key=settings.MINIO_ROOT_PASSWORD,
                    secure=settings.MINIO_USE_SSL
                )
                self._ensure_bucket_exists()
                self._set_bucket_policy()
                logger.info("Successfully connected to MinIO")
                break
            except Exception as e:
                logger.warning(f"Failed to connect to MinIO, retrying... ({retries} attempts left)")
                retries -= 1
                if retries == 0:
                    raise e
                time.sleep(5)

    def _ensure_bucket_exists(self):
        """Проверка существования корзины и её создание при необходимости"""
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET_NAME):
                self.client.make_bucket(settings.MINIO_BUCKET_NAME)
                logger.info(f"Bucket {settings.MINIO_BUCKET_NAME} created")
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {e}")
            raise

    def _set_bucket_policy(self):
        """Установка публичной политики для бакета"""
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{settings.MINIO_BUCKET_NAME}/*"]
                }
            ]
        }
        try:
            self.client.set_bucket_policy(settings.MINIO_BUCKET_NAME, json.dumps(policy))
            logger.info(f"Bucket policy set for {settings.MINIO_BUCKET_NAME}")
        except S3Error as e:
            logger.error(f"Error setting bucket policy: {e}")
            raise

    async def upload_file(self, file: UploadFile) -> str:
        """
        Загрузка файла в MinIO
        
        Args:
            file (UploadFile): Загружаемый файл
            
        Returns:
            str: URL для доступа к файлу
            
        Raises:
            ValueError: Если расширение файла не разрешено
            S3Error: При ошибке загрузки в MinIO
        """
        # Проверка расширения файла
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(f"File extension {file_ext} is not allowed")

        try:
            # Генерация уникального имени файла
            file_name = f"{os.urandom(16).hex()}{file_ext}"
            
            # Загрузка файла
            file_data = file.file.read()
            self.client.put_object(
                settings.MINIO_BUCKET_NAME,
                file_name,
                io.BytesIO(file_data),
                length=len(file_data),
                content_type=file.content_type
            )

            # Формируем прямую ссылку на объект
            return f"http://{settings.MINIO_HOST}:{settings.MINIO_PORT}/{settings.MINIO_BUCKET_NAME}/{file_name}"

        except S3Error as e:
            logger.error(f"Error uploading file: {e}")
            raise
        finally:
            file.file.close()

    async def get_file(self, filename: str) -> bytes:
        try:
            # Получаем объект из MinIO
            data = self.client.get_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=filename
            )
            # Читаем все данные
            return data.read()
        except Exception as e:
            raise ValueError(f"Error getting file from MinIO: {str(e)}")