from typing import Optional
from botocore.exceptions import ClientError


class DocumentService():
    def __init__(self, s3) -> None:
        self.s3 = s3

    def create_presigned_upload_url(self, bucket_name, object_name, expiration=3600) -> Optional[str]:
        try:
            response = self.s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            print(e)
            return None
