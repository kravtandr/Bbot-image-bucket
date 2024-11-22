from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .config import settings
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

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


# Создаем таблицы
models.Base.metadata.create_all(bind=database.engine)

@app.post("/records/", response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, db: Session = Depends(database.get_db)):
    db_record = models.Record(
        text=record.text,
        is_active=record.is_active
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/records/", response_model=List[schemas.Record])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    records = db.query(models.Record).offset(skip).limit(limit).all()
    return records