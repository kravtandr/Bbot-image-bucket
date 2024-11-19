from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .config import settings
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Image Upload API",
    description="API для загрузки изображений в MinIO",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене следует указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутера
app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """
    Эндпоинт для проверки работоспособности сервиса
    """
    return {"status": "healthy"}