from typing import Optional
from src.domain.entity.Picture import Picture


class PictureService():

    def __init__(self, dynamodb) -> None:
        self.repository = dynamodb.Table('PictureTable')

    def save(self, picture: Picture) -> Picture:
        self.repository.put_item(Item=picture.dict())
        return picture

    def get_by_id(self, pictureId: str) -> Optional[Picture]:
        response = self.repository.get_item(Key={'id': pictureId})
        return response.get('Item')

    def update_item(self, pictureId, picture: Picture) -> Picture:
        picture.id = pictureId
        self.repository.put_item(Item=picture)
        return picture
