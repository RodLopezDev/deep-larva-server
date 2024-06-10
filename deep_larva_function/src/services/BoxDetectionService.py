from typing import Optional
from src.domain.entity.BoxDetection import BoxDetection


class BoxDetectionService():
    def __init__(self, dynamodb) -> None:
        self.repository = dynamodb.Table('BoxDetectionTable')

    def save(self, box: BoxDetection) -> BoxDetection:
        self.repository.put_item(Item=box.dict())
        return box

    def get_by_id(self, id: str) -> Optional[BoxDetection]:
        response = self.repository.get_item(Key={'id': id})
        return response.get('Item')

    def get_by_pictureId(self, pictureId: str) -> list[BoxDetection]:
        raise Exception('Not implemented')
        # response = self.repository.get_item(Key={'pictureId': pictureId})
        # return response.get('Item')

    def update_item(self, boxId: str, picture: BoxDetection) -> BoxDetection:
        picture.id = boxId
        self.repository.put_item(Item=picture)
        return picture


__all__ = ['BoxDetectionService']
