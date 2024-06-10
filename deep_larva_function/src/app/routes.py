import os
from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, UploadFile, Body

from src.app.aws import dynamodb, s3
from src.domain.entity.Picture import Picture
from src.domain.request.PictureDTO import PictureDTO
from src.services.PictureService import PictureService

router = APIRouter()
service = PictureService(dynamodb)

UPLOAD_DIR = "/tmp/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/hello")
async def hello_world():
    return {}


@router.post("/picture", response_model=PictureDTO, tags=["Picture Management"])
async def save(picture: PictureDTO = Body(...)):
    service.save(picture=Picture(
        deviceId=picture.deviceId,
        id=picture.id
    ))
    return picture


@router.post("/bitmap/{pictureId}")
async def upload_bitmap(pictureId: int, file: UploadFile = File(...)):
    if file.content_type != "image/png":
        return JSONResponse(status_code=400, content={"message": "Only BMP files are allowed."})

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    s3.upload_file(file_location, 'deep-larva-storage', file.filename)
    os.remove(file_location)

    return {"message": f"File '{file.filename}' uploaded successfully."}


@router.get('/')
async def home():
    return {'status': 'OK'}

__all__ = ["router"]
