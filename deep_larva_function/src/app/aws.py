import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
