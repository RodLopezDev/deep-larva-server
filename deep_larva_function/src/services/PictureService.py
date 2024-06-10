from src.domain.entity.Picture import Picture

class PictureService():
    def __init__(self, dynamodb) -> None:
        self.repository = dynamodb.Table('PictureTable')

    def save(self, picture: Picture):
        self.repository.put_item(Item=picture.dict())