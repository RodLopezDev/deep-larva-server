import os
import uuid
from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, UploadFile, Body

from src.app.aws import dynamodb, s3
from src.services.PictureService import PictureService
from src.services.BoxDetectionService import BoxDetectionService

from src.domain.entity.Picture import Picture
from src.domain.entity.BoxDetection import BoxDetection
from src.domain.request.PictureDTO import SavePictureDTO, BoxDTO

router = APIRouter()
pService = PictureService(dynamodb)
bdService = BoxDetectionService(dynamodb)

UPLOAD_DIR = "/tmp/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get('/', tags=["Home"])
async def home():
    return {'status': 'OK'}


@router.post("/picture", response_model=Picture, tags=["Picture Management"])
async def save(dto: SavePictureDTO = Body(...)):
    picture = pService.save(picture=Picture(
        id=dto.picture.uuid,
        deviceId=dto.picture.deviceId,
        count=dto.picture.count,
        pathFile='',
        pathProcessed='',
        time=dto.picture.time,
        timestamp=dto.picture.timestamp
    ))

    def convert(input: BoxDTO) -> BoxDetection:
        return BoxDetection(
            id=str(uuid.uuid4()),
            pictureId=picture.id,
            v1=input.v1,
            v2=input.v2,
            v3=input.v3,
            v4=input.v4
        )

    boxes = list(map(convert, dto.boxes))
    for box in boxes:
        bdService.save(box)

    return picture


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
