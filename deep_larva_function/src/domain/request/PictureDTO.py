from typing import List

from pydantic import BaseModel, Field


class BoxDTO(BaseModel):
    id: int = Field()
    pictureId: int = Field()
    v1: int = Field()
    v2: int = Field()
    v3: int = Field()
    v4: int = Field()


class PictureDTO(BaseModel):
    id: int = Field()
    uuid: str = Field()
    deviceId: str = Field()
    filePath: str = Field()
    thumbnailPath: str = Field()
    processedFilePath: str = Field()
    hasMetadata: bool = Field()
    syncWithCloud: bool = Field()
    count: int = Field()
    time: int = Field()
    timestamp: int = Field()


class SavePictureDTO(BaseModel):
    picture: PictureDTO
    boxes: List[BoxDTO]


__all__ = ["SavePictureDTO"]
