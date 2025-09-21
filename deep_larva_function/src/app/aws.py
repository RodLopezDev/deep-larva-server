"""
AWS clients for the deep-larva-server
"""

import boto3
from botocore.config import Config

s3 = boto3.client(
    "s3", config=Config(s3={"addressing_style": "path"}, signature_version="s3v4")
)
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
