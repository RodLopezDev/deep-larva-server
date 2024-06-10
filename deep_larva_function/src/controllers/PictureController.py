import uuid

from src.domain.entity.Picture import Picture
from src.domain.entity.BoxDetection import BoxDetection

from src.domain.request.PictureDTO import SavePictureDTO, BoxDTO

from src.services.PictureService import PictureService
from src.services.BoxDetectionService import BoxDetectionService


class PictureController:
    def __init__(
        self,
        pictureService: PictureService,
        boxService: BoxDetectionService
    ):
        self.picture = pictureService
        self.boxes = boxService

    def save(self, dto: SavePictureDTO):
        picture = self.picture.save(picture=Picture(
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
            self.boxes.save(box)

        return picture


__all__ = ['PictureController']
