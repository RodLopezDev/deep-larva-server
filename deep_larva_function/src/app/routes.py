import os
import uuid
from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, UploadFile, Body

from src.app.aws import dynamodb, s3
from src.services.PictureService import PictureService
from src.services.BoxDetectionService import BoxDetectionService

from src.controllers.PictureController import PictureController

from src.domain.entity.Picture import Picture
from src.domain.entity.BoxDetection import BoxDetection
from src.domain.request.PictureDTO import SavePictureDTO, BoxDTO

router = APIRouter()
pService = PictureService(dynamodb)
bdService = BoxDetectionService(dynamodb)
controller = PictureController(pService, bdService)

UPLOAD_DIR = "/tmp/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get('/', tags=["Home"])
async def home():
    return {'status': 'OK'}


@router.post("/picture", response_model=Picture, tags=["Picture Management"])
async def save(dto: SavePictureDTO = Body(...)):
    return controller.save(dto)


@router.post("/bitmap/{type}/{pictureId}", tags=["Picture Management"])
async def upload_bitmap(type: str, pictureId: int, file: UploadFile = File(...)):
    if file.content_type != "image/png":
        return JSONResponse(status_code=400, content={"message": "Only BMP files are allowed."})
    if type != 'file' and type != 'processed':
        return JSONResponse(status_code=400, content={"message": "Incorrect type."})
    picture = pService.get_by_id(pictureId)
    if not picture:
        return JSONResponse(status_code=404, content={"message": "Picture not found."})

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    s3.upload_file(file_location, 'deep-larva-storage', file.filename)
    os.remove(file_location)

    if (type == 'file'):
        picture.pathFile = 'file_location'
    elif (type == 'processed'):
        picture.pathProcessed = 'file_location'

    pService.update_item(pictureId, picture)
    return {"message": f"File '{file.filename}' uploaded successfully."}

__all__ = ["router"]
