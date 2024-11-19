from fastapi import APIRouter, UploadFile, HTTPException
from ..services.minio_service import MinioService
from ..config import settings
import io

router = APIRouter()
minio_service = MinioService()

@router.post("/upload")
async def upload_file(file: UploadFile):
    """
    Эндпоинт для загрузки файла
    
    Args:
        file (UploadFile): Загружаемый файл
        
    Returns:
        dict: Словарь с URL загруженного файла
        
    Raises:
        HTTPException: При ошибке загрузки или неверном формате файла
    """
    # Читаем файл в память
    try:
        contents = await file.read()
        file_size = len(contents)

        # Проверка размера файла
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large"
            )
        
        # Создаем новый SpooledTemporaryFile с содержимым
        file.file = io.BytesIO(contents)
        
        # Загружаем файл
        file_url = await minio_service.upload_file(file)
        return {"url": file_url}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))