from pydantic import BaseModel


class BoxDetection(BaseModel):
    id: str
    pictureId: str
    v1: int
    v2: int
    v3: int
    v4: int
