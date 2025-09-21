import uuid

from src.domain.constants.featureFlags import IS_ENABLED_BUCKET
from src.domain.entity.BoxDetection import BoxDetection
from src.domain.entity.Picture import Picture
from src.domain.request.PictureDTO import BoxDTO, SavePictureDTO
from src.domain.response.NewPictureResponse import NewPictureResponse
from src.services.BoxDetectionService import BoxDetectionService
from src.services.DocumentService import DocumentService
from src.services.PictureService import PictureService


def convert_builder(picture: Picture):
    def convert(input: BoxDTO) -> BoxDetection:
        return BoxDetection(
            id=str(uuid.uuid4()),
            pictureId=picture.id,
            v1=input.v1,
            v2=input.v2,
            v3=input.v3,
            v4=input.v4,
        )

    return convert


class PictureController:
    def __init__(
        self,
        pictureService: PictureService,
        boxService: BoxDetectionService,
        documentService: DocumentService,
    ):
        self.picture = pictureService
        self.boxes = boxService
        self.document = documentService

    def save(self, dto: SavePictureDTO) -> NewPictureResponse:
        if not IS_ENABLED_BUCKET:
            return NewPictureResponse(
                id="", originalFileURL="", processedFileURL="", circuitBreak=True
            )

        bucket_name = "deep-larva-storage"
        file_relative_path = f"{dto.picture.uuid}-file.png"
        processed_file_relative_path = f"{dto.picture.uuid}-processed.png"

        picture = self.picture.save(
            picture=Picture(
                id=dto.picture.uuid,
                deviceId=dto.picture.deviceId,
                count=dto.picture.count,
                pathFile=f"s3://{bucket_name}/{file_relative_path}",
                pathProcessed=f"s3://{bucket_name}/{processed_file_relative_path}",
                time=dto.picture.time,
                timestamp=dto.picture.timestamp,
            )
        )

        boxes = list(map(convert_builder(picture), dto.boxes))
        for box in boxes:
            self.boxes.save(box)

        original_file_presigned_url = self.document.create_presigned_upload_url(
            bucket_name, file_relative_path
        )
        processed_file_presigned_url = self.document.create_presigned_upload_url(
            bucket_name, processed_file_relative_path
        )

        return NewPictureResponse(
            id=picture.id,
            originalFileURL=original_file_presigned_url or "",
            processedFileURL=processed_file_presigned_url or "",
            circuitBreak=False,
        )


__all__ = ["PictureController"]
