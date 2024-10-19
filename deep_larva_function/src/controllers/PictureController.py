import uuid

from src.domain.entity.Picture import Picture
from src.domain.entity.BoxDetection import BoxDetection
from src.domain.response.NewPictureResponse import NewPictureResponse

from src.domain.request.PictureDTO import SavePictureDTO, BoxDTO
from src.domain.constants.featureFlags import IS_ENABLED_BUCKET

from src.services.PictureService import PictureService
from src.services.DocumentService import DocumentService
from src.services.BoxDetectionService import BoxDetectionService


class PictureController:
    def __init__(
        self,
        pictureService: PictureService,
        boxService: BoxDetectionService,
        documentService: DocumentService
    ):
        self.picture = pictureService
        self.boxes = boxService
        self.document = documentService

    def save(self, dto: SavePictureDTO) -> NewPictureResponse:
        if not IS_ENABLED_BUCKET:
            return NewPictureResponse(
                id="",
                originalFileURL="",
                processedFileURL="",
                circuitBreak=True
            )

        bucket_name = "deep-larva-storage"
        fileRelativePath = f"{dto.picture.uuid}-file.png"
        processedfileRelativePath = f"{dto.picture.uuid}-processed.png"

        picture = self.picture.save(picture=Picture(
            id=dto.picture.uuid,
            deviceId=dto.picture.deviceId,
            count=dto.picture.count,
            pathFile=f"s3://{bucket_name}/{fileRelativePath}",
            pathProcessed=f"s3://{bucket_name}/{processedfileRelativePath}",
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

        originalFilePresignedUrl = self.document.create_presigned_upload_url(
            bucket_name,
            fileRelativePath
        )
        processedFilePresignedUrl = self.document.create_presigned_upload_url(
            bucket_name,
            processedfileRelativePath
        )

        return NewPictureResponse(
            id=picture.id,
            originalFileURL=originalFilePresignedUrl,
            processedFileURL=processedFilePresignedUrl,
            circuitBreak=False
        )


__all__ = ['PictureController']
