from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .config import settings
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()

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



# Удалите все таблицы и создайте заново
models.Base.metadata.drop_all(bind=database.engine)
# Создаем таблицы
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/command/", response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, db: Session = Depends(database.get_db)):
    db_record = models.Record(
        command=record.command.model_dump(),  # Преобразуем Pydantic модель в dict
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/commands/", response_model=List[schemas.Record])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    records = db.query(models.Record).offset(skip).limit(limit).all()
    return records