import os
import boto3
import botocore


class S3Utils:
    def __init__(self):
        self.instance = boto3.Session().client(
            "s3",
            aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get(
                "S3_SECRET_ACCESS_KEY")
        )

    def upload_to_s3(self, file):
        try:
            self.instance.upload_fileobj(
                file,
                os.environ.get("S3_BUCKET_NAME"),
                file.filename
            )
        except Exception as e:
            return e

    def get_file(self, filename):
        file = self.instance.get_object(
            Bucket=os.environ.get("S3_BUCKET_NAME"), Key=filename)
        return file
