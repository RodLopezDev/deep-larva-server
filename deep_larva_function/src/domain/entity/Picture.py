from pydantic import BaseModel


class Picture(BaseModel):
    id: str
    deviceId: str
