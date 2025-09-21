"""
Routes for the deep-larva-server
"""

import os

from fastapi import APIRouter, Body, HTTPException, Request
from pydantic import BaseModel
from src.app.aws import dynamodb, s3
from src.controllers.PictureController import PictureController
from src.domain.request.PictureDTO import SavePictureDTO
from src.domain.response.NewPictureResponse import NewPictureResponse
from src.services.BoxDetectionService import BoxDetectionService
from src.services.DocumentService import DocumentService
from src.services.PictureService import PictureService

router = APIRouter()
pService = PictureService(dynamodb)
bdService = BoxDetectionService(dynamodb)
dService = DocumentService(s3)
controller = PictureController(pService, bdService, dService)


@router.get("/", tags=["Home"])
async def home():
    return {"status": "OK"}


api_server_key = os.getenv("API_SERVER_KEY")


class CameraConfig(BaseModel):
    """
    Camera config
    """

    brand: str
    model: str
    iso: int
    exposure: int
    shutterSpeed: int


@router.get("/v1/camera/{brandh}/{model}/config", response_model=CameraConfig)
async def get_camera_config(brand: str, model: str, request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != api_server_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if brand == "SAMSUNG" and model == "SM-A536E":
        return CameraConfig(
            brand="SAMSUNG", model="SM-A536E", iso=100, exposure=-2, shutterSpeed=20
        )
    if brand == "SAMSUNG" and model == "SM-G781B":
        return CameraConfig(
            brand="SAMSUNG", model="SM-G781B", iso=80, exposure=-2, shutterSpeed=17
        )
    if brand == "SAMSUNG" and model == "SM-A325M":
        return CameraConfig(
            brand="SAMSUNG", model="SM-A325M", iso=100, exposure=-2, shutterSpeed=20
        )
    if brand == "SAMSUNG" and model == "SM-A305G":
        return CameraConfig(
            brand="SAMSUNG", model="SM-A305G", iso=200, exposure=-2, shutterSpeed=7
        )
    if brand == "SAMSUNG" and model == "SM-G980F":
        return CameraConfig(
            brand="SAMSUNG", model="SM-G980F", iso=50, exposure=-2, shutterSpeed=20
        )
    if brand == "HONOR" and model == "WDY-LX3":
        return CameraConfig(
            brand="HONOR", model="WDY-LX3", iso=160, exposure=0, shutterSpeed=17
        )

    raise HTTPException(status_code=404, detail="Camera not found")


@router.post(
    "/v1/picture", response_model=NewPictureResponse, tags=["Picture Management"]
)
async def save(dto: SavePictureDTO = Body(...)):
    return controller.save(dto)


@router.get("/health", tags=["Health"])
async def health():
    return {"app": "deep-larva-server", "version": "0.0.1", "stage": "PROD"}


__all__ = ["router"]
