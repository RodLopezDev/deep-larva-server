from pydantic import BaseModel


class Picture(BaseModel):
    id: str
    deviceId: str
    pathFile: str
    pathProcessed: str
    count: int
    time: int
    timestamp: int
