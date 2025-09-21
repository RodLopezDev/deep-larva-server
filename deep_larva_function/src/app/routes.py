import os
import uuid

from fastapi import APIRouter, Body, File, UploadFile
from fastapi.responses import JSONResponse
from src.app.aws import dynamodb, s3
from src.controllers.PictureController import PictureController
from src.domain.entity.BoxDetection import BoxDetection
from src.domain.entity.Picture import Picture
from src.domain.request.PictureDTO import BoxDTO, SavePictureDTO
from src.domain.response.NewPictureResponse import NewPictureResponse
from src.services.BoxDetectionService import BoxDetectionService
from src.services.DocumentService import DocumentService
from src.services.PictureService import PictureService

router = APIRouter()
pService = PictureService(dynamodb)
bdService = BoxDetectionService(dynamodb)
dService = DocumentService(s3)
controller = PictureController(pService, bdService, dService)

UPLOAD_DIR = "/tmp/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", tags=["Home"])
async def home():
    return {"status": "OK"}


@router.post("/picture", response_model=NewPictureResponse, tags=["Picture Management"])
async def save(dto: SavePictureDTO = Body(...)):
    return controller.save(dto)


# @router.post("/bitmap/{type}/{pictureId}", tags=["Picture Management"])
# async def upload_bitmap(type: str, pictureId: str, file: UploadFile = File(...)):
#     if file.content_type != "image/png":
#         return JSONResponse(status_code=400, content={"message": "Only BMP files are allowed."})
#     if type != 'file' and type != 'processed':
#         return JSONResponse(status_code=400, content={"message": "Incorrect type."})
#     picture = pService.get_by_id(pictureId)
#     if not picture:
#         return JSONResponse(status_code=404, content={"message": "Picture not found."})

#     file_location = os.path.join(UPLOAD_DIR, file.filename)
#     bucket_name = "deep-larva-storage"
#     file_s3_name = f"{pictureId}-{type}.png"
#     with open(file_location, "wb") as f:
#         f.write(await file.read())
#     s3.upload_file(file_location, bucket_name, file_s3_name)
#     os.remove(file_location)

#     if (type == 'file'):
#         picture['pathFile'] = f"s3://{bucket_name}/{file_s3_name}"
#     elif (type == 'processed'):
#         picture['pathProcessed'] = f"s3://{bucket_name}/{file_s3_name}"

#     pService.update_item(picture)
#     return {"message": f"File '{file.filename}' uploaded successfully."}

__all__ = ["router"]
