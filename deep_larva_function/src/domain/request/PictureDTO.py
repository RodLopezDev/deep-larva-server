from typing import List
from pydantic import BaseModel, Field


class BoxDTO(BaseModel):
    v1: int = Field(default=1)
    v2: int = Field(default=1)
    v3: int = Field(default=1)
    v4: int = Field(default=1)


class PictureDTO(BaseModel):
    id: str = Field(default="1234")
    deviceId: str = Field(default="1234")
    boxes: List[BoxDTO]


__all__ = ['PictureDTO']
