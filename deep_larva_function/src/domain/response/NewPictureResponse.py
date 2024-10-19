from typing import List
from pydantic import BaseModel, Field


class NewPictureResponse(BaseModel):
    id: str = Field()
    originalFileURL: str = Field()
    processedFileURL: str = Field()
    circuitBreak: bool = Field()
